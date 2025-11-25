# Azure Bastion

Azure Bastion is a fully managed service that provides secure and seamless RDP and SSH access to your virtual machines directly through the Azure Portal.

## Key Features

- **Secure Access**: Connect to your VMs using SSL (port 443) directly from the Azure portal.
- **No Public IP**: Your VMs do not need a public IP address. Bastion acts as a gateway.
- **Protection**: Protects your VMs from port scanning and other internet-based threats.

## Implementation Details

### 1. Subnet Requirement
- Requires a dedicated subnet named `AzureBastionSubnet`.
- The subnet must be created in the Hub VNet (in a Hub and Spoke topology).

### 2. Public IP
- The Bastion host itself requires a **Public IP** address to be accessible from the Azure Portal (internet).
- However, the VMs it connects to (in the Spokes) use **Private IPs**.

## Bastion vs. Jump Host

| Feature | Azure Bastion | Jump Host (Jump Server) |
|---------|---------------|-------------------------|
| **Type** | PaaS (Platform as a Service) | IaaS (VM) |
| **Management** | Fully managed by Azure | Managed by you (OS updates, patching) |
| **Access** | Browser-based (HTML5) | RDP client / SSH client |
| **Security** | No Public IP on target VM | Target VM might need Public IP or complex rules |
| **Cost** | Hourly charge (can be higher) | VM cost (can be lower if small size) |

> **Note**: In the session, it was clarified that connecting via Bastion is functionally similar to RDP but more secure as it avoids exposing the VM directly to the internet.
