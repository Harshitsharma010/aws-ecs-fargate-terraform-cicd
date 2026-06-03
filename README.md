# AWS ECS Fargate Terraform CI/CD Deployment Lab

Containerized FastAPI service deployed to AWS ECS Fargate using Docker, Amazon ECR, Terraform, Application Load Balancer, IAM, security groups, and CloudWatch Logs.

> **Status**  
> Manual AWS deployment completed and verified. Infrastructure was destroyed after screenshots to avoid ongoing AWS charges.

## Project Overview

This project demonstrates a production-style cloud deployment flow for a small backend API. The API is packaged as a Docker image, pushed to Amazon ECR, and deployed to ECS Fargate behind a public Application Load Balancer.

The goal is to show the core CloudOps workflow without adding unnecessary services such as NAT Gateway, RDS, Route 53, Kubernetes, or private networking.

## What This Project Proves

| Area | Proof |
| --- | --- |
| Backend API | FastAPI service with health, version, metadata, and error endpoints |
| Containerization | Dockerfile builds a runnable `cloudops-api` image |
| Image registry | Docker image pushed to Amazon ECR |
| Infrastructure as Code | Terraform creates AWS networking, ECS, ALB, IAM, and logs |
| Compute | ECS Fargate runs the container without managing EC2 servers |
| Public routing | ALB exposes the API over HTTP port `80` |
| Health checks | ALB target group checks `/health` on container port `8000` |
| Observability | Container logs are shipped to CloudWatch Logs |
| Cost control | Infrastructure can be destroyed with `terraform destroy` |

## Architecture

```text
User
  |
  | HTTP :80
  v
Application Load Balancer
  |
  | Target group :8000
  v
ECS Fargate Service
  |
  | Runs container image
  v
Amazon ECR: cloudops-api:latest

ECS task logs -> CloudWatch Logs: /ecs/cloudops-api
```

## Tech Stack

| Layer | Tooling |
| --- | --- |
| API | FastAPI, Uvicorn |
| Runtime | Python 3.12 slim container |
| Container | Docker |
| Registry | Amazon ECR |
| Infrastructure | Terraform |
| Compute | AWS ECS Fargate |
| Networking | VPC, public subnets, Internet Gateway, ALB |
| Security | IAM task execution role, ALB and ECS security groups |
| Logs | Amazon CloudWatch Logs |

## Repository Structure

```text
aws-ecs-fargate-terraform-cicd/
├── app/
│   ├── main.py
│   └── requirements.txt
├── infra/
│   ├── provider.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   └── README.md
├── docs/
│   └── README.md
├── screenshots/
│   └── deployment proof images
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Service status and project message |
| `GET` | `/health` | Health check with current UTC timestamp |
| `GET` | `/version` | Returns `APP_VERSION` and `APP_ENV` |
| `GET` | `/metadata` | Returns runtime and target platform metadata |
| `GET` | `/error` | Raises an intentional exception for CloudWatch log validation |

## Run Locally

Install dependencies:

```bash
pip install -r app/requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Test endpoints:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/metadata
```

## Run With Docker

Build the image:

```bash
docker build -t cloudops-api .
```

Run the container:

```bash
docker run -p 8000:8000 cloudops-api
```

Test the containerized API:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/version
curl http://127.0.0.1:8000/metadata
```

## AWS Deployment

The Docker image was pushed to Amazon ECR:

```text
753569822016.dkr.ecr.ap-south-1.amazonaws.com/cloudops-api:latest
```

Terraform deploys the AWS infrastructure in `ap-south-1`.

### Terraform Commands

Run from the `infra/` directory:

```bash
terraform init
terraform plan
terraform apply
```

After deployment, Terraform outputs:

| Output | Description |
| --- | --- |
| `alb_dns_name` | Public ALB DNS name for API testing |
| `ecs_cluster_name` | ECS cluster created by Terraform |
| `ecs_service_name` | ECS service running the Fargate task |
| `ecr_image_uri` | ECR image used by the task definition |

### Deployed Endpoint Tests

The deployed API was verified through the ALB DNS name:

```bash
curl http://cloudops-api-alb-380403081.ap-south-1.elb.amazonaws.com/health
curl http://cloudops-api-alb-380403081.ap-south-1.elb.amazonaws.com/version
curl http://cloudops-api-alb-380403081.ap-south-1.elb.amazonaws.com/metadata
```

Example successful responses:

```json
{"status":"healthy","timestamp":"2026-06-03T21:56:35.468463Z"}
{"version":"1.0.0","environment":"dev"}
{"service":"cloudops-api","runtime":"FastAPI","containerized":true,"target_platform":"AWS ECS Fargate","logs":"CloudWatch"}
```

> **Note**  
> The live ALB endpoint was destroyed after verification to prevent ongoing AWS charges. Screenshots in this repository document the successful deployment.

## Deployment Proof

| Proof | Screenshot |
| --- | --- |
| Terraform apply completed | [`terraform-apply-success.png`](screenshots/terraform-apply-success.png) |
| ALB endpoint returned API responses | [`alb-curl-health-version-metadata.png`](screenshots/alb-curl-health-version-metadata.png) |
| ECS cluster created | [`ecs-cluster.png`](screenshots/ecs-cluster.png) |
| ECS service running | [`ecs-service-running.png`](screenshots/ecs-service-running.png) |
| Target group healthy | [`target-group-healthy.png`](screenshots/target-group-healthy.png) |
| Load balancer active | [`load-balancer-active.png`](screenshots/load-balancer-active.png) |
| CloudWatch log group and stream | [`cloudwatch-logs.png`](screenshots/cloudwatch-logs.png) |
| ECR image pushed | [`ecr-image-latest.png`](screenshots/ecr-image-latest.png) |

## Cost Control

This lab intentionally avoids NAT Gateway, RDS, Route 53, EKS, private subnets, and other paid extras. The Application Load Balancer, ECS Fargate task, CloudWatch logs, and data transfer can still generate charges while running.

Destroy the infrastructure after testing:

```bash
cd infra
terraform destroy
```

The demo infrastructure was destroyed after proof capture, and `terraform state list` returned no managed resources.

## Current Limitations

- GitHub Actions CI/CD is not added yet.
- Deployment is currently manual through Docker, AWS CLI, ECR, and Terraform.
- The public ALB endpoint is not permanently live because resources were destroyed after verification.

## Next Planned Step

Add GitHub Actions CI/CD to build the Docker image, push it to ECR, and deploy updates to ECS automatically.
