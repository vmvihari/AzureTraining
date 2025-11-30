# Deployment Slots

## What are Deployment Slots?

Deployment slots are live apps with their own hostnames. You can use them to create separate environments (e.g., Dev, Test, Staging) within the same App Service Plan (Standard tier or higher).

-   **Production Slot**: The live app accessible to end-users.
-   **Non-Production Slots**: Separate environments for testing changes before they go live.

## Swapping Slots

Swapping is the process of promoting code from a non-production slot to production.

### How it Works
1.  **Deploy**: You deploy your new code to the `Staging` slot.
2.  **Test**: You verify the changes in the `Staging` environment.
3.  **Swap**: You trigger a swap operation. Azure warms up the `Staging` slot and then instantly switches the routing.
    -   `Staging` content becomes `Production`.
    -   `Production` content moves to `Staging`.

### Benefits
-   **Zero Downtime**: The swap happens instantly, ensuring no interruption for users.
-   **Easy Rollback**: If issues are found after swapping, you can simply swap back to restore the previous version.
-   **Production Testing**: You can route a small percentage of production traffic to a slot to test performance (Canary Testing).

> [!NOTE]
> **Database Connections**: Typically, database connection strings are "sticky" to the slot (configured as **Deployment slot setting**). This ensures that the Staging app connects to the Staging DB, and Production connects to Production DB, even after a swap.

## Workflow Example

1.  **Dev**: Developers push code to the `dev` branch.
2.  **Deploy**: App Service deploys this code to the `Development` slot.
3.  **Verify**: QA team tests the changes in the `Development` slot.
4.  **Swap**: Operations team swaps `Development` into `Production`.
5.  **Live**: The new features are now live for all users.
