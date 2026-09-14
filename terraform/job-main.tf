resource "databricks_job" "main_job" {
  name = "Main"
  description = "Main job for the release ${var.release_version}"
  
  task {
    task_key = "main"
      notebook_task {
      notebook_path = "${var.databricks_workspace_release_base_path}/${var.release_version}/core/main.py"
      source = "WORKSPACE"
    }
  }

  tags = var.tags

  environment {
    environment_key = "Default"
    spec {
      environment_version = "5"
    }
  }

  performance_target = "PERFORMANCE_OPTIMIZED"
}

output "job_id" {
  description = "The ID of the main Databricks job"
  value       = databricks_job.main_job.id
}

output "job_url" {
  description = "The web URL to manage or view the main Databricks job"
  value       = databricks_job.main_job.url
}
