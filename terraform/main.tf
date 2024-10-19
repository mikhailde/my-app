terraform {
#  backend "http" {
#    address = "https://gitlab.com/api/v4/projects/60883301/terraform/state/default"
#    lock_address = "https://gitlab.com/api/v4/projects/60883301/terraform/state/default/lock"
#    unlock_address = "https://gitlab.com/api/v4/projects/60883301/terraform/state/default/lock"
#    username = "$CI_REGISTRY_USER"
#    password = "$CI_TERRAFORM_PASSWORD"
#    lock_method = "POST"
#    unlock_method = "DELETE"
#    retry_wait_min = 5
#  }
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.33.0"
    }
  }
}

output "ci_job_token" {
  value = "$CI_TERRAFORM_PASSWORD" # or var.ci_job_token if you define it as variable
  sensitive = true # Очень важно пометить как sensitive, чтобы не выводить в обычный output
}

locals {
  image      = "${var.image_registry}:${var.image_tag}"
}

variable "image_registry" {
  description = "Container registry for the image"
  type        = string
}

variable "image_tag" {
  description = "Tag of the Docker image"
  type        = string
  default     = "latest"
}

resource "kubernetes_namespace" "app_ns" {
  metadata {
    name = "my-app"
  }
}

resource "kubernetes_deployment" "app_deployment" {
  metadata {
    name      = "my-app"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "my-app"
      }
    }

    template {
      metadata {
        labels = {
          app = "my-app"
        }
      }

      spec {
        container {
          image = local.image
          name  = "my-app"

          port {
            container_port = 8080
          }

          liveness_probe {
            http_get {
              path = "/"
              port = 8080
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/"
              port = 8080
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app_service" {
  metadata {
    name      = "my-app"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    selector = {
      app = "my-app"
    }

    port {
      protocol    = "TCP"
      port        = 8080
      target_port = 8080
    }

    type = "NodePort"
  }
}
