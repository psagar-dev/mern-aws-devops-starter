## 🚀 MERN Microservices Deployment on Elastic Kubernetes Service (EKS) with Helm, Jenkins, and MERN App

This project demonstrates deploying a **MERN application** (React frontend + Node.js microservices + MongoDB Atlas) on **Azure Kubernetes Service (EKS)**.

---

### 📂 Project Structure
```
mern-microservices-starter
├── Jenkinsfile
├── README.md
├── backend
│   ├── helloService
│   │   ├── Dockerfile
│   │   ├── index.js
│   │   ├── package-lock.json
│   │   └── package.json
│   └── profileService
│       ├── Dockerfile
│       ├── document.txt
│       ├── index.js
│       ├── package-lock.json
│       └── package.json
├── document.txt
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── nginx
│   │   └── nginx.conf
│   ├── package-lock.json
│   ├── package.json
│   ├── public/
│   └── src/
├── images/
├── helm/
├── k8s
│   ├── frontend
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── hello
│   │   ├── deployment.yaml
│   │   ├── secret.yaml
│   │   └── service.yaml
│   ├── namespace.yaml
│   └── profile
│       ├── deployment.yaml
│       ├── secret.yaml
│       └── service.yaml
```

### 🚀 Create Elastic Kubernetes Service (EKS) Cluster

```bash
eksctl create cluster \
  --name mern-cluster \
  --region ap-south-1 \
  --nodegroup-name mern-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 5 \
  --managed
```
### Flag breakdown
- `eksctl create cluster`: Provisions the EKS control plane and a node group with sensible defaults.
- `--name mern-cluster`: Sets the EKS cluster name.
- `--region ap-south-1`: Uses the Mumbai AWS region.
- `--nodegroup-name mern-workers`: Names the worker node group.
- `--node-type t3.medium`: Chooses EC2 instance type for nodes.
- `--nodes 2`: Desired (initial) node count.
- `--nodes-min 2`: Minimum node count.
- `--nodes-max 5`: Maximum node count.
- `--managed`: Creates an EKS Managed Node Group (AWS-managed lifecycle).

![Clustor](/images/eks-cluster.png)
![Clustor UI](/images/eks-cluster-ui.png)

### 🔑 Configure Kubeconfig

```bash
aws eks update-kubeconfig --region ap-south-1 --name mern-cluster
```
### ✅ Verify connection
```
kubectl get nodes
kubectl cluster-info
```
![AKS ](/images/eks-switch-local-to-aks.png)

![AKS ](/images/cluster-detail.png)
### 🌉 Create a Docker Network

Before running the services, create a Docker bridge network:

```bash
docker network create --driver bridge mernapp
```

### 📛 Create a Kubernetes Namespace

Before deploying your services, it's a best practice to isolate them within a dedicated Kubernetes namespace.

A predefined namespace file is available at: `k8s/namespace.yaml`
```bash
apiVersion: v1
kind: Namespace
metadata:
  name: mern-microservice
```
🚀 Apply the Namespace
Use the following command to create the namespace in your cluster:
```bash
kubectl apply -f k8s/namespace.yaml
```
![namespace k8s](/images/namespace-ui.png)

#### 📂 Backend Repository Identification
🔗 **Repository**: `https://github.com/psagar-dev/mern-microservices-starter`

**Purpose:** This repository contains the backend code for the MERN application, built with Node.js and Express.js, handling API requests, MongoDB interactions, and authentication.

Technologies:

- **Node.js**: Runtime for the backend server.
- **Express.js**: Framework for building RESTful APIs.
- **MongoDB**: Database for storing application data.
- **Mongoose**: ODM for MongoDB.

```bash
git clone https://github.com/psagar-dev/mern-microservices-starter.git
```
For `Hello Service`
```bash
cd backend/helloService
npm install
npm start
```

For `Profile Service`
```bash
cd backend/profileService
npm install
npm start
```
#### 📂 Frontend Repository Identification
🔗 **Repository**: `https://github.com/psagar-dev/mern-microservices-starter`

**Purpose**: This repository contains the frontend code for the MERN application, built with React, providing a user interface for interacting with the backend APIs.

Technologies:

- **React**: Library for building the user interface.
- **Axios**: For making HTTP requests to the backend.
- **React Router**: For client-side routing.
- **Nginx**: For serving the production build.

```bash
git clone https://github.com/psagar-dev/mern-microservices-starter.git
cd backend/frontend
npm install
npm run dev
```

## ⚙️ Backend -  Express.js(Node Js)
### 👋 Hello Service
#### 🐳 Steps to Deploy an Application on Docker
📁 Create a `Dockerfile` inside the `backend/helloService` directory:

```Dockerfile
# Stage 1: Install Deps & build
FROM node:22-alpine AS builder

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application code to the working directory
COPY . .

# remove devDependencies
RUN npm prune --production

# Stage 2: Runtime: only prod artifacts on Alpine
#FROM node:lts-alpine as production
FROM node:22-alpine AS production

# Set the working directory in the container to /app
WORKDIR /app

# Install curl for healthchecks
RUN apk add --no-cache curl

# Copy only the necessary files from the builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app ./

# Build the application
EXPOSE 3001

# CMd to run the application
CMD ["node", "index.js"]
```
### 🔍 Local Testing & Validation
Build the Docker image:
```
docker image build --no-cache --network=mernapp -t securelooper/mern-microservices-hello .
```
![mern Hello microservices](/images/mern-hello-build.png)


Push the image to Docker Hub.
```
docker image push securelooper/mern-microservices-hello
```

Run the container:
```
docker container run -d --name mern-microservices-hello -e PORT=3001 -p 3001:3001 securelooper/mern-microservices-hello
```
**Base URL:** `http://localhost:3001`
![mern Hello microservices live](/images/mern-hello-live.png)

### ☸️ Steps to Deploy an Application on Kubernetes
##### 🗂️ 1. Create Secret
📄 **File**: `k8s/hello/secret.yaml`
```yml
apiVersion: v1
kind: Secret
metadata:
  name: hello-backend-secrets
  namespace: mern-microservice
type: Opaque
data:
  PORT: MzAwMQo=
```
📌 **Apply Secret**

```bash
kubectl apply -f k8s/hello/secret.yaml
```
🔍 **Verify Secret**
```bash
kubectl get secret -n mern-microservice
```
![secret](/images/hello-service-secret.png)
![secret](/images/secret.png)
#### 📄 2 Create Deployment
**File:** `k8s/hello/deployment.yaml`
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-backend
  labels:
    app: hello-backend
    tier: hello-backend
    environment: production
  namespace: mern-microservice
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-backend
  template:
    metadata:
      labels:
        app: hello-backend
        tier: hello-backend
        environment: production
    spec:
      restartPolicy: Always
      containers:
      - name: mern-microservices-hello
        image: securelooper/mern-microservices-hello:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3001
        envFrom:
        - secretRef:
            name: hello-backend-secrets
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 40
          periodSeconds: 5
```

📌 **Apply Deployment**
```bash
kubectl apply -f k8s/hello/deployment.yaml
```
🔍 **Verify Pods**
```bash
kubectl get pods -n mern-microservice
```
📜 **View Logs to Confirm Communication**
```
kubectl logs deploy/hello-backend -n mern-microservice
```
OR
```
kubectl logs pod/<pod_name> -n mern-microservice
```
![Node](/images/hello-deploy-logs.png)
![Node](/images/node-ui.png)
#### 📄 3 Create Service
**File:** `k8s/hello/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-backend
  namespace: mern-microservice
  labels:
    app: hello-backend
    tier: hello-backend
    environment: production
spec:
  selector:
    app: hello-backend
  ports:
  - port: 3001
    targetPort: 3001
  type: LoadBalancer
```

📌 **Apply Service**
```bash
kubectl apply -f k8s/hello/service.yaml
```
🔍 **Verify Service**
```bash
kubectl get svc -n mern-microservice
```

🔁 **Test Inter-Service Communication Using cURL**

Run a shell inside the user pod:
```bash
kubectl exec -it deploy/hello-backend -n mern-microservice -- sh
```
From inside the pod, test communication:
```bash
curl http://hello-backend.mern-microservice.svc.cluster.local:3001/health
```
![Hello service](/images/hello-service.png)
![Hello service UI](/images/service-ui.png)
#### 🧪 4 Test with Port Forwarding (For Localhost)
```bash
kubectl port-forward service/backend -n=learner-insights 3001:3001 --address=0.0.0.0
```
🌍 Access the service in your browser or tool like Postman:
run it
```bash
http://localhost:3001/health
```

---

### 👤 Profile Service
#### 🐳 Steps to Deploy an Application on Docker
📁 Create a `Dockerfile` inside the `backend/profileService` directory:
```Dockerfile
# Stage 1: Install Deps & build
FROM node:22-alpine AS builder

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application code to the working directory
COPY . .

# remove devDependencies
RUN npm prune --production

# Stage 2: Runtime: only prod artifacts on Alpine
#FROM node:lts-alpine as production
FROM node:22-alpine AS production

# Set the working directory in the container to /app
WORKDIR /app

# Install curl for healthchecks
RUN apk add --no-cache curl

# Copy only the necessary files from the builder stage
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app ./

# Build the application
EXPOSE 3002

# CMd to run the application
CMD ["node", "index.js"]
```

### 🔍 Local Testing & Validation
Build the Docker image:
```
docker image build --no-cache -t securelooper/mern-microservices-profile .
```
![mern Profile microservices](/images/mern-profile-build.png)

Push the image to Docker Hub.
```
docker image push securelooper/mern-microservices-profile
```

Run the container:
```
docker container run -d --name mern-microservices-profile --network=mernapp -e PORT=3002 -e MONGO_URL="mongodb://root:root@192.168.31.100:27017/mern-microservices?authSource=admin" -p 3002:3002 securelooper/mern-microservices-profile
```
**Base URL:** `http://localhost:3002`
![mern profile microservices live](/images/mern-profile-live.png)

### ☸️ Steps to Deploy an Application on Kubernetes
##### 🗂️ 1. Create Secret
📄 **File**: `k8s/profile/secret.yaml`
```yml
apiVersion: v1
kind: Secret
metadata:
  name: profile-backend-secrets
  namespace: mern-microservice
type: Opaque
data:
  PORT: MzAwMg==
  MONGO_URL: bW9uZ29kYjovL3Jvb3Q6cm9vdEAxOTIuMTY4LjMxLjEwMDoyNzAxNy9tZXJuLW1pY3Jvc2VydmljZXMtc3RhcnRlcj9hdXRoU291cmNlPWFkbWlu
```
📌 **Apply Secret**

```bash
kubectl apply -f k8s/profile/secret.yaml
```
🔍 **Verify Secret**
```bash
kubectl get secret -n mern-microservice
```
![Profile secret](/images/profile-secret.png)
![secret](/images/secret.png)
#### 📄 2 Create Deployment
**File:** `k8s/profile/deployment.yaml`
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: profile-backend
  labels:
    app: profile-backend
    tier: profile-backend
    environment: production
  namespace: mern-microservice
spec:
  replicas: 1
  selector:
    matchLabels:
      app: profile-backend
  template:
    metadata:
      labels:
        app: profile-backend
        tier: profile-backend
        environment: production
    spec:
      restartPolicy: Always
      containers:
      - name: mern-microservices-profile
        image: securelooper/mern-microservices-profile:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3002
        envFrom:
        - secretRef:
            name: profile-backend-secrets
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 3002
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3002
          initialDelaySeconds: 40
          periodSeconds: 5
```

📌 **Apply Deployment**
```bash
kubectl apply -f k8s/profile/deployment.yaml
```
🔍 **Verify Pods**
```bash
kubectl get pods -n mern-microservice
```
📜 **View Logs to Confirm Communication**
```
kubectl logs deploy/profile-backend -n mern-microservice
```
OR
```
kubectl logs pod/<pod_name> -n mern-microservice
```
![Profile Deploy](/images/profile-deploy-log.png)
![Profile Deploy](/images/node-ui.png)
#### 📄 3 Create Service
**File:** `k8s/profile/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: profile-backend
  namespace: mern-microservice
  labels:
    app: profile-backend
    tier: profile-backend
    environment: production
spec:
  selector:
    app: profile-backend
  ports:
  - port: 3002
    targetPort: 3002
  type: LoadBalancer
```

📌 **Apply Service**
```bash
kubectl apply -f k8s/profile/service.yaml
```
🔍 **Verify Service**
```bash
kubectl get svc -n mern-microservice
```

![service UI](/images/service-ui.png)
🔁 **Test Inter-Service Communication Using cURL**

Run a shell inside the user pod:
```
kubectl exec -it deploy/profile-backend -n mern-microservice -- sh
```
From inside the pod, test communication:
```
curl http://profile-backend.mern-microservice.svc.cluster.local:3002/health
```

#### 🧪 4 Test with Port Forwarding (For localhost)
```bash
kubectl port-forward service/backend -n=mern-microservice 3002:3002 --address=0.0.0.0
```
🌍 Access the service in your browser or tool like Postman:
run it
```bash
http://localhost:3002/health
```

---
### 🎨 Frontend Service
#### 🐳 Steps to Deploy an Application on Docker
📁 Create a `Dockerfile` inside the `frontend` directory:

```Dockerfile
# STAGE 1: Build
FROM node:22-alpine AS builder

# Accept build-time API URL
ARG REACT_APP_API_BASE_URL_HELLO
ARG REACT_APP_API_BASE_URL_PROFILE
ENV REACT_APP_API_BASE_URL_HELLO=$REACT_APP_API_BASE_URL_HELLO
ENV REACT_APP_API_BASE_URL_PROFILE=$REACT_APP_API_BASE_URL_PROFILE

# Set the working directory in the container to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application code to the working directory
COPY . .

RUN npm run build

# STAGE 2: Serve
FROM nginx:alpine

# Install curl for healthchecks
RUN apk add --no-cache curl

# Set the working directory in the container to /usr/share/nginx/html
RUN rm -rf /usr/share/nginx/html/*

# Copy only the necessary files from the builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose
EXPOSE 80

# Build the application
CMD ["nginx", "-g", "daemon off;"]
```
### 🔍 Local Testing & Validation
Build the Docker image:
```
docker image build --build-arg REACT_APP_API_BASE_URL_HELLO=http://192.168.31.100:3001 --build-arg REACT_APP_API_BASE_URL_PROFILE=http://192.168.31.100:3002 -t securelooper/mern-microservices-frontend .
```
![mern Frontend](/images/mern-frontend-build.png)


Push the image to Docker Hub.
```
docker image push securelooper/mern-microservices-frontend
```

Run the container:
```
docker container run -d --name mern-microservices-frontend -p 3000:80 securelooper/mern-microservices-frontend
```
**Base URL:** `http://localhost:3000`
![mern Frontend live](/images/mern-frontend-live.png)


### ☸️ Steps to Deploy an Application on Kubernetes
#### 📄 2 Create Deployment
**File:** `k8s/frontend/deployment.yaml`
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
    tier: frontend
    environment: production
  namespace: mern-microservice
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
        environment: production
    spec:
      restartPolicy: Always
      containers:
      - name: mern-microservices-frontend
        image: securelooper/mern-microservices-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 80
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 60
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 40
          periodSeconds: 5
```

📌 **Apply Deployment**
```bash
kubectl apply -f k8s/frontend/deployment.yaml
```
🔍 **Verify Pods**
```bash
kubectl get pods -n mern-microservice
```
📜 **View Logs to Confirm Communication**
```
kubectl logs deploy/frontend -n mern-microservice
```
OR
```
kubectl logs pod/<pod_name> -n mern-microservice
```
![Frontend Deploy](/images/frontend-deploy-log.png)

![Frontend Deploy](/images/node-ui.png)

#### 📄 3 Create Service
**File:** `k8s/frontend/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: mern-microservice
  labels:
    app: frontend
    tier: frontend
    environment: production
spec:
  selector:
    app: frontend
  ports:
  - port: 3000
    targetPort: 80
  type: LoadBalancer
```

📌 **Apply Service**
```bash
kubectl apply -f k8s/frontend/service.yaml
```
🔍 **Verify Service**
```bash
kubectl get svc -n mern-microservice
```
![Frontend Service](/images/service-ui.png)
#### 🧪 4 Test with Port Forwarding (For localhost)
```bash
kubectl port-forward service/backend -n=mern-microservice 3000:80 --address=0.0.0.0
```
🌍 Access the service in your browser or tool like Postman:
run it
```bash
http://localhost:3000
```
### 🚀 Helm Deployment Guide for MERN Microservices

#### 📦 Check releases
```bash
helm list -n mern-microservice
```
![AKS Cluster Helm List](/images/helm-list.png)

***

#### 👋 Hello Service deploy
```bash
helm upgrade --install mern-microservice-hello helm/hello \
  -f helm/hello/values.yaml \
  --namespace mern-microservice \
  --create-namespace
```
- Uses upgrade --install for idempotent rollout **:repeat:**
- Namespace auto-created with --create-namespace **:factory:**

***

### 🧩 Profile Service deploy
```bash
helm upgrade --install mern-microservice-profile helm/profile \
  -f helm/profile/values.yaml \
  --namespace mern-microservice \
  --create-namespace
```
- Values overridden via -f values.yaml **:memo:**
- Consistent release naming for easy helm list **:label:**

***

### 🖥️ Frontend Service deploy
```bash
helm upgrade --install mern-microservice-frontend helm/frontend \
  -f helm/frontend/values.yaml \
  --namespace mern-microservice \
  --create-namespace
```

***

### **🌍 Production App Live:**
![AKS ](/images/production-live.png)

---
## 📜 Project Information

### 📄 License Details
This project is released under the MIT License, granting you the freedom to:
- 🔓 Use in commercial projects
- 🔄 Modify and redistribute
- 📚 Use as educational material

## 📞 Contact

📧 Email: [Email Me](securelooper@gmail.com
)
🔗 LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/sagar-93-patel)  
🐙 GitHub: [GitHub Profile](https://github.com/psagar-dev)  

---

<div align="center">
  <p>Built with ❤️ by Sagar Patel</p>
</div>