resource "azurerm_container_registry" "main" {
  name                = "acrproductiondev782011"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  sku           = "Basic"
  admin_enabled = false

  tags = {
    environment = "dev"
    project     = "azure-production-deployment"
    managed_by  = "terraform"
  }
}