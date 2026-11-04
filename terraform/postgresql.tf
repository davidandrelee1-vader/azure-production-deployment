resource "azurerm_postgresql_flexible_server" "main" {
  name                         = "psql-${var.project_name}-${var.environment}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "16"
  administrator_login          = var.postgres_admin_username
  administrator_password       = var.postgres_admin_password
  storage_mb                   = 32768
  sku_name                     = "B_Standard_B1ms"
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  delegated_subnet_id           = azurerm_subnet.postgresql.id
  private_dns_zone_id           = azurerm_private_dns_zone.postgresql.id
  public_network_access_enabled = false

  depends_on = [
    azurerm_private_dns_zone_virtual_network_link.postgresql
  ]

  tags = var.tags
}
