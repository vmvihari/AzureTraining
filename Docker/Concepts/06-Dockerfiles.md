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

---

## 5. Other Key Instructions

### RUN (Build-Time Execution)

*   **Purpose**: Executes commands inside the image **during the build process**.
*   **Use Case**: Installing packages, creating folders, setting file permissions.
*   **Result**: Creates a new layer committed to the image.

```Dockerfile
RUN apt-get update && apt-get install -y python3
```

### WORKDIR (Set Working Directory)

*   **Purpose**: Sets the working directory for any subsequent `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions.
*   **Behavior**:
    *   If the directory doesn't exist, it is created.
    *   It's like doing `cd` inside the build.
    *   All future relative paths are relative to this `WORKDIR`.

```Dockerfile
WORKDIR /app
COPY . . 
# The above copies files from host current dir to /app inside container
```

### EXPOSE (Documentation Only)

*   **Critical Concept**: The `EXPOSE` instruction **DOES NOT** publish the port.
*   **Purpose**: It acts as **documentation** for the person running the container, letting them know which port the application is listening on.
*   **Action Required**: You MUST still use the `-p` flag when running the container to actually publish the port to the host.

```Dockerfile
# Documentation
EXPOSE 80

# You still need to run:
# docker run -p 8080:80 my-image
```

---

## 6. CMD vs. ENTRYPOINT (Runtime Instructions)

This is a very common interview question. Both define what happens when the container starts, but they behave differently when arguments are passed to `docker run`.

| Feature | CMD | ENTRYPOINT |
| :--- | :--- | :--- |
| **Purpose** | Default command/args | Main executable to run |
| **Override?** | **Easy**. Arguments to `docker run` completely replace the CMD. | **Hard**. Arguments to `docker run` are *appended* to the ENTRYPOINT (treated as args). |
| **Use Case** | Default shell, or fallback args | Executables that should always run (e.g., binaries) |

### Example Scenario

**Dockerfile with CMD:**
```Dockerfile
CMD ["echo", "Hello"]
```
*   `docker run myimage` -> Outputs: "Hello"
*   `docker run myimage echo Bye` -> Outputs: "Bye" (CMD replaced)

**Dockerfile with ENTRYPOINT:**
```Dockerfile
ENTRYPOINT ["echo", "Hello"]
```
*   `docker run myimage` -> Outputs: "Hello"
*   `docker run myimage World` -> Outputs: "Hello World" ("World" appended)

> **Security Insight**: Use `ENTRYPOINT` for production applications to prevent users from easily overriding the startup command to run arbitrary things (like `/bin/bash`).

---

## 7. Layer Optimization

Every `RUN`, `COPY`, `ADD` instruction creates a layer. To keep images small:

**Bad Practice (Many Layers):**
```Dockerfile
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y curl
```

**Good Practice (Chain Commands):**
Use `&&` to combine commands into a single `RUN` instruction. This creates only **one layer** for all operations.

```Dockerfile
RUN apt-get update && \
    apt-get install -y vim curl && \
    rm -rf /var/lib/apt/lists/*
```
