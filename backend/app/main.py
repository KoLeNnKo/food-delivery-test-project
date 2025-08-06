from fastapi import FastAPI
from app.api.v1 import auth, restaurants, cart, orders, couriers, users

app = FastAPI()
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(restaurants.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
app.include_router(couriers.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1/users")