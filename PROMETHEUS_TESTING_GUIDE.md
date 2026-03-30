# 📊 Prometheus Testing Guide - Simple Steps

## Prerequisites
Make sure your application is running first:
```bash
docker-compose up --build
```
Wait until you see messages like "Running on http://0.0.0.0:5000" for all services.

---

## Step-by-Step Guide

### **STEP 1: Open Prometheus in Browser**

1. Open your web browser (Chrome, Edge, Firefox - any browser)
2. Type this in the address bar:
   ```
   http://localhost:9090
   ```
3. Press **Enter**

**What you'll see:**
- Prometheus homepage with a search box at the top
- Navigation menu: Alerts, Graph, Status, Help

---

### **STEP 2: Check if Services are Running**

1. Click on **"Status"** in the top menu
2. Click on **"Targets"** from the dropdown

**What you'll see:**
A table showing all your microservices with their status:

```
Endpoint                          State    Labels                    Last Scrape
http://gateway:5000/metrics       UP       job="gateway"            2s ago
http://user-service:5001/metrics  UP       job="user-service"       3s ago
http://product-service:5002/...   UP       job="product-service"    2s ago
http://order-service:5003/...     UP       job="order-service"      1s ago
http://notification-service:...   UP       job="notification-..."   2s ago
```

✅ **If all show "UP" = Everything is working!**
❌ **If any show "DOWN" = That service has a problem**

---

### **STEP 3: Run Some Queries (Check Metrics)**

#### 3A. Go to the Graph Page

1. Click **"Graph"** in the top menu
2. You'll see:
   - A text box with placeholder "Expression (press Shift+Enter for newlines)"
   - Two tabs: **Console** and **Graph**
   - An **"Execute"** button

---

#### 3B. Query #1 - Check Which Services Are Running

1. Click in the text box
2. Type exactly:
   ```
   up
   ```
3. Click the blue **"Execute"** button

**What you'll see (Console tab):**
```
Element                                            Value
up{instance="gateway:5000", job="gateway"}         1
up{instance="user-service:5001", ...}              1
up{instance="product-service:5002", ...}           1
up{instance="order-service:5003", ...}             1
up{instance="notification-service:5004", ...}      1
```

- **Value 1 = Service is UP** ✅
- **Value 0 = Service is DOWN** ❌

**To see as a graph:**
1. Click the **"Graph"** tab (next to Console)
2. You'll see a line graph with values over time

---

#### 3C. Query #2 - Check How Many Requests Each Service Received

1. **Clear the text box** (delete "up")
2. Type exactly:
   ```
   http_requests_total
   ```
3. Click **"Execute"**

**What you'll see:**
```
Element                                                      Value
http_requests_total{endpoint="/health", job="gateway", ...} 15
http_requests_total{endpoint="/products", job="gateway"...} 8
http_requests_total{endpoint="/users", job="user-servi...}  5
...
```

This shows:
- How many times each endpoint was called
- The number keeps increasing as you use the application

---

#### 3D. Query #3 - See Request Activity Rate

1. Clear the text box
2. Type exactly:
   ```
   rate(http_requests_total[5m])
   ```
3. Click **"Execute"**
4. Click the **"Graph"** tab

**What you'll see:**
- A line graph showing requests per second
- If you're actively using the app, the line goes up
- If no one is using it, the line is flat at 0

---

### **STEP 4: Test in Real-Time**

#### Make Some Traffic:

**Option A: Use the Frontend**
1. Open http://localhost:8081 in another browser tab
2. Click around (view products, login page, etc.)
3. Go back to Prometheus
4. Run the query again: `http_requests_total`
5. Click **Execute** - the numbers should be higher!

**Option B: Use Verification Script**
1. Open a new terminal/command prompt
2. Go to your project folder:
   ```bash
   cd d:\cproject\microservices-project
   ```
3. Run:
   ```bash
   python verify_deployment.py
   ```
4. Go back to Prometheus and run: `http_requests_total`
5. The numbers should increase!

---

## 🎯 Quick Reference - Best Queries to Try

| What You Want to Check | Query to Type | Expected Output |
|------------------------|---------------|-----------------|
| Are services running? | `up` | All should show `1` |
| Total requests received | `http_requests_total` | Numbers (increases over time) |
| Requests in last 5 mins | `rate(http_requests_total[5m])` | Requests per second |
| Response time | `http_request_duration_seconds` | Time in seconds |
| Only check gateway | `up{job="gateway"}` | `1` if gateway is up |

---

## 🔍 Understanding the Output

### Console Tab vs Graph Tab

**Console Tab:**
- Shows exact numbers in a table
- Good for seeing current values
- Example: "Service has received 25 requests"

**Graph Tab:**
- Shows trends over time as a line chart
- Good for seeing patterns
- Example: "Requests are increasing at 2 per second"

### Time Range Selector

At the top right, you'll see time controls:
- Click **`-`** to zoom out (see more time)
- Click **`+`** to zoom in (see less time)
- Select duration: `5m`, `15m`, `1h`, `3h`, etc.

---

## ✅ Success Checklist

After following these steps, you should be able to:
- [ ] Open Prometheus (http://localhost:9090)
- [ ] See all 5 services as "UP" in Status → Targets
- [ ] Run the query `up` and see all values = 1
- [ ] Run `http_requests_total` and see request counts
- [ ] Generate traffic and see numbers increase
- [ ] Switch between Console and Graph views

---

## 🆘 Troubleshooting

**Problem: Can't access http://localhost:9090**
- Solution: Make sure `docker-compose up --build` is running

**Problem: All services show "DOWN"**
- Solution: Wait 30 seconds after starting docker-compose, then refresh the page

**Problem: No data in graphs**
- Solution: Generate some traffic first by opening http://localhost:8081 or running `python verify_deployment.py`

**Problem: Query shows "No data"**
- Solution: Check if metric name is spelled correctly (case-sensitive!)

---

## 📸 What You Should See (Text Representation)

### Prometheus Homepage:
```
┌─────────────────────────────────────────────────┐
│  Prometheus                                      │
│  [Alerts] [Graph] [Status] [Help]               │
├─────────────────────────────────────────────────┤
│                                                  │
│  Expression (press Shift+Enter for newlines)    │
│  ┌───────────────────────────────────────────┐  │
│  │ up                                         │  │
│  └───────────────────────────────────────────┘  │
│  [Execute]                                       │
│                                                  │
│  [Console] [Graph]                              │
│  ┌───────────────────────────────────────────┐  │
│  │ up{instance="gateway:5000", ...}      1   │  │
│  │ up{instance="user-service:5001", ...} 1   │  │
│  │ up{instance="product-service:...}     1   │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## Next Steps

Once you're comfortable with Prometheus:
1. Try setting up **Grafana** for prettier dashboards (http://localhost:3000)
2. Create custom queries for your specific needs
3. Set up alerts for when services go down

Need help with any step? Just ask!
