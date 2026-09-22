# Azure Secure Network Platform â€” Architecture

## Overview

Azure Secure Network Platform demonstrates a segmented Azure application architecture using Azure Virtual Network integration, private endpoints, private DNS, and network security controls.

The application is hosted on Azure App Service. Outbound communication from the application is integrated with an Azure Virtual Network, while private endpoints provide private connectivity to Azure resources.

## Architecture

                         INTERNET
                            |
                         HTTPS
                            |
                            v
                 +----------------------+
                 |    Azure App Service |
                 |   Web / API tier     |
                 +----------+-----------+
                            |
                     VNet Integration
                            |
                            v
              +---------------------------+
              | VNet 10.20.0.0/16        |
              |                           |
              |  +---------------------+  |
              |  | App Integration     |  |
              |  | 10.20.1.0/26       |  |
              |  |                     |  |
              |  | NSG                 |  |
              |  | App Service         |  |
              |  | delegation          |  |
              |  +----------+----------+  |
              |             |             |
              |             v             |
              |  +---------------------+  |
              |  | Private Services    |  |
              |  | 10.20.2.0/24       |  |
              |  |                     |  |
              |  | Private Endpoints   |  |
              |  +---------------------+  |
              +---------------------------+
                            |
                            v
                       Azure Storage

The architecture separates the App Service integration subnet from the subnet used for private endpoints.

## Network Layout

The virtual network is:

VNet: 10.20.0.0/16

It contains two subnets.

### App Integration Subnet

Name:    snet-app-integration
Address: 10.20.1.0/26

This subnet is used for App Service VNet Integration and has the required App Service delegation.

An NSG is associated with the subnet to provide network-level security controls for traffic routed through the integration subnet.

### Private Services Subnet

Name:    snet-private-services
Address: 10.20.2.0/24

This subnet contains private endpoints used to provide private connectivity to Azure services.

## App Service VNet Integration

The App Service is integrated with:

vnet-secure-network-platform
â””â”€â”€ snet-app-integration

VNet Integration provides the App Service with outbound connectivity through the virtual network.

It does not make the public App Service endpoint private by itself.

## Private Endpoints

Private endpoints are used for private access to Azure resources.

The deployment contains private endpoints for:

- App Service
- Azure Storage Blob

The App Service private endpoint provides private inbound connectivity to the application.

The Storage private endpoint provides private connectivity to Blob Storage.

## Private DNS

Private DNS zones provide name resolution for the private endpoints.

The deployment uses:

privatelink.azurewebsites.net
privatelink.blob.core.windows.net

The private DNS records resolve the services to their private endpoint addresses inside the virtual network.

## Network Security Group

The App Integration subnet is associated with:

nsg-app-integration

The NSG provides a place to define and control network traffic associated with the integration subnet.

The current deployment retains the Azure default NSG rules and does not add unnecessary custom rules.

## Storage Access

Storage access is designed around the private endpoint rather than direct public access.

The Storage Blob private endpoint is located in the private services subnet.

This keeps the private service path inside the virtual network while avoiding unnecessary exposure of the storage service to the public network.

## Infrastructure as Code

Terraform manages the Azure infrastructure.

The configuration defines the networking components, App Service configuration, private endpoints, private DNS zones, storage resources, and network security controls.

This allows the environment to be reproduced consistently rather than relying on manual Azure Portal configuration.

## Design Considerations

The architecture intentionally uses a small number of Azure networking components.

It does not introduce additional services such as:

- Azure Firewall
- VPN Gateway
- ExpressRoute
- Application Gateway
- Bastion
- NAT Gateway

These services were not required for the application's current networking requirements.

The design focuses on demonstrating practical Azure network segmentation, private connectivity, DNS resolution, and App Service integration without adding unnecessary infrastructure.
