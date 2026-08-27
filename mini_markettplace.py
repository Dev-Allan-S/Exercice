import json
class User:
    next_id=1
    def __init__(self, user_name, user_active=True, user_id=None):
        self.user_name=user_name
        self.user_active=user_active
        if user_id is not None:
            self.user_id=user_id
        else:
            self.user_id=User.next_id
            User.next_id+=1

    @classmethod
    def load_user(cls, user):
        return cls(user.get("user_name"), user.get("user_active"), user.get("user_id"))

    def prepare_user_data_to_save(self):
        return self.__dict__

    def __str__(self):
        return f"{self.user_name} {self.user_active} {self.user_id}"

    def __repr__(self):
        return self.__str__()

class Users:
    def __init__(self):
        self.users = []
        self.load_users()

    def add_user(self, user):
        self.users.append(user)

    def select_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id==user_id:
                return user

    def load_users(self):
        max_id=0
        try:
            with open("markettplace_data.json", "r") as data:
                users=json.loads(data.read())
                users=users.get("Users")
            for user in users:
                load_user=User.load_user(user)
                if load_user.user_id > max_id:
                    max_id=load_user.user_id
                self.users.append(load_user)
            if max_id > User.next_id:
                User.next_id=max_id+1
        except Exception as error:
            line_number = error.__traceback__.tb_lineno
            print(f"Error message: {error}")
            print(f"Error happened on line: {line_number}")

    def deactivation_user(self, search_user):
        search = self.select_user_by_id(search_user)
        if search:
            if search.user_active==True:
                search.user_active=False
            else:
                print("User already deactivated")
        else:
            print("User not found")

    def list_of_users(self):
        print(self.users)

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

    def prepare_data_product(self):
        return self.__dict__

    def mark_as_sold(self):
        if self.sold==False:
            self.sold=True
            return True
        else:
            return False

    @classmethod
    def load_product(cls, product):
        return cls(product.get("product_name"), product.get("price"), product.get("sold"), product.get("product_id"))
    def __str__(self):
        return f"{self.product_name}, {self.price}R$, {self.sold}, {self.product_id}"

    def __repr__(self):
        return self.__str__()

class Marketplace:
    def __init__(self, users):
        self.storage=[]
        self.users=users
        self.load_storage()
        self.sale_completed=[]

    def add_product(self, product):
        self.storage.append(product)

    def remove_product(self, product):
        search=self.select_product(product)
        if search:
            if search.sold==False:
                self.storage.remove(search)
            else:
                print("This product is sold, it can't removed")
        else:
            print(f"Product: {product} not found")

    def list_of_products(self):
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
            if seller.user_active and buyer.user_active:
                if product.mark_as_sold():
                    finish_sale = Sale(product, seller, buyer)
                    print(f"The seller: {seller.user_name} sell: {product.product_name} to: {buyer.user_name} by: {product.price}R$")
                    self.sale_completed.append(finish_sale)
                else:
                    print(f"Sorry mr.(s) {buyer.user_name} this product is not available")
            else:
                if seller.user_active == False:
                    print(f"Sorry {seller.user_name} please check you your register")
                elif buyer.user_active == False:
                    print(f"Sorry {buyer.user_name} please check you your register")
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
        return [product.prepare_data_product() for product in self.storage]

    def prepare_user_to_save(self):
        return [user.prepare_user_data_to_save() for user in self.users.users]

    def save_data(self):
        with open("markettplace_data.json", "w") as data:
            data.write(json.dumps({"Product":self.prepare_product_to_save(), "Users":self.prepare_user_to_save()}, indent=4))

    def complete_sale_save(self):
        clear_data=[]
        for item in self.sale_completed:
            item=item.prepare_data_to_save()
            product=item.get("product")
            seller=item.get("seller")
            buyer=item.get("buyer")
            clear_data.append({"Product":product.product_id, "Seller":seller.user_id, "Buyer":buyer.user_id})
        with open("sales_history_new.json", "w") as data:
            data.write(json.dumps({"Sales": clear_data}, indent=4))

    def load_storage(self):
        try:
            max_id=0
            with open("markettplace_data.json", "r") as data:
                storage=(json.loads(data.read()))
                storage=(storage.get("Product"))
                for product in storage:
                    load_product=Product.load_product(product)
                    if load_product.product_id > max_id:
                        max_id=load_product.product_id
                    self.storage.append(load_product)
            if max_id > Product.next_id:
                Product.next_id=max_id+1
        except Exception as error:
            line_number = error.__traceback__.tb_lineno
            print(f"Error message: {error}")
            print(f"Error happened on line: {line_number}")

    def load_history_of_sales(self):
        try:
            with open("sales_history_new.json", "r") as data:
                data=json.loads(data.read())
                for d in data.get("Sales"):
                    load_sale=Sale.load_sales(d, self.users, self.storage)
                    self.sale_completed.append(load_sale)
        except Exception as error:
            line_number = error.__traceback__.tb_lineno
            print(f"Error message: {error}")
            print(f"Error happened on line: {line_number}")

    def __str__(self):
        return f"{self.storage}, {self.sale_completed}"

class Sale:
    def __init__(self, product, seller, buyer):
        self.product=product
        self.seller=seller
        self.buyer=buyer

    def prepare_data_to_save(self):
        return self.__dict__

    @classmethod
    def load_sales(cls,sale, users, storage):
        product=sale.get("Product")
        seller=sale.get("Seller")
        buyer=sale.get("Buyer")
        if users:
            seller=users.select_user_by_id(seller)
            buyer=users.select_user_by_id(buyer)
        for pro in storage:
            if product==pro.product_id:
                return cls(pro, seller, buyer)

    def __str__(self):
        return f"{self.product}, {self.seller}, {self.buyer}"

    def __repr__(self):
        return self.__str__()
