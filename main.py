
import random

def count(num):
    count = 0
    for x in num:
        count += 1
    return (count)

class deck:

    def __init__(self):
        self.p_deck = [i for i in range(3,36)]
        random.shuffle(self.p_deck)
        x = 0
        while x < 9: 
            x += 1
            self.p_deck.remove(random.choice(self.p_deck))

    def flip(self):
        self.show_card = self.p_deck.pop()
'''
class start_info:
   
    p_count = []
    names = []
    count = 0

    def __init__(self): 

        players = int(input("How many player do you have?"))
        #if players !int:
        #    int(input("Please enter a number of players between 3 and 5."))
            
        while count < players:
            count +=1
            p_count.append(count) 
        print (p_count)

        for x in p_count:
            name =str(input("What is " + str(x) + " players Name?"))
            names.append(name) 
        print(names)
'''
# Assigns players assets
players = ["Hallie","Danny","Cory"]



class player:
    def __init__(self,name):
        self.name = name
        self.chips = 11 
        self.cards = []
Deck = deck()

p_list = {}
c = 1
for x in players:
    p_list.update({str(c):x})
    c += 1

for x, y in p_list.items():
    globals()[x] = player(y)


class rotate:
    def rotate_dict(self):
        m_element = dict([next(iter(p_list.items()))])
        (p_list.pop(next(iter(p_list.keys()))))
        p_list.update(m_element)

    def shift (self,cur_player):
        while (next(iter(p_list.keys()))) != cur_player:
            self.rotate_dict()

    def same_player(self,cur_player):
        for y in p_list.values():
            if not y  == cur_player:
                self.rotate_dict()
            else:
                print ("\n\tPlease answer y or n.\n")
                break
Rotate = rotate()
class game:
    chip_pot =0
    def anti(self,player):
        globals()[player].chips -= 1
        print(f"\n Remaining Chips: {str(globals()[player].chips)}")
        self.chip_pot += 1
        print (f"\n Pot: {str(self.chip_pot)}\n")
        
    def take_card(self,player):
        globals()[player].cards.append(Deck.show_card)
        globals()[player].chips += self.chip_pot
        print(f"\n {globals()[player].name}'s New Chip Total: {str(globals()[player].chips)}")
        print(f"\n {globals()[player].name}'s Cards: {str(globals()[player].cards)}\n")
        self.chip_pot = 0

    def round(self):
        n_player = 1
        Deck.flip()
        print (f"Current Card: {Deck.show_card}\n")
        while type(Deck.show_card) == int:
            for x,y in p_list.items():
                print(f" {globals()[x].name}'s Cards: {str(globals()[x].cards)}\n")
                if globals()[x].chips == 0:
                    Deck.show_card = str(Deck.show_card)
                    self.take_card(x)
                    print(globals()[x].cards)
                    break
                else:
                    
                    response = input(str(f"{y} would you like to keep the card? y or n "))
                    if response == "y":
                        Deck.show_card = str(Deck.show_card)
                        self.take_card(x)
                        Rotate.shift(x)
                        break
                    elif response == "n":
                        self.anti(x)
                        continue
                    else: 
                        Rotate.same_player(y)
                        break 
    def start_hold(self):
        count =0
        trigger_end = False
        while not trigger_end  == True:
            if not len(Deck.p_deck) == 0:
                count += 1
                self.round()
            if len(Deck.p_deck) == 0:
                trigger_end = True
                print (trigger_end)
                self.end_game()


    def end_game(self):
        consecutives = []
        for x, y in p_list.items():
            print(y)
            for c in globals()[x].cards:
                remove = int(c) +1
                remove = str(remove)

                if remove in globals()[x].cards:
                    print(remove)
                    consecutives.append(remove) 
                
            for r in consecutives:
                consecutives.sort()
                globals()[x].cards.remove(r)
                print(globals()[x].cards)
                print(consecutives)
Game= game()
Game.start_hold()
