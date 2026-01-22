//==========================================================================
//Definition of the HTTP Load Balancer
//==========================================================================
resource "volterra_http_loadbalancer" "f5aiapp-lb" {
  depends_on = [
    volterra_origin_pool.f5aiapp_origin_pool,
    volterra_app_firewall.waap-tf
  ]

  name      = "${var.f5xc_namespace}-f5aiapp-lb"
  namespace = var.f5xc_namespace
  domains   = ["${var.f5xc_namespace}-lb.${var.app_domain}"]
  // HTTPS configuration with automatic certificate management
  https_auto_cert {
    add_hsts              = true
    http_redirect         = true
    no_mtls               = true
    enable_path_normalize = true
    tls_config {
      default_security = true
    }
  }

  default_route_pools {
    pool {
      name      = volterra_origin_pool.f5aiapp_origin_pool.name
      namespace = var.f5xc_namespace
    }
    weight = 1
  }

  advertise_on_public_default_vip = true

  no_service_policies = true
  no_challenge        = true
  disable_rate_limit  = true

  app_firewall {
    name      = volterra_app_firewall.waap-tf.name
    namespace = var.f5xc_namespace
  }

  user_id_client_ip = true
  source_ip_stickiness = true

  # ---------------------------
  # Module 3 Task 2 (Bot Defense) — only when enabled
  # ---------------------------
  dynamic "bot_defense" {
    for_each = var.enable_bot_advanced ? [1] : []
    content {
      policy {
        javascript_mode = "ASYNC_JS_NO_CACHING"

        js_insert_all_pages {
          javascript_location = "AFTER_HEAD"
        }

        protected_app_endpoints {
          http_methods = ["METHOD_POST"]

          flow_label {
            authentication {
              login_mfa = true
            }
          }

          metadata {
            name = "login-endpoint"
          }

          mitigation {
            block {
              status = "PaymentRequired"
            }
          }

          path {
            path = "/login"
          }
        }
      }
      regional_endpoint = "US"
    }
  }

  # ---------------------------
  # Module 3 Task (API Discovery) — only when enabled
  # - api_specification supports referencing an API definition object
  # - discovery controls exist under single_lb_app.enable_discovery (marked deprecated in schema, but still modeled)
  # ---------------------------
  dynamic "api_specification" {
    for_each = var.enable_api_discovery ? [1] : []
    content {
      validation_disabled = false

      api_definition {
        name      = volterra_api_definition.f5aiapp_api_def[0].name
        namespace = var.f5xc_namespace
      }
    }
  }

  dynamic "single_lb_app" {
    for_each = var.enable_api_discovery ? [1] : []
    content {
      enable_discovery {}
    }
  }
}
