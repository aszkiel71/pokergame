import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'backend')))  # GPT KAZAŁ TO DODAĆ BO MI SIĘ WYKURWIAŁ PROGRAM (COS W STYLU NO MODULE ''HAND'' FOUND)
import unittest
from backend.hand import Hand
from backend.card import Card
from backend.deck import Deck


class TestHandCardValue(unittest.TestCase):

    def test_high_card(self):
        cards = [Card("Hearts", 2), Card("Diamonds", 4), Card("Spades", 7), Card("Hearts", "J"), Card("Clubs", 9)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "high card")

    def test_pair(self):
        cards = [Card("Hearts", 2), Card("Diamonds", 5), Card("Clubs", 7), Card("Hearts", "J"), Card("Diamonds", 2)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "pair")

    def test_two_pairs(self):
        cards = [Card("Hearts", 2), Card("Spades", 5), Card("Diamonds", 2), Card("Clubs", 5), Card("Hearts", "J")]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "two pairs")

    def test_three_of_a_kind(self):
        cards = [Card("Hearts", 2), Card("Diamonds", 2), Card("Clubs", 5), Card("Spades", 2), Card("Hearts", "J")]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "three of a kind")

    def test_straight(self):
        cards = [Card("Hearts", 8), Card("Spades", 6), Card("Clubs", 7), Card("Diamonds", 9), Card("Hearts", 5)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "straight")

    def test_flush(self):
        cards = [Card("Hearts", 7), Card("Hearts", 2), Card("Hearts", 4), Card("Hearts", "J"), Card("Hearts", 9)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "flush")

    def test_full_house(self):
        cards = [Card("Hearts", 2), Card("Clubs", 5), Card("Diamonds", 2), Card("Spades", 5), Card("Hearts", 2)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "full house")

    def test_four_of_a_kind(self):
        cards = [Card("Hearts", 2), Card("Clubs", 5), Card("Diamonds", 2), Card("Spades", 2), Card("Hearts", 2)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "four of a kind")

    def test_straight_flush(self):
        cards = [Card("Hearts", 7), Card("Hearts", 9), Card("Hearts", 5), Card("Hearts", 6), Card("Hearts", 8)]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "straight flush")

    def test_royal_flush(self):
        cards = [Card("Hearts", "J"), Card("Hearts", 10), Card("Hearts", "Q"), Card("Hearts", "A"), Card("Hearts", "K")]
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), "royal flush")

    def test_get_values(self):
        cards = [Card("Hearts", 2), Card("Hearts", 4), Card("Hearts", 7), Card("Hearts", 9), Card("Hearts", "J")]
        hand = Hand(cards)
        self.assertEqual(hand.get_values(), [2, 4, 7, 9, "J"])

    def test_get_suits(self):
        cards = [Card("Hearts", 2), Card("Diamonds", 2), Card("Spades", 2), Card("Clubs", 2), Card("Hearts", 5)]
        hand = Hand(cards)
        self.assertEqual(hand.get_suits(), ["Hearts", "Diamonds", "Spades", "Clubs", "Hearts"])


class TestHandCompareDefault(unittest.TestCase):
    def setUp(self):
        # ROYAL FLUSH -> STR8 FLUSH -> FOUR OF A KIND -> FULL_HOUSE -> STR8 -> THREE OF A KIND -> TWO PAIRS -> PAIR -> HIGH CARD
        self.royal_flush = Hand([
            Card("Hearts", 10),
            Card("Hearts", "J"),
            Card("Hearts", "Q"),
            Card("Hearts", "K"),
            Card("Hearts", "A"),
        ])

        self.straight_flush = Hand([
            Card("Hearts", 3),
            Card("Hearts", 4),
            Card("Hearts", 5),
            Card("Hearts", 6),
            Card("Hearts", 7),
        ])

        self.four_of_a_kind = Hand([
            Card("Hearts", 10),
            Card("Spades", 10),
            Card("Clubs", 10),
            Card("Diamonds", 10),
            Card("Hearts", "A"),
        ])

        self.full_house = Hand([
            Card("Hearts", 10),
            Card("Clubs", 10),
            Card("Hearts", "Q"),
            Card("Diamonds", "Q"),
            Card("Spades", "Q"),
        ])

        self.flush = Hand([
            Card("Hearts", 3),
            Card("Hearts", 5),
            Card("Hearts", 10),
            Card("Hearts", "J"),
            Card("Hearts", "A")]
        )

        self.straight = Hand([
            Card("Clubs", 2),
            Card("Hearts", 3),
            Card("Spades", 4),
            Card("Diamonds", 5),
            Card("Clubs", 6),
        ])

        self.three_of_a_kind = Hand([
            Card("Hearts", 10),
            Card("Spades", 10),
            Card("Diamonds", 10),
            Card("Hearts", "K"),
            Card("Hearts", "A"),
        ])

        self.two_pairs = Hand([
            Card("Hearts", 10),
            Card("Spades", 10),
            Card("Hearts", "Q"),
            Card("Spades", "Q"),
            Card("Diamonds", 2),
        ])

        self.pair = Hand([
            Card("Hearts", 10),
            Card("Spades", 10),
            Card("Hearts", 8),
            Card("Spades", 5),
            Card("Diamonds", 3),
        ])

        self.high_card = Hand([
            Card("Hearts", 10),
            Card("Spades", 3),
            Card("Hearts", 4),
            Card("Spades", 8),
            Card("Diamonds", 9),
        ])

    # 22.30 -> 23.28

    def test_royal_flush_vs_straight_flush(self):
        self.assertTrue(self.royal_flush > self.straight_flush)

    def test_straight_flush_vs_four_of_a_kind(self):
        self.assertTrue(self.straight_flush > self.four_of_a_kind)

    def test_four_of_a_kind_vs_full_house(self):
        self.assertTrue(self.four_of_a_kind > self.full_house)

    def test_full_house_vs_flush(self):
        self.assertTrue(self.full_house > self.flush)

    def test_flush_vs_straight(self):
        self.assertTrue(self.flush > self.straight)

    def test_straight_vs_three_of_a_kind(self):
        self.assertTrue(self.straight > self.three_of_a_kind)

    def test_three_of_a_kind_vs_two_pairs(self):
        self.assertTrue(self.three_of_a_kind > self.two_pairs)

    def test_two_pairs_vs_pair(self):
        self.assertTrue(self.two_pairs > self.pair)

    def test_pair_vs_high_card(self):
        self.assertTrue(self.pair > self.high_card)

    def test_straight_flush_vs_straight_flush(self):
        hand1 = Hand([Card('Hearts', 10), Card('Hearts', 'J'), Card('Hearts', 'Q'), Card('Hearts', 'K'),
                      Card('Hearts', 'A')])  # Ace-high straight flush
        hand2 = Hand([Card('Spades', 9), Card('Spades', 10), Card('Spades', 'J'), Card('Spades', 'Q'),
                      Card('Spades', 'K')])  # King-high straight flush
        hand3 = Hand([Card('Clubs', 10), Card('Clubs', 'J'), Card('Clubs', 'Q'), Card('Clubs', 'K'),
                      Card('Clubs', 'A')])  # Same Ace-high straight flush as hand1

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

    def test_four_of_a_kind_vs_four_of_a_kind(self):
        hand1 = Hand([Card('Hearts', 9), Card('Diamonds', 9), Card('Clubs', 9), Card('Spades', 9),
                      Card('Hearts', 'K')])  # Four nines, king kicker
        hand2 = Hand([Card('Hearts', 8), Card('Diamonds', 8), Card('Clubs', 8), Card('Spades', 8),
                      Card('Hearts', 'A')])  # Four eights, ace kicker
        hand3 = Hand([Card('Hearts', 9), Card('Diamonds', 9), Card('Clubs', 9), Card('Spades', 9),
                      Card('Hearts', 'K')])  # Same hand as hand1
        hand4 = Hand([Card('Hearts', 9), Card('Diamonds', 9), Card('Clubs', 9), Card('Spades', 9),
                      Card('Hearts', 'A')]) # Four nines, ace kicker

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertFalse(hand1 > hand4)
        self.assertTrue(hand1 < hand4)

    def test_full_house_vs_full_house(self):
        hand1 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'K'), Card('Clubs', 'K'), Card('Hearts', 9),
                      Card('Diamonds', 9)])  # Full house, kings over nines
        hand2 = Hand([Card('Hearts', 'Q'), Card('Diamonds', 'Q'), Card('Clubs', 'Q'), Card('Hearts', 10),
                      Card('Diamonds', 10)])  # Full house, queens over tens
        hand3 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'K'), Card('Clubs', 'K'), Card('Spades', 9),
                      Card('Clubs', 9)])  # Same as hand1
        hand4 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'K'), Card('Clubs', 'K'), Card('Hearts', 10),
                      Card('Diamonds', 10)]) # Full house, kings over tens

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertFalse(hand1 > hand4)
        self.assertTrue(hand1 < hand4)

    def test_flush_vs_flush(self):
        hand1 = Hand([Card('Hearts', 2), Card('Hearts', 4), Card('Hearts', 6), Card('Hearts', 8),
                      Card('Hearts', 10)])  # Flush with 10 high then 8
        hand2 = Hand([Card('Spades', 3), Card('Spades', 5), Card('Spades', 7), Card('Spades', 9),
                      Card('Spades', 'J')])  # Flush with jack high
        hand3 = Hand([Card('Diamonds', 2), Card('Diamonds', 4), Card('Diamonds', 6), Card('Diamonds', 8),
                      Card('Diamonds', 10)])  # Same flush as hand1
        hand4 = Hand([Card('Hearts', 2), Card('Hearts', 4), Card('Hearts', 6), Card('Hearts', 9),
                      Card('Hearts', 10)]) # Flush with 10 high then 9

        self.assertTrue(hand2 > hand1)
        self.assertFalse(hand2 < hand1)
        self.assertFalse(hand2 == hand1)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertFalse(hand1 > hand4)
        self.assertTrue(hand1 < hand4)

    def test_straight_vs_straight(self):
        hand1 = Hand([Card('Hearts', 5), Card('Diamonds', 6), Card('Clubs', 7), Card('Spades', 8),
                      Card('Hearts', 9)])  # Straight 9 high
        hand2 = Hand([Card('Hearts', 4), Card('Diamonds', 5), Card('Clubs', 6), Card('Spades', 7),
                      Card('Hearts', 8)])  # Straight 8 high
        hand3 = Hand([Card('Diamonds', 5), Card('Clubs', 6), Card('Spades', 7), Card('Hearts', 8),
                      Card('Diamonds', 9)])  # Same straight as hand1
        hand4 = Hand([Card('Hearts', 5), Card('Diamonds', 4), Card('Clubs', 3), Card('Spades', 2),
                      Card('Hearts', "A")])

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertTrue(hand1 > hand4)
        self.assertFalse(hand1 < hand4)
        self.assertFalse(hand1 == hand4)

    def test_three_of_a_kind_vs_three_of_a_kind(self):
        hand1 = Hand([Card('Hearts', 7), Card('Diamonds', 7), Card('Clubs', 7), Card('Hearts', 10),
                      Card('Diamonds', 'J')])  # Three 7s, jack kicker
        hand2 = Hand([Card('Hearts', 6), Card('Diamonds', 6), Card('Clubs', 6), Card('Hearts', 9),
                      Card('Diamonds', 'Q')])  # Three 6s, queen kicker
        hand3 = Hand([Card('Clubs', 7), Card('Spades', 7), Card('Diamonds', 7), Card('Clubs', 10),
                      Card('Spades', 'J')])  # Same hand as hand1
        hand4 = Hand([Card('Hearts', 7), Card('Diamonds', 7), Card('Clubs', 7), Card('Hearts', 10),
                      Card('Diamonds', 'Q')])  # Three 7s, queen kicker

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertFalse(hand1 > hand4)
        self.assertTrue(hand1 < hand4)

    def test_two_pairs_vs_two_pairs(self):
        hand1 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'K'), Card('Clubs', 10), Card('Spades', 10),
                      Card('Hearts', 3)])  # Two pairs (kings and tens), 3 kicker
        hand2 = Hand([Card('Hearts', 'Q'), Card('Diamonds', 'Q'), Card('Clubs', 9), Card('Spades', 9),
                      Card('Hearts', 2)])  # Two pairs (queens and nines), 2 kicker
        hand3 = Hand([Card('Clubs', 'K'), Card('Spades', 'K'), Card('Diamonds', 10), Card('Hearts', 10),
                      Card('Diamonds', 3)])  # Same hand as hand1
        hand4 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'K'), Card('Clubs', 10), Card('Spades', 10),
                      Card('Hearts', 2)])  # Two pairs (kings and tens), 2 kicker

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertTrue(hand1 > hand4)
        self.assertFalse(hand1 < hand4)

    def test_pair_vs_pair(self):
        hand1 = Hand([Card('Hearts', 'J'), Card('Diamonds', 'J'), Card('Clubs', 9), Card('Spades', 8),
                      Card('Hearts', 2)])  # Pair of jacks last 2
        hand2 = Hand([Card('Hearts', 10), Card('Diamonds', 10), Card('Clubs', 7), Card('Spades', 6),
                      Card('Hearts', 3)])  # Pair of tens
        hand3 = Hand([Card('Clubs', 'J'), Card('Spades', 'J'), Card('Hearts', 9), Card('Diamonds', 8),
                      Card('Clubs', 2)])  # Same hand as hand1
        hand4 = Hand([Card('Hearts', 'J'), Card('Diamonds', 'J'), Card('Clubs', 9), Card('Spades', 8),
                      Card('Hearts', 3)])  # Pair of jacks last 3

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertFalse(hand1 > hand4)
        self.assertTrue(hand1 < hand4)

    def test_high_card_vs_high_card(self):
        hand1 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'J'), Card('Clubs', 9), Card('Spades', 8),
                      Card('Hearts', 7)])  # King-high
        hand2 = Hand([Card('Hearts', 'Q'), Card('Diamonds', 10), Card('Clubs', 9), Card('Spades', 8),
                      Card('Hearts', 7)])  # Queen-high
        hand3 = Hand([Card('Diamonds', 'K'), Card('Spades', 'J'), Card('Clubs', 9), Card('Hearts', 8),
                      Card('Diamonds', 7)])  # Same hand as hand1
        hand4 = Hand([Card('Hearts', 'K'), Card('Diamonds', 'Q'), Card('Clubs', 9), Card('Spades', 8),
                      Card('Hearts', 7)])  # King-high then Q

        self.assertTrue(hand1 > hand2)
        self.assertFalse(hand1 < hand2)
        self.assertFalse(hand1 == hand2)

        self.assertTrue(hand1 == hand3)
        self.assertFalse(hand1 > hand3)
        self.assertFalse(hand1 < hand3)

        self.assertFalse(hand1 == hand4)
        self.assertFalse(hand1 > hand4)
        self.assertTrue(hand1 < hand4)


class TestRandomHandCompare(unittest.TestCase):
    def test_compare_two_random_hands(self):
        deck = Deck()
        for i in range(10):
            first_hand = Hand(deck.generate_random_cards(5))
            second_hand = Hand(deck.generate_random_cards(5))
            self.assertNotEqual(first_hand, second_hand,
                                "hand1 = hand2")  ### TO WYKURWIA ERROR ALE DLATEGO, ŻE JESZCZENIE POROWNUJE KTORY ''TEN SAM'' UKLAD JEST SILNIEJSZY
            if first_hand > second_hand:
                self.assertTrue(first_hand > second_hand,
                                "Error. First hand should be better than second hand. (THERE : first_hand < second_hand)")
            elif first_hand < second_hand:
                self.assertTrue(first_hand < second_hand,
                                "Error. Second hand should be better than first hand. (THERE : first_hand > second_hand)")


if __name__ == "__main__":
    unittest.main()
