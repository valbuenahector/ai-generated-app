"""
F5 Distributed Cloud (F5XC) Workload Manager

This script provides a management interface for F5XC Workloads via the Volterra API.
It supports creating, replacing, getting, deleting, and upserting workloads on Customer Edge (CE) Virtual Sites.

Usage:
    python workload_manager.py [operation]

Operations:
    create  - Create a new workload
    replace - Replace an existing workload configuration
    get     - Retrieve workload details
    delete  - Delete a workload
    upsert  - Create if not exists, otherwise replace

Required Environment Variables (GitLab CI/CD):
    F5XC_API_URL            - The API endpoint URL (e.g., https://tenant.console.ves.volterra.io/api)
    TF_VAR_f5xc_api_p12_file - Path to your F5XC API P12 certificate file
    VES_P12_PASSWORD        - Password for the P12 certificate
    F5XC_TENANT        - Your F5XC Tenant name
    F5XC_NAMESPACE     - The F5XC Namespace to operate in
    F5XC_SITE_NAME     - The name of the Customer Edge Virtual Site
    F5XC_WORKLOAD_NAME - The name of the workload
    IMAGE_REF          - The container image reference (registry/image:tag)

Optional Environment Variables:
    F5XC_SITE_NAMESPACE     - Namespace for the virtual site (default: "shared")
    F5XC_REGISTRY_NAME      - Name of the container registry object (default: <namespace>-acr)
    F5XC_WORKLOAD_PORT      - The port the workload listens on (default: 5000)

Example:
    export F5XC_API_URL="https://my-tenant.console.ves.volterra.io/api"
    export TF_VAR_f5xc_api_p12_file="path-to-cert.p12"
    export VES_P12_PASSWORD="passowrd"
    export F5XC_TENANT="my-tenant"
    export F5XC_NAMESPACE="my-ns"
    export F5XC_SITE_NAME="my-ce-vsite"
    export F5XC_WORKLOAD_NAME="my-app"
    export IMAGE_REF="my-registry.azurecr.io/my-app:v1"
    export APP_DOMAIN="lab-app.f5demos.com"
    export F5XC_REGISTRY_NAME="appworld2026-az-cr"
    export F5XC_WORKLOAD_PORT=5000

    python workload_manager.py upsert
"""

import os
import requests
import json
import argparse
import sys
from requests_pkcs12 import Pkcs12Adapter

class VolterraWorkloadManager:
    def __init__(self, api_url, tenant, namespace, p12_file, p12_password):
        self.api_url = api_url.rstrip('/') if api_url else None
        self.tenant = tenant
        self.namespace = namespace
        self.p12_file = p12_file
        self.p12_password = p12_password

    def _get_session(self):
        session = requests.Session()
        
        if self.p12_file and os.path.exists(self.p12_file):
            # Mount Pkcs12Adapter to handle the P12 certificate directly
            adapter = Pkcs12Adapter(
                pkcs12_filename=self.p12_file,
                pkcs12_password=self.p12_password
            )
            session.mount(self.api_url, adapter)
        else:
            print(f"Error: Certificate file not found at {self.p12_file}")
            sys.exit(1)

        session.headers.update({
            "Content-Type": "application/json"
        })
        return session

    def _get_payload(self, name, image, site_name, port, container_registry_name, site_namespace):
        return {
            "metadata": {
                "name": name,
                "namespace": self.namespace,
                "labels": {},
                "annotations": {},
                "disable": False
            },
            "spec": {
                "service": {
                    "num_replicas": 1,
                    "containers": [
                        {
                            "name": name,
                            "image": {
                                "name": image,
                                "container_registry": {
                                    "namespace": self.namespace,
                                    "name": container_registry_name,
                                    "kind": "container_registry"
                                },
                                "pull_policy": "IMAGE_PULL_POLICY_DEFAULT"
                            },
                            "init_container": False,
                            "flavor": "CONTAINER_FLAVOR_TYPE_TINY",
                            "command": [],
                            "args": []
                        }
                    ],
                    "volumes": [],
                    "deploy_options": {
                        "deploy_ce_virtual_sites": {
                            "virtual_site": [
                                {
                                    "namespace": site_namespace,
                                    "name": site_name,
                                    "kind": "virtual_site"
                                }
                            ]
                        }
                    },
                    "advertise_options": {
                        "advertise_in_cluster": {
                            "port": {
                                "info": {
                                    "port": port,
                                    "protocol": "PROTOCOL_TCP",
                                    "same_as_port": {}
                                }
                            }
                        }
                    },
                    "family": {
                        "v4": {}
                    }
                }
            }
        }

    def _parse_response(self, response):
        """Helper to safely parse JSON response and provide debugging on failure."""
        if not response.text:
            return {"status": "empty_response", "code": response.status_code}
        try:
            return response.json()
        except json.JSONDecodeError:
            print(f"Error: Received non-JSON response (HTTP {response.status_code})")
            # If it looks like HTML, print a snippet to help debug proxy/auth issues
            if response.text.strip().startswith('<'):
                print(f"Response snippet: {response.text[:200]}...")
            else:
                print(f"Raw response: {response.text[:500]}...")
            raise

    def create_workload(self, name, image, site_name, port, container_registry_name, site_namespace):
        url = f"{self.api_url}/config/namespaces/{self.namespace}/workloads"
        payload = self._get_payload(name, image, site_name, port, container_registry_name, site_namespace)
        
        session = self._get_session()
        response = session.post(url, json=payload)
        response.raise_for_status()
        return self._parse_response(response)

    def replace_workload(self, name, image, site_name, port, container_registry_name, site_namespace):
        url = f"{self.api_url}/config/namespaces/{self.namespace}/workloads/{name}"
        payload = self._get_payload(name, image, site_name, port, container_registry_name, site_namespace)
        
        session = self._get_session()
        response = session.put(url, json=payload)
        response.raise_for_status()
        return self._parse_response(response)

    def get_workload(self, name):
        url = f"{self.api_url}/config/namespaces/{self.namespace}/workloads/{name}"
        session = self._get_session()
        response = session.get(url)
        response.raise_for_status()
        return self._parse_response(response)

    def delete_workload(self, name):
        url = f"{self.api_url}/config/namespaces/{self.namespace}/workloads/{name}"
        session = self._get_session()
        payload = {
            "name": name,
            "namespace": self.namespace
        }
        response = session.delete(url, json=payload)
        response.raise_for_status()
        return self._parse_response(response)

    def upsert_workload(self, name, image, site_name, port, container_registry_name, site_namespace):
        try:
            self.get_workload(name)
            action = "replaced"
            result = self.replace_workload(name, image, site_name, port, container_registry_name, site_namespace)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                action = "created"
                result = self.create_workload(name, image, site_name, port, container_registry_name, site_namespace)
            else:
                raise
        return result, action

def main():
    parser = argparse.ArgumentParser(description='F5XC Workload Manager')
    parser.add_argument('operation', choices=['create', 'replace', 'delete', 'get', 'upsert'], help='Operation to perform')
    
    # Required Environment variables
    required_vars = [
        'F5XC_API_URL', 'F5XC_TENANT', 
        'F5XC_NAMESPACE', 'F5XC_SITE_NAME', 'F5XC_WORKLOAD_NAME', 'IMAGE_REF',
        'F5XC_REGISTRY_NAME', 'F5XC_WORKLOAD_PORT',
        'TF_VAR_f5xc_api_p12_file', 'VES_P12_PASSWORD'
    ]
    
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    api_url = os.getenv('F5XC_API_URL')
    tenant = os.getenv('F5XC_TENANT')
    namespace = os.getenv('F5XC_NAMESPACE')
    site_name = os.getenv('F5XC_SITE_NAME')
    workload_name = os.getenv('F5XC_WORKLOAD_NAME')
    image_name = os.getenv('IMAGE_REF')
    container_registry_name = os.getenv('F5XC_REGISTRY_NAME')
    port = int(os.getenv('F5XC_WORKLOAD_PORT'))
    
    # Optional Environment variables with defaults
    site_namespace = os.getenv('F5XC_SITE_NAMESPACE', 'shared')


    p12_file = os.getenv('TF_VAR_f5xc_api_p12_file')
    p12_password = os.getenv('VES_P12_PASSWORD')

    manager = VolterraWorkloadManager(api_url, tenant, namespace, p12_file, p12_password)
    args = parser.parse_args()

    try:
        if args.operation == 'create':
            print(f"Creating workload {workload_name} in namespace {namespace}...")
            result = manager.create_workload(workload_name, image_name, site_name, port, container_registry_name, site_namespace)
            print(f"Action: created")
        elif args.operation == 'replace':
            print(f"Replacing workload {workload_name} in namespace {namespace}...")
            result = manager.replace_workload(workload_name, image_name, site_name, port, container_registry_name, site_namespace)
            print(f"Action: replaced")
        elif args.operation == 'get':
            print(f"Getting workload {workload_name} in namespace {namespace}...")
            result = manager.get_workload(workload_name)
            print(json.dumps(result, indent=2))
        elif args.operation == 'delete':
            print(f"Deleting workload {workload_name} in namespace {namespace}...")
            result = manager.delete_workload(workload_name)
            print(f"Action: deleted")
        elif args.operation == 'upsert':
            print(f"Upserting workload {workload_name} in namespace {namespace}...")
            result, action = manager.upsert_workload(workload_name, image_name, site_name, port, container_registry_name, site_namespace)
            print(f"Action: {action}")
            
    except Exception as e:
        print(f"Error during {args.operation}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            # Avoid printing full response if it might contain sensitive info, but usually 
            # F5XC errors are safe. However, the rule says "never log full headers".
            try:
                error_data = e.response.json()
                print(f"Response Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Response Error: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
