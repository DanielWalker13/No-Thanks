"""Test cases for main."""

import pytest

import main
import helper


def test_rotate_list():
    """Test rotating list order."""
    start = ["Danny", "Hallie", "Cory", "AJ", "Alex", "Austin", "Cinco"]
    expected = ["Hallie", "Cory", "AJ", "Alex", "Austin", "Cinco", "Danny"]
    assert helper.rotate_list_order(start, "Hallie") == expected


def test_identify_dupes():
    """Test Game.identify_dupes method."""
    ls = [1, 2, 3, 4, 4, 7, 7, 9, 10]
    dupes = helper.identify_dupes(ls)

    assert dupes == {4, 7}


def test_Deck():
    """Test Deck object."""
    deck = main.Deck()
    assert len(deck.cards) == 24
    for card in deck.cards:
        assert int(card)
        assert card in range(3, 36)
    show_card = deck.flip()

    assert int(show_card)
    assert show_card in range(3, 36)


@pytest.fixture
def user_data_input():
    """Fixture for user input data."""
    data = {
        "player_names_by_count": {
            3: ["Danny", "Hallie", "Cory"],
            4: ["Danny", "Hallie", "Cory", "AJ"],
            5: ["Danny", "Hallie", "Cory", "AJ", "Alex"],
            6: ["Danny", "Hallie", "Cory", "AJ", "Alex", "Austin"],
            7: ["Danny", "Hallie", "Cory", "AJ", "Alex", "Austin", "Cinco"],
        },
        "oldest_by_player_count": {
            3: {"position": 2, "name": "Hallie"},
            4: {"position": 3, "name": "Cory"},
            5: {"position": 4, "name": "AJ"},
            6: {"position": 5, "name": "Alex"},
            7: {"position": 6, "name": "Austin"},
        },
        "chips_by_player_count": {3: 11, 4: 11, 5: 11, 6: 9, 7: 7},
        "oldest_order": {
            3: ["Hallie", "Cory", "Danny"],
            4: ["Cory", "AJ", "Danny", "Hallie"],
            5: ["AJ", "Alex", "Hallie", "Cory", "Danny"],
            6: ["Alex", "Austin", "Danny", "AJ", "Hallie", "Cory"],
            7: ["Austin", "Cinco", "Cory", "Danny", "AJ", "Hallie", "Alex"],
        },
    }
    return data


@pytest.mark.parametrize("player_count", [3, 4, 5, 6, 7])
def test_start_info_init_with_different_player_counts(
    mocker, player_count, user_data_input
):
    # Prepare side_effect list for input mocking: player count + player names
    side_effect = (
        [player_count]
        + user_data_input["player_names_by_count"][player_count]
        + [user_data_input["oldest_by_player_count"][player_count]["position"]]
    )

    mocker.patch("builtins.input", side_effect=side_effect)

    start_info = main.StartInfo()

    assert start_info.p_count == player_count
    assert (
        start_info.oldest
        == user_data_input["oldest_by_player_count"][player_count]["name"]
    )
    assert start_info.names == user_data_input["player_names_by_count"][player_count]
    assert (
        start_info.start_chips == user_data_input["chips_by_player_count"][player_count]
    )


def test_player_init():
    """Test Player object."""
    player = main.Player("Danny", 11)
    assert player.name == "Danny"
    assert player.chips == 11
    assert player.cards == []


# UPGRADE: Get mock_start_info and mock_deck from fixture
@pytest.fixture
def game_with_mocks(mocker):
    mock_start_info = mocker.MagicMock()
    mock_start_info.names = ["Dan", "Hallie", "Cory"]
    mock_start_info.oldest = "Hallie"
    mock_start_info.p_count = 3
    mock_start_info.start_chips = 11
    mock_deck = mocker.MagicMock()

    def custom_pop_side_effect():
        result = (
            game._deck.cards.pop()
        )  # Assuming initial_cards is accessible in this scope
        mock_deck.cards = game._deck.cards
        return result

    mock_deck.flip.side_effect = custom_pop_side_effect

    mock_deck_class = mocker.patch("main.Deck", return_value=mock_deck)
    mock_start_info_class = mocker.patch("main.StartInfo", return_value=mock_start_info)

    game = main.Game()  # Initial setup with mocks
    yield game, mock_deck, mock_start_info, mock_start_info_class, mock_deck_class


# UPGRADE: Upgrade to paramaterize and use fixtures?
# Not sure that it's possible
def test_game_init(game_with_mocks):
    """Test Game class attributes from init."""

    game, _, mock_start_info, _, _ = game_with_mocks
    oldest_order = ["Hallie", "Cory", "Dan"]

    # Instantiate Game, which now uses mocked StartInfo and Deck
    game = main.Game()

    # Assertions to verify behavior
    assert len(game.players) == 3
    for player in game.players:
        assert player.name in mock_start_info.names
        assert len(game.players) == mock_start_info.p_count
        assert player.chips == mock_start_info.start_chips
        assert player.cards == []

    # Verify that the oldest player is in the first position
    actual_order = [player.name for player in game.players]
    assert actual_order == oldest_order

    with pytest.raises(AttributeError):
        _ = game.show_card


def test_game_anti(game_with_mocks):
    """Test Game.anti method."""

    game, _, _, _, _ = game_with_mocks

    assert game.chip_pot == 0
    game.anti(game.players[0])
    assert game.chip_pot == 1
    assert game.players[0].chips == 10


def test_game_take_card(game_with_mocks):
    """Test Game.take_card method."""

    game, _, _, _, _ = game_with_mocks

    # game.players[0].chips = 11
    game.chip_pot = 11
    game.take_card(game.players[0], 24)
    assert game.players[0].cards == [24]
    assert game.players[0].chips == 22


def test_game_round_zero_chips(game_with_mocks):
    """Test Game.round method."""
    game, mock_deck, _, _, _ = game_with_mocks

    mock_deck.cards = [24, 25, 26, 27, 28]

    game._deck.cards = mock_deck.cards
    game.players[0].chips = 0
    game.round()
    # No chips: Forced to take card
    assert len(game._deck.cards) == 4
    assert game.show_card not in game._deck.cards
    assert game.players[0].cards == [game.show_card]
    assert len(game.players[0].cards) == 1


def test_game_round_take_card(mocker, game_with_mocks):
    """Test Game.round method."""
    game, mock_deck, _, _, _ = game_with_mocks

    mock_deck.cards = [24, 25, 26, 27, 28]

    game._deck.cards = mock_deck.cards

    mocker.patch("builtins.input", side_effect=["n", "n", "n", "y"])
    game.round()
    # No chips: Forced to take card
    assert game.players[0].chips == 13
    assert game.show_card not in game._deck.cards
    assert game.players[0].cards == [game.show_card]
    assert len(game.players[0].cards) == 1


# def test_game_run(mocker, game_with_mocks):
#     """Test Game.round method."""
#     game, mock_deck, _, _, _ = game_with_mocks

#     mock_deck.cards = [14, 24]

#     game._deck.cards = mock_deck.cards

#     mocker.patch("builtins.input", side_effect=["y", "y"])
#     mock_end_game = mocker.patch.object(game, "end_game")
#     mock_exit = mocker.patch("builtins.exit")

#     game.run()

#     assert game._deck.cards == []

#     mock_end_game.assert_called_once()
#     mock_exit.assert_called_once()


@pytest.fixture
def end_game_data():
    """Fixture for end_game data."""
    data = {
        "cards": {
            "p1": [4, 5, 7, 10, 16, 17, 20, 21],  # 57 - 8 = 49
            "p2": [
                9,
                11,
                13,
                19,
                22,
                23,
                24,
                25,
                27,
                28,
                30,
                32,
                35,
            ],  # 198 - 11 = 187
            "p3": [12, 15, 34],  # 61 - 14 = 47
        },
        "chips": {"p1": 8, "p2": 11, "p3": 14},
        "total_points": {"p1": 49, "p2": 187, "p3": 47},
    }
    return data


def test_game_end_totals(game_with_mocks, end_game_data):
    """Test Game.end_game method."""
    game, mock_deck, _, _, _ = game_with_mocks

    game.players[0].chips = end_game_data["chips"]["p1"]
    game.players[1].chips = end_game_data["chips"]["p2"]
    game.players[2].chips = end_game_data["chips"]["p3"]

    game.players[0].cards = end_game_data["cards"]["p1"]
    game.players[1].cards = end_game_data["cards"]["p2"]
    game.players[2].cards = end_game_data["cards"]["p3"]

    game.end_game()

    card_ls = [
        card for pl_cards in end_game_data["cards"].values() for card in pl_cards
    ]
    assert len(card_ls) == 24
    assert game.players[0].total_points == end_game_data["total_points"]["p1"]
    assert game.players[1].total_points == end_game_data["total_points"]["p2"]
    assert game.players[2].total_points == end_game_data["total_points"]["p3"]


def test_winners_points(game_with_mocks):
    """Test Game.end_game method."""
    game, mock_deck, _, _, _ = game_with_mocks

    game.players[0].total_points = 4
    game.players[1].total_points = 8
    game.players[2].total_points = 15

    assert game.winner() == [game.players[0], game.players[1], game.players[2]]


def test_winners_points_ties(game_with_mocks):
    """Test Game.end_game method."""
    game, mock_deck, _, _, _ = game_with_mocks

    game.players[0].toral_points = 8
    game.players[1].total_points = 8
    game.players[2].total_points = 15

    game.players[0].cards = [4, 5, 7, 10]
    game.players[1].cards = [26]
    game.players[2].cards = [6, 8, 9, 11]

    assert game.winner() == [game.players[1], game.players[0], game.players[2]]

    game.players[0].cards = [4, 5, 7, 10]
    game.players[1].cards = [6, 8, 9, 11]
    game.players[2].cards = [12, 15, 34]

    assert game.winner() == [game.players[1], game.players[0], game.players[2]]


def test_game_reset(game_with_mocks):
    """Test Game.reset method."""
    game, _, _, mock_start_info_class, mock_deck_class = game_with_mocks

    # Call the reset method
    game.reset()

    # Assert that StartInfo and Deck have been re-initialized
    assert mock_start_info_class.call_count == 2
    assert mock_deck_class.call_count == 2
