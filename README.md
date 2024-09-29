# OpenWB-Scripts

These Scripts are designed to be used with files from OpenWB (www.openwb.de).

## OpenWB Parser

These Parser parse the log files and calculate how a battery would have improved the System.
The Improvement can either be saving in terms of cost of electrical energy (usage from power grid vs. feed to power grid),
or in terms of autarky.

The parser differ for the version 1.9 and 2.x as the log files are differently.
In version 1.9 the log files are available as CSV files and for version 2.x the log files can be requested in JSON format.

### Configuration for the script

Both versions use the same YAML configuration file format. An example file:
```
PV:
  peak: 10000
battery:
  cappacity: 16000
  max_charge_power: 10000
  max_discharge_power: 10000
  efficiency: 85
time:
  start: 2022-07-01
  end: 2024-06-30
LogFolder:
  Folder: "daily/"
OpenWB-IP:
  IP: OPENWB-IP
```
There are a few sections in the YAML file. The `PV` section lits all needed attributes of the photovoltaik system.
The `battery` section lists all attributes for the battery. The `time` section defines start and end date (both are included, a one dail parse starts and ends at the same date). And last section is the `LogFolder` section, this can be used to store the log files in different locations in case the validation for battery shall be done for different systems.

### Version for OpenWB 1.9

The OpenWB-Parser for version 1.9 is located in the subfolder `OpenWB-Parser_1.9`.

The log files need to be downloaded prior to using this script.
The log files are available at `http://OPENWB-IP/openWB/web/logging/data/daily/`.
With following linux command the log files can be downloaded:
```
cd OpenWB-Parser_1.9
mkdir daily
wget -P ./daily -r http://OPENWB-IP/openWB/web/logging/data/daily
```
In the above commands `OPENWB-IP` needs to be replaced by the actual IP address of the OpenWB server.

After downloading the log files and configuring the parser using the yaml file, the script can be used
```
python3 OpenWB-Parser.py
```

### Version for OpenWB 2.x

The OpenWB-Parser for version 2.x is located in the subfolder `OpenWB-Parser_2.x`.

Not implemented yet.