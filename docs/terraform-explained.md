# Terraform Explained

This document explains the Terraform files in this project.

## File Overview

| File | Purpose |
| --- | --- |
| `provider.tf` | Configures Terraform and the AWS provider |
| `variables.tf` | Defines reusable inputs such as region, project name, app port, and ECR image URI |
| `main.tf` | Creates the AWS infrastructure |
| `outputs.tf` | Prints useful deployment values after `terraform apply` |

## Provider

`provider.tf` pins the AWS provider and uses:

```hcl
provider "aws" {
  region = var.aws_region
}
```

The default region is:

```text
ap-south-1
```

## Variables

Important variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `aws_region` | `ap-south-1` | AWS region |
| `project_name` | `cloudops-api` | Resource name prefix |
| `vpc_cidr` | `10.0.0.0/16` | VPC network range |
| `public_subnet_cidrs` | `10.0.1.0/24`, `10.0.2.0/24` | Two public subnets |
| `app_port` | `8000` | FastAPI container port |
| `desired_count` | `1` | One ECS task for demo |
| `ecr_image_uri` | ECR image URI | Docker image used by ECS |

## Networking Resources

Terraform creates:

- VPC
- two public subnets
- Internet Gateway
- public route table
- route table associations

The design is intentionally simple and public-only to avoid NAT Gateway cost.

## Security Groups

ALB security group:

```text
Internet -> ALB on port 80
```

ECS task security group:

```text
ALB security group -> ECS task on port 8000
```

This is the core security boundary of the project.

## Load Balancer

Terraform creates:

- Application Load Balancer
- target group on port `8000`
- health check path `/health`
- HTTP listener on port `80`

The ALB gives the service a public DNS name and performs health checks before routing traffic.

## ECS Resources

Terraform creates:

- ECS cluster
- task definition
- ECS service

The task definition uses:

```text
launch type: FARGATE
cpu: 256
memory: 512
container: cloudops-api
container port: 8000
```

The ECS service keeps one running task attached to the target group.

## IAM Role

The ECS task execution role uses:

```text
AmazonECSTaskExecutionRolePolicy
```

This lets ECS pull the image from ECR and write logs to CloudWatch.

## CloudWatch Logs

The log group is:

```text
/ecs/cloudops-api
```

Retention is set to 7 days to avoid unlimited log growth.

## Outputs

Terraform prints:

| Output | Meaning |
| --- | --- |
| `alb_dns_name` | Public DNS name for API testing |
| `ecs_cluster_name` | ECS cluster name |
| `ecs_service_name` | ECS service name |
| `ecr_image_uri` | Image used by the task definition |
