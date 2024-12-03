# import UI
import json
import time
#from deck import Deck
#from game import PokerGame


class UserNotFound(Exception):
    def __init__(self, username):
        super().__init__(f"User {username} not found.")
        self.username = username


class User:

    taken_usernames = set()   # przechowuje zajete nazwy uzytkownikow
    logged_user = None ## aktualnie zalogowany uzytkownik. potrzebne przy odnoszeniu sie do niego

    def __init__(self, username, balance, email, password, phone_number):
        self.username = username
        self.phone_number = phone_number
        self.balance = balance
        self.email = email
        self.password = password

    @classmethod
    def load_taken_usernames(cls):     # wczytywanie taken_usernames z 'data.txt'
        with open("data.json", "r") as file:
            data = json.load(file)
            users = data.get("users", [])
            for user in users:
                cls.taken_usernames.add(user["username"])


    @classmethod
    def is_available_username(cls, username):
        if username in cls.taken_usernames:
            return False
        return True   # wiadomo. jak w nazwie. sprawdza czy nazwa jest dostepna (jak dostepna to zwraca True)



    @classmethod
    def main(cls):   # Główna metoda, która sie uruchamia za kazdym razem
        cls.load_taken_usernames()
        while True:
            print("Available actions : \n1. Login\n2. Register\n3. Forgot Password (doesn't work obv)")
            decision = input("What would you like to do? :  ")
            print('\n')
            if decision == "1":
                cls.login()
                break
            elif decision == "2":
                cls.register()
                break
            elif decision == "3":
                print("Currently, it doesn't work ;( \n")
            elif decision == "niger":
                cls.admin_panel()

    @classmethod
    def login(cls):
        cls.load_taken_usernames()  # wczytuje zajete nazwy uzytkownika
        # logowanie
        while True:
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            user_found = False   # przełącznik, czy znaleziono uzytkowniak

            with open("data.json", "r") as file:
                data = json.load(file)
                users = data.get("users", [])

                for user in users:
                    if user["username"] == username:   # poszukiwanie w JSON'ie czy jest taki username
                        user_found = True
                        if user["password"] == password:
                            print("Login successful")
                            cls.logged_user = cls(
                                username=user["username"],
                                balance=user["balance"],
                                email=user["email"],
                                password=user["password"],
                                phone_number=user["phone_number"]
                            )
                            cls.options()  # Przekierowanie do opcji po zalogowaniu
                            return
                        else:
                            print("Invalid password. Please try again.")
                            break

            if not user_found:
                print("Invalid username. Please try again.")


    @classmethod
    def register(cls):   # metoda pozwalajca na rejestracja (z reszta wiadomo -- Register)
        cls.load_taken_usernames()  # ładuje zajete usernames

        while True:
            username = input("Enter your username: ")
            if not cls.is_available_username(username):   # JEZELI ZAJETE
                print("Sorry, that username is already taken.")
            else:
                break   #JEŻELI NIE ZAJETE TO WYCHODZI Z WHILE I PYTA O PASSWORD

        while True:
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")
            if password != confirm_password:
                print("Sorry, your passwords don't match. Try again.")  # gdy hasla sie nie zgadza
            else:
                break    # JEZELI WSZYSTKO SIE ZGADZA WYCHODZI Z WHILE. Nastepnie wypytuje o reszte informacji (nr tel, mail)

        while True:
            phone_number = input("Enter your phone number: ")
            if phone_number.isdigit() == False:
                print("Sorry, your phone number must contain only digits.") # error gdy blad w numerze
            else:
                break   # JEZELI WSZYSTKO SIE ZGADZA WYCHODZI Z WHILE. Potem pyta o mail'a.

        while True:
            email = input("Enter your email: ")
            if '@' not in email: #brak '@' error
                print("Sorry, you must enter a valid email address.") # error gdy blad w mail'u
            else:
                break  # gdy wszystko sie zgadza tworzy konto. Registeration succesful

        new_user = {
            "username": username,
            "password": password,
            "email": email,
            "phone_number": phone_number,
            "balance": 500
        }
        #default balance to 500$. Tworzy nowego uzytkownika ktory ma wlasne dane

        with open("data.json", "r+") as file:
            data = json.load(file) #wczytywanie danych z JSON
            users = data.get("users", []) #pobieramy z JSON'a z klucza "users" (jeżeli nie istnieje to po przeicnku zwraca pustą liste)
            users.append(new_user) #
            data["users"] = users
            file.seek(0)  # tak sie robi by program dopisywal juz istniejacego klucza ''users'' a nie kurwa tworzyl nowa na koncu pliku (wkurwiajace jest potem naprawianie tego reczne)
            json.dump(data, file, indent=4)  #zapisujemy do JSON'a. Ident = ilosc spacji. Technicznie nie potrzebne ale dla oka dobre

        print("Registration succesful. Try to log in.") # komunikat #
        cls.login()

    @classmethod
    def get_logged_user_data(cls):
        if cls.logged_user:
            print(f"Your username : {cls.logged_user.username}")
            print(f"Your balance: {cls.logged_user.balance}")
            print(f"Email: {cls.logged_user.email}")
            print(f"Phone number: {cls.logged_user.phone_number}")
        else:
            print("No user currently logged in")



    @classmethod
    def get_user_data(cls, username):
        with open("data.json", "r") as file:
            data = json.load(file)
            users = data.get("users", [])

            for user in users:
                if user["username"] == username:
                    return {
                        "username": user["username"],
                        "balance": user["balance"],
                        "email": user["email"],
                        "phone_number": user["phone_number"]
                    }
        raise UserNotFound(username)

    @classmethod
    def admin_panel(cls):
        password = input("Enter admin password : ")
        while True:
            if password == "talar":
                print("Welcome in admin panel\nAvailable options:\n1. Find user\n2. Users list")
                opt = input("Select an option : ")

                if opt == "1":  # FIND USER
                    username = input("Enter username: ")
                    try:
                        user_data = cls.get_user_data(username)
                        print("User found:")
                        print(f"Username: {user_data['username']}")
                        print(f"Balance: {user_data['balance']}")
                        print(f"Email: {user_data['email']}")
                        print(f"Phone number: {user_data['phone_number']}")
                        print("\n")
                        while True:
                            ask = input("Do you want to change user data?\n1. Yes\n2. No\nOpt : ")
                            if ask == "1":
                                print("Which field do you want to change?")
                                print("1. Username")
                                print("2. Password")
                                print("3. Email")
                                print('4. Phone number')
                                print("5. Balance")
                                field_opt = input("Select an option : ")
                                if field_opt == "1":
                                 #   cls.load_taken_usernames()
                                    new_username = input("Enter new username: ")
                                    if cls.is_available_username(new_username):
                                        user_data["username"] = new_username  # zmiana username
                                        print("User changed successfully")
                                    else:
                                        print("Sorry, that username is already taken.")

                                elif field_opt == "2":
                                    new_password = input("Enter new password: ")
                                    user_data["password"] = new_password
                                    print("Password changed successfully")

                                elif field_opt == "3":
                                    while True:
                                        new_email = input("Enter new email: ")
                                        if '@' in new_email:
                                            user_data["email"] = new_email
                                            print("Email changed successfully")
                                            break
                                        else:
                                            print("Sorry, you must enter a valid email address.")

                                elif field_opt == "4":
                                    while True:
                                        new_phone_number = input("Enter new phone number: ")
                                        if new_phone_number.isdigit() == True:
                                            user_data["phone_number"] = new_phone_number
                                            print("Phone number changed successfully")
                                            break
                                        else:
                                            print("Sorry, you must enter a valid phone number. (Only digits are allowed)")


                                elif field_opt == "5":
                                    while True:
                                        new_balance = input("Enter new balance: ")
                                        if new_balance.isdigit():
                                            user_data["balance"] = int(new_balance)
                                            print("Balance changed successfully")
                                            break
                                        else:
                                            print("Sorry, that balance must be an integer.")

                                # updateowanie w JSON'IE:
                                with open("data.json", "r+") as file:
                                    data = json.load(file)
                                    for user in data["users"]:  # iterowanie w 'slowniku' z JSON
                                        if user["username"] == username:
                                            user.update(user_data)  # .update() -> aktualizuje dane
                                            break

                                    file.seek(0)
                                    json.dump(data, file, indent=4)
                                    file.truncate()  # usuwa wszystkie stare informacje
                            elif ask == "2":
                                break
                            else:
                                print("Invalid option. Please try again.")
                    except UserNotFound as e:
                        print(e)
                elif opt == "2":  # USERS LIST
                    with open("data.json", "r") as file:
                        data = json.load(file)
                        users = data.get("users", [])
                        print("List of users:")
                        for user in users:
                            print(user["username"])
                else:
                    print("Invalid option. Please try again.")

    @classmethod
    def options(cls):                   ### metoda pokazuje dostepne opcja
        if cls.logged_user:
            print(f"Hello, {cls.logged_user.username}. Your current balance is {cls.logged_user.balance}.")
            while True:
                print(f"Available actions: ")
                print(f"1. Training with bots")
                print(f"2. Find lobby")
                print(f"3. Rules")
                print(f"4. Poker hands")
                print(f"5. Credits")
                print(f"6. My data")
                print(f"7. Past games")
                opt = input("What would you like to do? : ")
                if opt == "1":
                    time.sleep(1)
                    while True:
                        number_of_hands = input("How many hands would you like to play? : ")
                        if number_of_hands.isdigit():
                            number_of_hands = int(number_of_hands)
                            break

                    #players = [
                        #Player(cls.logged_user.username, cls.logged_user.balance, cls.logged_user.email, cls.logged_user.phone_number)
                        #Player("VenonRoche" .. .. . . . .)
                        #
                #  ]

                    break
                if opt == "2":
                    for i in range(3):
                        print("Searching for a game")
                        time.sleep(0.5)
                        print("Searching for a game . ")
                        time.sleep(0.5)
                        print("Searching for a game . .")
                        time.sleep(0.5)
                        print("Searching for a game . . .")
                        time.sleep(1.5)
                    print("No game found ...")
                    break
                if opt == "6":
                    cls.get_logged_user_data()
                else:
                    print("Available actions : ")
                    print(f"1. Training with bots")
                    print(f"2. Find lobby")
                    print(f"3. Rules")
                    print(f"4. Poker hands")
                    print(f"5. Credits")
                    print(f"6. My data")
                    print(f"7. Past games")