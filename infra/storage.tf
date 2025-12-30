resource "azurerm_storage_account" "datalake" {
  name                     = "paystreamstore1234"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  hierarchical_namespace   = true
}
