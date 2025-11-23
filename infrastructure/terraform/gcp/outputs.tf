# Terraform Outputs

# VPC
output "vpc_id" {
  description = "VPC ID"
  value       = google_compute_network.main.id
}

output "vpc_name" {
  description = "VPC name"
  value       = google_compute_network.main.name
}

output "subnet_id" {
  description = "Subnet ID"
  value       = google_compute_subnetwork.main.id
}

# Cloud Run
output "cloud_run_url" {
  description = "Cloud Run service URL"
  value       = google_cloud_run_service.analytics_lab.status[0].url
}

output "cloud_run_service_name" {
  description = "Cloud Run service name"
  value       = google_cloud_run_service.analytics_lab.name
}

# Cloud SQL
output "cloud_sql_connection_name" {
  description = "Cloud SQL connection name"
  value       = google_sql_database_instance.postgres.connection_name
}

output "cloud_sql_private_ip" {
  description = "Cloud SQL private IP address"
  value       = google_sql_database_instance.postgres.private_ip_address
}

output "database_name" {
  description = "Database name"
  value       = google_sql_database.main.name
}

# Artifact Registry
output "artifact_registry_url" {
  description = "Artifact Registry repository URL"
  value       = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.main.repository_id}"
}

# Deployment Instructions
output "deployment_instructions" {
  description = "Instructions for deploying the application"
  value = <<-EOT
    
    🚀 GCP Deployment Instructions:
    
    1. Build and push Docker image:
       gcloud auth configure-docker ${var.gcp_region}-docker.pkg.dev
       docker build -t ${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.main.repository_id}/analytics-lab:latest ../../
       docker push ${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.main.repository_id}/analytics-lab:latest
    
    2. Deploy new revision:
       gcloud run services update ${google_cloud_run_service.analytics_lab.name} \
         --region ${var.gcp_region} \
         --image ${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.main.repository_id}/analytics-lab:latest
    
    3. Access your application:
       ${google_cloud_run_service.analytics_lab.status[0].url}
    
    4. Database connection:
       Connection Name: ${google_sql_database_instance.postgres.connection_name}
       Database: ${google_sql_database.main.name}
       User: ${var.db_username}
  EOT
}
