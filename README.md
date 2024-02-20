

# No Thank: Card Game

Backup of an old practice repo circa 2019
Did some minor refactoring, may want to convert apis and build out a react front end 

Mostly in good shape 

## Bugs
- "winner" function is failing unit test
    + Seems mock for player 1 is not being set properly
    + ensure that winner function produces:
        * Winner by lowest points if there are not ties
        * Ties broken by fewest cards
        * Card ties are brokes by lowest card in hand

