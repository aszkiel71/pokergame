# PORADNIK, JAK ODWOŁYWAĆ SIĘ DO DANYCH UŻYTKOWNIKA ZALOGOWANEGO

from user import User

def test():
    if User.logged_user: # warunek konieczny -- uzytkownik zalogowany musi byc
        print(User.logged_user.balance)
        print(User.logged_user.username)
        print(User.logged_user.email)
        print(User.logged_user.phone_number)
    else:
        raise AttributeError("User is not logged in. No kurwa niestety.")
test()  # no tu nam wykurwi ze nie zalogwoany no bo nie zalogowany