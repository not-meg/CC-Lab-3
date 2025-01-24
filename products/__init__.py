from products import dao

class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod  # Optimization: Changed the load method to a static method for cleaner code and explicit type hinting.
    def load(data: dict) -> 'Product':
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data['qty']
        )

def list_products() -> list[Product]:
    # Optimization: Used list comprehension for conciseness and better readability.
    return [Product.load(product) for product in dao.list_products()]

def get_product(product_id: int) -> Product:
    product_data = dao.get_product(product_id)
    if not product_data:  # Optimization: Added a null check to handle cases where the product might not exist.
        return None  # Return None if the product does not exist
    return Product.load(product_data)

def add_product(product: dict):
    dao.add_product(product)

def update_qty(product_id: int, qty: int):
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)
