variable "f5xc_api_p12_file" {
    type = string
}

variable "f5xc_api_url" {
    type = string
}
variable "f5xc_tenant"      { 
    type = string
}
variable "f5xc_namespace" {
  type = string
}

variable "f5xc_workload_name" {
  type = string
}

# Depending on your XC model you might need a "site locator" / virtual site name.
variable "f5xc_site_name" {
  type = string
}

variable "app_domain" {
  type = string
  description = "Application domain"
}

variable "enable_waf" {
  type    = bool
  default = true
}

variable "enable_api_discovery" {
  type    = bool
  default = false
}

variable "enable_bot_advanced" {
  type    = bool
  default = false
}

variable "enable_rate_limiting" {
  type    = bool
  default = false
}

