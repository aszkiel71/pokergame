import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                             'backend')))
from backend.card import Card
from backend.hand import Hand
from backend.hand_selector import HandSelector


class TestSimpleSelection(unittest.TestCase):


    def test_1(self):
        hole_cards = [Card("Hearts", 2), Card("Hearts", 3)]
        community_cards = [Card("Diamonds", 3), Card("Spades", 3), Card("Hearts", 6), Card("Hearts", 7), Card("Hearts", 9)]
        best_hand = Hand([Card("Hearts", 2), Card("Hearts", 3), Card("Hearts", 6), Card("Hearts", 7), Card("Hearts", 9)])  # Flush
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_2(self):
        hole_cards = [Card("Hearts", 4), Card("Spades", 4)]
        community_cards = [Card("Diamonds", "K"), Card("Spades", "K"), Card("Hearts", "K"), Card("Hearts", 8), Card("Clubs", 7)]
        best_hand = Hand([Card("Diamonds", "K"), Card("Spades", "K"), Card("Hearts", "K"), Card("Hearts", 4), Card("Spades", 4)])  # Full House
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_3(self):
        hole_cards = [Card("Clubs", 5), Card("Diamonds", 7)]
        community_cards = [Card("Spades", 6), Card("Hearts", 8), Card("Diamonds", 9), Card("Hearts", "J"), Card("Hearts", "Q")]
        best_hand = Hand([Card("Clubs", 5), Card("Diamonds", 7), Card("Spades", 6), Card("Hearts", 8), Card("Diamonds", 9)])  # Straight
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_4(self):
        hole_cards = [Card("Diamonds", 10), Card("Clubs", 10)]
        community_cards = [Card("Hearts", 2), Card("Spades", 10), Card("Hearts", 3), Card("Clubs", 7), Card("Diamonds", 9)]
        best_hand = Hand([Card("Diamonds", 10), Card("Clubs", 10), Card("Spades", 10), Card("Clubs", 7), Card("Diamonds", 9)])  # Three of a Kind
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_5(self):
        hole_cards = [Card("Clubs", "Q"), Card("Diamonds", 9)]
        community_cards = [Card("Hearts", 8), Card("Spades", 7), Card("Diamonds", 6), Card("Hearts", 5), Card("Hearts", "J")]
        best_hand = Hand([Card("Diamonds", 9), Card("Hearts", 8), Card("Spades", 7), Card("Diamonds", 6), Card("Hearts", 5)])  # Straight
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_6(self):
        hole_cards = [Card("Hearts", "K"), Card("Spades", 2)]
        community_cards = [Card("Clubs", 10), Card("Diamonds", 5), Card("Spades", "Q"), Card("Diamonds", "A"), Card("Clubs", 9)]
        best_hand = Hand([Card("Hearts", "K"), Card("Diamonds", "A"), Card("Spades", "Q"), Card("Clubs", 10), Card("Clubs", 9)])  # High Card
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_7(self):
        hole_cards = [Card("Hearts", "Q"), Card("Spades", "J")]
        community_cards = [Card("Hearts", "K"), Card("Clubs", 10), Card("Diamonds", 9), Card("Hearts", 3),Card("Hearts", 5)]
        best_hand = Hand([Card("Hearts", "K"), Card("Hearts", "Q"), Card("Spades", "J"), Card("Clubs", 10), Card("Diamonds", 9)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_8(self):
        hole_cards = [Card("Hearts", 6), Card("Clubs", "J")]
        community_cards = [Card("Spades", "J"), Card("Hearts", 6), Card("Diamonds", "J"), Card("Clubs", 6), Card("Hearts", 10)]
        best_hand = Hand([Card("Hearts", 6), Card("Clubs", 6), Card("Spades", "J"), Card("Hearts", "J"), Card("Diamonds", "J")])  # Full House
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_9(self):
        hole_cards = [Card("Clubs", 5), Card("Hearts", 5)]
        community_cards = [Card("Spades", 5), Card("Diamonds", 5), Card("Hearts", "K"), Card("Spades", "A"), Card("Diamonds", "Q")]
        best_hand = Hand([Card("Spades", 5), Card("Diamonds", 5), Card("Hearts", 5), Card("Clubs", 5), Card("Spades", "A")])  # Four of a Kind
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_10(self):
        hole_cards = [Card("Hearts", "K"), Card("Diamonds", 2)]
        community_cards = [Card("Spades", "K"), Card("Clubs", 2), Card("Diamonds", "Q"), Card("Hearts", 9), Card("Diamonds", 6)]
        best_hand = Hand([Card("Hearts", "K"), Card("Spades", "K"), Card("Diamonds", 2), Card("Clubs", 2), Card("Diamonds", "Q")])  # Two Pair
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

class TestEdgeCase(unittest.TestCase):

    def test_four_of_a_kind_vs_full_house(self):
        hole_cards = [Card("Spades", "Q"), Card("Hearts", "Q")]
        community_cards = [Card("Diamonds", "Q"), Card("Clubs", "Q"), Card("Hearts", 5), Card("Spades", 5), Card("Diamonds", 9)]
        best_hand = Hand([Card("Spades", "Q"), Card("Hearts", "Q"), Card("Diamonds", "Q"), Card("Clubs", "Q"), Card("Hearts", 9)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_straight_flush_vs_four_of_a_kind(self):
        hole_cards = [Card("Clubs", 2), Card("Clubs", 3)]
        community_cards = [Card("Clubs", 4), Card("Clubs", 5), Card("Clubs", 6), Card("Diamonds", "A"), Card("Hearts", 8)]
        best_hand = Hand([Card("Clubs", 2), Card("Clubs", 3), Card("Clubs", 4), Card("Clubs", 5), Card("Clubs", 6)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_flush_vs_full_house(self):
        hole_cards = [Card("Hearts", "A"), Card("Hearts", 9)]
        community_cards = [Card("Hearts", "J"), Card("Hearts", 2), Card("Hearts", 7), Card("Clubs", 7), Card("Spades", 7)]
        best_hand = Hand([Card("Hearts", "A"), Card("Hearts", 9), Card("Hearts", "J"), Card("Hearts", 7), Card("Hearts", 2)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_full_house_vs_flush(self):
        hole_cards = [Card("Hearts", "A"), Card("Spades", "A")]
        community_cards = [Card("Hearts", "Q"), Card("Clubs", "Q"), Card("Diamonds", "Q"), Card("Hearts", 3), Card("Hearts", 2)]
        best_hand = Hand([Card("Diamonds", "Q"), Card("Clubs", "Q"), Card("Hearts", "Q"), Card("Hearts", "A"), Card("Spades", "A")])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_straight_vs_flush(self):
        hole_cards = [Card("Clubs", 5), Card("Spades", 6)]
        community_cards = [Card("Hearts", 7), Card("Diamonds", 8), Card("Clubs", 9), Card("Hearts", 2), Card("Spades", 3)]
        best_hand = Hand([Card("Clubs", 5), Card("Spades", 6), Card("Hearts", 7), Card("Diamonds", 8), Card("Clubs", 9)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_two_pairs_vs_pair(self):
        hole_cards = [Card("Diamonds", 6), Card("Spades", 6)]
        community_cards = [Card("Hearts", 10), Card("Diamonds", 10), Card("Clubs", 9), Card("Hearts", 2), Card("Spades", 5)]
        best_hand = Hand([Card("Diamonds", 10), Card("Hearts", 10), Card("Diamonds", 6), Card("Spades", 6), Card("Clubs", 9)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    # Corrected straight tiebreaker test
    def test_straight_tiebreaker(self):
        hole_cards = [Card("Spades", 4), Card("Hearts", 3)]
        community_cards = [Card("Clubs", 5), Card("Diamonds", 6), Card("Hearts", 7), Card("Hearts", 2), Card("Spades", 8)]
        best_hand = Hand([Card("Spades", 4), Card("Clubs", 5), Card("Diamonds", 6), Card("Hearts", 7), Card("Spades", 8)])  # Corrected straight from 4 to 8
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_flush_vs_straight(self):
        hole_cards = [Card("Clubs", "A"), Card("Clubs", 4)]
        community_cards = [Card("Clubs", 9), Card("Clubs", 7), Card("Clubs", 5), Card("Spades", 8), Card("Diamonds", 6)]
        best_hand = Hand([Card("Clubs", "A"), Card("Clubs", 9), Card("Clubs", 7), Card("Clubs", 5), Card("Clubs", 4)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_high_card_vs_pair(self):
        hole_cards = [Card("Hearts", "K"), Card("Diamonds", 2)]
        community_cards = [Card("Spades", 3), Card("Clubs", 4), Card("Hearts", 5), Card("Diamonds", 7), Card("Clubs", 8)]
        best_hand = Hand([Card("Hearts", "K"), Card("Clubs", 7), Card("Diamonds", 4), Card("Hearts", 5), Card("Clubs", 8)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_ace_high_tiebreaker(self):
        hole_cards = [Card("Hearts", "A"), Card("Diamonds", "K")]
        community_cards = [Card("Spades", 2), Card("Clubs", 3), Card("Diamonds", 4), Card("Hearts", 6), Card("Clubs", 7)]
        best_hand = Hand([Card("Hearts", "A"), Card("Diamonds", "K"), Card("Spades", 7), Card("Clubs", 6), Card("Diamonds", 4)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)

    def test_high_card_with_kicker(self):
        hole_cards = [Card("Clubs", "K"), Card("Diamonds", "Q")]
        community_cards = [Card("Spades", 2), Card("Clubs", 3), Card("Diamonds", 4), Card("Hearts", 5),Card("Clubs", 7)]
        best_hand = Hand([Card("Diamonds", "Q"), Card("Clubs", "K"), Card("Clubs", 7), Card("Hearts", 5), Card("Diamonds", 4)])
        self.assertEqual(HandSelector(community_cards, hole_cards).select_best_hand(), best_hand)


if __name__ == '__main__':
    unittest.main()
