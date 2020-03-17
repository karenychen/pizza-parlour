class Drink:
    """ A drink in pizza parlour order.

    === Attributes ===
    name: name of the drink
    price: price of the drink
    """
    name: str
    price: float

    def __init__(self, name: str):
        """Precondition: name is one of coke, diet coke, coke zero, pepsi, diet pepsi, dr.pepper, water, juice"""
        self.name = name
        if name == 'water':
            self.price = 1.00
        elif name == 'juice':
            self.price = 2.00
        else:
            self.price = 3.00