import bme680
import time
import datetime
from bh1745 import BH1745
from lsm303d import LSM303D

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

print('\n\nPolling:')
try:
    while True:
        if sensor.get_sensor_data():
            today = datetime.datetime.now()
            xyz = lsm.magnetometer()
            orientation = "Orientation: {:+06.2f} : {:+06.2f} : {:+06.2f}".format(*xyz)
            r,g,b = bh1745.get_rgb_scaled()
            colour = ('#{:02x}{:02x}{:02x}'.format(r, g, b))
            output = 'Date and Time: {5}Temperature: {0:.2f} C, Pressure: {1:.2f} hPa, Humidity: {2:.2f} %RH, {4}. Colour: {3}.'.format(
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity,
                colour,
                orientation,
                today)

            if sensor.data.heat_stable:
                print('{0}, Gas Resistance: {1} Ohms'.format(
                    output,
                    sensor.data.gas_resistance))

            else:
                print(output)

        time.sleep(1)

except KeyboardInterrupt:
    bh1745.set_leds(0)

