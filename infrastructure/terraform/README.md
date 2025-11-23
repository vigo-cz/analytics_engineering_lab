# Terraform Infrastructure for AWS

Complete Terraform setup for deploying the Analytics Engineering Lab to AWS.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────▼────┐
                    │   ALB   │ (Load Balancer)
                    └────┬────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼────┐     ┌────▼────┐     ┌────▼────┐
   │Streamlit│     │ Jupyter │     │Metabase │
   └────┬────┘     └────┬────┘     └────┬────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                    ┌────▼────┐
                    │   ECS   │ (Fargate)
                    │ Private │
                    │ Subnet  │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │   RDS   │ (PostgreSQL)
                    │ Private │
                    │ Subnet  │
                    └─────────┘
```

## Resources Created

- **VPC** with public and private subnets across 2 AZs
- **Application Load Balancer** (ALB) for routing traffic
- **ECS Fargate** cluster and service for running containers
- **RDS PostgreSQL** database (Multi-AZ for production)
- **ECR** repository for Docker images
- **Security Groups** with least-privilege access
- **IAM Roles** for ECS tasks
- **Secrets Manager** for sensitive data
- **CloudWatch Logs** for monitoring

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **Terraform** >= 1.0 installed
4. **Docker** installed (for building images)

## Quick Start

### 1. Configure AWS Credentials

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

### 2. Set Variables

```bash
# Copy example variables file
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
# Set database password via environment variable
export TF_VAR_db_password="your-secure-password-here"
```

### 3. Initialize Terraform

```bash
cd infrastructure/terraform
terraform init
```

### 4. Plan Deployment

```bash
terraform plan
```

Review the plan to see what resources will be created.

### 5. Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted. This will take ~10-15 minutes.

### 6. Build and Push Docker Image

```bash
# Get ECR login command from Terraform output
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(terraform output -raw ecr_repository_url | cut -d'/' -f1)

# Build image
docker build -t $(terraform output -raw ecr_repository_url):latest ../../

# Push image
docker push $(terraform output -raw ecr_repository_url):latest
```

### 7. Update ECS Service

```bash
aws ecs update-service \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --service $(terraform output -raw ecs_service_name) \
  --force-new-deployment \
  --region us-east-1
```

### 8. Access Your Applications

```bash
# Get URLs
terraform output alb_url
terraform output streamlit_url
terraform output jupyter_url
terraform output metabase_url
```

## Configuration

### Environment Variables

Set these before running Terraform:

```bash
export TF_VAR_db_password="your-secure-password"
export TF_VAR_aws_region="us-east-1"
export TF_VAR_environment="dev"
```

### terraform.tfvars

Key variables to customize:

```hcl
aws_region  = "us-east-1"
environment = "dev"  # or "staging", "prod"

# ECS sizing
ecs_task_cpu    = 2048  # 2 vCPUs
ecs_task_memory = 4096  # 4 GB

# RDS sizing
db_instance_class = "db.t3.micro"  # Free tier
```

## Cost Estimation

**Development Environment** (~$50-100/month):
- ECS Fargate: ~$30/month (2 vCPU, 4GB RAM)
- RDS db.t3.micro: ~$15/month
- ALB: ~$20/month
- NAT Gateway: ~$30/month
- Data transfer: Variable

**Production Environment** (~$200-400/month):
- ECS Fargate (larger): ~$100/month
- RDS Multi-AZ: ~$60/month
- ALB: ~$20/month
- NAT Gateway: ~$60/month (2 AZs)
- Data transfer: Variable

**Cost Optimization Tips**:
1. Use smaller instance types for dev
2. Stop ECS tasks when not in use
3. Use RDS snapshots instead of running instances for dev
4. Consider AWS Free Tier for first 12 months

## Deployment Workflow

### Initial Deployment
```bash
terraform init
terraform plan
terraform apply
# Build and push Docker image
# Update ECS service
```

### Update Application Code
```bash
# Build new image
docker build -t $(terraform output -raw ecr_repository_url):latest .
docker push $(terraform output -raw ecr_repository_url):latest

# Force new deployment
aws ecs update-service --cluster <cluster-name> --service <service-name> --force-new-deployment
```

### Update Infrastructure
```bash
# Modify .tf files
terraform plan
terraform apply
```

### Destroy Infrastructure
```bash
terraform destroy
```

## Environments

### Development
```bash
terraform workspace new dev
terraform workspace select dev
terraform apply -var-file="dev.tfvars"
```

### Production
```bash
terraform workspace new prod
terraform workspace select prod
terraform apply -var-file="prod.tfvars"
```

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /ecs/analytics-lab-dev --follow
```

### ECS Service Status
```bash
aws ecs describe-services \
  --cluster analytics-lab-cluster-dev \
  --services analytics-lab-service-dev
```

### RDS Status
```bash
aws rds describe-db-instances \
  --db-instance-identifier analytics-lab-postgres-dev
```

## Troubleshooting

### ECS Tasks Not Starting
```bash
# Check task logs
aws logs tail /ecs/analytics-lab-dev --follow

# Check task definition
aws ecs describe-task-definition --task-definition analytics-lab-dev

# Check service events
aws ecs describe-services --cluster <cluster> --services <service>
```

### Cannot Access ALB
- Check security groups
- Verify target group health checks
- Check ECS task status

### Database Connection Issues
- Verify security group rules
- Check RDS endpoint in environment variables
- Verify secrets in Secrets Manager

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use Secrets Manager** for sensitive data
3. **Enable encryption** at rest and in transit
4. **Use private subnets** for ECS tasks and RDS
5. **Restrict security groups** to minimum required access
6. **Enable CloudWatch Logs** for audit trail
7. **Use IAM roles** instead of access keys
8. **Enable MFA** for AWS account

## Backup and Recovery

### RDS Automated Backups
- Retention: 7 days (configurable)
- Backup window: 03:00-04:00 UTC

### Manual RDS Snapshot
```bash
aws rds create-db-snapshot \
  --db-instance-identifier analytics-lab-postgres-dev \
  --db-snapshot-identifier analytics-lab-snapshot-$(date +%Y%m%d)
```

### Restore from Snapshot
```bash
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier analytics-lab-postgres-restored \
  --db-snapshot-identifier analytics-lab-snapshot-20250123
```

## Resources

- [Terraform AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)

## Support

For issues or questions:
1. Check CloudWatch Logs
2. Review Terraform plan output
3. Consult AWS documentation
4. Check security group rules
