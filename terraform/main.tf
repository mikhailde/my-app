terraform {
  backend "http" {
    address = "https://gitlab.com/api/v4/projects/60883301/terraform/state/default"
    lock_address = "https://gitlab.com/api/v4/projects/60883301/terraform/state/default/lock"
    unlock_address = "https://gitlab.com/api/v4/projects/60883301/terraform/state/default/lock"
    lock_method = "POST"
    unlock_method = "DELETE"
    retry_wait_min = 5
  }
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.33.0"
    }
  }
}

locals {
  image      = "${var.image_registry}:${var.image_tag}"
}

resource "kubernetes_namespace" "app_ns" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_deployment" "app_deployment" {
  metadata {
    name      = var.app_name
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.app_name
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
          name  = var.app_name

          port {
            container_port = var.app_port
            name           = "http"
          }

          port {
            container_port = var.metrics_port
            name           = "metrics"
          }

          liveness_probe {
            http_get {
              path = "/"
              port = var.app_port
            }
            initial_delay_seconds = var.probe_initial_delay
            period_seconds        = var.probe_period_seconds
          }

          readiness_probe {
            http_get {
              path = "/"
              port = var.app_port
            }
            initial_delay_seconds = var.probe_initial_delay
            period_seconds        = var.probe_period_seconds
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "app_service" {
  metadata {
    name      = var.app_name
    namespace = kubernetes_namespace.app_ns.metadata[0].name
    labels = {
      app = var.app_name
    }
  }

  spec {
    selector = {
      app = var.app_name
    }

    port {
      protocol    = "TCP"
      port        = var.app_port
      target_port = var.app_port
      name        = "http"
    }

    port {
      protocol    = "TCP"
      port        = var.metrics_port
      target_port = var.metrics_port
      name        = "metrics"
    }

    type = "NodePort"
  }
}

resource "kubernetes_manifest" "canary" {
  manifest = {
    "apiVersion" = "flagger.app/v1beta1"
    "kind" = "Canary"
    "metadata" = {
      "name" = var.app_name
      "namespace" = kubernetes_namespace.app_ns.metadata[0].name
    }
    "spec" = {
      "targetRef" = {
        "apiVersion" = "apps/v1"
        "kind" = "Deployment"
        "name" = kubernetes_deployment.app_deployment.metadata[0].name
      }
      "service" = {
        "port" = var.app_port
        "portDiscovery" = true
      }
      "analysis" = {
        "interval" = var.canary_interval
        "threshold" = var.canary_threshold
        "maxWeight" = var.canary_max_weight
        "stepWeight" = var.canary_step_weight
        "metrics" = [
          {
            "name" = "request-success-rate"
            "thresholdRange" = {
              "min" = 99
            }
            "interval" = "30s"
          },
          {
            "name" = "request-duration"
            "thresholdRange" = {
              "max" = var.canary_request_duration
            }
            "interval" = "30s"
          }
        ]
        "webhooks" = []
      }
      "progressDeadlineSeconds" = 600
    }
  }
}

resource "kubernetes_manifest" "service_monitor" {
  manifest = {
    "apiVersion" = "monitoring.coreos.com/v1"
    "kind" = "ServiceMonitor"
    "metadata" = {
      "name" = var.app_name
      "namespace" = kubernetes_namespace.app_ns.metadata[0].name
      "labels" = {
        "app.kubernetes.io/name" = "my-app"
      }
    }
    "spec" = {
      "selector" = {
        "matchLabels" = {
          "app" = "my-app"
        }
      }
      "endpoints" = [
        {
          "port" = "metrics"
          "interval" = var.service_monitor_interval
        }
      ]
    }
  }
}
