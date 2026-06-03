# AWS ECS Fargate Terraform CI/CD Deployment Lab

A containerized FastAPI service designed to demonstrate AWS ECS Fargate deployment using Docker, ECR, ALB, Terraform, GitHub Actions, IAM, security groups, and CloudWatch.

## What This Project Will Prove

- Dockerized backend API
- ECR image workflow
- ECS Fargate deployment
- Application Load Balancer public endpoint
- Terraform infrastructure
- GitHub Actions CI/CD
- CloudWatch logs and health checks
- IAM role and security group basics

## Completed Scope

- FastAPI app
- Dockerfile
- Local Docker testing
- ECR image workflow
- Terraform infrastructure for ECS Fargate
- Public Application Load Balancer endpoint
- CloudWatch log group with 7-day retention
- Deployment screenshots and proof

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Service status and project message |
| GET | `/health` | Health check with current UTC timestamp |
| GET | `/version` | App version and environment values |
| GET | `/metadata` | Service metadata for the deployment lab |
| GET | `/error` | Intentional exception for log validation |

## Run Locally

```bash
pip install -r app/requirements.txt
uvicorn app.main:app --reload
```

## Run With Docker

```bash
docker build -t cloudops-api .
docker run -p 8000:8000 cloudops-api
curl http://localhost:8000/health
curl http://localhost:8000/version
curl http://localhost:8000/metadata
```

## AWS Deployment

The Docker image was pushed to Amazon ECR:

```text
753569822016.dkr.ecr.ap-south-1.amazonaws.com/cloudops-api:latest
```

Terraform creates the AWS infrastructure in `ap-south-1`:

- VPC with two public subnets
- Internet Gateway and public route table
- Application Load Balancer on port `80`
- Target group forwarding to container port `8000`
- ECS cluster and Fargate service
- ECS task definition using the ECR image
- ECS task execution IAM role
- Security groups for ALB and ECS tasks
- CloudWatch log group `/ecs/cloudops-api`

Run Terraform from the `infra/` folder:

```bash
terraform init
terraform plan
terraform apply
```

After apply, Terraform outputs the ALB DNS name. Test the deployed API:

```bash
curl http://cloudops-api-alb-380403081.ap-south-1.elb.amazonaws.com/health
curl http://cloudops-api-alb-380403081.ap-south-1.elb.amazonaws.com/version
curl http://cloudops-api-alb-380403081.ap-south-1.elb.amazonaws.com/metadata
```

## Deployment Proof

Screenshots are stored in `screenshots/` and include proof of:

- ECR image pushed with the `latest` tag
- Terraform apply output
- ECS cluster and service running
- Fargate task running
- ALB public endpoint responding
- Target group health check passing
- CloudWatch log group and log stream

## Destroy After Demo

This project creates AWS resources that can incur charges, especially the Application Load Balancer and ECS Fargate task. Destroy the infrastructure after testing and screenshots:

```bash
cd infra
terraform destroy
```

## Next Planned Steps

- Add GitHub Actions CI/CD
- Improve documentation with a step-by-step deployment guide
- Add more screenshots as deployment proof

## Known Limitation

GitHub Actions CI/CD is not added yet. The current deployment is manual using Docker, ECR, Terraform, and AWS CLI.
