import redis
from app.core.config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

class CartService:
    @staticmethod
    def add_to_cart(user_id: int, dish_id: int, quantity: int):
        cart_key = f"cart:{user_id}"
        r.hincrby(cart_key, dish_id, quantity)

    @staticmethod
    def get_cart(user_id: int) -> dict:
        cart_key = f"cart:{user_id}"
        return {k.decode(): v.decode() for k, v in r.hgetall(cart_key).items()}

    @staticmethod
    def clear_cart(user_id: int):
        cart_key = f"cart:{user_id}"
        r.delete(cart_key)