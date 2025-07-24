import os
from enum import Enum

class DisplayState(Enum):
    OFF=0
    ON=1

def toggle_display(state: DisplayState, display: str):
    if state == DisplayState.OFF:
        os.system(f'xset -display {display} dpms force off')
    else:
        os.system(f'xset -display {display} dpms force on')