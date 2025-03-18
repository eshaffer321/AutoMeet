variable "b2_application_key" {
  type        = string
  description = "The name of the application"
  default = "automeet"
}

resource "b2_application_key" "automeet" {
  key_name     = var.b2_application_key
  capabilities = ["readFiles"]
}

data "b2_application_key" "automeet" {
  key_name = b2_application_key.automeet.key_name
}

output "application_key" {
  value = data.b2_application_key.automeet.key_name
}
