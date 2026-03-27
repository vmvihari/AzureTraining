# Infrastructure as Code and Automation

## Infrastructure as Code (IaC)
In DevOps, infrastructure is managed using code (IaC) rather than manual configuration.
-   **Reusability**: IaC scripts can be reused across environments (Dev, Stage, Prod) by simply changing configuration values.
-   **Languages**: Scripting languages like **Python** are crucial for writing these automations.

## Verification and Reporting
Automation isn't just about execution; it's also about verification.
-   **Scripts**: Use Shell or Python scripts to verify installations or configurations.
-   **Reporting**: Instead of manually checking thousands of VMs, scripts can generate reports (e.g., CSV files) as proof of success. This is often required to close Change Requests.

## Cost Optimization
Automation helps in optimizing cloud costs.
-   **Scheduled Shutdowns**: Automate the shutdown of non-production VMs (Dev, Test) during non-working hours (e.g., 7 PM to 7 AM).
-   **Tagging**: Use tags (e.g., `Environment=Dev`) to categorize resources, making it easy to target specific groups for automation.
-   **Tools**: Azure Functions can be used to schedule these jobs.
