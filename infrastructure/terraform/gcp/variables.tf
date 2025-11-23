# Variables for Analytics Engineering Lab Infrastructure (GCP)

variable "gcp_project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP region to deploy resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "analytics-lab"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Cloud Run Configuration
variable "cloud_run_cpu" {
  description = "CPU allocation for Cloud Run service"
  type        = string
  default     = "2"
}

variable "cloud_run_memory" {
  description = "Memory allocation for Cloud Run service"
  type        = string
  default     = "4Gi"
}

variable "cloud_run_min_instances" {
  description = "Minimum number of Cloud Run instances"
  type        = number
  default     = 0  # Scale to zero when not in use
}

variable "cloud_run_max_instances" {
  description = "Maximum number of Cloud Run instances"
  type        = number
  default     = 2
}

# Cloud SQL Configuration
variable "db_tier" {
  description = "Cloud SQL instance tier"
  type        = string
  default     = "db-f1-micro"  # Smallest tier
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "analytics_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "analytics_admin"
  sensitive   = true
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  # Set via environment variable: TF_VAR_db_password
}

# Application Configuration
variable "container_port_streamlit" {
  description = "Port for Streamlit app"
  type        = number
  default     = 8501
}

variable "container_port_jupyter" {
  description = "Port for Jupyter Lab"
  type        = number
  default     = 8888
}

variable "container_port_metabase" {
  description = "Port for Metabase"
  type        = number
  default     = 3000
}

# Docker Image
variable "docker_image_tag" {
  description = "Docker image tag to deploy"
  type        = string
  default     = "latest"
}

# Tags
variable "additional_labels" {
  description = "Additional labels for resources"
  type        = map(string)
  default     = {}
}
