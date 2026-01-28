# Introduction to Dockerfiles

A **Dockerfile** is a text document that contains all the commands a user could call on the command line to assemble an image. It is the "recipe" for creating your custom Docker images.

## 1. Anatomy of a Dockerfile

A Dockerfile has no extension (just `Dockerfile`).

### Common Instructions

| Instruction | Description | Example |
| :--- | :--- | :--- |
| **FROM** | **Required**. Sets the Base Image to start from. | `FROM nginx:latest` |
| **LABEL** | Adds metadata (Author, Version, Description). Replaces the deprecated `MAINTAINER`. | `LABEL version="1.0"` |
| **COPY** | Copies files from local host to image. | `COPY index.html /app/` |
| **ADD** | Like COPY, but can also **extract tars** and download URLs. | `ADD assets.tar.gz /app/` |
| **CMD** | The command the container runs by default when started. | `CMD ["nginx", "-g", "daemon off;"]` |
| **WORKDIR** | Sets the working directory for subsequent instructions. | `WORKDIR /app` |

---

## 2. COPY vs. ADD

This is a common interview question and practical distinction.

*   **COPY**:
    *   **Simple**. It only supports copying local files/directories into the container.
    *   **Best Practice**: Use this unless you specifically need ADD's features.

*   **ADD**:
    *   **Advanced**.
    *   If the source is a **local tar archive** (gzip, bzip2, etc.), it is automatically unpacked (extracted) into the destination.
    *   If the source is a **URL**, it downloads the file.

---

## 3. Building an Image

Once you have a Dockerfile, you "build" it into an image.

```bash
# General syntax
docker build -t <image_name>:<tag> <context_path>

# Example
docker build -t my-app:v1 .
```

*   `-t`: Tags the image (Name + Version).
*   `.`: The "Build Context" (current directory). Docker sends files in this directory to the daemon to process `COPY/ADD` instructions.

---

## 4. Layers and Caching

Every instruction in a Dockerfile (`FROM`, `COPY`, `RUN`) creates a new **Layer**.

*   **Read-Only**: These layers are read-only and stacked.
*   **Build Cache**: When you rebuild an image, Docker checks if the instruction changed.
    *   If nothing changed, it reuses the existing layer from the **Cache** (Super fast).
    *   If something changed (e.g., you modified a file referenced by `COPY`), that layer and **all subsequent layers** are rebuilt.

> **Tip**: Order matters! Put stable instructions (like installing dependencies) early, and frequent changes (like copying source code) later to maximize cache usage.
