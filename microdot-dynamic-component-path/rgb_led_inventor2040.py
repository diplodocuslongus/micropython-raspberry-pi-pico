# specific for the inventor2040 from pimoroni
import time
# from machine import Pin,PWM
from inventor import Inventor2040W, NUM_LEDS

#RGB
RED = 0
GREEN = 1
BLUE = 2


"""
Displays a rotating rainbow pattern on Inventor 2040 W's onboard LED bars.

Press "User" to exit the program.
"""

# Constants
BRIGHTNESS = 0.4    # The brightness of the LEDs
UPDATES = 50        # How many times the LEDs will be updated per second

# Create a new Inventor2040W
board = Inventor2040W()

# Variables
offset = 0.0

# Class that wil interface with our RGB Module
class OnBoardLEDModule:
    def __init__(self, leds_idx):
        self.leds = leds_idx
        self.init_leds()
    
    # Initialize leds by turning off all led then blinking once the ones we want to interact with
    def init_leds(self):
        for i in range(NUM_LEDS):
            board.leds.set_rgb(i,0,0,0)
        for i in self.leds:
            board.leds.set_rgb(i,255,0,0)
            time.sleep(0.5)
            board.leds.set_rgb(i,0,0,0)
        
    # Turn off RGB
    def turn_off_rgb(self):
        for i in range(NUM_LEDS):
            board.leds.set_rgb(i,0,0,0)
        time.sleep(0.1)
    
    # Set RGB Color
    def set_rgb_color(self, color):
        red, green, blue = color
        self.turn_off_rgb()  
        for i in range(self.leds):
            board.leds.set_rgb(i,red,green,blue)
        
        
    

# Class that wil interface with our RGB Module
class RGBLEDModule:
    def __init__(self, pwm_pins):
        self.pwms = [PWM(Pin(pwm_pins[RED])),PWM(Pin(pwm_pins[GREEN])),
                PWM(Pin(pwm_pins[BLUE]))]
        self.init_pwms()
    
    # Initialize PWM Pins
    def init_pwms(self):
        for pwm in self.pwms:
            pwm.freq(1000)
    
    # Deinitialize PWM fins
    def deinit_pwms(self):
        self.turn_off_rgb()
        for pwm in self.pwms:
            pwm.deinit()
    
    # Map RGB values from 0-255 to duty cycle 0-65535
    def map_range(self, x, in_min, in_max, out_min, out_max):
      return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    # Turn off RGB
    def turn_off_rgb(self):        
        self.pwms[RED].duty_u16(0)
        self.pwms[GREEN].duty_u16(0)
        self.pwms[BLUE].duty_u16(0)
        time.sleep(0.1)
    
    # Set RGB Color
    def set_rgb_color(self, color):
        red, green, blue = color
        
        self.turn_off_rgb()  
        
        self.pwms[RED].duty_u16(self.map_range(red, 0, 255, 0, 65535))
        self.pwms[GREEN].duty_u16(self.map_range(green, 0, 255, 0, 65535))
        self.pwms[BLUE].duty_u16(self.map_range(blue, 0, 255, 0, 65535))

# standalone test
rgb_led_module = OnBoardLEDModule([0 , 1, 5])
