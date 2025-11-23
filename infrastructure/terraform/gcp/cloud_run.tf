# Cloud Run Service

# Service Account for Cloud Run
resource "google_service_account" "cloud_run" {
  account_id   = "${var.project_name}-cloud-run-${var.environment}"
  display_name = "Cloud Run Service Account for ${var.project_name}"
}

# Grant Cloud SQL Client role to service account
resource "google_project_iam_member" "cloud_sql_client" {
  project = var.gcp_project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# Grant Secret Manager Secret Accessor role
resource "google_project_iam_member" "secret_accessor" {
  project = var.gcp_project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# Cloud Run Service
resource "google_cloud_run_service" "analytics_lab" {
  name     = "${var.project_name}-${var.environment}"
  location = var.gcp_region

  template {
    spec {
      service_account_name = google_service_account.cloud_run.email

      containers {
        image = "${var.gcp_region}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.main.repository_id}/analytics-lab:${var.docker_image_tag}"

        resources {
          limits = {
            cpu    = var.cloud_run_cpu
            memory = var.cloud_run_memory
          }
        }

        ports {
          container_port = var.container_port_streamlit
        }

        env {
          name  = "ENVIRONMENT"
          value = var.environment
        }

        env {
          name  = "DB_HOST"
          value = "/cloudsql/${google_sql_database_instance.postgres.connection_name}"
        }

        env {
          name  = "DB_PORT"
          value = "5432"
        }

        env {
          name  = "DB_NAME"
          value = var.db_name
        }

        env {
          name  = "DB_USER"
          value = var.db_username
        }

        env {
          name = "DB_PASSWORD"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.db_password.secret_id
              key  = "latest"
            }
          }
        }
      }

      # Cloud SQL connection
      containers {
        image = "gcr.io/cloudsql-docker/gce-proxy:latest"
        args  = ["-instances=${google_sql_database_instance.postgres.connection_name}=tcp:5432"]
      }
    }

    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"         = var.cloud_run_min_instances
        "autoscaling.knative.dev/maxScale"         = var.cloud_run_max_instances
        "run.googleapis.com/cloudsql-instances"    = google_sql_database_instance.postgres.connection_name
        "run.googleapis.com/vpc-access-connector"  = google_vpc_access_connector.main.id
        "run.googleapis.com/vpc-access-egress"     = "private-ranges-only"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_iam_member.cloud_sql_client,
    google_project_iam_member.secret_accessor
  ]
}

# Allow unauthenticated access (for dev - restrict in prod)
resource "google_cloud_run_service_iam_member" "public_access" {
  count = var.environment == "dev" ? 1 : 0

  service  = google_cloud_run_service.analytics_lab.name
  location = google_cloud_run_service.analytics_lab.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
