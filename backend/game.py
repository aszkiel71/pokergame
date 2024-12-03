from backend.hand_selector import HandSelector
from player import Player
from deck import Deck
import random
import time

# Działanie programu.
# -> Program dostaje nastepujace informacje ile botów wczytuje gra (my przyjmujemy, ze 4)
# Nastepnie program wywoluje etapy gry:
# 1) Small Blind (pierwszy gracz od rozdajacego)
# 2) Big Blind (drugi gracz od rozdajacego)
# 3) Nastepuje rozdanie kart
# 4) Pierwsza runda licytacji (AKCJE: CALL, CHECK, RAISE, PASS, ALL IN)
# 5) FLOP
# 6) Druga runda licytacji (AKCJE: ... )
# 7) TURN
# 8) Trzecia runda licytacji (AKCJE : ... )
# 9) RIVER
# 10) Czwarta runda licytacji
# 11) Showdown
# 12) Podział puli


class PokerGame:

    def __init__(self, users=None):
        self.deck = Deck()
        self.players = self.get_players()
        self.community_cards = []
        self.pot = 0  # initial pot
        self.current_bet = 0  # current bet
        self.dealer_index = None  # remember dealer index
        self.game_phase = "pre-flop"
        self.game()

    # Przeniosłem pobieranie graczy do osobnego pliku, ponieważ obiekt player musi być połączony z obiektem game, więc player jest tworzony dopiero po utworzeniu gry
    # Nie robi to problemu bo player jest tworzony na potrzeby konkretnej gry na podstawie obiektu user
    def get_players(self):
        return [
            Player("V", 1000, "v@v.com", 123456, 739, self),
            Player("VernonRoche", 1000, "wolna@temeria.tm", 1209321, 3201, self, True),
            Player("Takemura", 1000, "jebac@arasake.com", 129321, 2500, self, True),
            Player("Geralt", 1000, "kaedwen@kaermorhen.blaviken", 892101, 3021, self, True)
            ]

    def table(self):
        print("Players at the table:")
        for player in self.players:
            print(player.username)
        self.dealer_index = random.randint(0, len(self.players) - 1) # losuje dealer'a
        dealer = self.players[self.dealer_index]
        print(f"Starting with player: {dealer.username}")

    def deal_cards(self):   # rozdawanie kart
        random.shuffle(self.deck.deck)
        for player in self.players:
            player.hole_cards = [self.deck.deck.pop(), self.deck.deck.pop()]
        print(f"Your cards: {self.players[0].hole_cards}")

    def smallBlind(self):
        small_blind_index = (self.dealer_index + 1) % len(self.players)  # kolejny gracz od dealer'a jest dealerem  ( % przez liczbe graczy by index nie wyszedl poza liczbe graczy
        small_blind_player = self.players[small_blind_index]

        if small_blind_player.username == "V":   # tutaj zakladamy, ze my sterujemy 'V'. Potem to bedzie trzeba zmienic na logged.username
            while True:
                sb_amount = int(input("How much do you want to bet for Small Blind (1-50): "))
                if sb_amount > 0:
                    break
                else:
                    print("You should enter at least 1.")
        else:
            sb_amount = random.randint(1, 50)   # bot losuje stawke
            print(f"{small_blind_player.username} goes in for Small Blind: {sb_amount}")

        self.pot += sb_amount                   # stawka rosnie o small blind
        self.current_bet = sb_amount            # aktualny bet = small blind
        small_blind_player.balance -= sb_amount # odejmuje balance o kwote zakladu
        print(f"Current pot: {self.pot}")

    def bigBlind(self):   # analogiczne do small blind
        big_blind_index = (self.dealer_index + 2) % len(self.players)  # kolejny gracz po small blindzie
        big_blind_player = self.players[big_blind_index]

        if big_blind_player.username == "V":  # my sterujemy tylko 'V'
            while True:
                bb_amount = int(input(f"How much do you want to bet for Big Blind (more than {self.current_bet}): "))
                if bb_amount > self.current_bet:  # sprawdza czy wchodizmy za wiecej niz jest bet
                    break
                else:
                    print("Your bet cannot be lower than current bet")

        else:
            bb_amount = random.randint(51, 75)
            print(f"{big_blind_player.username} goes in for Big Blind: {bb_amount}")

        self.pot += bb_amount
        self.current_bet = bb_amount
        big_blind_player.balance -= bb_amount
        print(f"Current pot: {self.pot}")

    def flop(self):
        self.game_phase = "flop"
        print("\n==== FLOP ====")
        for _ in range(3):
            card = self.deck.deck.pop()
            self.community_cards.append(card)
        print(f"Community cards: {self.community_cards}")

    def turn(self):
        self.game_phase = "turn"
        print("\n==== TURN ====")
        card = self.deck.deck.pop()
        self.community_cards.append(card)
        print(f"Community cards: {self.community_cards}")

    def river(self):
        self.game_phase = "river"
        print("\n==== RIVER ====")
        card = self.deck.deck.pop()
        self.community_cards.append(card)
        print(f"Community cards: {self.community_cards}")

    def negotiation(self, player):
        # jezeli gracz not is_active, to go pomijamy przy negocjacjach
        if not player.is_active:
            return

        if player.username == "V":  # Sterowanie tylko 'V' (potem trzeba to zamienic na logged_user.username na dalszym etapie
            while True:
                print(f"Current pot: {self.pot}, Your balance: {player.balance}")
                print(f"Choose your action. Available actions: ", end="")

                # get_available_actions() przy okazji printuje od razu (tylko dla gracza) więc nie trzeba ręcznie tego robić
                available_actions = player.get_available_actions()

                action = input("Choose an action : ").lower()

                if action == "fold":
                    player.fold_action()
                    break
                elif action == "check" and "check" in available_actions:   # warunek na check
                    player.check_action()
                    break
                elif action == "call" and "call" in available_actions:
                    player.call_action()
                    break
                elif action == "raise" and "raise" in available_actions:
                    player.raise_action()
                    break
                else:
                    print("This option is not available.")
                    time.sleep(1.5)

        ## tu logika dla bota
        else:
            print(f"{player.username}'s turn (bot).")
            time.sleep(1.5)

            available_actions = player.get_available_actions()

            # na potrzebe symulacji ustalilem losowo akcje bota
            # nie podpinalem tego do niczego bo jest to mocno "hardkorowa" wersja + nie potrafie tego zrobic na szybko

            if "check" not in available_actions and "raise" in available_actions and "call" in available_actions:  # gdy nie mozemy check
                action_probabilities = {"pass": 0.3, "call": 0.4, "raise": 0.3}

            if "check" in available_actions and "call" not in available_actions and "raise" not in available_actions:
                action_probabilities = {"check": 1.0, "pass": 0.0, "call": 0.0, "raise": 0.0}

            if player.balance < self.current_bet and "check" not in available_actions:  # gdy mozemy tylko pass
                action_probabilities = {"pass": 1.0}

    # Funkcja zwraca wygrywającą rękę tzn. najsilniejszą ręke przy kartach w grze
    # Dodatkowo funkcja generuje rękę każdego gracza (tj. atrybut player.hand)
    def get_winning_hand(self):
        hands = []
        for player in self.players:
            player.hand = HandSelector(self.community_cards, player.hole_cards).select_best_hand()
            hands.append(player.hand)

        hands.sort()

        return hands[-1]

    # Funkcja zwraca tablice zawierającą graczy którzy wygrali (o długości 1 jeżeli wygrał jeden gracz lub więcej w przypadku remisu)
    def get_winner(self, winning_hand):
        winners = []
        for player in self.players:
            if player.hand == winning_hand:
                winners.append(player)

        return winners

    # Funkcja przekazuje pieniądze userowi (nie playerowi)
    def transfer_to_user(self, player):
        pass

    # Funkcja dzieląca pot pomiędzy zwycięzcami
    def split_pot(self, winners):
        prize = self.pot//len(winners)

        for winner in winners:
            self.transfer_to_user(winner)

        pass

    # Na koniec rozdania
    def showdown(self):

        winning_hand = self.get_winning_hand()
        winners = self.get_winner(winning_hand)

        print("Game is over")

        for player in self.players:
            time.sleep(1.5)
            print(f"{player.username}'s hole cards: {player.hole_cards}")
            print(f"{player.username}'s hand: {player.hand}")

        if len(winners) > 1:
            print(f"Game ended with a draw! Players {', '.join(winners)} won!")
            self.split_pot(winners)
        else:
            print(f"Player {winners[0]} won!")
            self.transfer_to_user(winners[0])

    # w play_round trzeba zmienic jedna rzecz
    # negocjacje nie dzialaja w prawidlowy sposob
    # tzn.
    # np jak gra czterech graczy
    # A : check
    # B : check
    # C : raise
    # D : call
    # tu konczy sie kolejka, a powinno pojsc jeszcze 'jedna' tura az do tego co 'raise'
    # czyli potem D, A, B, C
    # DOPOKI AZ KAZDY GRACZ NIE ZAGRA check albo pass
    # Jezeli chodzi o ALL-IN to tego w ogole nie robilem na razie
    # Na razie boty (stan na 21.09.2024 na 16:05) nie podejmują w ogóle decyzji

    def play_round(self, starting_index):
        for i in range(len(self.players)):
            current_player = self.players[(starting_index + i) % len(self.players)]   # wyznaczamy aktualnego gracza
            self.negotiation(current_player)

    def game(self):
        self.get_players()

        self.table()
        time.sleep(2)

        # Small Blind and Big Blind
        self.smallBlind()
        time.sleep(2)
        self.bigBlind()
        time.sleep(2)

        # Deal cards
        self.deal_cards()
        time.sleep(2)

        # Pierwsza faza negocjacji
        starting_index = (self.dealer_index + 3) % len(self.players)
        self.play_round(starting_index)
        time.sleep(2)

        # Flop
        self.flop()
        time.sleep(2)

        # Druga faza negocjacji.
        starting_index = (self.dealer_index + 1) % len(self.players)
        self.play_round(starting_index)
        time.sleep(2)

        # Turn
        self.turn()
        time.sleep(2)

        # Trzecia faza negocjacji
        self.play_round(starting_index)
        time.sleep(2)

        # River
        self.river()
        time.sleep(2)

        # Czwarta faza negocjacji
        self.play_round(starting_index)
        time.sleep(2)

        # Showdown
        print("\n === Showdown ===")
        print(f"Community cards: {self.community_cards}")
        time.sleep(2)
        self.showdown()

game = PokerGame()

