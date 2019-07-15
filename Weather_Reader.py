import bme680
import time
import datetime
import csv
from bh1745 import BH1745
from lsm303d import LSM303D

theDelay = 120

fieldname = ["Unix", "Date","Time", "Temperature", "Pressure", "Humidity", "Colour", "Orientation","Gas Resistance", "Heat Stability"]
f_name = "CSVfile_" + str(datetime.date.today()) + ".csv"
print(f_name)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

bh1745 = BH1745()
lsm = LSM303D(0x1d)

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

bh1745.setup()
bh1745.set_leds(1)
time.sleep(1)

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

def write_headers(names):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writeheader()
    while True:
        env_read(fieldname, theDelay)

def env_read(names, delay):
    tempa = sensor.data.temperature
    pres = sensor.data.pressure
    hum = sensor.data.humidity

    dt = time.time()
    d = datetime.date.today()
    ti = time.strftime("%H:%M:%S")

    r,g,b = bh1745.get_rgb_scaled()
    colour = '#{:02x}{:02x}{:02x}'.format(r, g, b)

    xyz = lsm.magnetometer()
    orientation = "{:+06.2f} : {:+06.2f} : {:+06.2f}".format(*xyz)

    heat_stability = sensor.data.heat_stable
    gas_resistance = sensor.data.gas_resistance
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writerow({"Unix":dt ,"Date": d, "Time": ti, "Temperature": tempa, "Pressure": pres, "Humidity": hum, "Colour":colour, "Orientation":orientation,"Gas Resistance":gas_resistance, "Heat Stability": heat_stability})
    time.sleep(delay)

def ch(file_name):
    with open(file_name, "r") as f:
        theReader = csv.reader(f)
        theNames = next(theReader)
        if theNames == fieldname:
            while True:
                env_read(fieldname,theDelay)
        else:
            write_headers(fieldname)

try:
    ch(f_name)
except IOError:
    write_headers(fieldname)
except KeyboardInterrupt:
    bh1745.set_leds(0)
