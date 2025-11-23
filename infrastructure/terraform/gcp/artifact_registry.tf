# Artifact Registry for Docker Images

resource "google_artifact_registry_repository" "main" {
  location      = var.gcp_region
  repository_id = "${var.project_name}-${var.environment}"
  description   = "Docker repository for analytics engineering lab"
  format        = "DOCKER"

  labels = {
    environment = var.environment
    project     = var.project_name
  }
}
