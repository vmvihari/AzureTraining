# Azure Firewall & Network Security

This module covers the implementation of secure network architectures in Azure, focusing on the Hub and Spoke model, Azure Firewall, and traffic management.

## Concepts

| Concept | Description |
|---------|-------------|
| [Hub and Spoke Architecture](./Concepts/01-HubAndSpokeArchitecture.md) | Centralized network topology for managing common services and security. |
| [Azure Firewall](./Concepts/02-AzureFirewall.md) | Managed, cloud-based network security service that protects your Azure Virtual Network resources. |
| [Azure Bastion](./Concepts/03-AzureBastion.md) | Secure and seamless RDP/SSH connectivity to your virtual machines. |
| [Routing and Peering](./Concepts/04-RoutingAndPeering.md) | Managing traffic flow between VNets and through the Firewall using User Defined Routes (UDR). |
| [Network Security Groups](./Concepts/05-NetworkSecurityGroups.md) | Filtering network traffic to and from Azure resources in an Azure virtual network. |

## Key Takeaways
- **Hub & Spoke**: The standard for enterprise network topology in Azure.
- **Centralized Security**: Azure Firewall acts as the "King" of security, inspecting all traffic leaving the network.
- **Traffic Control**: User Defined Routes (UDR) are essential to force traffic through the Firewall.
- **Secure Access**: Azure Bastion provides secure entry without exposing VMs to the public internet.
