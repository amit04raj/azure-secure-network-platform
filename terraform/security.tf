resource "azurerm_network_security_group" "app_integration" {
  name                = "nsg-app-integration"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = {
    project     = "azure-secure-network-platform"
    environment = "portfolio"
    managed_by  = "terraform"
  }
}

resource "azurerm_subnet_network_security_group_association" "app_integration" {
  subnet_id                 = azurerm_subnet.app_integration.id
  network_security_group_id = azurerm_network_security_group.app_integration.id
}