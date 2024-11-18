variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "OAUTH_CLIENT_ID" {
  type      = string
  sensitive = true
}

variable "OAUTH_CLIENT_SECRET" {
  type      = string
  sensitive = true
}
