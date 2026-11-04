variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  sensitive   = true

}

variable "location" {
  description = "Azure region for deployment"
  type        = string
  default     = "eastus2"

}

variable "project_name" {
  description = "Name of project"
  type        = string
  default     = "azure-production"


}

variable "environment" {
  description = "Deployment enviornment"
  type        = string
  default     = "dev"

}

variable "tags" {
  description = "Common tags for Azure resources"
  type        = map(string)

  default = {
    Project      = "Azure-Production-Deployment"
    Enviornement = "Development"
    ManagedBy    = "Terraform"

  }

}

variable "vnet_cidr" {
  description = "Cidr of the Vnet"
  type        = string
  default     = "10.20.0.0/16"


}

variable "app_subnet_cidr" {
  description = "Cidr of the app_subnet"
  type        = string
  default     = "10.20.1.0/27"


}

variable "db_subnet_cidr" {
  description = "Cidr of the db_subnet"
  type        = string
  default     = "10.20.2.0/27"


}
variable "postgres_admin_username" {
  description = "PostgreSQL administrator username"
  type        = string
  default     = "pgadminuser"
}


variable "postgres_admin_password" {
  description = "PostgreSQL administrator password"
  type        = string
  sensitive   = true
  nullable    = false
}

