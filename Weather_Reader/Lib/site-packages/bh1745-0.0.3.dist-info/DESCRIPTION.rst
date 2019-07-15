BH1745 Colour Sensor
====================

Most suited to detecting the illuminance and colour temperature of
ambient light, the BH1745 senses Red, Green and Blue light and converts
it to 16bit digital values.

Installing
==========

Stable library from PyPi:

-  Just run ``sudo pip install bh1745``

Latest/development library from GitHub:

-  ``git clone https://github.com/pimoroni/bh1745-python``
-  ``cd bh1745-python``
-  ``sudo ./install.sh``
0.0.3
-----

* Automagically call setup if not called by user
* Allow setup() to try alternate i2c addresses
* Added .ready() to determine if sensor is setup

0.0.2
-----

* Bumped i2cdevice dependency to >=0.0.4

0.0.1
-----

* Initial Release


