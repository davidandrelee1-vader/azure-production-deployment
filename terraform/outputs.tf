output "resource_group_name" {
  description = "Name of the Azure Resource Group"
  value       = azurerm_resource_group.main.name

}

output "resource_group_location" {
  description = "Location of the Azure Resource Group"
  value       = azurerm_resource_group.main.location

}

output "vnet_id" {
  description = "Vnet id"
  value       = azurerm_virtual_network.main.id
}

output "app_subnet_id" {
  description = "app-subnet id"
  value       = azurerm_subnet.container-apps.id
}

output "db_subnet_id" {
  description = "db-subnet id"
  value       = azurerm_subnet.postgresql.id
}