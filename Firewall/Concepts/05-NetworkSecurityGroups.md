# Network Security Groups (NSG)

Network Security Groups (NSGs) act as a basic firewall for filtering network traffic to and from Azure resources in an Azure virtual network.

## Overview

- **Function**: Contains security rules that allow or deny inbound network traffic to, or outbound network traffic from, several types of Azure resources.
- **Scope**: Can be associated with:
  - **Subnets**: Applies to all resources in the subnet.
  - **Network Interfaces (NICs)**: Applies to a specific VM.

## NSG vs. Azure Firewall

| Feature | Network Security Group (NSG) | Azure Firewall |
|---------|------------------------------|----------------|
| **Scope** | Subnet / NIC level | VNet / Subscription level |
| **Layer** | Layer 3 (Network) & Layer 4 (Transport) | Layer 3-7 (Network to Application) |
| **Filtering** | IP, Port, Protocol | IP, Port, Protocol, FQDN (Application) |
| **State** | Stateful | Fully Stateful as a Service |
| **Role** | Basic traffic filtering (ACLs) | Centralized, advanced network security |

## Best Practices

- **Defense in Depth**: Use both NSGs and Azure Firewall.
  - Use **Azure Firewall** for centralized, organization-wide traffic filtering (North-South traffic, Egress filtering).
  - Use **NSGs** for micro-segmentation within VNets (East-West traffic between subnets).

> **Session Note**: BalaKrishna described the Firewall as the "King" or primary layer of security, with NSGs acting as a secondary layer closer to the resources.
