# Terraform configuration for Analytics Engineering Lab
# Provider: Google Cloud Platform (GCP)
# Services: Cloud Run, Cloud SQL, VPC, Load Balancer, Artifact Registry

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Uncomment to use GCS backend for state management
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "analytics-lab/terraform.tfstate"
  # }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region

  default_labels = {
    project     = "analytics-engineering-lab"
    environment = var.environment
    managed_by  = "terraform"
  }
}
