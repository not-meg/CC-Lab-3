import json
from typing import List, Optional
from products import Product, get_product
from cart import dao

class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod  # Optimization: Changed the load method to a static method for clarity and included type hinting for better readability.
    def load(data: dict) -> 'Cart':
        # Optimization: The contents are now loaded as a list of Product objects directly using a list comprehension.
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[Product.load(p) for p in data['contents']],
            cost=data['cost']
        )

def get_cart(username: str) -> List[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:  # Optimization: Simplified the null check using `if not`.
        return []

    products_in_cart = []
    for cart_detail in cart_details:
        try:
            # Optimization: Replaced the unsafe `eval` function with `json.loads` for secure and efficient parsing.
            contents = json.loads(cart_detail['contents'])
        except json.JSONDecodeError:
            continue  # Optimization: Added error handling to skip invalid JSON entries.

        for product_id in contents:
            product = get_product(product_id)
            if product:  # Optimization: Added a check to ensure only valid products are appended.
                products_in_cart.append(product)

    return products_in_cart

def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    dao.delete_cart(username)
