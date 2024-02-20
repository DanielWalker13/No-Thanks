import random
import helper


class Deck:
    """Maintain the primary deck of cards for the game. Range 3-35."""

    def __init__(self) -> None:
        """Create a deck of cards and remove 9 random cards from the deck."""
        self.cards = [i for i in range(3, 36)]
        random.shuffle(self.cards)

        for _ in range(9):
            self.cards.remove(random.choice(self.cards))

    def flip(self) -> int:
        """Flip the top card of the deck and remove it from the deck."""
        return self.cards.pop()

    def __repr__(self) -> str:
        """Return the number of cards in the deck and the cards in the deck."""
        return str(f"Total Cards: {len(self.cards)}, {self.cards}")

    def __str__(self) -> str:
        """Return the number of cards in the deck and the cards in the deck."""
        return str(f"Total Cards: {len(self.cards)}, {self.cards}")


class StartInfo:
    """Collect the metadata for the game."""

    def __init__(self) -> None:
        """Initiate metadata collection."""
        self.player_count()
        self.player_names()
        self.oldest_player()
        self.start_chip_count()

    def player_count(self) -> None:
        """Collect the number of players."""
        player_num = 0
        valid_pos = [3, 4, 5, 6, 7]
        while not player_num in valid_pos:
            if player_num != 0 and player_num < 3 or player_num > 7:
                player_num = int(
                    input(
                        "Test: Invalid number of players: Please enter a number of players between 3 and 7. \n"
                    )
                )
            else:
                player_num = int(input("How many player do you have? \n"))
        self.p_count = player_num

    def player_names(self) -> None:
        """Collect the names of the players."""
        names = []
        for pl_pos, _ in enumerate(range(self.p_count), 1):
            valid = False
            while not valid:
                name = str(input(f"What is {pl_pos} players Name? \n"))
                if name in names:
                    print("Name already taken, please choose another name.")
                else:
                    valid = True
                    names.append(name)
        self.names = names

    def oldest_player(self) -> None:
        """Collect the oldest player."""
        pl_order = {}
        for i, name in enumerate(self.names, 1):
            pl_order[i] = name
            print(f"{i}. {name}")

        valid = False
        while not valid:
            valid = False
            while not valid:
                oldest = int(input("Who is the oldest player (number)? \n"))
                if oldest in pl_order.keys():
                    valid = True
                    self.oldest = pl_order[oldest]
                else:
                    print(
                        "Please choose a valid numeric option for oldest player name."
                    )

    def start_chip_count(self) -> None:
        """Collect the number of chips for each player."""

        if self.p_count >= 3 and self.p_count <= 5:
            self.start_chips = 11
        elif self.p_count == 6:
            self.start_chips = 9
        elif self.p_count == 7:
            self.start_chips = 7


class Player:
    """Maintain the player's assets for the game."""

    def __init__(self, name: str, chips: int) -> None:
        """Create the player's assets."""
        self.name = name
        self.chips = chips
        self.cards: list[int] = []
        self.total_points: int = 0

    def add_chips(self, new_chips: int) -> None:
        """Add a chip to the player's assets."""
        self.chips += new_chips

    def remove_chips(self, rm_chip: int) -> None:
        """Remove a chip from the player's assets."""
        self.chips -= rm_chip

    def add_card(self, new_card: int) -> None:
        """Add a card to the player's assets."""
        self.cards.append(new_card)

    def __repr__(self) -> str:
        """Return the player's assets."""
        return f"{self.name} has {self.chips} chips, {self.cards} cards, and {self.total_points} total points."

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------


class Game:
    """Maintain the game's assets and workflow."""

    def __init__(self) -> None:
        """Create the game's assets."""
        self.game_setup()

    def game_setup(self) -> None:
        self._metadata = StartInfo()
        self._deck = Deck()
        self.chip_pot = 0
        self.players = self.generate_players()

    # TEST: Verify this works
    def generate_players(self) -> list[Player]:
        """Create the players for the game."""
        players = []

        starting_order = helper.rotate_list_order(
            self._metadata.names, self._metadata.oldest
        )
        for name in starting_order:
            players.append(Player(name, self._metadata.start_chips))
        return players

    def anti(self, player: Player) -> None:
        """No Thanks: Add a chip to pot."""
        player.remove_chips(1)
        print(f"\n {player.name} remaining Chips: {player.chips}")
        self.chip_pot += 1
        print(f"\n Pot: {str(self.chip_pot)}\n")

    def take_card(self, player: Player, card: int) -> None:
        """Take a card from the deck and add it to the player's assets."""
        player.cards.append(card)
        print(f"Chips: {player.chips}, Pot: {self.chip_pot}")
        player.add_chips(self.chip_pot)
        print(f"\n {player.name}'s New Chip Total: {player.chips}")
        print(f"\n {player.name}'s Cards: {player.cards}\n")
        self.players = helper.rotate_list_order(self.players, player)

    def round(self) -> None:
        """
        round wokflow:
            1. Flip the card : done
            2. Check if current player has chips
            3. If player has no chips, take card
            4. If player has chips, take option
            5. If player takes card, rotate to next player

        """

        self.chip_pot = 0
        self.show_card = self._deck.flip()

        taken = False
        while not taken:
            for player in self.players:
                print(f"Remaining Cards: {len(self._deck.cards)}\n")
                print(f"Active Card: {self.show_card}\n")
                print(f"Player: {player.name}\n")
                if player.chips == 0:
                    self.take_card(player, self.show_card)
                    print(f"{player.name} was forced to take{self.show_card}")
                    print(f"New hand {player.cards}")
                    taken = True
                else:
                    # UPGRADE: add input validation
                    valid_input = ["y", "n", "yes", "no"]
                    valid = False
                    while not valid:
                        answer = input(
                            str(
                                f"{player.name} would you like to keep the card? y or n \n"
                            )
                        ).lower()
                        if answer in valid_input and answer in ["y", "yes"]:
                            self.take_card(player, self.show_card)
                            taken = True
                            valid = True
                            print(f"{player.name} took {self.show_card}")

                        elif answer in valid_input and answer in ["n", "no"]:
                            self.anti(player)
                            print(
                                f"{player.name} passed on {self.show_card} and antied up."
                            )
                            valid = True

                        else:
                            print("\n\tPlease answer y or n.\n")
                print(f"Taken: {taken}")
                if taken:
                    break

    def run(self) -> None:
        """Run a single game."""
        count = 0
        trigger_end = False
        while not trigger_end:
            if not len(self._deck.cards) == 0:
                count += 1
                self.round()
            else:
                trigger_end = True
                print("Game Over! \n")
                self.end_game()
                win_order = self.winner()
                self.print_winner(win_order)
                exit()

    # answer = input("Would you like to play another game? (Ongoing Development) \n")")

    #     if answr in ["y", "yes"]:
    #         self.run()
    #     else:
    #         print("Thanks for playing! \n")
    #         exit()

    def reset(self) -> None:
        """Reset the game."""
        self.game_setup()

    def restart_game(self) -> None:
        """Restart the game."""
        # FIX: Not working
        self.game_setup()
        self.run()
        # self.run(

    def end_game(self) -> None:
        """End the game and tally the scores."""
        print("Totaling Score \n")
        for player in self.players:
            score_nums, _ = helper.remove_sequential_numbers(player.cards)
            print(f"Player Cards: {player.cards}")
            print(f"Scoring Numbers: {score_nums}")
            player.cards = score_nums
            player.total_points = sum(player.cards) - player.chips

    def winner(self) -> list[Player]:
        """Determine the winner of the game."""

        def custom_sort(players: list[Player]):
            """Sort the players by total points, number of cards, and the lowest card."""
            points_priority = (
                players.total_points
            )  # Negative to ensure higher points come first
            cards_priority = sorted(players.cards)  # Sort cards to find lowest card
            return (points_priority, cards_priority)
            # return (players.total_points, len(players.cards), min(players.cards))

        win_order = sorted(self.players, key=custom_sort)
        return win_order

    def print_winner(self, win_order) -> None:
        """Print the winner of the game."""
        [
            print(player.name, player.total_points, len(player.cards))
            for player in win_order
        ]


if __name__ == "__main__":
    game = Game()
    # game.round()
    game.run()
