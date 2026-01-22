//==========================================================================
//Definition of the Origin Pool
//==========================================================================
resource "volterra_origin_pool" "f5aiapp_origin_pool" {
  name = "${var.f5xc_namespace}-f5aiapp-pool"
  namespace = var.f5xc_namespace

  origin_servers {
    k8s_service {
      service_name = "${var.f5xc_workload_name}.${var.f5xc_namespace}"

      # site locator / where the service runs (common lab pattern: virtual site)
      site_locator {
        virtual_site {
          #vsite is shared resource in the lab
          name      = var.f5xc_site_name
          namespace = "shared"
        }
      }
      vk8s_networks = true
    }
  }

  no_tls = true
  port = 5000
  loadbalancer_algorithm = "LB_OVERRIDE"
  endpoint_selection = "LOCAL_PREFERRED"
}
