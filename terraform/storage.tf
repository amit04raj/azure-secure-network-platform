resource "azurerm_storage_account" "private_service" {
  name                     = "stsecnetworkplatform01"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  public_network_access_enabled   = false
  default_to_oauth_authentication = true
  shared_access_key_enabled       = false
  local_user_enabled              = false
  allow_nested_items_to_be_public = false
  min_tls_version                 = "TLS1_2"

  tags = {
    project     = "azure-secure-network-platform"
    environment = "portfolio"
    managed_by  = "terraform"
  }
}