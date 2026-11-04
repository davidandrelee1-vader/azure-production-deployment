# Prepared monitoring infrastructure. Creating this workspace incurs Azure charges.
# Not applied or validated against the user's live subscription.
resource "azurerm_log_analytics_workspace" "container_apps" {
  name                = "law-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}
