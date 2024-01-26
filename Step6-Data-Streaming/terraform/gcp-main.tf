terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}


# VM instance Kafka
resource "google_compute_instance" "vm_instance" {
  name          = "mta-kafka-instance"
  project       = var.project
  machine_type  = "e2-standard-4"
  zone          = var.region

  boot_disk {
    initialize_params {
      image = var.vm_image
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
}

# VM instance Spark
resource "google_compute_instance" "vm_instance" {
  name          = "mta-spark-instance"
  project       = var.project
  machine_type  = "e2-standard-4"
  zone          = var.region

  boot_disk {
    initialize_params {
      image = var.vm_image
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
}

# VM instance data-stream
resource "google_compute_instance" "vm_instance" {
  name          = "mta-data-stream-instance"
  project       = var.project
  machine_type  = "e2-standard-4"
  zone          = var.region

  boot_disk {
    initialize_params {
      image = var.vm_image
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }
}