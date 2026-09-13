aws_region           = "us-east-1"
tags                 = {
                        "Owner"        = "Suraj"
                        "environment"  = "dev"
                        "component"    = "scheduler-service"
                       }

databricks_local_base_path             = "notebooks"
databricks_workspace_release_base_path = "/ops/release"
databricks_workspace_develop_base_path = "/ops/develop"
release_version = "1.2.0"
