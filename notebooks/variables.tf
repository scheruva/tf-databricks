variable "aws_region" {
  description = "AWS Region to deploy resources in"
}

variable "tags" {
  description = "Tags to be applied to all resources"
  type        = map(string)
}

variable "databricks_host" {
  description = "The hostname of the Databricks workspace (e.g., adb-12345.12.azuredatabricks.net)"
  type        = string
}

variable "databricks_token" {
  description = "Databricks Personal Access Token (PAT) or Service Principal Token"
  type        = string
  sensitive   = true
}

variable "databricks_local_base_path" {
  description = "Local path where Databricks notebooks are stored"
  type        = string
}

variable "databricks_workspace_release_base_path" {
  description = "Base path in Databricks workspace where notebooks will be stored"
  type        = string
}

variable "databricks_workspace_develop_base_path" {
  description = "Base path in Databricks workspace for development notebooks"
  type        = string
}

variable "release_version" {
  description = "Release version for the deployment"
  type        = string
}