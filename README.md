# AWS ECS Fargate Terraform CI/CD Deployment Lab

Containerized FastAPI service deployed to AWS ECS Fargate using Docker, Amazon ECR, Terraform, Application Load Balancer, IAM, security groups, and CloudWatch Logs.

> **Status**  
> Manual AWS deployment completed and verified. Infrastructure was destroyed after screenshots to avoid ongoing AWS charges.

## Project Overview

This project demonstrates a production-style cloud deployment flow for a small backend API. The API is packaged as a Docker image, pushed to Amazon ECR, and deployed to ECS Fargate behind a public Application Load Balancer.

The goal is to show the core CloudOps workflow without adding unnecessary services such as NAT Gateway, RDS, Route 53, Kubernetes, or private networking.

## Remote Reviewer Snapshot

| Question | Answer |
| --- | --- |
| What was deployed? | A Dockerized FastAPI API named `cloudops-api` |
| Where did it run? | AWS ECS Fargate in `ap-south-1` |
| How was infrastructure created? | Terraform HCL in `infra/` |
| How was traffic routed? | Public ALB on port `80` to ECS task port `8000` |
| How were logs captured? | CloudWatch Logs group `/ecs/cloudops-api` |
| How was CI validated? | GitHub Actions ran API tests and Docker image build |
| Was cost controlled? | Yes. The Terraform stack was destroyed after proof capture |

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

Full architecture notes are available in [`docs/architecture.md`](docs/architecture.md).

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
|-- app/
|   |-- main.py
|   `-- requirements.txt
|-- infra/
|   |-- provider.tf
|   |-- variables.tf
|   |-- main.tf
|   |-- outputs.tf
|   `-- README.md
|-- docs/
|   |-- README.md
|   `-- architecture.md
|-- screenshots/
|   `-- numbered deployment proof images
|-- Dockerfile
|-- .dockerignore
|-- .gitignore
`-- README.md
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

## Continuous Integration

GitHub Actions runs a CI workflow on every push and pull request to `main`.

The workflow validates:

- Python 3.12 dependency installation
- FastAPI endpoint tests with `pytest` and `httpx`
- Docker image build with `docker build -t cloudops-api .`

The CI workflow does not deploy to AWS, push to ECR, or require AWS secrets.

CI proof is captured in [`09-github-actions-ci-success.png`](screenshots/09-github-actions-ci-success.png).

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

| Step | Proof | Screenshot |
| --- | --- | --- |
| 01 | Terraform apply completed | [`01-terraform-apply-success.png`](screenshots/01-terraform-apply-success.png) |
| 02 | ECR image pushed | [`02-ecr-image-latest.png`](screenshots/02-ecr-image-latest.png) |
| 03 | ECS cluster active | [`03-ecs-cluster-active.png`](screenshots/03-ecs-cluster-active.png) |
| 04 | ECS service running | [`04-ecs-service-running.png`](screenshots/04-ecs-service-running.png) |
| 05 | Target group healthy | [`05-target-group-healthy.png`](screenshots/05-target-group-healthy.png) |
| 06 | Load balancer active | [`06-load-balancer-active.png`](screenshots/06-load-balancer-active.png) |
| 07 | ALB endpoint returned API responses | [`07-alb-api-curl-responses.png`](screenshots/07-alb-api-curl-responses.png) |
| 08 | CloudWatch log group and stream | [`08-cloudwatch-logs.png`](screenshots/08-cloudwatch-logs.png) |
| 09 | GitHub Actions CI passed | [`09-github-actions-ci-success.png`](screenshots/09-github-actions-ci-success.png) |

## Cost Control

This lab intentionally avoids NAT Gateway, RDS, Route 53, EKS, private subnets, and other paid extras. The Application Load Balancer, ECS Fargate task, CloudWatch logs, and data transfer can still generate charges while running.

Destroy the infrastructure after testing:

```bash
cd infra
terraform destroy
```

The demo infrastructure was destroyed after proof capture, and `terraform state list` returned no managed resources.

## Current Limitations

- GitHub Actions currently runs CI only; deployment automation is not added yet.
- Deployment is currently manual through Docker, AWS CLI, ECR, and Terraform.
- The public ALB endpoint is not permanently live because resources were destroyed after verification.

## Next Planned Step

Add GitHub Actions CD to push the Docker image to ECR and deploy updates to ECS automatically.
