terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state-dev"
    storage_account_name = "sttfstate782011"
    container_name       = "tfstate"
    key                  = "azure-production-dev.tfstate"

    use_azuread_auth = true
    use_cli          = true
  }
}