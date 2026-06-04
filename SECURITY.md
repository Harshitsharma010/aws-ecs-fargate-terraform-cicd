# Security Notes

This project is a portfolio AWS ECS Fargate deployment lab, not a production service. The goal is to demonstrate cloud deployment, infrastructure as code, logging, and cost-aware cleanup.

## Current Security Controls

| Area | Control |
| --- | --- |
| Public access | Only the Application Load Balancer is exposed on HTTP port `80` |
| Backend access | ECS task security group allows port `8000` only from the ALB security group |
| IAM | ECS task execution role uses `AmazonECSTaskExecutionRolePolicy` for image pull and logs |
| Logs | Container logs are sent to CloudWatch Logs with 7-day retention |
| CI | GitHub Actions runs tests and Docker build only; it does not use AWS secrets |
| Cost control | Terraform resources were destroyed after proof capture |

## Known Limitations

- The demo uses HTTP, not HTTPS.
- The ECS task uses a public IP to avoid NAT Gateway cost.
- Terraform state is local for this lab instead of using a remote backend.
- GitHub Actions does not deploy to AWS yet.
- No WAF, custom domain, or production abuse protection is configured.

## Production Hardening Backlog

- Add HTTPS through ACM and ALB listener on port `443`.
- Add Terraform remote state with S3 and DynamoDB locking.
- Add GitHub Actions CD using OIDC instead of long-lived AWS keys.
- Add stricter monitoring and CloudWatch alarms.
- Add rate limiting or WAF if exposed as a real public API.
- Move ECS tasks to private subnets if the project budget allows NAT Gateway or another controlled egress pattern.

## Reporting

This is a learning project. Do not submit production security reports for the demo endpoint because the infrastructure is destroyed after verification.
