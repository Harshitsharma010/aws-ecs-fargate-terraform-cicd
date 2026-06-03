# Architecture Notes

This document explains the AWS ECS Fargate deployment in interview-friendly language.

## Request Flow

```text
User or API client
  |
  | HTTP request on port 80
  v
Application Load Balancer
  |
  | forwards to target group on port 8000
  v
ECS Fargate task
  |
  | runs Docker container: cloudops-api
  v
FastAPI application
```

The public entry point is the Application Load Balancer. The FastAPI container listens on port `8000`, but users access the service through ALB port `80`.

## AWS Components

| Component | Purpose |
| --- | --- |
| VPC | Isolates the project network with CIDR `10.0.0.0/16` |
| Public subnets | Place the ALB and Fargate task in reachable availability zones |
| Internet Gateway | Allows public internet traffic to reach the ALB |
| Route table | Sends outbound internet traffic through the Internet Gateway |
| ALB security group | Allows inbound HTTP `80` from the internet |
| ECS security group | Allows inbound `8000` only from the ALB security group |
| Target group | Tracks Fargate task IPs and checks `/health` |
| ECS cluster | Logical group that runs the Fargate service |
| Task definition | Defines CPU, memory, image, port, environment variables, and logs |
| ECS service | Keeps one Fargate task running and attached to the target group |
| CloudWatch log group | Stores container logs under `/ecs/cloudops-api` |
| IAM execution role | Lets ECS pull the ECR image and write logs |

## Security Boundary

The ECS task is not directly opened to the entire internet. Its security group allows inbound traffic only from the ALB security group on port `8000`.

```text
Internet -> ALB security group -> ECS task security group -> container port 8000
```

This demonstrates the basic production pattern of exposing the load balancer publicly while keeping backend tasks behind controlled security group rules.

## Health Check Behavior

The ALB target group calls:

```text
GET /health
```

A healthy response returns:

```json
{
  "status": "healthy",
  "timestamp": "UTC timestamp ending with Z"
}
```

If the task is still starting, image pulling, or failing, the ALB can temporarily return `503 Service Temporarily Unavailable` until a healthy target is registered.

## Cost Control

This lab avoids NAT Gateway, RDS, Route 53, private subnets, SageMaker, Bedrock, and Kubernetes. The main cost-bearing resources are the Application Load Balancer, Fargate task runtime, CloudWatch logs, and data transfer.

The infrastructure was destroyed after proof capture:

```bash
terraform destroy
terraform state list
```

An empty `terraform state list` confirmed that Terraform had no remaining managed AWS resources.

## Interview Explanation

In one sentence:

> I deployed a Dockerized FastAPI service to AWS ECS Fargate with Terraform, exposed it through an ALB, restricted backend access with security groups, shipped logs to CloudWatch, verified health checks, and destroyed the infrastructure after capturing proof to control cost.
