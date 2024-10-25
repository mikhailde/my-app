output "namespace_name" {
  description = "Namespace for the application"
  value       = kubernetes_namespace.app_ns.metadata[0].name
}

output "deployment_name" {
  description = "Deployment name"
  value       = kubernetes_deployment.app_deployment.metadata[0].name
}

output "service_name" {
  description = "Service name"
  value       = kubernetes_service.app_service.metadata[0].name
}

output "app_image" {
  description = "Full image path"
  value       = local.image
}
