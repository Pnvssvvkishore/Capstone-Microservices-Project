# ==============================================================
# deploy-k8s.ps1  -  Deploy microservices stack to Kubernetes
# ==============================================================

$ErrorActionPreference = "Continue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Microservices K8s Deployment Script" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Step 1: Build images
Write-Host "`n[1/4] Building Docker images..." -ForegroundColor Yellow
$services = @("api-gateway","user-service","product-service","order-service","notification-service","review-service","sentiment-service","frontend")

foreach ($svc in $services) {
    $imageName = "microservices-project-$svc"
    Write-Host "  Building $imageName..." -ForegroundColor Gray
    docker build -t "$imageName:latest" "./$svc"
}

# Step 2: Minikube Load
$isMinikube = $false
try {
    $status = minikube status --format '{{.Host}}'
    if ($status -eq "Running") { $isMinikube = $true }
} catch { }

if ($isMinikube) {
    Write-Host "`n[2/4] Loading images into Minikube..." -ForegroundColor Yellow
    foreach ($svc in $services) {
        minikube image load "microservices-project-$svc:latest"
    }
} else {
    Write-Host "`n[2/4] Skipping Minikube load (not detected/running)." -ForegroundColor Gray
}

# Step 3: Apply
Write-Host "`n[3/4] Applying Kubernetes manifests..." -ForegroundColor Yellow
kubectl apply -f kubernetes.yaml

# Step 4: Wait
Write-Host "`n[4/4] Waiting for pods..." -ForegroundColor Yellow
$apps = @("postgres","redis","rabbitmq","user-service","product-service","order-service","notification-service","review-service","sentiment-service","api-gateway","frontend")
foreach ($app in $apps) {
    Write-Host "  Waiting for $app..." -ForegroundColor Gray
    kubectl wait --for=condition=ready pod -l "app=$app" --timeout=60s
}

Write-Host "`nDeployment Complete!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:30081" -ForegroundColor White
