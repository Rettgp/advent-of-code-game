import unittest
import os
from textwrap import dedent
from app.ferry import Seating

HUGE_DATA_FILE = os.path.join(os.path.dirname(__file__), "test_data/huge_test_input")
DATA_FILE = os.path.join(os.path.dirname(__file__), "test_data/test_input")

def read_from_file(file_input) -> Seating:
    with open(file_input, "r") as f:
        content = f.read()
        return Seating(content=content)


class TestSeatingState(unittest.TestCase):
    def setUp(self):
        self.test_input = ""


    def test_occupied_seat(self):
        seating = Seating(content="L")
        self.assertFalse(seating.state.get((0, 0)))


    def test_not_unoccupied_seat(self):
        seating = Seating(content="#")
        self.assertTrue(seating.state.get((0, 0)))


    def test_ground_is_not_counted(self):
        seating = Seating(content=".")
        self.assertEqual(len(seating.state), 0)


    def test_seat_becomes_occupied_if_no_adjacent_occupied(self):
        seating = Seating(content="L")
        self.assertEqual(len(seating.state), 1)

        self.assertFalse(seating.state.get((0,0)))
        seating.cycle()
        self.assertTrue(seating.state.get((0,0)))


    def test_seat_stays_occupied_if_no_adjacent_occupied(self):
        seating = Seating(content="#")
        self.assertEqual(len(seating.state), 1)

        seating.cycle()
        self.assertTrue(seating.state.get((0, 0)))


    def test_number_of_occupied_seats_is_zero_if_no_adjacent_seats(self):
        seating = Seating(content="#")
        self.assertEqual(len(seating.state), 1)
        self.assertEqual(seating.number_of_adjacent_occupied_seats(row = 0, column = 0), 0)


    def test_number_of_occupied_seats_is_correct(self):
        seating = Seating(content=dedent("""L###L
                                            LLLLL
                                            ###LL"""))

        self.assertEqual(seating.number_of_adjacent_occupied_seats(row = 0, column = 2), 2)
        self.assertEqual(seating.number_of_adjacent_occupied_seats(row = 1, column = 2), 5)
        self.assertEqual(seating.number_of_adjacent_occupied_seats(row = 2, column = 2), 1)


    def test_number_of_occupied_seats_does_not_account_for_ground(self):
        seating = Seating(content=".L#.")
        self.assertEqual(seating.number_of_adjacent_occupied_seats(row = 0, column = 1), 1)


    def test_seat_becomes_unoccupied_if_four_adjacent_seat_occupied(self):
        seating = Seating(content=dedent("""L###L
                                            LL#LL
                                            ###LL"""))

        seating.cycle()
        self.assertFalse(seating.state.get((1, 2)))


    def test_ground_stays_ground_after_cycle(self):
        seating = Seating(content=".")

        self.assertFalse(seating.state.get((0, 0)))
        seating.cycle()
        self.assertFalse(seating.state.get((0, 0)))


    def test_number_of_occupied_seats_accounts_for_occupied_seats(self):
        seating = Seating(content=dedent("""L###L
                                            LL#LL
                                            ###LL"""))

        self.assertEqual(seating.total_occupied_seats(), 7)


    def test_state_becomes_stable_if_nothing_changes(self):
        seating = Seating(content="L")

        self.assertFalse(seating.stable)
        seating.cycle()
        self.assertFalse(seating.stable)
        seating.cycle()
        self.assertTrue(seating.stable)


    def test_integration(self):
        seating = read_from_file(DATA_FILE)

        while not seating.stable:
            seating.cycle()

        self.assertEqual(seating.total_occupied_seats(), 37)


    def test_integration_huge(self):
        seating = read_from_file(HUGE_DATA_FILE)

        while not seating.stable:
            seating.cycle()

        self.assertEqual(seating.total_occupied_seats(), 2319)