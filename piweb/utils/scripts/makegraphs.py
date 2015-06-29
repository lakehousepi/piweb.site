from utils.config import pins
from utils.led import LEDController

import utils.graphing as pwgraphs

def make_and_store_graphs():
    green = LEDController(led_pin=pins.GREEN_LED)
    green.on()

    pwgraphs.make_four_graphs(savefile=True)

    green.off()
