# Azure Secure Network Platform

A Terraform-managed Azure platform demonstrating secure cloud networking, private connectivity, managed identity, RBAC, storage isolation, and controlled application access.

## Project Objective

This project evolves a basic Azure application into a security-focused cloud architecture.

The primary objectives are:

- Azure Virtual Network design
- Network segmentation
- App Service VNet Integration
- Private Endpoints
- Private DNS
- Managed Identity
- Azure RBAC
- Storage network isolation
- HTTPS and TLS hardening
- Infrastructure as Code with Terraform
- Automated testing and deployment with GitHub Actions

The application workload remains intentionally simple. The focus of this project is the **security and networking architecture surrounding the workload**.

---

## Architecture

```text
                         INTERNET
                             |
                           HTTPS
                             |
                             v
                 +-----------------------+
                 |      Azure App        |
                 |       Service         |
                 | app-secure-network-   |
                 |       platform        |
                 +-----------+-----------+
                             |
                     VNet Integration
                             |
                             v
                +--------------------------+
                | App Integration          |
                | 10.20.1.0/26             |
                | Microsoft.Web/serverFarms|
                | Delegation + NSG         |
                +-----------+--------------+
                            |
                   Azure VNet 10.20.0.0/16
                            |
                            v
                +------------------------+
                | Private Services       |
                | 10.20.2.0/24           |
                +-----------+------------+
                            |
                     +------+------+
                     |             |
                     v             v
              App Service PE   Storage PE
                10.20.2.5       10.20.2.4
                     |             |
                     v             v
                App Service    Storage Account
                               Public Access OFF
```

---

## Network Design

The network is organized into separate address spaces based on workload requirements.

### Virtual Network

```text
vnet-secure-network-platform
10.20.0.0/16
```

### App Integration Subnet

```text
snet-app-integration
10.20.1.0/26
```

This subnet is delegated to:

```text
Microsoft.Web/serverFarms
```

It is used by App Service VNet Integration for outbound connectivity into the virtual network.

An NSG is associated with this subnet to provide a dedicated location for network security controls.

### Private Services Subnet

```text
snet-private-services
10.20.2.0/24
```

This subnet is used for Private Endpoints.

It currently contains:

- App Service Private Endpoint
- Storage Blob Private Endpoint

The App Service Integration subnet and Private Services subnet are intentionally separated because they serve different Azure networking functions.

---

## Azure Resources

The platform is deployed in the `centralindia` Azure region.

### Core Resources

| Resource | Name |
|---|---|
| Resource Group | `rg-azure-secure-network-platform` |
| Virtual Network | `vnet-secure-network-platform` |
| App Integration Subnet | `snet-app-integration` |
| Private Services Subnet | `snet-private-services` |
| Network Security Group | `nsg-app-integration` |
| App Service Plan | `asp-secure-network-platform` |
| App Service | `app-secure-network-platform` |
| Storage Account | `stsecnetworkplatform01` |
| Storage Private Endpoint | `pe-storage-blob` |
| App Service Private Endpoint | `pe-app-service` |

---

## App Service

The application runs on Azure App Service using Linux and Python 3.12.

The App Service is configured with:

- HTTPS-only access
- Minimum TLS version 1.2
- FTP/FTPS basic authentication disabled
- WebDeploy basic authentication disabled
- System-assigned managed identity
- VNet Integration
- Private Endpoint

The application workload is intentionally simple and provides a small set of utility functions.

It provides:

- A web interface at `/`
- A calculator API at `POST /api/v1/calculator`
- A CIDR calculation API at `POST /api/v1/cidr`
- A unit conversion API at `POST /api/v1/convert`
- A health endpoint at `/health`

The utility functionality is intentionally kept simple so that the primary focus remains on the Azure networking and security architecture.

A previous public storage connectivity test endpoint was intentionally removed as part of the final security hardening. Storage access is not exposed through a public diagnostic endpoint.

---

## Private Connectivity

This project demonstrates two different Private Endpoint use cases.

### App Service Private Endpoint

The App Service has a Private Endpoint:

```text
pe-app-service
10.20.2.5
```

The Private Endpoint connection is approved and provisioned successfully.

Private DNS is provided through:

```text
privatelink.azurewebsites.net
```

The DNS zone is linked to the project VNet.

The Private Endpoint also provides private DNS resolution for the App Service SCM endpoint.

### Storage Private Endpoint

The Storage Account has a Blob Private Endpoint:

```text
pe-storage-blob
10.20.2.4
```

The Private Endpoint connection is approved and provisioned successfully.

Private DNS is provided through:

```text
privatelink.blob.core.windows.net
```

The DNS zone is linked to the project VNet.

This allows resources using the VNet to resolve the Storage Account Blob endpoint to its private address.

---

## Storage Security

The project uses a dedicated Storage Account:

```text
stsecnetworkplatform01
```

The Storage Account is configured with:

- Public network access disabled
- Shared Key authentication disabled
- OAuth authentication enabled/preferred
- Anonymous blob access disabled
- Local user access disabled
- Minimum TLS version 1.2
- Blob Private Endpoint
- Private DNS
- Azure RBAC

The application does not rely on a Storage Account access key.

Instead, the App Service uses its managed identity to authenticate to Azure Storage.

---

## Identity and Access Control

The App Service has a system-assigned managed identity.

That identity is granted:

```text
Storage Blob Data Contributor
```

at the Storage Account scope.

This provides the application with the permissions required for blob data operations without embedding long-lived credentials in the application.

The GitHub Actions deployment identity is separate from the App Service runtime identity.

The deployment identity is used for CI/CD, while the managed identity is used by the running application.

This separation reduces unnecessary permission overlap between deployment and runtime operations.

---

## Application Access

The App Service currently retains its public HTTPS endpoint so that the application can be directly accessed and its functionality can be demonstrated.

The public application surface consists of the Utility Hub web interface, utility APIs, and the health endpoint.

At the same time, the App Service has a Private Endpoint that provides private connectivity from the VNet.

This is an intentional architecture decision for this project.

The project demonstrates that an App Service can have private connectivity established through a Private Endpoint while the public application endpoint remains available for direct demonstration and verification.

A future architecture could disable public App Service access and operate the application as a private-only service when an appropriate private client or private ingress architecture is introduced.

---

## Infrastructure as Code

All Azure infrastructure for this project is managed using Terraform.

Terraform provisions and manages:

- Resource Group
- Virtual Network
- Subnets
- Subnet delegation
- Network Security Group
- App Service Plan
- Linux Web App
- Managed Identity
- Storage Account
- Storage RBAC
- Storage Private Endpoints
- App Service Private Endpoint
- Private DNS Zones
- Private DNS Zone VNet Links

Terraform state and local variable files are excluded from source control.

A previous successful infrastructure validation produced:

```text
No changes. Your infrastructure matches the configuration.
```

At the time of that validation, Terraform reported that the deployed Azure infrastructure matched the Terraform configuration.

---

## CI/CD

GitHub Actions provides automated application testing and deployment.

The deployment workflow performs the following steps:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs application dependencies
4. Runs the automated test suite
5. Authenticates to Azure using OpenID Connect
6. Deploys the application to Azure App Service
7. Verifies the application health endpoint

Azure authentication uses GitHub Actions OIDC rather than a stored client secret.

The CI/CD identity and application runtime identity are intentionally separate.

---

## Testing

The project includes automated tests using `pytest`.

The current test suite verifies:

- `/health` returns the expected health response
- The homepage loads successfully
- Application metadata matches the project configuration

The application also provides the following utility APIs:

- `POST /api/v1/calculator`
- `POST /api/v1/cidr`
- `POST /api/v1/convert`

These utility endpoints are part of the application workload and are manually verified during local and deployed application testing.

Local automated test execution:

```text
7 passed
```

The same tests are executed by the GitHub Actions workflow before deployment.

---

## Project Structure

```text
azure-secure-network-platform/
|
+-- app/
|   +-- main.py
|   +-- calculator.py
|   +-- cidr.py
|   +-- converter.py
|   +-- static/
|   |   +-- script.js
|   |   +-- style.css
|   |
|   +-- templates/
|       +-- index.html
|
+-- tests/
|   +-- test_api.py
|   +-- test_network.py
|
+-- terraform/
|   +-- providers.tf
|   +-- variables.tf
|   +-- main.tf
|   +-- networking.tf
|   +-- security.tf
|   +-- storage.tf
|   +-- storage_rbac.tf
|   +-- private_endpoint.tf
|   +-- private_endpoint_app.tf
|   +-- app_service.tf
|
+-- docs/
|
+-- .github/
|   +-- workflows/
|       +-- deploy.yml
|
+-- .gitignore
+-- .gitattributes
+-- README.md
+-- requirements.txt
```

---

## Security Principles Demonstrated

### Network Segmentation

Separate subnets are used for App Service VNet Integration and Private Endpoints.

### Private Connectivity

Private Endpoints provide private connectivity to Azure services without requiring public network access for the Storage Account.

### Identity-Based Authentication

Managed Identity and Azure RBAC are used instead of embedding Storage Account keys in the application.

### Least Privilege

The application identity receives the Storage Blob Data Contributor role at the Storage Account scope rather than broader subscription-level permissions.

### Secure Transport

HTTPS is enforced and TLS 1.2 is configured as the minimum TLS version.

### Separation of Responsibilities

The CI/CD identity is separate from the runtime managed identity.

### Infrastructure as Code

Terraform provides a reproducible and reviewable representation of the Azure infrastructure.

---

## Verification Evidence

The deployed platform was validated at multiple layers.

### Application Health

The deployed application returned:

```text
HTTP 200 OK
```

from:

```text
/health
```

### App Service Private Endpoint

```text
Connection: Approved
Provisioning: Succeeded
Private IP: 10.20.2.5
```

### Storage Private Endpoint

```text
Connection: Approved
Provisioning: Succeeded
Private IP: 10.20.2.4
```

### Terraform

```text
No changes. Your infrastructure matches the configuration.
```

### Automated Tests

```text
7 passed
```

The same tests are executed by the GitHub Actions workflow before deployment.

---

## Project Scope

This project intentionally focuses on the foundations of secure Azure networking and identity.

The primary areas demonstrated are:

- Azure Virtual Network design
- Network segmentation
- App Service VNet Integration
- Private Endpoints
- Private DNS
- Storage network isolation
- Managed Identity
- Azure RBAC
- HTTPS and TLS hardening
- Terraform
- CI/CD security

The project does not attempt to implement every Azure security service.

Advanced monitoring, detection, response, governance, and automation are outside the scope of this project.
---
