#!/bin/bash

# Engineering Blog Recommendation System - Terraform Deployment Script
# This script deploys the infrastructure using Terraform

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TERRAFORM_DIR="infra/terraform"
BACKEND_BUCKET="your-terraform-state-bucket"
DYNAMODB_TABLE="terraform-lock-table"
AWS_REGION="us-east-1"
ENVIRONMENT="dev"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        print_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

# Function to check AWS credentials
check_aws_credentials() {
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Please run 'aws configure' first."
        exit 1
    fi
    print_success "AWS credentials verified"
}

# Function to check if S3 backend bucket exists
check_backend_bucket() {
    if ! aws s3 ls "s3://$BACKEND_BUCKET" &> /dev/null; then
        print_warning "Backend bucket '$BACKEND_BUCKET' does not exist. Creating it..."
        aws s3 mb "s3://$BACKEND_BUCKET" --region $AWS_REGION
        aws s3api put-bucket-versioning --bucket $BACKEND_BUCKET --versioning-configuration Status=Enabled
        aws s3api put-bucket-encryption --bucket $BACKEND_BUCKET --server-side-encryption-configuration '{
            "Rules": [
                {
                    "ApplyServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        }'
        print_success "Backend bucket created and configured"
    else
        print_success "Backend bucket exists"
    fi
}

# Function to check if DynamoDB table exists
check_dynamodb_table() {
    if ! aws dynamodb describe-table --table-name $DYNAMODB_TABLE &> /dev/null; then
        print_warning "DynamoDB table '$DYNAMODB_TABLE' does not exist. Creating it..."
        aws dynamodb create-table \
            --table-name $DYNAMODB_TABLE \
            --attribute-definitions AttributeName=LockID,AttributeType=S \
            --key-schema AttributeName=LockID,KeyType=HASH \
            --billing-mode PAY_PER_REQUEST \
            --region $AWS_REGION
        print_success "DynamoDB table created"
    else
        print_success "DynamoDB table exists"
    fi
}

# Function to initialize Terraform
init_terraform() {
    print_status "Initializing Terraform..."
    cd $TERRAFORM_DIR
    terraform init
    print_success "Terraform initialized"
}

# Function to validate Terraform configuration
validate_terraform() {
    print_status "Validating Terraform configuration..."
    terraform validate
    print_success "Terraform configuration is valid"
}

# Function to format Terraform code
format_terraform() {
    print_status "Formatting Terraform code..."
    terraform fmt -recursive
    print_success "Terraform code formatted"
}

# Function to plan Terraform deployment
plan_terraform() {
    print_status "Creating Terraform plan..."
    terraform plan -out=tfplan
    print_success "Terraform plan created"
}

# Function to apply Terraform changes
apply_terraform() {
    print_status "Applying Terraform changes..."
    terraform apply tfplan
    print_success "Terraform changes applied successfully"
}

# Function to show outputs
show_outputs() {
    print_status "Terraform outputs:"
    terraform output
}

# Function to clean up plan file
cleanup() {
    if [ -f "tfplan" ]; then
        rm tfplan
        print_status "Cleaned up plan file"
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  init      - Initialize Terraform and check prerequisites"
    echo "  plan      - Create a Terraform plan"
    echo "  apply     - Apply Terraform changes"
    echo "  deploy    - Full deployment (init, plan, apply)"
    echo "  destroy   - Destroy all resources (use with caution)"
    echo "  validate  - Validate Terraform configuration"
    echo "  format    - Format Terraform code"
    echo "  outputs   - Show Terraform outputs"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 init      # Initialize and check prerequisites"
    echo "  $0 plan      # Create a plan"
    echo "  $0 apply     # Apply changes"
    echo "  $0 deploy    # Full deployment"
}

# Function to handle destroy
destroy_terraform() {
    print_warning "This will destroy ALL resources. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Destroying Terraform resources..."
        terraform destroy -auto-approve
        print_success "Resources destroyed"
    else
        print_status "Destroy cancelled"
    fi
}

# Main script logic
main() {
    case "${1:-help}" in
        "init")
            print_status "Checking prerequisites..."
            check_command "terraform"
            check_command "aws"
            check_aws_credentials
            check_backend_bucket
            check_dynamodb_table
            init_terraform
            validate_terraform
            format_terraform
            print_success "Initialization complete"
            ;;
        "plan")
            cd $TERRAFORM_DIR
            validate_terraform
            format_terraform
            plan_terraform
            ;;
        "apply")
            cd $TERRAFORM_DIR
            if [ ! -f "tfplan" ]; then
                print_error "No plan file found. Run '$0 plan' first."
                exit 1
            fi
            apply_terraform
            show_outputs
            cleanup
            ;;
        "deploy")
            print_status "Starting full deployment..."
            $0 init
            $0 plan
            $0 apply
            print_success "Deployment complete!"
            ;;
        "destroy")
            cd $TERRAFORM_DIR
            destroy_terraform
            ;;
        "validate")
            cd $TERRAFORM_DIR
            validate_terraform
            ;;
        "format")
            cd $TERRAFORM_DIR
            format_terraform
            ;;
        "outputs")
            cd $TERRAFORM_DIR
            show_outputs
            ;;
        "help"|*)
            show_usage
            ;;
    esac
}

# Trap to clean up on exit
trap cleanup EXIT

# Run main function with all arguments
main "$@" 