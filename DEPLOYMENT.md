# Deployment Guide

This guide explains how to deploy the Engineering Blog Recommendation System infrastructure using Terraform.

## Prerequisites

Before deploying, ensure you have the following installed:

- **Terraform** (>= 1.5.0)
- **AWS CLI** (>= 2.0)
- **Docker** (for building container images)
- **Git**

## Quick Start

1. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

2. **Update the backend configuration:**
   Edit `infra/terraform/backend.tf` and update the bucket name:
   ```hcl
   terraform {
     backend "s3" {
       bucket         = "your-unique-terraform-state-bucket"
       key            = "dev/terraform.tfstate"
       region         = "us-east-1"
       dynamodb_table = "terraform-lock-table"
       encrypt        = true
     }
   }
   ```

3. **Deploy the infrastructure:**
   ```bash
   ./deploy.sh deploy
   ```

## Deployment Script Usage

The `deploy.sh` script provides several commands:

### Initialize and Check Prerequisites
```bash
./deploy.sh init
```
This command:
- Checks if Terraform and AWS CLI are installed
- Verifies AWS credentials
- Creates S3 backend bucket if it doesn't exist
- Creates DynamoDB lock table if it doesn't exist
- Initializes Terraform
- Validates and formats the configuration

### Create a Deployment Plan
```bash
./deploy.sh plan
```
Creates a Terraform plan showing what resources will be created/modified.

### Apply Changes
```bash
./deploy.sh apply
```
Applies the Terraform plan and creates/modifies resources.

### Full Deployment
```bash
./deploy.sh deploy
```
Runs the complete deployment process (init → plan → apply).

### Validate Configuration
```bash
./deploy.sh validate
```
Validates the Terraform configuration.

### Format Code
```bash
./deploy.sh format
```
Formats all Terraform files.

### Show Outputs
```bash
./deploy.sh outputs
```
Displays Terraform outputs (ALB DNS, ECR URLs, etc.).

### Destroy Resources
```bash
./deploy.sh destroy
```
⚠️ **Use with caution** - Destroys all resources.

## Infrastructure Components

The deployment creates the following AWS resources:

### VPC and Networking
- **VPC** with public and private subnets
- **Internet Gateway** for public subnets
- **NAT Gateway** for private subnets
- **Security Groups** for ALB and ECS

### Container Registry
- **ECR repositories** for backend and frontend images

### Load Balancer
- **Application Load Balancer** with target groups
- **HTTPS listener** (requires SSL certificate)

### Container Orchestration
- **ECS Fargate cluster**
- **ECS services** for backend and frontend
- **Auto scaling** based on CPU/memory usage

### Additional Services
- **Lambda function** (if configured)
- **CloudWatch logs** for monitoring

## Configuration

### Environment Variables

You can customize the deployment by setting environment variables:

```bash
export AWS_REGION="us-west-2"
export BACKEND_BUCKET="my-terraform-state"
export ENVIRONMENT="production"
```

### Terraform Variables

Create a `terraform.tfvars` file to customize the deployment:

```hcl
aws_region = "us-east-1"
environment = "dev"
backend_cpu = "512"
backend_memory = "1024"
frontend_cpu = "256"
frontend_memory = "512"
```

## Deployment Process

1. **Backend Setup:**
   - Creates S3 bucket for Terraform state
   - Creates DynamoDB table for state locking
   - Initializes Terraform backend

2. **Infrastructure Creation:**
   - VPC and networking components
   - ECR repositories
   - ALB and target groups
   - ECS cluster and services

3. **Application Deployment:**
   - Builds and pushes Docker images to ECR
   - Updates ECS services with new images
   - Configures auto scaling

## Monitoring and Troubleshooting

### Check Deployment Status
```bash
# View ECS services
aws ecs list-services --cluster engineering-blog-rec-system

# Check service status
aws ecs describe-services --cluster engineering-blog-rec-system --services backend-service

# View logs
aws logs describe-log-groups --log-group-name-prefix /ecs/
```

### Common Issues

1. **Backend bucket doesn't exist:**
   - The script will create it automatically
   - Ensure your AWS credentials have S3 permissions

2. **ECS tasks not starting:**
   - Check security group rules
   - Verify subnet configuration
   - Check CloudWatch logs for errors

3. **ALB health checks failing:**
   - Verify backend service is running
   - Check health check path and port
   - Ensure security groups allow traffic

## Security Considerations

- **State Encryption:** Terraform state is encrypted in S3
- **IAM Roles:** ECS tasks use least-privilege IAM roles
- **Security Groups:** Restrictive security group rules
- **HTTPS:** ALB uses HTTPS (requires SSL certificate)

## Cost Optimization

- **Fargate Spot:** Use spot instances for non-critical workloads
- **Auto Scaling:** Configure appropriate scaling policies
- **Resource Sizing:** Start with minimal resources and scale up
- **Monitoring:** Use CloudWatch to monitor costs

## Cleanup

To destroy all resources:

```bash
./deploy.sh destroy
```

⚠️ **Warning:** This will permanently delete all resources and data.

## Support

For issues or questions:
1. Check the CloudWatch logs
2. Review the Terraform plan output
3. Verify AWS credentials and permissions
4. Check the application logs in ECS 