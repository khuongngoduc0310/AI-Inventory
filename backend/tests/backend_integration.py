"""
Week-1 smoke tests
------------------
1. Health check
2. User registration
3. Login → obtain JWT
4. Access protected route (create + list products)
5. Token rejection when JWT missing/invalid
"""

import requests
import json
from random import randint

BASE = "http://localhost:8000"

EMAIL = f"test{randint(0, 9999)}@week1.com"
PASSWORD = "s3cret"

# ---------- 1. Health ----------
r = requests.get(f"{BASE}/health")
assert r.status_code == 200, "Health failed"
print("✅ Health check")

# ---------- 2. Registration ----------
reg = requests.post(
    f"{BASE}/api/v1/auth/register",
    json={"username": "week1_user", "email": EMAIL, "password": PASSWORD},
)
assert reg.status_code == 201, f"Register failed: {reg.text}"
user = reg.json()
print("✅ Registered user", user["id"])

# ---------- 3. Login ----------
login = requests.post(
    f"{BASE}/api/v1/auth/login",
    data={"username": EMAIL, "password": PASSWORD},  # OAuth2 form
)
assert login.status_code == 200, f"Login failed: {login.text}"
token = login.json()["access_token"]
print("✅ JWT received")

# ---------- 4. Protected route ----------
headers = {"Authorization": f"Bearer {token}"}
product_in = {"name": "Week1 Mouse", "sku": f"MOUSE-{randint(0, 9999)}", "stock_quantity": 25, "price": 29.99}

create = requests.post(f"{BASE}/api/v1/inventory/products", json=product_in, headers=headers)
assert create.status_code == 200, f"Create product failed: {create.text}"
prod = create.json()
print("✅ Created product", prod["id"])

list_p = requests.get(f"{BASE}/api/v1/inventory/products", headers=headers)
assert list_p.status_code == 200 and len(list_p.json()) >= 1
print("✅ Listed products")

# ---------- 5. Unauthorized access ----------
no_token = requests.get(f"{BASE}/api/v1/inventory/products")
assert no_token.status_code == 403, "Should reject missing token"
bad_header = requests.get(f"{BASE}/api/v1/inventory/products", headers={"Authorization": "Bearer invalid"})
assert bad_header.status_code == 401, "Should reject bad token"
print("✅ Auth rejection works")

print("\n🎉 Week-1 tests passed!")