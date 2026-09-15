resource "azurerm_private_endpoint" "app" {
  name                = "pe-app-service"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  subnet_id           = azurerm_subnet.private_services.id

  private_service_connection {
    name                           = "psc-app-service"
    private_connection_resource_id = azurerm_linux_web_app.app.id
    is_manual_connection           = false
    subresource_names              = ["sites"]
  }

  private_dns_zone_group {
    name                 = "app-service-dns"
    private_dns_zone_ids = [azurerm_private_dns_zone.app.id]
  }

  tags = {
    project     = "azure-secure-network-platform"
    environment = "portfolio"
    managed_by  = "terraform"
  }
}

resource "azurerm_private_dns_zone" "app" {
  name                = "privatelink.azurewebsites.net"
  resource_group_name = azurerm_resource_group.main.name

  tags = {
    project     = "azure-secure-network-platform"
    environment = "portfolio"
    managed_by  = "terraform"
  }
}

resource "azurerm_private_dns_zone_virtual_network_link" "app" {
  name                  = "link-app-service"
  private_dns_zone_name = azurerm_private_dns_zone.app.name
  resource_group_name   = azurerm_resource_group.main.name
  virtual_network_id    = azurerm_virtual_network.main.id

  tags = {
    project     = "azure-secure-network-platform"
    environment = "portfolio"
    managed_by  = "terraform"
  }
}