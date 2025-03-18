variable "b2_application_key" {
  type        = string
  description = "The name of the application"
  default = "automeet"
}

variable "bucket_name" {
  type = string
  description = "Name of the b2 bucket to hold the audio data"
  default = "automeet-bucket"
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

resource "b2_bucket" "example" {
  bucket_name = var.bucket_name
  bucket_type = "allPrivate"

  bucket_info = {
    "project" = "automeet"
  }

  default_server_side_encryption {
    algorithm = "AES256"
    mode      = "SSE-B2"
  }

}