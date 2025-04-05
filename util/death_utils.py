# util/death_utils.py

death_keywords = [
    "died", "was slain", "fell", "burned", "blew up", "hit the ground too hard",
    "was shot", "was killed", "was pricked", "walked into", "drowned",
    "experienced kinetic energy", "was blown up", "was impaled", "was squashed",
    "was skewered", "went up in flames", "tried to swim in lava", "was struck by lightning",
    "discovered the floor was lava", "was killed by magic", "froze to death", "was stung",
    "was obliterated", "was fireballed", "starved to death", "suffocated in a wall",
    "was squished", "left the confines of this world", "was poked to death", "was destroyed",
    "fell out of the world", "withered away"
]

def is_death_message(event_description):
    return any(keyword in event_description for keyword in death_keywords)