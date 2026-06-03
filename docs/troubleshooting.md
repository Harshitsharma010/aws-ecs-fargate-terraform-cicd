# Troubleshooting Guide

This guide documents the main issues encountered or expected in the ECS Fargate deployment flow.

## ALB Returns `503 Service Temporarily Unavailable`

Likely causes:

- ECS task is still starting.
- Container image is still being pulled from ECR.
- Target group health check has not passed yet.
- Task stopped after startup.
- Security group or port mapping is incorrect.

Checks:

```bash
aws ecs describe-services --cluster cloudops-api-cluster --services cloudops-api-service --region ap-south-1
aws ecs list-tasks --cluster cloudops-api-cluster --service-name cloudops-api-service --region ap-south-1
aws elbv2 describe-target-groups --names cloudops-api-tg --region ap-south-1
```

Then use the target group ARN:

```bash
aws elbv2 describe-target-health --target-group-arn TARGET_GROUP_ARN --region ap-south-1
```

## Terraform Cannot Reach AWS STS

Example error:

```text
lookup sts.ap-south-1.amazonaws.com: no such host
```

Likely cause:

- Local DNS or network issue.

Checks:

```bash
aws sts get-caller-identity
nslookup sts.ap-south-1.amazonaws.com
ping google.com
```

Possible fix:

```bash
ipconfig /flushdns
```

Then retry:

```bash
terraform plan
```

## Docker Port `8000` Already In Use

Likely cause:

- Local Uvicorn server or another container is already using port `8000`.

Checks:

```bash
docker ps
```

Stop the running container:

```bash
docker stop CONTAINER_ID
```

## ECS Task Stops After Creation

Likely causes:

- ECR image URI is wrong.
- ECS task execution role cannot pull the image.
- Container command fails.
- App does not listen on the expected port.

Checks:

```bash
aws ecs describe-tasks --cluster cloudops-api-cluster --tasks TASK_ARN --region ap-south-1
aws logs describe-log-streams --log-group-name /ecs/cloudops-api --region ap-south-1
```

## GitHub Actions Cannot Import `app.main`

Example error:

```text
ModuleNotFoundError: No module named 'app'
```

Fix used:

```yaml
env:
  PYTHONPATH: ${{ github.workspace }}
```

This makes the repository root importable during the GitHub Actions test run.

## Terraform Destroy Fails Midway

If DNS or network fails during destroy, rerun:

```bash
terraform destroy
```

Terraform is state-aware and will continue deleting remaining resources.

Verify cleanup:

```bash
terraform state list
```

An empty output means Terraform has no remaining managed resources.
