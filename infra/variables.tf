variable "aws_region" {
  description = "AWS region for the ECS Fargate deployment."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name prefix used for AWS resources."
  type        = string
  default     = "cloudops-api"
}

variable "vpc_cidr" {
  description = "CIDR block for the project VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the two public subnets."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "app_port" {
  description = "Container port exposed by the FastAPI service."
  type        = number
  default     = 8000
}

variable "desired_count" {
  description = "Number of ECS tasks to run."
  type        = number
  default     = 1
}

variable "ecr_image_uri" {
  description = "Existing ECR image URI for the cloudops-api container."
  type        = string
  default     = "753569822016.dkr.ecr.ap-south-1.amazonaws.com/cloudops-api:latest"
}
