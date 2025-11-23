# Secret Manager for sensitive data

# Enable Secret Manager API
resource "google_project_service" "secretmanager" {
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

# Database Password Secret
resource "google_secret_manager_secret" "db_password" {
  secret_id = "${var.project_name}-db-password-${var.environment}"

  replication {
    automatic = true
  }

  depends_on = [google_project_service.secretmanager]
}

# Database Password Secret Version
resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = var.db_password
}
