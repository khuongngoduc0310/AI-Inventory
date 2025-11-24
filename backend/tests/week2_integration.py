import requests

BASE = "http://localhost:8000"
# Reuse Week-1 token or login again
r = requests.post(f"{BASE}/api/v1/auth/login", data={"username": "test@example.com", "password": "testpass123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Get product ID from Week-1 test
products = requests.get(f"{BASE}/api/v1/inventory/products", headers=headers).json()
product_id = products[0]["id"]

# Forecast
f = requests.get(f"{BASE}/api/v1/inventory/forecast/{product_id}", headers=headers)
assert f.status_code == 200
data = f.json()
assert len(data["predictions"]) == 14
assert "stockout_risk" in data
print("✅ Week-2 forecast works")