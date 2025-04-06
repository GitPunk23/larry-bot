import re
from util.death_utils import is_death_message

class Event:
    event_description = None
    player = None
    timestamp = None
    LOG_PATTERN = re.compile(r"\[([^\]]+)\] \[Server thread/INFO\]: (.+)")

    def __init__(self, timestamp, player, event_description):
        self.timestamp = timestamp
        self.player = player
        self.event_description = event_description

    def __repr__(self):
        return f"Event(timestamp={self.timestamp}, player={self.player}, event_description={self.event_description})"

    @classmethod
    def from_log_line(cls, line):
        match = cls.LOG_PATTERN.match(line)
        if match and cls.filter_event_message(line):
            timestamp = match.group(1)
            event_description = match.group(2)
            player_name, event_description = event_description.split(' ', 1)
            return cls(timestamp, player_name, event_description)
        return None

    @classmethod
    def is_match(cls, other):
        return (cls.timestamp == other.timestamp and
                cls.player == other.player and
                cls.event_description == other.event_description)

    @classmethod
    def filter_event_message(cls, line):
        valid = is_death_message(line)

        return valid