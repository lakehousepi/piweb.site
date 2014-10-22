import os
import glob
import time

class TempReader(object):
    def __init__(self, temp_sensor_pin):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
 
        self.temp_sensor_pin = temp_sensor_pin
        self.base_dir  = '/sys/bus/w1/devices/'
        counter = 0
        incomplete = True
        while counter < 5 and incomplete:
            try:
                self.device_folder = glob.glob(
                    self.base_dir + 
                    str(self.temp_sensor_pin) +
                    '*')[0]
                incomplete = False
            except IndexError:
                counter += 1
                time.sleep(10)
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)/1000.0
            temp_f = (temp_c * 180.0/100.0) + 32.0
        tempdict = {
            'temp_c': temp_c,
            'temp_f': temp_f
        }
        return tempdict
