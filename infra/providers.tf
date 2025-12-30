terraform {
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~>3.90" }
    databricks = { source = "databricks/databricks", version="~>1.35.0" }
  }
}
provider "azurerm" { features {} }
provider "databricks" {}
