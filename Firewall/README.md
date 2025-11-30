# Azure Firewall & Network Security

This module covers the implementation of secure network architectures in Azure, focusing on the Hub and Spoke model, Azure Firewall, and traffic management.

## Table of Contents

### Concepts
- [Hub and Spoke Architecture](./Concepts/01-HubAndSpokeArchitecture.md)
- [Azure Firewall](./Concepts/02-AzureFirewall.md)
- [Azure Bastion](./Concepts/03-AzureBastion.md)
- [Routing and Peering](./Concepts/04-RoutingAndPeering.md)
- [Network Security Groups](./Concepts/05-NetworkSecurityGroups.md)

### Labs
- [Lab 1: Azure Firewall - Hub and Spoke Architecture](./Labs/Lab01-AzureFirewall.md)

## Key Takeaways
- **Hub & Spoke**: The standard for enterprise network topology in Azure.
- **Centralized Security**: Azure Firewall acts as the "King" of security, inspecting all traffic leaving the network.
- **Traffic Control**: User Defined Routes (UDR) are essential to force traffic through the Firewall.
- **Secure Access**: Azure Bastion provides secure entry without exposing VMs to the public internet.
