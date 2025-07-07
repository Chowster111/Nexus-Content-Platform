# Infrastructure as Code — Terraform for Dev Environment

## Overview

This `infra/terraform` setup provisions our entire development infrastructure on AWS using a **modular Terraform architecture**. It uses best practices for clear separation of concerns, reusability, and security.

The key components are:

* **VPC** with public subnets to host our resources.
* **ECR (Elastic Container Registry)** for storing and versioning our Docker images.
* **ECS (Elastic Container Service) with Fargate** for serverless container orchestration.
* **ALB (Application Load Balancer)** to expose our services to the internet.
* **Lambda** for batch jobs and scraping tasks that do not require always-on containers.
* Optional **S3 remote state backend** with DynamoDB for state locking.

This setup is intended for the **development environment** but follows patterns that scale well for staging and production with minimal adjustments.

---

## File & Folder Structure

```
infra/terraform/
├── main.tf
├── backend.tf
├── provider.tf
├── variables.tf
├── outputs.tf
├── modules/
│   ├── vpc/
│   ├── ecr/
│   ├── alb/
│   ├── ecs_fargate/
│   ├── lambda/
```

### Root-level files

* **`main.tf`**
  Orchestrates all modules. It declares how modules connect and passes the required inputs and outputs between them.

* **`backend.tf`** (optional but recommended)
  Defines the **remote backend** configuration for storing Terraform state in an S3 bucket and locking it with DynamoDB. This prevents multiple team members from corrupting state during simultaneous applies. For development, local state is acceptable, but remote state is the standard for real environments.

* **`provider.tf`**
  Configures the AWS provider, region, and version constraints.

* **`variables.tf`**
  Declares root-level variables such as the AWS region and any shared configuration values. Keeps configuration consistent and flexible.

* **`outputs.tf`**
  Exposes useful output values such as the ALB DNS name, ECR repository URLs, and Lambda ARNs so they can be referenced externally or by deployment pipelines.

---

## Modules

Each major piece of infrastructure is implemented as a reusable module. This pattern promotes clarity, reusability, and testability.

### `modules/vpc/`

* Creates the VPC, public subnets, internet gateway, route tables, and subnet associations.
* Provides output values for the VPC ID and public subnet IDs, which are consumed by other modules.

**Why:**
A dedicated networking layer allows flexible scaling later. Even for dev, having this explicit avoids hardcoding or assuming default VPCs.

---

### `modules/ecr/`

* Provisions ECR repositories for the backend and frontend containers.
* Outputs the repository URLs so Docker images can be tagged and pushed as part of the CI/CD pipeline.

**Why:**
Separates image storage from the compute layer. Using ECR instead of Docker Hub reduces latency, integrates IAM permissions, and improves security.

---

### `modules/alb/`

* Creates an Application Load Balancer with security groups.
* Configures a listener and target group to forward traffic to the ECS tasks.
* Exposes the ALB DNS for testing or DNS configuration.

**Why:**
An ALB decouples incoming traffic from your compute resources. This pattern supports scaling containers independently, and provides better observability and routing flexibility.

---

### `modules/ecs_fargate/`

* Sets up the ECS cluster, task definition for the backend container, ECS service, and related security groups.
* Connects the service to the ALB’s target group.

**Why:**
Fargate abstracts away EC2 management. It’s ideal for a dev environment because you don’t maintain servers or clusters. The tradeoff is higher cost per compute unit compared to reserved EC2 instances, but the operational simplicity is worth it in dev.

---

### `modules/lambda/`

* Provisions an IAM role for Lambda execution.
* Creates a simple Lambda function that can be updated with zipped code (e.g., a scraper job).

**Why:**
Batch jobs or event-driven tasks often don’t justify an always-running container. Lambda gives you serverless compute for lightweight tasks. For more complex scraping, you could switch to containers on ECS instead.

---

## Trade-offs and Design Considerations

### Remote vs. Local State

* Using an **S3 backend with DynamoDB locking** prevents concurrent updates from breaking state. For solo development, local state is acceptable but risks accidental overwrites if multiple engineers apply changes simultaneously.

### VPC Design

* The VPC uses only public subnets for simplicity in dev. In production, a more robust design would include private subnets, NAT gateways, and strict security group rules for defense in depth.

### Fargate vs. EC2 ECS

* Fargate reduces operational overhead by abstracting the host infrastructure. It costs more per CPU/GB than managing EC2 instances but speeds up iteration and testing for development workloads.

### Modules

* Modules increase clarity but add a bit of upfront complexity. In return, you gain reusable, testable building blocks that simplify scaling to multiple environments.

---

## Deployment Workflow

1. **Initialize Terraform**

   ```bash
   terraform init
   ```

   This configures the backend and downloads module dependencies.

2. **Plan Changes**

   ```bash
   terraform plan
   ```

   Review all changes before applying.

3. **Apply Infrastructure**

   ```bash
   terraform apply
   ```

   This provisions the VPC, ECR repos, ECS cluster, ALB, and Lambda function.

4. **Push Docker Images**
   Use the ECR URLs from `terraform output` to tag and push your containers.

   ```bash
   aws ecr get-login-password --region <region> | \
     docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

   docker build -t backend .
   docker tag backend:latest <repo_url>:latest
   docker push <repo_url>:latest
   ```

5. **Verify**
   Use the ALB DNS output to test your deployed containers.

---

## Future Improvements

* Add parameterized environments for staging and production using workspaces or separate state files.
* Introduce private networking with NAT gateways for improved security.
* Add an RDS or DynamoDB module if you need a managed database.
* Integrate CI/CD pipelines to build images, push to ECR, and run `terraform apply` automatically.

---

## Summary

This structure provides a robust, modular foundation for deploying containerized applications on AWS using ECS Fargate, along with serverless batch processing via Lambda.
The trade-offs balance cost, simplicity, and flexibility making it ideal for iterative development while following patterns that scale well in production.



