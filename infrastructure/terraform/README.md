# Terraform Infrastructure

This directory contains Terraform configurations for deploying the Analytics Engineering Lab to cloud platforms.

## Available Platforms

### AWS
**Location**: `aws/`  
**Services**: ECS Fargate, RDS PostgreSQL, ALB, ECR  
**Best for**: Enterprise deployments, complex networking requirements  
**Cost**: ~$50-100/month (dev), ~$200-400/month (prod)

[📖 AWS Documentation](./aws/README.md)

### GCP
**Location**: `gcp/`  
**Services**: Cloud Run, Cloud SQL, Artifact Registry  
**Best for**: Serverless, cost-effective deployments  
**Cost**: ~$10-30/month (dev), ~$50-150/month (prod)

[📖 GCP Documentation](./gcp/README.md)

## Quick Comparison

| Feature | AWS | GCP |
|---------|-----|-----|
| **Compute** | ECS Fargate (containers) | Cloud Run (serverless) |
| **Database** | RDS PostgreSQL | Cloud SQL PostgreSQL |
| **Networking** | VPC + ALB + NAT Gateway | VPC + VPC Connector |
| **Scaling** | Min 1 task running | Scale to zero ✅ |
| **Pricing Model** | Pay per hour | Pay per 100ms |
| **Setup Complexity** | More complex | Simpler |
| **Dev Cost** | ~$50-100/month | ~$10-30/month |
| **Prod Cost** | ~$200-400/month | ~$50-150/month |

## Which Should You Choose?

### Choose AWS if:
- ✅ You need enterprise-grade features
- ✅ You require complex networking (VPNs, Direct Connect)
- ✅ You're already using AWS services
- ✅ You need more control over infrastructure
- ✅ You require always-on services

### Choose GCP if:
- ✅ You want **lower costs** (especially for dev/staging)
- ✅ You prefer **serverless** (scale to zero)
- ✅ You want **simpler** infrastructure
- ✅ You have **variable traffic** (Cloud Run scales automatically)
- ✅ You want **faster deployments**

**Recommendation for this project**: Start with **GCP** for cost savings and simplicity. You can always migrate to AWS later if needed.

## Getting Started

### 1. Choose Your Platform

```bash
# For AWS
cd infrastructure/terraform/aws

# For GCP
cd infrastructure/terraform/gcp
```

### 2. Follow Platform-Specific Guide

Each platform has its own detailed README:
- [AWS Setup Guide](./aws/README.md)
- [GCP Setup Guide](./gcp/README.md)

## Directory Structure

```
terraform/
├── aws/                          # AWS infrastructure
│   ├── main.tf                  # Provider configuration
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Output values
│   ├── vpc.tf                   # VPC networking
│   ├── ecs.tf                   # ECS Fargate
│   ├── rds.tf                   # RDS PostgreSQL
│   ├── alb.tf                   # Application Load Balancer
│   ├── ecr.tf                   # Elastic Container Registry
│   ├── security_groups.tf       # Security groups
│   ├── secrets.tf               # Secrets Manager
│   ├── terraform.tfvars.example # Example variables
│   └── README.md                # AWS documentation
│
├── gcp/                          # GCP infrastructure
│   ├── main.tf                  # Provider configuration
│   ├── variables.tf             # Input variables
│   ├── outputs.tf               # Output values
│   ├── vpc.tf                   # VPC networking
│   ├── cloud_run.tf             # Cloud Run service
│   ├── cloud_sql.tf             # Cloud SQL PostgreSQL
│   ├── artifact_registry.tf     # Artifact Registry
│   ├── iam.tf                   # IAM & API enablement
│   ├── secrets.tf               # Secret Manager
│   ├── terraform.tfvars.example # Example variables
│   └── README.md                # GCP documentation
│
└── README.md                     # This file
```

## Common Workflow

Regardless of platform, the workflow is similar:

```bash
# 1. Navigate to platform directory
cd aws/  # or gcp/

# 2. Copy and edit variables
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# 3. Set secrets via environment variables
export TF_VAR_db_password="your-secure-password"

# 4. Initialize Terraform
terraform init

# 5. Review plan
terraform plan

# 6. Apply infrastructure
terraform apply

# 7. Build and push Docker image
# (See platform-specific README)

# 8. Deploy application
# (See platform-specific README)
```

## Cost Optimization Tips

### For Both Platforms:
1. **Use smaller instance sizes** for dev/staging
2. **Stop resources** when not in use
3. **Use spot/preemptible instances** for non-critical workloads
4. **Monitor costs** regularly
5. **Set up billing alerts**

### AWS-Specific:
- Use Fargate Spot for dev environments
- Use RDS snapshots instead of running instances
- Consider Aurora Serverless v2 for variable workloads

### GCP-Specific:
- Enable Cloud Run scale-to-zero for dev
- Use Cloud SQL automatic storage increases
- Use committed use discounts for prod

## Multi-Cloud Strategy

You can deploy to both platforms simultaneously:

```bash
# Deploy to AWS
cd aws/
terraform apply

# Deploy to GCP
cd ../gcp/
terraform apply
```

**Use cases**:
- **High availability** across cloud providers
- **Cost comparison** testing
- **Migration** from one platform to another
- **Disaster recovery**

## State Management

### Local State (Default)
Terraform state is stored locally in `terraform.tfstate`.

**⚠️ Warning**: Don't commit `terraform.tfstate` to git!

### Remote State (Recommended for Teams)

**AWS (S3 + DynamoDB)**:
```hcl
# In aws/main.tf, uncomment:
backend "s3" {
  bucket         = "your-terraform-state-bucket"
  key            = "analytics-lab/terraform.tfstate"
  region         = "us-east-1"
  encrypt        = true
  dynamodb_table = "terraform-state-lock"
}
```

**GCP (Cloud Storage)**:
```hcl
# In gcp/main.tf, uncomment:
backend "gcs" {
  bucket = "your-terraform-state-bucket"
  prefix = "analytics-lab/terraform.tfstate"
}
```

## Security Best Practices

1. **Never commit secrets** - Use environment variables or secret managers
2. **Use remote state** with encryption
3. **Enable state locking** to prevent concurrent modifications
4. **Use separate environments** (dev, staging, prod)
5. **Review plans** before applying
6. **Use least-privilege IAM** roles
7. **Enable audit logging**
8. **Rotate credentials** regularly

## Troubleshooting

### Common Issues

**Terraform init fails**:
- Check internet connection
- Verify credentials are configured
- Ensure required APIs are enabled (GCP)

**Apply fails with permission errors**:
- Verify IAM roles/permissions
- Check service account has required access
- Enable required APIs

**State lock errors**:
- Wait for other operations to complete
- Force unlock if necessary (use with caution)

### Getting Help

- Check platform-specific README
- Review Terraform error messages
- Check cloud provider console
- Review logs in CloudWatch (AWS) or Cloud Logging (GCP)

## Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GCP Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
