# PowerShell script to generate traffic for metrics visualization
Write-Host "🚀 Generating API traffic to populate Prometheus & Grafana..." -ForegroundColor Cyan

$headers = @{ "Content-Type" = "application/json" }
$baseUrl = "http://localhost:5000"

# Wait for services to be ready
Write-Host "⏳ Waiting for API Gateway..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    # 1. Register multiple users
    Write-Host "`n📝 Registering users..." -ForegroundColor Green
    for ($i = 1; $i -le 5; $i++) {
        $body = @{
            name = "User $i"
            email = "user$i@example.com"
            password = "password123"
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Method Post -Uri "$baseUrl/register" -Headers $headers -Body $body -ErrorAction SilentlyContinue
            Write-Host "  ✓ Registered: User $i" -ForegroundColor Gray
        } catch {
            Write-Host "  ℹ User $i already exists (expected)" -ForegroundColor DarkGray
        }
    }

    # 2. Login multiple times
    Write-Host "`n🔑 Performing logins..." -ForegroundColor Green
    for ($i = 1; $i -le 5; $i++) {
        $body = @{
            email = "user$i@example.com"
            password = "password123"
        } | ConvertTo-Json
        
        try {
            Invoke-RestMethod -Method Post -Uri "$baseUrl/login" -Headers $headers -Body $body -ErrorAction SilentlyContinue | Out-Null
            Write-Host "  ✓ Login: User $i" -ForegroundColor Gray
        } catch {
            Write-Host "  ✗ Login failed for User $i" -ForegroundColor Red
        }
    }

    # 3. Create products
    Write-Host "`n📦 Creating products..." -ForegroundColor Green
    $products = @(
        @{ name = "Laptop"; price = 1200.00 },
        @{ name = "Mouse"; price = 25.00 },
        @{ name = "Keyboard"; price = 75.00 },
        @{ name = "Monitor"; price = 300.00 }
    )

    foreach ($product in $products) {
        $body = $product | ConvertTo-Json
        try {
            Invoke-RestMethod -Method Post -Uri "$baseUrl/products" -Headers $headers -Body $body -ErrorAction SilentlyContinue | Out-Null
            Write-Host "  ✓ Created: $($product.name)" -ForegroundColor Gray
        } catch {
            Write-Host "  ℹ Product $($product.name) may already exist" -ForegroundColor DarkGray
        }
    }

    # 4. Get products multiple times
    Write-Host "`n🔍 Fetching products..." -ForegroundColor Green
    for ($i = 1; $i -le 10; $i++) {
        Invoke-RestMethod -Method Get -Uri "$baseUrl/products" -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  ✓ Fetch #$i" -ForegroundColor Gray
    }

    # 5. Create orders
    Write-Host "`n🛒 Creating orders..." -ForegroundColor Green
    for ($i = 1; $i -le 5; $i++) {
        $body = @{
            user_id = $i
            product_id = ($i % 4) + 1
        } | ConvertTo-Json
        
        try {
            Invoke-RestMethod -Method Post -Uri "$baseUrl/orders" -Headers $headers -Body $body -ErrorAction SilentlyContinue | Out-Null
            Write-Host "  ✓ Order created for User $i" -ForegroundColor Gray
        } catch {
            Write-Host "  ✗ Order failed for User $i" -ForegroundColor Red
        }
    }

    # 6. Check notifications
    Write-Host "`n📬 Checking notifications..." -ForegroundColor Green
    for ($i = 1; $i -le 3; $i++) {
        Invoke-RestMethod -Method Get -Uri "$baseUrl/notifications" -ErrorAction SilentlyContinue | Out-Null
        Write-Host "  ✓ Notification check #$i" -ForegroundColor Gray
    }

    Write-Host "`n✅ Traffic generation complete!" -ForegroundColor Green
    Write-Host "📊 Now check your dashboards:" -ForegroundColor Cyan
    Write-Host "   • Prometheus: http://localhost:9090" -ForegroundColor White
    Write-Host "   • Grafana: http://localhost:3000" -ForegroundColor White
    Write-Host "`n💡 Tip: Refresh Grafana dashboard to see the new metrics!" -ForegroundColor Yellow

} catch {
    Write-Host "`n❌ Error: $_" -ForegroundColor Red
    Write-Host "💡 Make sure services are running: docker-compose ps" -ForegroundColor Yellow
}
