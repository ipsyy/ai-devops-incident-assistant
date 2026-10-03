import streamlit as st
from llm_client import analyze_log
from guardrails import validate_input, validate_output
from output_guardrails import check_recommendations
from sample_data import INCIDENTS
from evaluator import EVALUATION_CASES


st.set_page_config(
    page_title="AI DevOps Incident Assistant",
    page_icon="🛠️"
)

st.title("🛠️ AI DevOps Incident Assistant")
st.caption("A beginner GenAI project for first-pass DevOps incident analysis.")


choice = st.selectbox(
    "Choose a sample incident",
    ["-- Select --"] + list(INCIDENTS.keys())
)


sample = ""

if choice != "-- Select --":
    sample = INCIDENTS[choice]


log_text = st.text_area(
    "Incident / error log",
    value=sample,
    height=220,
    placeholder="Paste a technical log here, or choose a sample above."
)


if st.button("Analyze Incident"):

    if not log_text.strip():
        st.warning("Please enter a log first.")
        st.stop()

    allowed, message = validate_input(log_text)

    if not allowed:
        st.error(message)
        st.stop()

    with st.spinner("Analyzing incident with local AI model..."):
        result = analyze_log(log_text)

    output_allowed, output_message = validate_output(result)

    if not output_allowed:
        st.error(output_message)
        st.stop()

    safe, warnings = check_recommendations(result)

    if not safe:
        st.warning(
            "The AI response contains potentially destructive recommendations. "
            "Please review them before taking any action."
        )

    st.markdown("### AI Analysis")
    st.markdown(result)

    st.info(
        "Demo project only: recommendations are suggestions "
        "and should be verified by an engineer before any "
        "production action."
    )


st.divider()

st.subheader("Evaluation")

st.write(
    "Run the golden test set to check whether the assistant "
    "identifies the expected incident concepts."
)


if st.button("Run Evaluation Tests"):

    passed_cases = 0

    with st.spinner("Running evaluation tests..."):

        for case in EVALUATION_CASES:

            result = analyze_log(case["log"])
            result_lower = result.lower()

            missing = []

            for concept_group in case["required_concepts"]:

                if not any(
                    concept.lower() in result_lower
                    for concept in concept_group
                ):
                    missing.append(" / ".join(concept_group))

            if not missing:

                passed_cases += 1

                st.success(
                    f"PASS — {case['name']}"
                )

            else:

                st.error(
                    f"FAIL — {case['name']} "
                    f"(Missing: {', '.join(missing)})"
                )

    total_cases = len(EVALUATION_CASES)

    score = (passed_cases / total_cases) * 100

    st.metric(
        "Overall Score",
        f"{passed_cases}/{total_cases} ({score:.0f}%)"
    )