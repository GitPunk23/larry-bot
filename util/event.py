import re

class Event:
    LOG_PATTERN = re.compile(r"\[([^\]]+)\] \[Server thread/INFO\]: (.+)")

    def __init__(self, timestamp, player, event_description):
        self.timestamp = timestamp
        self.player = player
        self.event_description = event_description

    @classmethod
    def from_log_line(cls, line):
        match = cls.LOG_PATTERN.match(line)
        if match:
            timestamp = match.group(1)
            event_description = match.group(2)
            player_name, event_description = event_description.split(' ', 1)
            return cls(timestamp, player_name, event_description)
        return None

    def __repr__(self):
        return f"Event(timestamp={self.timestamp}, player={self.player}, event_description={self.event_description})"

    def is_match(self, other):
        return (self.timestamp == other.timestamp and
                self.player == other.player and
                self.event_description == other.event_description)