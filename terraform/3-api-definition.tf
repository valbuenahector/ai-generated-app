resource "volterra_api_definition" "f5aiapp_api_def" {
  count = var.enable_api_discovery ? 1 : 0

  name      = "${var.f5xc_namespace}-f5aiapp-api-def"
  namespace = var.f5xc_namespace

  # Reads the OpenAPI file content into a string; the field supports list(string)
  swagger_specs = [file(var.openapi_spec_path)]

  # Reasonable lab defaults (optional fields in schema)
  strict_schema_origin = true
}
