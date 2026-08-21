import json

class User:
    next_id=1
    def __init__(self, user_name, user_id=None):
        self.user_name=user_name
        if user_id is not None:
            self.user_id=user_id
        else:
            self.user_id=User.next_id
            User.next_id+=1

    @classmethod
    def load_user(cls, user):
        max_id=0
        temp_users=[]
        for u in user:
            load_user=cls(u["user_name"], u["user_id"])
            if u["user_id"]>max_id:
                max_id=u["user_id"]
            temp_users.append(load_user)
        User.next_id=max_id+1
        return temp_users
    def __str__(self):
        return f"{self.user_name} {self.user_id}"

    def __repr__(self):
        return self.__str__()

class Users:
    def __init__(self):
        self.users = []
        self.load_users()

    def add_user(self, user):
        self.users.append(user)

    def list_of_users(self):
        print(self.users)

    def select_user(self, user_name):
        for user in self.users:
            if user.user_name==user_name:
                return user


    def select_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id==user_id:
                return user

    def load_users(self):
        with open("markettplace_data.json", "r") as data:
            users=json.loads(data.read())
        users=User.load_user(users.get("Users"))
        for user in users:
            self.users.append(user)

    def __str__(self):
        return f"{self.users}"

    def __repr__(self):
        return self.__str__()

class Product:
    next_id=1
    def __init__(self, product_name, price, sold=False, product_id=None):
        self.product_name=product_name
        self.price=price
        self.sold=sold
        if product_id is not None:
            self.product_id=product_id
        else:
            self.product_id=Product.next_id
            Product.next_id+=1

    def mark_as_sold(self):
        if self.sold==False:
            self.sold=True
            return True
        else:
            return False

    @classmethod
    def load_product(cls, products):
        temp_data=[]
        max_id=0
        for product in products:
            load_product=cls(product["product_name"], product["price"], product["sold"], product["product_id"])
            if product["product_id"] > max_id:
                max_id=product["product_id"]
            temp_data.append(load_product)
        Product.next_id=max_id+1
        return temp_data
    def __str__(self):
        return f"{self.product_name}, {self.price}R$, {self.sold}, {self.product_id}"

    def __repr__(self):
        return self.__str__()

class Marketplace:
    def __init__(self, users=None):
        self.storage=[]
        self.users=users
        self.load_storage()
        self.sale_completed=[]

    def add_product(self, product):
        self.storage.append(product)

    def marketplace_products(self):
        print(self.storage)
    def select_product(self, select_product):
        for product in self.storage:
            if select_product==product.product_name:
                return product

    def select_product_by_id(self, product_id):
        for product in self.storage:
            if product_id==product.product_id:
                return product

    def complete_sale(self, product, seller, buyer):
    
        if product and seller and buyer:
            if product.mark_as_sold():
                finish_sale = Sale(product, seller, buyer)
                self.sale_completed.append(finish_sale)
            else:
                print(f"Sorry mr.(s) {buyer.user_name} this product is not available")
        else:
            if not product:
                print("Product not found")
            elif not seller:
                print("seller not found")
            elif not buyer:
                print("buyer not found")

    def list_of_salers(self):
        if self.sale_completed:
            print(self.sale_completed)
        else:
            print("No sales to display")


    def prepare_product_to_save(self):
        temp_data=[]
        for product in self.storage:
            data=product.__dict__
            temp_data.append(data)
        return temp_data

    def prepare_user_to_save(self):
        temp_data=[]
        users=self.users
        for user in users.users:
            data=user.__dict__
            temp_data.append(data)
        return temp_data

    def save_data(self):
        with open("markettplace_data.json", "w") as data:
            data.write(json.dumps({"Product":self.prepare_product_to_save(), "Users":self.prepare_user_to_save()}, indent=4))

    def complete_sale_save(self):
        temp_data = []
        clear_data = []
        for item in self.sale_completed:
            temp_data.append(item.__dict__)
        for item in temp_data:
            clear_data.append({"Product":item.get("product").__dict__, "Seller":item.get("seller").__dict__, "Buyer":item.get("buyer").__dict__})
        with open("sales_history.json", "w") as data:
            data.write(json.dumps({"Sellers": clear_data}, indent=4))
        print(clear_data)

    def load_storage(self):
        with open("markettplace_data.json", "r") as data:
            storage=(json.loads(data.read()))
            storage=Product.load_product(storage.get("Product"))
        for product in storage:
            self.storage.append(product)

    def load_hostory_of_sales(self):
        with open("sales_history.json", "r") as data:
            data=json.loads(data.read())
            data=data.get("Sellers")
            load_sale=Sale.load_sales(data, self.users, self.storage)
            for sale in load_sale:
                self.sale_completed.append(sale)

    def __str__(self):
        return f"{self.storage}, {self.save_history}, {self.sale_completed}"

class Sale:
    def __init__(self, product, seller, buyer):
        self.product=product
        self.seller=seller
        self.buyer=buyer

    @classmethod
    def load_sales(cls,sales, users, storage):
        temp_data=[]
        for sale in sales:
            seller=sale.get("Seller")
            seller=seller.get("user_id")
            buyer=sale.get("Buyer")
            buyer=buyer.get("user_id")
            if users:
                seller=users.select_user_by_id(seller)
                buyer=users.select_user_by_id(buyer)
            product=sale.get("Product")
            product=product.get("product_id")
            for pro in storage:
                if pro.product_id==product:
                    product=pro
            temp_data.append(cls(product, seller, buyer))
        return temp_data

    def __str__(self):
        return f"{self.product}, {self.seller}, {self.buyer}"

    def __repr__(self):
        return self.__str__()

users = Users()
ana=User("ana")
seller=users.select_user("maria")
users.add_user(ana)
marketplace=Marketplace(users)
monitor=Product("Monitor", 2000)
marketplace.add_product(monitor)
marketplace.load_hostory_of_sales()
marketplace.list_of_salers()
