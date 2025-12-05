import neopixel
import board
import digitalio
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC

from kmk.modules.encoder import EncoderHandler

class VolumeEncoderHandler(EncoderHandler):
    def on_rotate(self, kbd, direction):
        global volume_level
        if direction == 1:  # clockwise
            volume_level = min(100, volume_level + 5)
        elif direction == -1:  # counterclockwise
            volume_level = max(0, volume_level - 5)
        super().on_rotate(kbd, direction)

    def on_press(self, kbd, pin):
        global mute_state
        mute_state = not mute_state
        super().on_press(kbd, pin)
from kmk.modules.display import Display
from kmk.modules.oled import OLED

# ----------------------------------------------------------
#                 MAIN KEYBOARD INSTANCE
# ----------------------------------------------------------

keyboard = KMKKeyboard()

# ----------------------------------------------------------
#                   PIN DEFINITIONS
# ----------------------------------------------------------
SWITCH_PINS = [
    board.GP4,   # SW1 = OLED MODE CYCLE
    board.GP0,   # SW2 = NEXT
    board.GP29,  # SW3 = PREVIOUS
    board.GP1,   # SW4 = VOICE CHAT TOGGLE
    board.GP2,   # SW5 = PLAY/PAUSE
]

ENC_A = board.GP3
ENC_B = board.GP27
ENC_BTN = board.GP28

LED_PIN = board.GP26

volume_level = 50

# ----------------------------------------------------------
#                     SWITCH SCANNER
# ----------------------------------------------------------

keyboard.matrix = KeysScanner(
    pins=SWITCH_PINS,
    value_when_pressed=False,
)

keyboard.keymap = [
    [
        KC.NO,     # SW1 (handled in hook)
        KC.MNXT,   # SW2
        KC.MPRV,   # SW3
        KC.V,      # SW4 (voice chat toggle)
        KC.MPLY,   # SW5
    ]
]

# ----------------------------------------------------------
#                     ENCODER SETUP
# ----------------------------------------------------------

encoder = VolumeEncoderHandler()
keyboard.modules.append(encoder)

encoder.pins = ((ENC_A, ENC_B, ENC_BTN),)
encoder.map = [
    ((KC.VOLU,), (KC.VOLD,)),
]

# ----------------------------------------------------------
#                     LED SETUP
# ----------------------------------------------------------

# NeoPixel LED on single GPIO
NUM_LEDS = 1
led = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.3, auto_write=True)

mute_state = False
oled_mode = 0

# ----------------------------------------------------------
#              OLED SETUP (UPTIME CLOCK)
# ----------------------------------------------------------

oled = OLED(
    i2c=board.I2C(),
    width=128,
    height=32,
    fps=10,
)

display = Display(oled=oled)
keyboard.modules.append(display)

boot_time = time.monotonic()

@display.text_area
def oled_render(kbd):
    global oled_mode

    if oled_mode == 0:
        elapsed = int(time.monotonic() - boot_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        return [
            " My Custom PCB ",
            "",
            f"    {hours:02d}:{minutes:02d}:{seconds:02d}",
            "",
        ]
    elif oled_mode == 1:
        return [
            " My Custom PCB ",
            "",
            "   Mode: Custom",
            "",
        ]
    elif oled_mode == 2:
        return [
            "   _____   ",
            "  /     \\  ",
            " |  O O  | ",
            "  \\_____\\  ",
        ]
    elif oled_mode == 3:
        bars = int(volume_level / 10)
        bar_str = "|" * bars + " " * (10 - bars)
        return [
            " My Custom PCB ",
            "",
            f"Volume: [{bar_str}]",
            f"   {volume_level}%",
        ]

# ----------------------------------------------------------
#             LED LOGIC HOOK (IMPORTANT!)
# ----------------------------------------------------------

def after_matrix_scan(kbd):
    global prev_matrix_state, mute_state, oled_mode

    state = kbd.matrix_state

    for i in range(len(SWITCH_PINS)):
        prev = prev_matrix_state[i]
        now = state[i]

        if not prev and now:
            if i == 0:  # SW1: cycle OLED mode
                oled_mode = (oled_mode + 1) % 4  # cycle between 0, 1, 2, and 3

        prev_matrix_state[i] = now

    # Red if muted, blue if not muted
    if mute_state:
        led[0] = (255, 0, 0)   # red
    else:
        led[0] = (0, 0, 255)   # blue

keyboard.after_matrix_scan.append(after_matrix_scan)

# ----------------------------------------------------------
#                     START FIRMWARE
# ----------------------------------------------------------

if __name__ == "__main__":
    keyboard.go()
