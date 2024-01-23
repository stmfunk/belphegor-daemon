import time
from watchdog.observers import Observers
from watchdog.events import PatternMatchingEventHandler


if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = False

