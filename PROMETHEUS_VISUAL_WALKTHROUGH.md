# 📊 Prometheus Visual Walkthrough - Step by Step

This guide shows you EXACTLY what you'll see at each step when using Prometheus.

---

## 🎬 Step 1: Open Prometheus Homepage

**What to do:** Open browser and go to `http://localhost:9090`

**What you'll see:**

```
╔══════════════════════════════════════════════════════════════════╗
║ 🔥 Prometheus                                           [Alerts] ║
║                                              [Graph] [Status] [Help]
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Expression (press Shift+Enter for newlines)                    ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │                                                             │ ║
║  │  (click here to type your query)                           │ ║
║  │                                                             │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  [ Execute ]                                    ⏱ 5m 15m 1h 3h  ║
║                                                                  ║
║  [ Console ] [ Graph ]                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │                                                             │ ║
║  │           (results will appear here after Execute)          │ ║
║  │                                                             │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

**Key elements:**
- Top navigation: Alerts, Graph, Status, Help
- Large text box for typing queries
- Blue "Execute" button
- Two tabs: Console and Graph
- Time range selector on the right (5m, 15m, 1h, 3h)

---

## 🎬 Step 2: Check Service Status

**What to do:** 
1. Click **"Status"** at the top
2. Click **"Targets"** from dropdown

**What you'll see:**

```
╔══════════════════════════════════════════════════════════════════╗
║ 🔥 Prometheus                    [Alerts] [Graph] [Status ▼] [Help]
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  📊 Targets                                                      ║
║                                                                  ║
║  gateway (1/1 up)                                               ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Endpoint: http://gateway:5000/metrics                       │ ║
║  │ State: ✅ UP                                                 │ ║
║  │ Labels: job="gateway"                                       │ ║
║  │ Last Scrape: 2.145s ago                                     │ ║
║  │ Scrape Duration: 0.008s                                     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  user-service (1/1 up)                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Endpoint: http://user-service:5001/metrics                  │ ║
║  │ State: ✅ UP                                                 │ ║
║  │ Labels: job="user-service"                                  │ ║
║  │ Last Scrape: 1.892s ago                                     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  product-service (1/1 up)                                       ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Endpoint: http://product-service:5002/metrics               │ ║
║  │ State: ✅ UP                                                 │ ║
║  │ Labels: job="product-service"                               │ ║
║  │ Last Scrape: 3.021s ago                                     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  order-service (1/1 up)                                         ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Endpoint: http://order-service:5003/metrics                 │ ║
║  │ State: ✅ UP                                                 │ ║
║  │ Labels: job="order-service"                                 │ ║
║  │ Last Scrape: 1.456s ago                                     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  notification-service (1/1 up)                                  ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Endpoint: http://notification-service:5004/metrics          │ ║
║  │ State: ✅ UP                                                 │ ║
║  │ Labels: job="notification-service"                          │ ║
║  │ Last Scrape: 2.781s ago                                     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

**What this means:**
- ✅ **UP** = Service is running perfectly
- ❌ **DOWN** = Service has a problem
- All 5 services should show "UP"
- "Last Scrape" shows when Prometheus last checked

---

## 🎬 Step 3: Run First Query - Check Services

**What to do:**
1. Click **"Graph"** at the top
2. Click in the text box
3. Type: `up`
4. Click blue **"Execute"** button

**What you'll see (Console Tab):**

```
╔══════════════════════════════════════════════════════════════════╗
║ 🔥 Prometheus                           [Alerts] [Graph] [Status] [Help]
╠══════════════════════════════════════════════════════════════════╣
║  Expression (press Shift+Enter for newlines)                    ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ up                                                          │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  [ Execute ]                                    ⏱ 5m 15m 1h 3h  ║
║                                                                  ║
║  [●Console ] [ Graph ]                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Element                                            Value    │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ up{instance="gateway:5000",                                │ ║
║  │    job="gateway"}                                    1     │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ up{instance="user-service:5001",                           │ ║
║  │    job="user-service"}                               1     │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ up{instance="product-service:5002",                        │ ║
║  │    job="product-service"}                            1     │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ up{instance="order-service:5003",                          │ ║
║  │    job="order-service"}                              1     │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ up{instance="notification-service:5004",                   │ ║
║  │    job="notification-service"}                       1     │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  5 elements found                                               ║
╚══════════════════════════════════════════════════════════════════╝
```

**What the numbers mean:**
- **Value = 1** → Service is UP ✅
- **Value = 0** → Service is DOWN ❌

---

## 🎬 Step 4: View as Graph

**What to do:** Click the **"Graph"** tab (next to Console)

**What you'll see:**

```
╔══════════════════════════════════════════════════════════════════╗
║ 🔥 Prometheus                           [Alerts] [Graph] [Status] [Help]
╠══════════════════════════════════════════════════════════════════╣
║  Expression                                                      ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ up                                                          │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║  [ Execute ]                                    ⏱ 5m 15m 1h 3h  ║
║                                                                  ║
║  [ Console ] [●Graph ]                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ 1.0 ┼─────────────────────────────────────────────────────│ ║
║  │     │█████████████████████████████████████████████████████│ ║
║  │     │█████████████████████████████████████████████████████│ ║
║  │     │█████████████████████████████████████████████████████│ ║
║  │     │█████████████████████████████████████████████████████│ ║
║  │     │█████████████████████████████████████████████████████│ ║
║  │ 0.5 ┼                                                      │ ║
║  │     │                                                      │ ║
║  │     │                                                      │ ║
║  │     │                                                      │ ║
║  │ 0.0 ┼─────────────────────────────────────────────────────│ ║
║  │     09:40    09:42    09:44    09:46    09:48    09:50    │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  Legend:                                                        ║
║  ▬ up{job="gateway"}                                            ║
║  ▬ up{job="user-service"}                                       ║
║  ▬ up{job="product-service"}                                    ║
║  ▬ up{job="order-service"}                                      ║
║  ▬ up{job="notification-service"}                               ║
╚══════════════════════════════════════════════════════════════════╝
```

**What this shows:**
- All lines are flat at **1.0** = All services running perfectly
- If a line drops to 0, that service went down at that time
- X-axis = Time
- Y-axis = 0 (down) or 1 (up)

---

## 🎬 Step 5: Check Request Counts

**What to do:**
1. Click in text box, select all (Ctrl+A)
2. Type: `http_requests_total`
3. Click **"Execute"**

**What you'll see (Console Tab):**

```
╔══════════════════════════════════════════════════════════════════╗
║ Expression                                                       ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ http_requests_total                                         │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║  [ Execute ]                                    ⏱ 5m 15m 1h 3h  ║
║                                                                  ║
║  [●Console ] [ Graph ]                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ Element                                            Value    │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ http_requests_total{                                       │ ║
║  │   endpoint="/health",                                      │ ║
║  │   job="gateway",                                           │ ║
║  │   method="GET"}                                       45   │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ http_requests_total{                                       │ ║
║  │   endpoint="/products",                                    │ ║
║  │   job="gateway",                                           │ ║
║  │   method="GET"}                                       23   │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ http_requests_total{                                       │ ║
║  │   endpoint="/users",                                       │ ║
║  │   job="gateway",                                           │ ║
║  │   method="GET"}                                       17   │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ http_requests_total{                                       │ ║
║  │   endpoint="/register",                                    │ ║
║  │   job="user-service",                                      │ ║
║  │   method="POST"}                                       8   │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ http_requests_total{                                       │ ║
║  │   endpoint="/login",                                       │ ║
║  │   job="user-service",                                      │ ║
║  │   method="POST"}                                       5   │ ║
║  ├────────────────────────────────────────────────────────────┤ ║
║  │ http_requests_total{                                       │ ║
║  │   endpoint="/orders",                                      │ ║
║  │   job="order-service",                                     │ ║
║  │   method="POST"}                                       3   │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  ... and 12 more elements                                       ║
╚══════════════════════════════════════════════════════════════════╝
```

**What the numbers mean:**
- **/health has 45** = The health endpoint was called 45 times
- **/products has 23** = Products page loaded 23 times
- **These numbers increase** every time someone uses the app

---

## 🎬 Step 6: View Requests as Graph

**What to do:** Click the **"Graph"** tab

**What you'll see:**

```
╔══════════════════════════════════════════════════════════════════╗
║  [ Console ] [●Graph ]                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ 50  ┼                                                  ╱─  │ ║
║  │     │                                            ╱────╯    │ ║
║  │     │                                      ╱────╯          │ ║
║  │ 40  ┼                                ╱────╯                │ ║
║  │     │                          ╱────╯                      │ ║
║  │     │                    ╱────╯  ████████  /products      │ ║
║  │ 30  ┼              ╱────╯       ♦♦♦♦♦♦♦♦♦  /users         │ ║
║  │     │        ╱────╯            ▲▲▲▲▲▲▲▲▲▲  /register     │ ║
║  │     │  ╱────╯                  ▼▼▼▼▼▼▼▼▼▼  /login        │ ║
║  │ 20  ┼─╯                        ○○○○○○○○○○  /orders       │ ║
║  │     │                                                      │ ║
║  │ 10  ┼                                                      │ ║
║  │     │                                                      │ ║
║  │  0  ┼────────────────────────────────────────────────     │ ║
║  │     09:40   09:42   09:44   09:46   09:48   09:50        │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  Legend (click to hide/show):                                  ║
║  ▬ /health (gateway) - Blue                                    ║
║  ▬ /products (gateway) - Green                                 ║
║  ▬ /users (gateway) - Orange                                   ║
║  ▬ /register (user-service) - Red                              ║
║  ▬ /login (user-service) - Purple                              ║
║  ▬ /orders (order-service) - Cyan                              ║
╚══════════════════════════════════════════════════════════════════╝
```

**What this shows:**
- Each **colored line** = Different endpoint
- Lines going **up** = More requests over time
- **Steeper lines** = Frequently used endpoints
- **Flatter lines** = Rarely used endpoints
- You can click legend items to hide/show specific lines

---

## 🎬 Step 7: Advanced Query - Request Rate

**What to do:**
1. Clear text box
2. Type: `rate(http_requests_total[5m])`
3. Click Execute
4. Click Graph tab

**What you'll see:**

```
╔══════════════════════════════════════════════════════════════════╗
║  Expression                                                      ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ rate(http_requests_total[5m])                               │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  [ Console ] [●Graph ]                                          ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │  5  ┼                                    ╱╲                │ ║
║  │     │                                  ╱╯  ╲╮              │ ║
║  │  4  ┼                                ╱      ╲              │ ║
║  │     │                              ╱╯        ╲╮            │ ║
║  │  3  ┼                            ╱            ╲            │ ║
║  │     │                          ╱╯              ╲╮          │ ║
║  │  2  ┼                        ╱                  ╲          │ ║
║  │     │                      ╱╯                    ╲╮        │ ║
║  │  1  ┼────────────────────╯                        ╲───────│ ║
║  │     │                                                      │ ║
║  │  0  ┼──────────────────────────────────────────────────   │ ║
║  │     09:40   09:42   09:44   09:46   09:48   09:50        │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  Y-axis: Requests per second                                   ║
║  Peak at 09:47 = 4.2 requests/second                           ║
╚══════════════════════════════════════════════════════════════════╝
```

**What this shows:**
- **Requests per second** instead of total count
- Peak shows when the app was busiest
- Useful for finding traffic patterns

---

## 📋 Quick Reference Card

### Common Queries You Should Try:

| Query | What It Shows |
|-------|---------------|
| `up` | Which services are running (1=up, 0=down) |
| `http_requests_total` | Total requests each endpoint received |
| `rate(http_requests_total[5m])` | Requests per second (last 5 mins) |
| `http_request_duration_seconds` | How long requests take |
| `up{job="gateway"}` | Just check the gateway service |
| `count(up == 1)` | How many services are up |

### Time Range Controls:
- **5m** = Last 5 minutes
- **15m** = Last 15 minutes
- **1h** = Last hour
- **3h** = Last 3 hours
- Click **+** to zoom in (less time)
- Click **-** to zoom out (more time)

### Two View Modes:
- **Console Tab**: Table with exact numbers
- **Graph Tab**: Line chart showing trends

---

## ✅ Testing Checklist

After following this guide, you should understand:
- [ ] How to navigate to Prometheus (localhost:9090)
- [ ] Where to check if services are UP (Status → Targets)
- [ ] How to type a query in the expression box
- [ ] How to click Execute to run a query
- [ ] Difference between Console and Graph views
- [ ] What the `up` query shows
- [ ] What `http_requests_total` shows
- [ ] How to read the graphs (lines going up = more activity)
- [ ] How to change time ranges

---

## 🎯 Practice Exercise

1. Start your application: `docker-compose up --build`
2. Open Prometheus: http://localhost:9090
3. Run query: `up` → All should be 1
4. Open your frontend: http://localhost:8081
5. Click around the website (view products, etc.)
6. Go back to Prometheus
7. Run query: `http_requests_total`
8. Click Execute again - **numbers should be higher!**
9. Switch to Graph tab - see the lines going up!

**Congratulations!** You now know how to use Prometheus! 🎉

---

## Need Help?

If you see:
- **All services DOWN** → Wait 30 seconds after starting docker-compose
- **No data** → Make sure to use the frontend/API to generate traffic first
- **"No datapoints found"** → Check if the query name is spelled correctly

For more help, ask me any questions!
