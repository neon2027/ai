
import bcrypt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)

    def remove_from_cart(self, product):
        self.cart.remove(product)

    def get_cart(self):
        return self.cart 
    
    def __str__(self):
        return f'Username: {self.username}, Password: {self.password}'
    
class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f'Name: {self.name}, Price: {self.price}'
    

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with open('users.txt', 'a') as f:
        f.write(f'{username},{hashed_password.decode("utf-8")}\n')

def login_user(username, password):
    with open('users.txt', 'r') as f:
        for line in f:
            stored_user, stored_hashed_password = line.strip().split(',')

            if stored_user == username:
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    return True

    return False

def get_user(username):
    with open('users.txt', 'r') as f:
        for line in f:
            stored_user, stored_hashed_password = line.strip().split(',')
            if stored_user == username:
                return User(stored_user, stored_hashed_password)

    return None

def add_product(name, price):
    with open('products.txt', 'a') as f:
        f.write(f'{name},{price}\n')

def get_products():
    products = []
    with open('products.txt', 'r') as f:
        for line in f:
            name, price = line.strip().split(',')
            products.append(Product(name, price))

    return products

def get_product(name):

    with open('products.txt', 'r') as f:
        for line in f:
            stored_name, stored_price = line.strip().split(',')
            if stored_name == name:
                return Product(stored_name, stored_price)

    return None

def get_cart(username):
    user = get_user(username)
    return user.get_cart()

def add_to_cart(username, product_name):
    user = get_user(username)
    product = get_product(product_name)
    user.add_to_cart(product)

def remove_from_cart(username, product_name):
    user = get_user(username)
    product = get_product(product_name)
    user.remove_from_cart(product)  

def count_cart(username):
    user = get_user(username)
    return len(user.get_cart())

def product_exists(name):
    with open('products.txt', 'r') as f:
        for line in f:
            stored_name, stored_price = line.strip().split(',')
            if stored_name == name:
                return True

    return False  

def main():
    invalid_credentials = False
    invalid_choice = False
    while True:
        print('\033c')
        print('='*20)

        if invalid_credentials:
            print('\033[91m' + 'Invalid credentials' + '\033[0m')

        if invalid_choice:
            print('\033[91m' + 'Invalid choice' + '\033[0m')


        print('1. Register')
        print('2. Login')
        print('3. Exit')

        choice = input('Enter your choice: ')

        if choice == '1':
            username = input('Enter username: ')
            password = input('Enter password: ')
            register_user(username, password)

        elif choice == '2':
            username = input('Enter username: ')
            password = input('Enter password: ')
            if login_user(username, password):
                first_login = True
                while True:
                    print('\033c')
                    print('='*20)
                    if first_login:
                        print('\033[92m' + 'Login Successfully' + '\033[0m')
                        first_login = False

                    print('Welcome to the store')
                    print('1. Add product')
                    print('2. View products')
                    print('3. Add to cart')
                    print('4. View cart')
                    print('5. Remove from cart')
                    print('6. Logout')
                    print('='*20)
                    choice = input('Enter your choice: ')
                
                    if choice == '1':
                        print('\033c')
                        print('='*20)
                        name = input('Enter product name: ')
                        price = input('Enter product price: ')
                        add_product(name, price)

                    elif choice == '2':
                        print('\033c')
                        print('='*20)
                        products = get_products()
                        for product in products:
                            print(product)

                        input('Press any key to continue')

                    elif choice == '3':
                        print('\033c')
                        print('='*20)
                        print('Add to cart')
                        
                        while True:
                            product_name = input('Enter product name: ')
                            
                            if product_exists(product_name):
                                add_to_cart(username, product_name)
                                print('Product added to cart')
                            else:
                                print('Product does not exist. Please enter a valid product name.')

                            choice = input('Do you want to add another product to cart? (y/n): ')
                            if choice.lower() == 'n':
                                break

                        count = count_cart(username)
                        print(f'You have {count} products in your cart')

                        input('Press any key to continue')


                    elif choice == '4':
                        print('\033c')
                        print('='*20)
                        cart = get_cart(username)
                        for product in cart:
                            print(product)

                        if not cart:
                            print('-- Cart is empty --')

                        input('Press any key to continue')

                    elif choice == '5':
                        print('\033c')
                        print('='*20)
                        product_name = input('Enter product name: ')
                        remove_from_cart(username, product_name)

                    elif choice == '6':
                        break

            else:
                invalid_credentials = True
                invalid_choice = False
                print('Login failed')

        elif choice == '3':
            break

        else:
            invalid_choice = True
            invalid_credentials = False
            print('Invalid choice')
    
if __name__ == '__main__':
    main()
