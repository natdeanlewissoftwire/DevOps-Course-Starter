output "webapp_url" {
  value = "https://${azurerm_linux_web_app.main.default_hostname}"
}
