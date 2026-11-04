
resource "azurerm_container_app" "api" {
  name                         = "ca-azure-production-api-dev"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"
  workload_profile_name        = "Consumption"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.container_app.id]
  }

  registry {
    server   = azurerm_container_registry.main.login_server
    identity = azurerm_user_assigned_identity.container_app.id
  }

  secret {
    name  = "postgres-password"
    value = var.postgres_admin_password
  }

  ingress {
    external_enabled = true
    target_port      = 5000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 0
    max_replicas = 1

    container {
      name   = "flask-api"
      image  = "${azurerm_container_registry.main.login_server}/azure-production-api:1.0"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "APP_ENV"
        value = "development"
      }

      env {
        name  = "PGHOST"
        value = azurerm_postgresql_flexible_server.main.fqdn
      }

      env {
        name  = "PGPORT"
        value = "5432"
      }

      env {
        name  = "PGDATABASE"
        value = azurerm_postgresql_flexible_server_database.app.name
      }

      env {
        name  = "PGUSER"
        value = var.postgres_admin_username
      }

      env {
        name        = "PGPASSWORD"
        secret_name = "postgres-password"
      }

      env {
        name  = "PGSSLMODE"
        value = "verify-full"
      }

      env {
        name  = "PGSSLROOTCERT"
        value = "/etc/ssl/certs/ca-certificates.crt"
      }
    }
  }

  depends_on = [
    azurerm_role_assignment.acr_pull
  ]

  tags = {
    environment = "dev"
    project     = "azure-production-deployment"
    managed_by  = "terraform"
  }
}
