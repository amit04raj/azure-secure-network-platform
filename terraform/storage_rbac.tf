resource "azurerm_role_assignment" "app_storage_blob_contributor" {
  scope                = azurerm_storage_account.private_service.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_web_app.app.identity[0].principal_id
}