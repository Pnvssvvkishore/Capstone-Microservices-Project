# E-Commerce Sentiment System - Implementation Plan (Updated)

This document outlines the systematic steps required to implement the remaining phases of the project: Functional Features (Sentiment Analysis), Architectural Enhancements, Production Readiness, and Kubernetes Migration.

## Phase 1: Functional Features (Sentiment Analysis) ✅
**Goal:** Build the core review and sentiment analysis engines missing from the original project scope.

*   [x] **Step 1:** Scaffold the `review-service` (Flask, PostgreSQL DB) to handle CRUD operations for product reviews. 
*   [x] **Step 2:** Scaffold the `sentiment-service` (Flask, using TextBlob) to assign Positive/Neutral/Negative scores to text.
*   [x] **Step 3:** Update the API Gateway to route to these new services.
*   [x] **Step 4:** Integrate the Frontend (Shopy UI) to display reviews, allow submission, and show the sentiment rating.
*   [x] **Step 5:** Update `docker-compose.yml` and Prometheus configs to scrape the new services.

## Phase 2: Architecture & Performance Enhancements ⚡
**Goal:** Introduce enterprise patterns (Caching, Async Messaging) to decouple services and improve speed.

*   [x] **Step 6:** Implement a **Redis Cache** in the `product-service` to speed up fetching the product catalog.
*   [x] **Step 7:** Deploy a **RabbitMQ** broker via Docker Compose.
*   [x] **Step 8:** Refactor the `order-service` -> `notification-service` communication from synchronous HTTP to asynchronous message events via RabbitMQ.
*   [x] **Step 9:** Add Retry / Circuit Breaker logic (Tenacity) to API Gateway service communications.

## Phase 3: Production Readiness & Security 🔒
**Goal:** Secure the application against unauthorized access and API abuse.

*   [x] **Step 10:** Implement **JWT Authentication** in the `user-service`.
*   [x] **Step 11:** Implement Gateway auth middleware to validate JWT tokens on protected routes.
*   [x] **Step 12:** Implement basic API **Rate Limiting** at the Gateway level using Redis.

## Phase 4: Kubernetes Migration ☸️
**Goal:** Migrate orchestration from Docker Compose to a production-ready Kubernetes setup.

*   [x] **Step 13:** Write Kubernetes Deployment and Service manifests (`kubernetes.yaml`) for all microservices, databases, and RabbitMQ.
*   [x] **Step 14:** Write an Ingress manifest for routing traffic (integrated into `kubernetes.yaml`).
*   [x] **Step 15:** Provide a deployment script (`deploy-k8s.ps1`) to build and spin up the cluster.

---
## Next Steps:
1.  **Validation:** Run the `deploy-k8s.ps1` script to verify the full cluster deployment.
2.  **Health Checks:** Implement explicit `/health` endpoints in all services for K8s Liveness/Readiness probes.
3.  **Documentation:** Finalize the project README with K8s instructions.
