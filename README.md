# tf-databricks
# Description
This is a databricks terraform deployment framework for working with gitlab & terraform to get databricks development & deployment done seamlessly.

# How to develop
- There is a databricks workspace dir called '/ops/develop/{develop_version}/'.
- All code changes should be made there so you can unit test the notebooks

# How to sync with gitlab
- Using CI/CD, run the Stage named sync-develop. This copies (exports) all the notebooks from databricks into the repo & commits
- This can be run multiple times during a development life-cycle without doing a release

# How to release
- Run sync-develop (unless you already did)
- Run the deploy-databricks stage 
  - this takes the notebooks from the repo & deploys them to databricks using the version in the terraform.tfvars file
    - the older release version contents are wiped out, but the directory structures remain
  - once this is complete, it will auto run the increment-develop stage, which increments the development (minor) version & pushes (imports) all notebooks into databricks as the new develop version
  - the older develop versions are not wiped out