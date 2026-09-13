# define databricks_notebook resource using loop for each notebook in the directory
resource "databricks_notebook" "notebook" {
  for_each = setunion(
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.py"),
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.scala"),
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.sql"),
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.ipynb"),
  )
  path   = "${var.databricks_workspace_release_base_path}/${var.release_version}/${each.value}"
  source = "${path.cwd}/../${var.databricks_local_base_path}/${each.value}"
}

output "debug_notebook_files" {
  value = setunion(
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.py"),
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.scala"),
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.sql"),
    fileset("${path.cwd}/../${var.databricks_local_base_path}", "**/*.ipynb"),
  )
}