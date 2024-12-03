from hand import Hand
import time


class Player():

    def __init__(self,username, balance, email, password, phone_number, game, is_bot=False):
        self.username = username
        self.balance = balance
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.is_bot = is_bot
        self.hole_cards = []
        self.current_bet = 0
        self.is_active = True
        self.game = game
        self.hand = None

    def __repr__(self):
        return self.username

    def reset_bet(self):
        self.current_bet = 0

    def reset_activity(self):
        self.is_active = True

    def get_available_actions(self):
        available_actions = ["fold"]

        if self.current_bet == self.game.current_bet:
            available_actions.append("check")

        if self.balance >= (self.game.current_bet - self.current_bet) and self.current_bet != self.game.current_bet:
            available_actions.append("call")

        if self.balance > self.game.current_bet:  # gdy moze raise
            available_actions.append("raise")

        if not self.is_bot:
            print(", ".join(available_actions))

        return available_actions

    def fold_action(self):
        print(f"{self.username} passes.")
        time.sleep(1.5)
        self.is_active = False  # wyłącza nas z gry

    def check_action(self):
        print(f"{self.username} checks.")
        time.sleep(1.5)
        return

    def call_action(self):
        call_amount = self.game.current_bet - self.current_bet
        self.balance -= call_amount
        self.current_bet += call_amount
        self.game.pot += call_amount
        print(f"{self.username} calls, adding {call_amount} to the pot.")
        time.sleep(1.5)
        return

    def raise_action(self):
        while True:
            raise_amount = input(f"How much do you want to raise? (minimum: {self.game.current_bet + 1}): ")
            if raise_amount.isnumeric():
                raise_amount = int(raise_amount)
                self.balance -= raise_amount
                self.current_bet += raise_amount
                self.game.pot += raise_amount
                self.game.current_bet = raise_amount
                print(f"{self.username} raises to {raise_amount}.")
                time.sleep(1.5)
                break

            else:
                print(f"Invalid raise amount.")