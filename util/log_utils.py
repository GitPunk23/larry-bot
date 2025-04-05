import os
import re
from dotenv import load_dotenv
from util.event import Event

load_dotenv()
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')

LOG_PATTERN = re.compile(r"\[([^\]]+)\] \[Server thread/INFO\]: (.+)")

def get_new_events(last_processed_timestamp):
    """Read the log file and return new events based on the last processed timestamp."""
    new_events = []
    with open(LOG_FILE_PATH, 'r') as log_file:
        for line in log_file:
            event = Event.from_log_line(line)
            if event:
                if last_processed_timestamp is None or event.timestamp > last_processed_timestamp:
                    new_events.append(event)
    if new_events:
        last_processed_timestamp = new_events[-1].timestamp
    return new_events, last_processed_timestamp