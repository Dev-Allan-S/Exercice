class User:
    user_id=1
    def __init__(self, user_name, user_id=None):
        self.user_name=user_name
        self.user_id=User.user_id
        User.user_id+=1


    def __str__(self):
        return f"{self.user_name} {self.user_id}"

    def __repr__(self):
        return self.__str__()

class Users:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def select_user(self, user_name):
        for user in self.users:
            if user.user_name==user_name:
                return user

class Product:
    next_id=1
    def __init__(self, product_name, price, sold=False, product_id=None):
        self.product_name=product_name
        self.price=price
        self.sold=sold
        self.product_id=Product.next_id
        Product.next_id+=1

    def mark_as_sold(self):
        if self.sold==False:
            self.sold=True
            return True
        else:
            return False
    def __str__(self):
        return f"{self.product_name}, {self.price}R$, {self.sold}, {self.product_id}"

    def __repr__(self):
        return self.__str__()

class Marketplace:
    def __init__(self):
        self.storage=[]
        self.sale_completed=[]

    def add_product(self, product):
        self.storage.append(product)

    def select_product(self, select_product):
        for product in self.storage:
            if select_product==product.product_name:
                return product

    def complete_sale(self, product, seller, buyer):
        if product.mark_as_sold():
            finish_sale = Sale(product, seller, buyer)
            print(finish_sale)
            self.sale_completed.append(finish_sale)
        else:
            print(f"Sorry mr.(s) {buyer.user_name} this product is not available")

    def __str__(self):
        return f"{self.storage}"

class Sale:
    def __init__(self, product, seller, buyer):
        self.product=product
        self.seller=seller
        self.buyer=buyer

    def __str__(self):
        return f"{self.product}, {self.seller}, {self.buyer}"

users = Users()
joao=User("joao")
maria=User("maria")
thiago=User("thiago")
users.add_user(joao)
users.add_user(maria)
users.add_user(thiago)
seller=users.select_user("joao")
buyer=users.select_user("maria")
new_buyer=users.select_user("thiago")

pc = Product("Computador", 1500)
marketplace=Marketplace()
marketplace.add_product(pc)
pc=marketplace.select_product("Computador")
marketplace.complete_sale(pc, seller, buyer)
marketplace.complete_sale(pc, seller, new_buyer)
