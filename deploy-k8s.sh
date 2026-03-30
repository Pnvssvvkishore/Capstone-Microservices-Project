#!/bin/bash
# Script to deploy the microservices stack to Kubernetes

echo "Creating Kubernetes components..."
kubectl apply -f kubernetes.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres --timeout=120s
kubectl wait --for=condition=ready pod -l app=redis --timeout=60s
kubectl wait --for=condition=ready pod -l app=rabbitmq --timeout=120s

echo "Postgres, Redis, and RabbitMQ are ready. Waiting for services..."
kubectl wait --for=condition=ready pod -l app=user-service --timeout=120s
kubectl wait --for=condition=ready pod -l app=product-service --timeout=120s
kubectl wait --for=condition=ready pod -l app=order-service --timeout=120s
kubectl wait --for=condition=ready pod -l app=api-gateway --timeout=120s
kubectl wait --for=condition=ready pod -l app=frontend --timeout=120s

echo "Deployment completed!"
echo "Access the frontend via NodePort 30081 (e.g. http://localhost:30081 if using Minikube)."
