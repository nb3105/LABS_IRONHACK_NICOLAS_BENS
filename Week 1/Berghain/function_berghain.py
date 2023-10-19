#GAME INITIATION

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
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

# start_game (no input parameters)

"""
starts the game: first lines are printed, function play_room is initiated while
input variable is the (saved) current room
"""

def start_game():
    """
    Start the game
    """
    print("You are in the street and want to go to Berhain. \nYou must get there ASAP!")
    play_room(game_state["current_room"])


# play_room (1 input parameter: which room the player is in)

"""
checks if current room is the target room (if yes, success), asks player for
intended action, initiates related functions)
"""

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You made it into Berhain. Enjoy Drake and have the time of your life.")
    else:
        print(f"You are now in the {room['name']}.")
        intended_action = input("What would you like to do next? Type '1' to explore, '2' to engage with something, '9' to reflect upon skills and tools, '0' to quit the game. ").strip() #HERE AND AFTER: UPDATED
        if intended_action == '1' or intended_action == '2' or intended_action == '9' or intended_action == '0':
            if intended_action == '1':
                explore_room(room) # Prints the items the player can explore
                play_room(room) # Re-initiates this very function
            elif intended_action == '2':
                examine_item(input("What would you like to engage with? ").strip())
            elif intended_action == '9':
                if game_state["keys_collected"] == []:
                    print("You have no skills, knowlege, or items worthy speaking of.")
                else:
                    current_inventory = [key["name"] for key in game_state["keys_collected"]] ### MAYBE TURN THIS INTO FUNCTION
                    current_inventory_str = str(current_inventory)[1:-1].replace("'","")
                    print(f"You have the following knowledge or items: {current_inventory_str}.")
                play_room(room)
            elif intended_action == '0':
                print("Bye bye.")
        else:
            print("Not sure what you mean. Type '1' to explore, '2' to engage with something, '9' to reflect upon skills and tools, '0' to quit the game. ") #UPDATED UNTIL HERE
            play_room(room) # Re-initiates this very function
        linebreak()


# explore_room (1 input parameter: which room the player is in)

"""
This function just prints out the items in a room that the player can explore.
"""

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You casually check out your surroundings. This is " + room["name"] + ". You notice " + ", ".join(items) + ".")


# get_next_room_of_door (2 input parameters: door, the current(!) room)

"""
Each door connects 2 rooms. This functions finds out which room is on the
other side of the door, dependent on the room the player is currently in.
"""

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
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
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = f"You engage with {item_name}. " # FSTRING INSTEAD
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "Looks pretty cool."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "You somehow don't feel ready for that yet."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += f"You now have {item_found['name']}." # FSTRING INSTEAD
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("That's not possible here.")

    if(next_room and input("Do you want to go there? Enter 'yes' or 'no'").strip() == 'yes'): #Spell correction "Enter"
        play_room(next_room)
    else:
        play_room(current_room)


