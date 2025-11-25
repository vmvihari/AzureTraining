# Azure Firewall

Azure Firewall is a managed, cloud-based network security service that protects your Azure Virtual Network resources. It is a fully stateful firewall as a service with built-in high availability and unrestricted cloud scalability.

## Key Concepts

### 1. Deployment
- **Subnet**: Requires a dedicated subnet named `AzureFirewallSubnet`.
- **Public IP**: Requires a Standard Public IP address. This IP is used for all outbound traffic from the VNet to the internet (SNAT).
- **Cost**: It is a premium resource (approx. $1.75/hr or ~140 INR/hr). For learning purposes, it should be deleted when not in use.

### 2. Rules
Azure Firewall processes rules in a specific order.

#### Network Rules
- Control traffic based on IP addresses, ports, and protocols.
- **Example**: Allow traffic from `10.1.0.0/24` (Spoke Subnet) to `8.8.8.8` (Google DNS) on Port `53`.

#### Application Rules
- Control traffic based on Fully Qualified Domain Names (FQDNs).
- **Example**: Allow traffic from `10.1.0.0/24` to `*.google.com` on Port `443`.
- **Why use FQDN?**: IP addresses for websites change frequently. FQDNs allow you to whitelist entire domains (e.g., `google.com`) without managing IPs.

### 3. The "Dummy Rule"
- By default, Azure Firewall blocks all traffic (Implicit Deny).
- To test connectivity or "block everything," you don't need to create a deny rule; simply having no allow rules achieves this.
- **Note**: In the session, a "dummy rule" was mentioned as a way to initially block or control traffic before specific allow rules are created.

### 4. Monitoring
- Azure Firewall integrates with **Azure Monitor** for centralized logging and alerting.
- You can set up alerts for specific traffic patterns or potential threats.
