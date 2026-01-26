# Introduction to Docker

Docker is the platform that enables microservices architecture by providing lightweight, portable environments called containers.

## What is Docker?
Docker is an open-source platform for developing, shipping, and running applications. It separates your applications from your infrastructure so you can deliver software quickly.

### Key Concepts

*   **Container**: A lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings.
*   **Image**: A read-only template with instructions for creating a Docker container. (Like a Class in OOP, where a Container is an Instance).

## Containers vs. Virtual Machines (VMs)

| Feature | Virtual Machines (VMs) | Docker Containers |
| :--- | :--- | :--- |
| **Architecture** | Runs a full Guest OS (Windows/Linux) on top of the Host OS via a Hypervisor. | Runs directly on the Host OS kernel, sharing system resources. |
| **Size** | Heavy (Gigabytes). Includes full OS. | Lightweight (Megabytes). Only includes app + libs. |
| **Boot Time** | Slow (Minutes). OS needs to boot. | Fast (Milliseconds). Starts like a process. |
| **Portability** | Less portable due to size and OS dependency. | Highly portable ("Build once, run anywhere"). |

## Why is Docker Critical?
1.  **Foundation**: Docker is the foundation for:
    *   **Kubernetes** (Container Orchestration).
    *   **ML Ops** (Machine Learning Operations).
    *   **AI Engineering**.
2.  **Consistency**: Eliminates the "It works on my machine" problem. The container works exactly the same in Dev, Test, and Production.
3.  **Microservices**: It is the standard way to package and deploy individual microservices.

## Upcoming Focus
The next phase of our training will focus deeply on:
1.  Writing **Dockerfiles**.
2.  Building **Images**.
3.  Running **Containers**.
