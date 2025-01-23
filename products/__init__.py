import concurrent.futures
from collections import defaultdict

class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])


def list_products() -> list[Product]:
    # Fetch all products in one call
    products = dao.list_products()
    return [Product.load(product) for product in products]


def get_product(product_id: int) -> Product:
    # Fetch product details once from the DAO
    product = dao.get_product(product_id)
    return Product.load(product)


def get_cart(username: str) -> list[Product]:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    # Fetch product ids from cart
    product_ids = []
    for cart_detail in cart_details:
        contents = eval(cart_detail['contents'])  # Should be optimized to avoid eval() for security reasons
        product_ids.extend(contents)

    # Fetch all product details in parallel using a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Fetch multiple products concurrently
        products = list(executor.map(get_product, product_ids))

    return products


def add_product(product: dict):
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)
