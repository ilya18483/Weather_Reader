import bme680
import time
import datetime
import csv
from bh1745 import BH1745
from lsm303d import LSM303D

theDelay = 120
hum_baseline = 40.0
burn_datapoints = 300

fieldname = ["Unix", "Date","Time", "Temperature", "Pressure", "Humidity", "Colour", "Orientation","Gas Resistance", "Heat Stability"]
f_name = "CSVfile_" + str(datetime.date.today()) + ".csv"
print(f_name)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

bh1745 = BH1745()
lsm = LSM303D(0x1d)

for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

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

burn_in_data = []

print("Collecting gas resistance data for {} datapoints\n".format(burn_datapoints))
for i in range(burn_datapoints):
    if sensor.get_sensor_data() and sensor.data.heat_stable:
        gas = sensor.data.gas_resistance
        burn_in_data.append(gas)
        print("Gas resistance: {} Ohm".format(gas))
        time.sleep(1)

gas_baseline = sum(burn_in_data[-50:]) / 50.0
print("Gas baseline: {} Ohms".format(gas_baseline))

def write_headers(names):
    with open(f_name, "a") as f:
        thewriter = csv.DictWriter(f, fieldnames=names)
        thewriter.writeheader()
    while True:
        env_read(fieldname, theDelay, gas_baseline, hum_baseline)

def env_read(names, delay, GRbase, Humbase):
    if sensor.get_sensor_data():
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

        hum_weighting = 0.25
        gas_offset = GRbase - gas_resistance
        hum_offset = hum - Humbase

        if hum_offset >0:
            hum_score = (100 - Humbase - hum_offset)
            hum_score /= (100 - Humbase)
            hum_score *= (hum_weighting * 100)
        else:
            hum_score = (Humbase + hum_offset)
            hum_score /= Humbase
            hum_score *= (hum_weighting * 100)

        if gas_offset > 0:
            gas_score = (gas_resistance / GRbase)
            gas_score *= (100 - (hum_weighting * 100))
        else:
            gas_score = 100 - (hum_weighting * 100)

        air_quality_score = hum_score + gas_score
        print("IAQ Index: {}".format(air_quality_score))

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
                env_read(fieldname,theDelay, gas_baseline, hum_baseline)
        else:
            write_headers(fieldname)

try:
    ch(f_name)
except IOError:
    write_headers(fieldname)
except KeyboardInterrupt:
    bh1745.set_leds(0)
