provider "kubernetes" {
  host                   = "https://${minikube_ip}:8443"
  client_certificate     = file("${local.kubeconfig}/client.crt")
  client_key             = file("${local.kubeconfig}/client.key")
  cluster_ca_certificate = file("${local.kubeconfig}/ca.crt")
}

data "external" "minikube_ip" {
  program = ["sh", "-c", "minikube ip"]
}

locals {
  kubeconfig = "~/.kube/config"
  image      = "${var.image_registry}:${var.image_tag}"
  minikube_ip = data.external.minikube_ip.result["stdout"]
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
          name  = "my-app-container"

          ports {
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
    name      = "my-app-service"
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
