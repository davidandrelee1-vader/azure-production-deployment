resource "azurerm_container_app_environment" "main" {
  name                       = "cae-azure-production-dev"
  location                   = azurerm_resource_group.main.location
  resource_group_name        = azurerm_resource_group.main.name
  infrastructure_subnet_id   = azurerm_subnet.container-apps.id
  logs_destination           = "log-analytics"
  log_analytics_workspace_id = azurerm_log_analytics_workspace.container_apps.id

  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
    minimum_count         = 0
    maximum_count         = 0
  }

  tags = {
    environment = "dev"
    project     = "azure-production-deployment"
    managed_by  = "terraform"
  }
}
