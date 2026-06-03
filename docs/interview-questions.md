# Interview Questions

This document helps explain the ECS Fargate lab without relying on the original build instructions.

## Core Architecture

### What happens when a user calls the ALB URL?

The request reaches the Application Load Balancer on port `80`. The ALB listener forwards the request to a target group configured for port `8000`. The target group routes traffic to the ECS Fargate task IP. The FastAPI container handles the request and returns JSON. Container logs are sent to CloudWatch Logs.

### Why use ECS Fargate instead of EC2?

Fargate runs containers without managing EC2 instances. It is useful for this lab because it demonstrates container deployment, task definitions, services, and load balancing while avoiding server patching and instance management.

### Why use ECR?

ECR stores the Docker image in AWS so ECS can pull it during task startup. The task definition references the ECR image URI.

### Why does the ALB listen on port `80` while the app listens on port `8000`?

Users call the public ALB over standard HTTP port `80`. The ALB forwards traffic internally to the container port `8000`, where Uvicorn serves the FastAPI app.

### Why does the ECS task security group allow port `8000` only from the ALB?

This prevents direct public access to the task. Internet traffic must enter through the ALB security group, and only the ALB can reach the backend container port.

### Why were public subnets used?

This cost-conscious lab avoids NAT Gateway and private subnets. The ECS task uses a public IP so it can pull the ECR image and send logs without adding NAT Gateway cost.

## Terraform

### What does Terraform manage in this project?

Terraform manages the VPC, public subnets, Internet Gateway, route table, security groups, ALB, target group, listener, ECS cluster, CloudWatch log group, IAM execution role, ECS task definition, and ECS service.

### What is Terraform state?

Terraform state records the real AWS resources created by Terraform. It lets Terraform know what exists so future `plan`, `apply`, and `destroy` commands can calculate changes correctly.

### Why should `terraform.tfstate` not be committed?

State can contain sensitive infrastructure details and is environment-specific. It should stay local for this lab or be stored in a secure remote backend in a more mature workflow.

### Why run `terraform destroy`?

The ALB and Fargate task can create ongoing AWS charges. Destroying the stack after screenshots and verification stops the demo resources from continuing to run.

## Operations

### Why did the ALB return `503` at first?

The ALB can return `503 Service Temporarily Unavailable` while ECS is still starting the task, pulling the image, or waiting for the target group health check to pass.

### How do you check if the service is healthy?

Use the ALB URL:

```bash
curl http://ALB_DNS_NAME/health
```

Also check the ECS service, target group health, and CloudWatch logs.

### What does CloudWatch prove here?

CloudWatch proves that the ECS task is running with the `awslogs` log driver and that container runtime logs are being captured centrally.

## CI/CD

### What does the current CI workflow do?

The GitHub Actions workflow runs on push and pull request to `main`. It installs Python 3.12 dependencies, runs API endpoint tests with `pytest`, and builds the Docker image.

### Why does CI not deploy yet?

The current workflow intentionally avoids AWS secrets and deployment. It validates code and Docker build only. Deployment automation can be added later after the manual deployment path is understood.
