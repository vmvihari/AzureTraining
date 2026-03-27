# Homework: Dockerfile Hands-On Practice (File, Image, and Runtime Management)

## Objective
By completing this homework, the trainee should be able to:
*   Write optimized Dockerfiles
*   Understand Docker image layers
*   Use `RUN`, `COPY`, `ADD`, `WORKDIR`, `EXPOSE`, `CMD`, and `ENTRYPOINT` correctly
*   Explain Alpine vs standard images
*   Demonstrate CMD vs ENTRYPOINT behavior practically

---

## Part 1: Dockerfile Instructions and Layer Optimization

### Step 1: Create a Project Directory
```bash
mkdir dockerfile-practice
cd dockerfile-practice
```

### Step 2: Create a Sample File
```bash
echo "Docker File Management Practice" > demo.txt
```

### Step 3: Create Dockerfile (Unoptimized Version)
```bash
nano Dockerfile
```
**Content:**
```Dockerfile
FROM ubuntu:22.04

RUN apt update
RUN apt install -y figlet

COPY demo.txt /app/

RUN ls /app > /app/output.txt
RUN ls /bin >> /app/output.txt
RUN ls /etc >> /app/output.txt
```

### Step 4: Build the Image
```bash
docker build -t docker-demo:v1 .
```

### Step 5: Check Image Layers
```bash
docker history docker-demo:v1
```
*   **Observation**: Multiple `RUN` instructions create multiple layers.

### Step 6: Optimize the Dockerfile
Edit the Dockerfile:
```bash
nano Dockerfile
```
**Content:**
```Dockerfile
FROM ubuntu:22.04

RUN apt update && apt install -y figlet

COPY demo.txt /app/

RUN ls /app > /app/output.txt && \
    ls /bin >> /app/output.txt && \
    ls /etc >> /app/output.txt
```

### Step 7: Rebuild and Compare
```bash
docker build -t docker-demo:v2 .
docker history docker-demo:v2
```
*   **Expected Result**:
    *   Reduced number of layers
    *   Smaller image size

---

## Part 2: WORKDIR Practical

### Step 1: Update Dockerfile
```Dockerfile
FROM ubuntu:22.04

WORKDIR /app

COPY demo.txt .

RUN pwd > workdir.txt
```

### Step 2: Build and Run
```bash
docker build -t workdir-demo .
docker run workdir-demo cat workdir.txt
```
*   **Expected Output**: `/app`

---

## Part 3: Alpine vs Standard Image Comparison

### Step 1: Pull Images
```bash
docker pull alpine
docker pull nginx
```

### Step 2: Check Image Sizes
```bash
docker images alpine nginx
```

### Step 3: Shell Difference
```bash
docker run -it alpine sh
docker run -it nginx bash
```
*   **Observation**:
    *   Alpine supports `sh` only
    *   NGINX supports `bash`

---

## Part 4: EXPOSE Instruction Demonstration

### Step 1: Create Dockerfile
```Dockerfile
FROM python:3.9

WORKDIR /app

RUN echo "print('Hello from container')" > app.py

EXPOSE 3000

CMD ["python3", "app.py"]
```

### Step 2: Build Image
```bash
docker build -t expose-demo .
```

### Step 3: Run Without Port Mapping
```bash
docker run expose-demo
```
*   **Observation**:
    *   Application runs
    *   No port is accessible externally

### Step 4: Run With Port Mapping
```bash
docker run -p 8080:3000 expose-demo
```
*   **Conclusion**:
    *   `EXPOSE` does not publish ports
    *   `-p` is mandatory

---

## Part 5: CMD vs ENTRYPOINT Practical

### CMD Example

1.  **Dockerfile with CMD**
    ```Dockerfile
    FROM ubuntu
    WORKDIR /app
    CMD ["pwd"]
    ```
2.  **Build and Run**
    ```bash
    docker build -t cmd-demo .
    docker run cmd-demo
    ```
    *   Output: `/app`
3.  **Override CMD**
    ```bash
    docker run cmd-demo ls -l
    ```
    *   **Result**: CMD is overridden successfully.

### ENTRYPOINT Example

1.  **Dockerfile with ENTRYPOINT**
    ```Dockerfile
    FROM ubuntu
    WORKDIR /app
    ENTRYPOINT ["pwd"]
    ```
2.  **Build and Run**
    ```bash
    docker build -t entrypoint-demo .
    docker run entrypoint-demo
    ```
    *   Output: `/app`
3.  **Attempt Override**
    ```bash
    docker run entrypoint-demo ls -l
    ```
    *   **Result**: Override does NOT work (it prints `/app`).

---

## Part 6: Interview Explanation Practice (Mandatory)

Each trainee must be able to explain verbally:
1.  Why combining `RUN` instructions reduces Docker image size.
2.  Difference between Alpine and standard images.
3.  Why `EXPOSE` is documentation and not networking.
4.  CMD vs ENTRYPOINT with real command examples.
5.  When to use CMD and when to use ENTRYPOINT in real projects.
