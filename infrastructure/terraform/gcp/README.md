# Terraform Infrastructure for GCP

Complete Terraform setup for deploying the Analytics Engineering Lab to Google Cloud Platform.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Internet                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────▼────┐
                    │Cloud Run│ (Serverless Containers)
                    │  Public │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │   VPC   │
                    │Connector│
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │Cloud SQL│ (PostgreSQL)
                    │ Private │
                    └─────────┘
```

## Resources Created

- **VPC** with private subnet
- **Cloud Run** service for running containers (serverless)
- **Cloud SQL PostgreSQL** database with private IP
- **VPC Access Connector** for Cloud Run to Cloud SQL communication
- **Artifact Registry** for Docker images
- **Secret Manager** for sensitive data
- **IAM** service accounts and permissions

## GCP vs AWS Comparison

| Feature | AWS | GCP |
|---------|-----|-----|
| **Compute** | ECS Fargate | Cloud Run |
| **Database** | RDS | Cloud SQL |
| **Images** | ECR | Artifact Registry |
| **Secrets** | Secrets Manager | Secret Manager |
| **Networking** | VPC + NAT Gateway | VPC + VPC Connector |
| **Pricing** | Pay per hour | Pay per 100ms (cheaper!) |
| **Scaling** | Min 1 task | Scale to zero ✅ |

**GCP Advantages**:
- ✅ **Cheaper** - Cloud Run scales to zero, pay only when used
- ✅ **Simpler** - Less networking complexity
- ✅ **Faster deploys** - Cloud Run deploys in seconds

## Prerequisites

1. **GCP Account** with billing enabled
2. **GCP Project** created
3. **gcloud CLI** installed and configured
4. **Terraform** >= 1.0 installed
5. **Docker** installed

## Quick Start

### 1. Install gcloud CLI

```bash
# macOS
brew install google-cloud-sdk

# Initialize
gcloud init
gcloud auth application-default login
```

### 2. Create GCP Project

```bash
# Create project
gcloud projects create your-project-id --name="Analytics Lab"

# Set project
gcloud config set project your-project-id

# Enable billing (required)
# Go to: https://console.cloud.google.com/billing
```

### 3. Set Variables

```bash
# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars
# Set gcp_project_id to your project ID

# Set database password
export TF_VAR_db_password="your-secure-password-here"
```

### 4. Initialize Terraform

```bash
cd infrastructure/terraform/gcp
terraform init
```

### 5. Plan Deployment

```bash
terraform plan
```

### 6. Deploy Infrastructure

```bash
terraform apply
```

Type `yes` when prompted. This takes ~5-10 minutes.

### 7. Build and Push Docker Image

```bash
# Configure Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev

# Get repository URL
REPO_URL=$(terraform output -raw artifact_registry_url)

# Build image
docker build -t ${REPO_URL}/analytics-lab:latest ../../../

# Push image
docker push ${REPO_URL}/analytics-lab:latest
```

### 8. Deploy to Cloud Run

```bash
# Cloud Run will automatically deploy the latest image
# Or force a new deployment:
gcloud run services update $(terraform output -raw cloud_run_service_name) \
  --region us-central1 \
  --image ${REPO_URL}/analytics-lab:latest
```

### 9. Access Your Application

```bash
# Get URL
terraform output cloud_run_url

# Open in browser
open $(terraform output -raw cloud_run_url)
```

## Configuration

### terraform.tfvars

Key variables to customize:

```hcl
gcp_project_id = "your-project-id"
gcp_region     = "us-central1"
environment    = "dev"

# Cloud Run sizing
cloud_run_cpu          = "2"
cloud_run_memory       = "4Gi"
cloud_run_min_instances = 0  # Scale to zero!

# Cloud SQL sizing
db_tier = "db-f1-micro"  # Smallest tier
```

## Cost Estimation

**Development Environment** (~$10-30/month):
- Cloud Run: ~$0-5/month (scales to zero!)
- Cloud SQL db-f1-micro: ~$7/month
- VPC Connector: ~$8/month
- Artifact Registry: ~$0.10/month
- Networking: Variable

**Production Environment** (~$50-150/month):
- Cloud Run (always-on): ~$30/month
- Cloud SQL (larger + HA): ~$50/month
- VPC Connector: ~$8/month
- Load Balancer (optional): ~$20/month

**GCP is ~50% cheaper than AWS** for this workload! 💰

## Deployment Workflow

### Initial Deployment
```bash
terraform init
terraform plan
terraform apply
# Build and push Docker image
```

### Update Application Code
```bash
# Build new image
docker build -t ${REPO_URL}/analytics-lab:latest .
docker push ${REPO_URL}/analytics-lab:latest

# Cloud Run auto-deploys on new image push
# Or force deployment:
gcloud run deploy $(terraform output -raw cloud_run_service_name) \
  --image ${REPO_URL}/analytics-lab:latest \
  --region us-central1
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

## Monitoring

### Cloud Run Logs
```bash
gcloud run services logs read $(terraform output -raw cloud_run_service_name) \
  --region us-central1 \
  --limit 50
```

### Cloud SQL Status
```bash
gcloud sql instances describe $(terraform output -raw cloud_sql_connection_name | cut -d':' -f3)
```

### View in Console
```bash
# Cloud Run
open "https://console.cloud.google.com/run"

# Cloud SQL
open "https://console.cloud.google.com/sql"

# Logs
open "https://console.cloud.google.com/logs"
```

## Troubleshooting

### Cloud Run Service Won't Start
```bash
# Check logs
gcloud run services logs read SERVICE_NAME --region us-central1

# Check service status
gcloud run services describe SERVICE_NAME --region us-central1
```

### Database Connection Issues
- Verify VPC Connector is attached to Cloud Run
- Check Cloud SQL private IP configuration
- Verify service account has `cloudsql.client` role

### Permission Errors
```bash
# Ensure APIs are enabled
gcloud services enable run.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable vpcaccess.googleapis.com
```

## Security Best Practices

1. **Never commit secrets** to version control
2. **Use Secret Manager** for all sensitive data
3. **Enable Cloud SQL SSL** (already configured)
4. **Use private IP** for Cloud SQL (already configured)
5. **Restrict Cloud Run access** in production (set `allUsers` to specific accounts)
6. **Enable Cloud Armor** for DDoS protection (optional)
7. **Use Workload Identity** for service accounts

## Backup and Recovery

### Cloud SQL Automated Backups
- Enabled by default
- Point-in-time recovery available (prod only)
- Backup window: 03:00 UTC

### Manual Backup
```bash
gcloud sql backups create \
  --instance=$(terraform output -raw cloud_sql_connection_name | cut -d':' -f3)
```

### Restore from Backup
```bash
gcloud sql backups restore BACKUP_ID \
  --backup-instance=SOURCE_INSTANCE \
  --backup-id=BACKUP_ID
```

## Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)
