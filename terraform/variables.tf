variable "image_registry" {
  description = "Container registry for the image"
  type        = string
}

variable "image_tag" {
  description = "Tag of the Docker image"
  type        = string
  default     = "latest"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "my-app"
}

variable "namespace" {
  description = "Namespace for the application"
  type        = string
  default     = "my-app"
}

variable "replicas" {
  description = "Number of replicas for the deployment"
  type        = number
  default     = 1
}

variable "app_port" {
  description = "Main application port"
  type        = number
  default     = 5000
}

variable "metrics_port" {
  description = "Metrics port"
  type        = number
  default     = 8080
}

variable "probe_initial_delay" {
  description = "Initial delay for readiness and liveness probes"
  type        = number
  default     = 5
}

variable "probe_period_seconds" {
  description = "Period seconds for readiness and liveness probes"
  type        = number
  default     = 10
}

variable "canary_interval" {
  description = "Interval for canary analysis"
  type        = string
  default     = "1m"
}

variable "canary_threshold" {
  description = "Threshold for canary analysis"
  type        = number
  default     = 5
}

variable "canary_max_weight" {
  description = "Maximum weight for canary analysis"
  type        = number
  default     = 50
}

variable "canary_step_weight" {
  description = "Step weight for canary analysis"
  type        = number
  default     = 10
}

variable "canary_request_success_rate" {
  description = "Threshold for request success rate in canary analysis"
  type        = number
  default     = 99
}

variable "canary_request_duration" {
  description = "Maximum request duration in milliseconds for canary analysis"
  type        = number
  default     = 500
}

variable "service_monitor_interval" {
  description = "Scrape interval for ServiceMonitor"
  type        = string
  default     = "10s"
}
