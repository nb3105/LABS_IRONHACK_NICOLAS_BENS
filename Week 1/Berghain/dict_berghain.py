#ROOM AND ITEMS

game_room = { ##### street
    "name": "street", # Adjusted
    "type": "room"
}

couch = { ##### bar
    "name": "bar",
    "type": "furniture"
}

piano = { ##### ATM
    "name": "ATM",
    "type": "furniture"
}

door_a = { ##### clothing store entrance
    "name": "clothing store entrance",
    "type": "door"
}

# clothing store (bedroom 1)
bedroom1 = { ##### clothing store
    "name": "clothing store", # Adjusted
    "type": "room"
}

queen_bed = { ##### cashier
    "name": "cashier",
    "type": "furniture"
}

door_b = { ##### back room entrance
    "name": "back room entrance",
    "type": "door"
}

door_c = { ##### crew to go to berghain
    "name": "crew to go to berghain",
    "type": "door"
}

# secret back room (bedroom 2)
bedroom2 = { ##### secret back room
    "name": "secret back room", # Adjusted
    "type": "room"
}

double_bed = { ##### clothes
    "name": "clothes",
    "type": "furniture"
}

dresser = { ##### local guy
    "name": "local guy",
    "type": "furniture"
}

# berghain line (dining_room)
living_room = { ##### berghain line
    "name": "berghain line", #Adjusted
    "type": "room"
}

dining_table = { ##### random hipster
    "name": "random hipster",
    "type": "furniture"
}

door_d = { ##### bouncer
    "name": "bouncer", # Corrected the name
    "type": "door"
}

# berghain (outside)
outside = { ##### berghain
    "name": "berghain"
}

# Keys
key_a = {
    "name": "cash", #####
    "type": "key",
    "target": door_a
}

key_b = {
    "name": "pass to secret back room", #####
    "type": "key",
    "target": door_b
}

key_c = {
    "name": "cool clothes", #####
    "type": "key",
    "target": door_c
}

key_d = {
    "name": "knowledge of drake playing tonight", #####
    "type": "key",
    "target": door_d
}

### Defining lists of relevant "types" (lists)
all_rooms = [game_room, bedroom1, bedroom2, living_room, outside] # Do we actually need this?
all_doors = [door_a, door_b, door_c, door_d] # Do we actually need this?
#all_keys = [key_a, key_b, key_c, key_d] # added - probably not necessary

### Establishing object relations (nested dictionaries: one dictionary that
### includes rooms/objects as keys and related rooms/objects as values)
object_relations = {
    "street": [couch, piano, door_a],
    "ATM": [key_a],
    "clothing store entrance": [game_room, bedroom1],
    "clothing store": [queen_bed, door_a, door_b, door_c],
    "cashier": [key_b],
    "back room entrance": [bedroom1, bedroom2],
    "crew to go to berghain": [bedroom1, living_room],
    "secret back room": [double_bed, dresser, door_b],
    "clothes": [key_c],
    "local guy": [key_d],
    "berghain line": [dining_table, door_c, door_d],
    "bouncer": [living_room, outside],
    "berghain": [door_d]
}

### Defining the game state

"""
Do not directly change this dict.
Instead, when a new game starts, make a copy of this
dict and use the copy to store gameplay state. This
way you can replay the game multiple times.
"""

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}