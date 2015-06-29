from utils.config import pins
from utils.led import LEDController

import utils.graphing as pwgraphs

def makegraphs():
    green = LEDController(led_pin=pins.GREEN_LED)
    green.on()

    pwgraphs.make_four_graphs(savefile=True)

    green.off()
