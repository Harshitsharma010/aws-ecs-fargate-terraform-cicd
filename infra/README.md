# Terraform Infrastructure

This folder contains Terraform for the AWS ECS Fargate deployment phase of the project.

## What Terraform Creates

- VPC with CIDR `10.0.0.0/16`
- Two public subnets in different availability zones
- Internet Gateway
- Public route table
- Security group for the Application Load Balancer allowing inbound HTTP on port `80`
- Security group for ECS tasks allowing inbound port `8000` only from the ALB
- Application Load Balancer
- Target group on port `8000` with health check path `/health`
- HTTP listener on port `80`
- ECS cluster
- CloudWatch log group with 7-day retention
- IAM ECS task execution role with `AmazonECSTaskExecutionRolePolicy`
- ECS Fargate task definition for `cloudops-api`
- ECS Fargate service with desired count `1` and public IP enabled

## Terraform Commands

Initialize Terraform:

```bash
terraform init
```

Preview the infrastructure changes:

```bash
terraform plan
```

Create the infrastructure:

```bash
terraform apply
```

Destroy the infrastructure after the demo:

```bash
terraform destroy
```

## Cost Warning

This setup is intentionally simple and avoids NAT Gateway, RDS, private subnets, Route 53, and other paid extras. However, resources such as the Application Load Balancer, ECS Fargate tasks, CloudWatch logs, and data transfer can still create AWS charges.

Run `terraform destroy` after the demo to avoid ongoing charges.
