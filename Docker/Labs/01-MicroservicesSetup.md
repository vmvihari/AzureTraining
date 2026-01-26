# Lab 01: Monolith vs. Microservices (Azure DevOps)

## Objective
Experience the structural differences between Monolithic and Microservices architectures using Azure DevOps. You will create projects, repositories, work items, and pipelines to simulate real-world management of both architectures.

**Prerequisites**: Access to Azure DevOps Organization.

## Part 1: Project & Repository Setup
### Task 1: Create Azure DevOps Project
1.  Log in to generic Azure DevOps organization.
2.  Click **New Project**.
3.  Details:
    *   **Name**: `food-delivery-architecture`
    *   **Visibility**: Private
    *   **Version Control**: Git
    *   **Work Item Process**: Agile
4.  Click **Create**.

### Task 2: Monolithic Repository Setup
1.  Navigate to **Repos**.
2.  Initialize the default repository (or create a new one named `food-delivery-monolith`).
3.  **Create Monolith Structure**:
    *   Go to **Files** -> **New File** (or use the kebab menu `...`).
    *   Create the following files (you can type `app/ui.py` to create folders automatically):
        *   `app/ui.py`: Add comment `# Handles User Interface`
        *   `app/cart.py`: Add comment `# Manages Shopping Cart`
        *   `app/order.py`: Add comment `# Processes Orders`
        *   `app/payment.py`: Add comment `# Handles Payments`
4.  **Purpose**: Observe how all unrelated logic resides in a single, tightly coupled repository.

## Part 2: Microservices Setup
### Task 3: Create Microservice Repositories
Create 4 separate repositories to simulate an independent microservices architecture.

1.  Click on the Repository dropdown (top breadcrumb) -> **New Repository**.
2.  Create `ui-service`.
    *   Add a `README.md`.
    *   **Content**: "Responsible for displaying the menu. Owned by Frontend Team. Failure: Menu unavailable, but backend still works."
3.  Create `cart-service`.
    *   Add a `README.md`.
    *   **Content**: "Manages user cart. Owned by Cart Team. Failure: Cannot add items, but can view menu."
4.  Create `order-service`.
    *   Add a `README.md`.
    *   **Content**: "Processes orders. Owned by Core Team."
5.  Create `payment-service`.
    *   Add a `README.md`.
    *   **Content**: "secure payment processing. Owned by FinTech Team."

## Part 3: Azure Boards (Real-World Workflow)
### Task 4: Work Items & Team Independence
Simulate how different teams work in parallel.

1.  Navigate to **Boards** -> **Work Items**.
2.  Create the following **User Stories** and assign them to different areas/repos if possible (mentally link them):
    *   **Story 1**: "Display food menu in UI"
        *   *Simulated Assignment*: `ui-service`
        *   Add 2 Tasks: "Design Mockup", "Implement HTML".
    *   **Story 2**: "Add items to cart"
        *   *Simulated Assignment*: `cart-service`
        *   Add 1 Bug: "Cart not updating correctly".
    *   **Story 3**: "Place order"
        *   *Simulated Assignment*: `order-service`
    *   **Story 4**: "Process payment"
        *   *Simulated Assignment*: `payment-service`

**Observation**: Notice how work can proceed on "Payment" without being blocked by "UI" changes.

## Part 4: Pipelines (Conceptual)
### Task 5: Independent CI Pipelines
Create a separate build pipeline for each service.

1.  Navigate to **Pipelines**.
2.  Click **Create Pipeline**.
3.  **Connect**: Azure Repos Git.
4.  **Select**: `cart-service` (Do not select the monolith).
5.  **Configure**: Starter Pipeline.
6.  **Review**: **DO NOT EDIT YAML**.
7.  **Save** (dropdown next to Run) -> **Save**.
8.  **Rename**: Rename the pipeline to `cart-service-pipeline`.

**Repeat** for all other services (`ui-service`, `order-service`, `payment-service`).

## Submission
*   Provide a screenshot of your **All Repositories** list showing the 5 repos.
*   Provide a screenshot of your **Pipelines** page showing 4 independent pipelines.
