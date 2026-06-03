# Deployment Proof Screenshots

This folder contains numbered proof screenshots for the AWS ECS Fargate deployment lab.

| Step | Screenshot | Proof |
| --- | --- | --- |
| 01 | `01-terraform-apply-success.png` | Terraform created the AWS stack successfully |
| 02 | `02-ecr-image-latest.png` | Docker image was pushed to Amazon ECR |
| 03 | `03-ecs-cluster-active.png` | ECS cluster was created and active |
| 04 | `04-ecs-service-running.png` | ECS Fargate service was running |
| 05 | `05-target-group-healthy.png` | ALB target group health check passed |
| 06 | `06-load-balancer-active.png` | Application Load Balancer was active |
| 07 | `07-alb-api-curl-responses.png` | Public ALB endpoint returned API responses |
| 08 | `08-cloudwatch-logs.png` | CloudWatch log group and stream captured logs |
| 09 | `09-github-actions-ci-success.png` | GitHub Actions CI passed tests and Docker build |
| 10 | `10-ecr-image-additional-proof.png` | Additional ECR image proof |
| 11 | `11-local-api-terminal-proof.png` | Additional local API terminal proof |
