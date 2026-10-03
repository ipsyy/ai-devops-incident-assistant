INCIDENTS = {
    "Kubernetes - CrashLoopBackOff": """ERROR: Pod payment-service-7d8f9c failed to start
Status: CrashLoopBackOff
Readiness probe failed
Connection refused: 10.0.2.15:8080""",

    "AWS S3 - AccessDenied": """ERROR: GetObject operation failed
AWS Error: AccessDenied
User is not authorized to perform s3:GetObject
Bucket: payments-prod""",

    "Database - Connection Timeout": """ERROR: Database connection failed
Connection timed out after 30 seconds
Host: db-prod.internal
Port: 5432""",

    "CI/CD - Docker Build Failure": """ERROR: GitHub Actions deployment failed
Step: Docker Build
Error: failed to solve: npm install exited with code 1""",

    "Terraform - Existing IAM Policy": """Error: Error creating IAM policy
StatusCode: 409
EntityAlreadyExists
Policy named application-access already exists"""
}
