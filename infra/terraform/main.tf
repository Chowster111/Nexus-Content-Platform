terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

# VPC
module "vpc" {
  source = "./modules/vpc"
}

# ECR
module "ecr" {
  source = "./modules/ecr"
}

# ALB
module "alb" {
  source       = "./modules/alb"
  vpc_id       = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids
}

# ECS Fargate
module "ecs_fargate" {
  source              = "./modules/ecs_fargate"
  vpc_id              = module.vpc.vpc_id
  public_subnet_ids   = module.vpc.public_subnet_ids
  alb_sg_id           = module.alb.alb_sg_id
  target_group_arn    = module.alb.backend_tg_arn
  backend_repo_url    = module.ecr.backend_repo_url
}

# Lambda
module "lambda" {
  source = "./modules/lambda"
}

# Outputs
output "alb_dns" {
  value = module.alb.alb_dns
}

output "ecr_backend_url" {
  value = module.ecr.backend_repo_url
}

output "ecr_frontend_url" {
  value = module.ecr.frontend_repo_url
}

output "lambda_arn" {
  value = module.lambda.lambda_arn
}

output "ecr_scraper_url" {
  value = module.ecr.scraper_repo_url
}
