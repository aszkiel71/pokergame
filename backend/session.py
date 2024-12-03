import uuid
import time

from user import User
from game import PokerGame


class PokerSession:
    def __init__(self, logged_user, number_of_hands, users):
        self.game_id = self.generate_game_id()  # id gry, ktore jest generowane
        self.logged_user = logged_user
        self.number_of_hands = number_of_hands
        self.users = users  # lista userów
        self.start_time = time.strftime("%Y-%m-%d %H:%M:%S")  # data rozpoczecia gry
        self.winners = None  # gracze ktorzy cos zarobili albo wyszli na zero
        self.losers = None  # gracze ktorzy stracili
        self.profit_and_loss_balance = None # bilans updatów do balance
        # Zmienna przechowuję obecny obiekt gry/jednego rozdania
        self.current_game = None
        # Za każdym razem gdy tworzony jest obiekt session odpala się ta funkcja, która zaczyna sesję
        self.start_session()

    # proponuje by profit_and_loss_balance był nwm tabela? słownikiem?
    # niech bedzie co jedno rozdanie aktualizwane
    # np jak gra 'V', 'Geralt', 'Talar' to na poczatku slownik bedzie wygladac tak:
    # profit_and_loss_balance = {
    #       "V" : 0
    #       "Geralt" : 0
    #       "Talar" : 0
    #   }
    # gdy geralt gołodupiec przekurwi po pierwszej rundzie 100, talar zremisuje z V to bedzie wygladac tak:
    #       "V" : 50
    #       "Geralt" : -100
    #       "Talar" : 50
    # itd.
    # na koniec gry np:
    # profit_and_loss_balance = {
    #       "V" : 700
    #       "Geralt" : -1000 (przekurwił dzis ostro)
    #       #Talar" : 300
    #   }
    # wtedy winners = ["V", "Talar"]
    #       losers = "Geralt"
    #       i potem wysylany jest do sessions.json całe info + aktualizacja data.json o balance
    # oczywiscie z balancem botów nic sie nie dzieje. niech grają na nasz koszt darmozjady jebane
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


    def generate_game_id(self):
        return str(uuid.uuid4())  # generuje id

    def display_session_info(self):
        print(f"Game ID: {self.game_id}")
        print(f"Start time: {self.start_time}")
        print(f"Logged in player: {self.logged_user.username}")
        print(f"Number of rounds: {self.num_of_rounds}")
        print("Players in the game:")
        for user in self.users:
            print(f"- {user.username}")

    #zapisywanie info o sesji do sessions.JSON
    def save_session(self):
        session_data = {
            "game_id" : self.game_id,
            "date" : self.start_time,
            "logged_user" : self.logged_user.username,
            "number_of_hands" : self.number_of_hands,
            "players" : self.players,
            "winners" : self.winners,
            "losers" : self.losers,
        }

        with open("sessions.json", "w") as sessions_file:
            pass

    def update_balance(self):
        #profit_and_loss_balance
        with open("data.json", "w") as balance_file:
            pass

    # Funkcja wywołuje rozdanie
    def start_game(self):
        current_game = PokerGame(self.users)

    def start_session(self):
        while True:
            self.start_game()