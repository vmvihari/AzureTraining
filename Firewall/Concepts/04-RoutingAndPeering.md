# Routing and Peering

In a Hub and Spoke architecture, **Routing** and **Peering** are critical for ensuring traffic flows correctly through the Firewall.

## VNet Peering

- **Definition**: Connecting two Virtual Networks (VNets) so they can communicate as if they were one network.
- **Usage**:
  - Connect **Hub VNet** <--> **Spoke VNet**.
  - **Important**: Peering is non-transitive. Spoke A cannot talk to Spoke B just because both are peered with the Hub. Traffic must be routed through a central appliance (Firewall).

## User Defined Routes (UDR)

By default, Azure routes traffic automatically between subnets and to the internet. To enforce security via Azure Firewall, you must override these defaults using **Route Tables**.

### Why use UDRs?
- To force all traffic from a Spoke VNet to go through the Azure Firewall in the Hub before going to the internet or another Spoke.
- This ensures all traffic is inspected and filtered.

### Configuration Steps
1.  **Create a Route Table**.
2.  **Add a Route**:
    - **Address Prefix**: `0.0.0.0/0` (Represents all traffic/internet).
    - **Next Hop Type**: `Virtual Appliance`.
    - **Next Hop IP Address**: Private IP address of the Azure Firewall.
3.  **Associate**: Link the Route Table to the **Spoke Subnet**.

## Traffic Flow Example

1.  **VM in Spoke** tries to access `google.com`.
2.  **UDR** on Spoke Subnet sees the destination matches `0.0.0.0/0`.
3.  Traffic is sent to **Azure Firewall** (Next Hop).
4.  **Azure Firewall** checks its Rules:
    - If allowed (e.g., Application Rule for `*.google.com`), traffic is forwarded to the internet.
    - If denied (or no rule exists), traffic is dropped.

> **Session Note**: Even though the Firewall has a Public IP, internal traffic from Spokes is routed to the Firewall's **Private IP**.
