import time
from time import sleep
from IPython.display import clear_output


# Defining rooms and their items
### main street and related objects
main_street = {
    "name": "main street",
    "type": "room"
}

bar = {
    "name": "bar",
    "type": "furniture"
}

atm = {
    "name": "atm",
    "type": "furniture"
}

door_a = {
    "name": "clothing store entrance",
    "type": "door"
}

### clothing store and related objects
clothing_store = {
    "name": "clothing store",
    "type": "room"
}

cashier = {
    "name": "cashier",
    "type": "furniture"
}

door_b = {
    "name": "back room door",
    "type": "door"
}

door_c = {
    "name": "street to berghain",
    "type": "door"
}

### secret back room and related objects
secret_back_room = {
    "name": "secret back room",
    "type": "room"
}

clothes = {
    "name": "clothes",
    "type": "furniture"
}

local_guy = {
    "name": "local guy",
    "type": "furniture"
}

### berghain line and related objects
berghain_line = {
    "name": "berghain line",
    "type": "room"
}

random_hipster = {
    "name": "random hipster",
    "type": "furniture"
}

door_d = {
    "name": "bouncer",
    "type": "door"
}

### berghain (target)
berghain = {
    "name": "berghain"
}

# Keys
key_a = {
    "name": "cash",
    "type": "key",
    "target": door_a
}

key_b = {
    "name": "the access to the secret back room",
    "type": "key",
    "target": door_b
}

key_c = {
    "name": "cool clothes",
    "type": "key",
    "target": door_c
}

key_d = {
    "name": "knowledge of DJ Norbert playing in Berghain tonight",
    "type": "key",
    "target": door_d
}

### Establishing object relations (nested dictionaries: one dictionary that
### includes rooms/objects as keys and related rooms/objects as values)
object_relations = {
    "main street": [bar, atm, door_a],
    "atm": [key_a],
    "clothing store entrance": [main_street, clothing_store],
    "clothing store": [cashier, door_a, door_b, door_c],
    "cashier": [key_b],
    "back room door": [clothing_store, secret_back_room],
    "street to berghain": [clothing_store, berghain_line],
    "secret back room": [clothes, local_guy, door_b],
    "clothes": [key_c],
    "local guy": [key_d],
    "berghain line": [random_hipster, door_c, door_d],
    "bouncer": [berghain_line, berghain],
    "berghain": [door_d]
}

### Defining the game state

"""
Do not directly change this dict.
Instead, when a new game starts, make a copy of this
dict and use the copy to store gameplay state. This
way you can replay the game multiple times.
"""

#COUNT DOWN
t = 10

def countdown(t):
    while t:
        mins,secs = divmod(t, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print("Time is up, you didn't make it to Berghain !")


#GAME INITIATION

INIT_GAME_STATE = {
    "current_room": main_street,
    "keys_collected": [],
    "target_room": berghain
}

#LINEBREAK

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

# EMPTYLINE

def emptyline():
    """
    Print an empty line
    """
    print()

def end_credits():
    """
    Prints end credits after finishing/quitting
    """
    print()
    print("~~~CREDITS~~~")
    print("Game by Nico and Seb, based on an Ironhack template")
    print("Thank you for playing!")

# start_game (no input parameters)

"""
starts the game: first lines are printed, function play_room is initiated while
input variable is the (saved) current room
"""

def start_game():
    """
    Start the game: First lines printed, play_room initiated with argument current room
    """
    print("You want to go to Berhain. \nYou must get there ASAP as you are in uber party mode!")
    print()
    sleep(4)
    play_room(game_state["current_room"])


# play_room (1 input parameter: which room the player is in)

"""
checks if current room is the target room (if yes, success), asks player for
intended action, initiates related functions)
"""

def play_room(room):
    """
    Playing a room. First checking if the room being played is the target room.
    If it is, the game will end with success. Otherwise, lets player either
    explore (list all items in the room) or examine an item, look at their
    inventory, or just quit playing the game.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        clear_output()
        print("Congrats! You made it into Berhain. Enjoy DJ Norbert and have the time. of. your. life.")
        end_credits()
    else:
        print(f"You are now in the {room['name']}.")
        intended_action = input("What would you like to do next? Type '1' to explore, '2' to engage with something, '9' to reflect upon skills and tools, '0' to quit the game. ").strip()
        if intended_action == '1' or intended_action == '2' or intended_action == '9' or intended_action == '0':
            if intended_action == '1':
                explore_room(room)
                play_room(room)
            elif intended_action == '2':
                examine_item(input("What would you like to engage with? ").strip())
            elif intended_action == '9':
                if game_state["keys_collected"] == []:
                    clear_output()
                    print("You have no skills, knowlege, or items worth speaking of.")
                else:
                    current_inventory = [key["name"] for key in game_state["keys_collected"]]
                    current_inventory_str = str(current_inventory)[1:-1].replace("'","")
                    clear_output()
                    print(f"You have the following knowledge or items: {current_inventory_str}.")
                play_room(room)
            elif intended_action == '0':
                clear_output()
                print("Only the best make it into Berghain - and today that was not you. Better luck next time!")
                end_credits()
        else:
            clear_output()
            print("Not sure what you mean.")
            play_room(room)
        linebreak()


# explore_room (1 input parameter: which room the player is in)

"""
This function just prints out the items in a room that the player can explore.
"""

def explore_room(room):
    """
    Explore a room. Lists all items belonging to this room.
    """
    clear_output()
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You casually check out your surroundings. This is the " + room["name"] + ". You notice: " + ", ".join(items) + ".")

# get_next_room_of_door (2 input parameters: door, the current(!) room)

"""
Each door connects 2 rooms. This functions finds out which room is on the
other side of the door, dependent on the room the player is currently in.
"""

def get_next_room_of_door(door, current_room):
    """
    Finds the two rooms connected to the given door based on object relations.
    Returns the room that is not the current room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room
        

# examine_item (1 input parameter: the item name)

"""
Function for item checks and all actions that can result from that, including
enterting the next room.
"""

def examine_item(item_name):
    """
    Examins an item which can be a door or furniture (another object).
    First makes sure the intended item belongs to the current room.
    Then checks if the item is a door. Tells player if the key hasn't been
    collected yet. Otherwise asks player if they want to go to the next
    room. If the item is not a door, then checks if it contains keys.
    Collects the key if found and updates the game state. At the end,
    plays either the current or the next room depending on the game state
    to keep playing.
    """
    clear_output()
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            if item["name"] == 'atm':
                output = f"You do your thing with the {item_name}. "
            elif item["name"] == 'clothes':
                output = f"You browse through and pick some {item_name}. "
            elif item["name"] == 'bar':
                output = f"You stop by the {item_name}. "
            else:
                output = f"You approach the {item_name}. "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You feel ready for it!"
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "You somehow don't feel ready for that yet."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += f"You now have {item_found['name']}."
                else:
                    output += "There isn't anything interesting about it."
                    if item["name"] == "bar":
                        output += " But you are pretty drunk now."
            print(output)
            break

    if(output is None):
        print("That's not possible here.")

    if(next_room and input("Do you want to go further? Enter '1' for 'yes' or '2' for 'no' ").strip() == '1'):
        clear_output()
        play_room(next_room)
    else:
        play_room(current_room)


### Starting the game
# Making a copy of the game state
game_state = INIT_GAME_STATE.copy()

