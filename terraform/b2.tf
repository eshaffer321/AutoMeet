variable "b2_application_key" {
  type        = string
  description = "The name of the application"
  default     = "automeet"
}

variable "bucket_name" {
  type        = string
  description = "Name of the b2 bucket to hold the audio data"
  default     = "automeet-bucket"
}

resource "b2_bucket" "automeet_bucket" {
  bucket_name = var.bucket_name
  bucket_type = "allPrivate"

  bucket_info = {
    "project" = "automeet"
  }

  default_server_side_encryption {
    algorithm = "AES256"
    mode      = "SSE-B2"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "b2_application_key" "automeet_key" {
  key_name  = var.b2_application_key
  bucket_id = b2_bucket.automeet_bucket.id
  capabilities = [
    "listBuckets",
    "listFiles",
    "readFiles",
    "writeFiles",
    "deleteFiles"
  ]

  lifecycle {
    prevent_destroy = true
  }
}

output "application_key" {
  value = b2_application_key.automeet_key.key_name
}

