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

## Current MVP Scope

- FastAPI app
- Dockerfile
- Local Docker testing
- Placeholder folders for infra, docs, screenshots, workflows

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

## Next Planned AWS Steps

- Create ECR repository
- Push Docker image to ECR
- Write Terraform for VPC, ECS Fargate, ALB, security groups, IAM, and CloudWatch logs
- Add GitHub Actions CI/CD
- Add screenshots and deployment proof

## Known Limitation

This first version is only a local containerized API. AWS infrastructure will be added in the next phase.
