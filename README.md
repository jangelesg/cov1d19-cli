#  Covid19 CLI-Tracker Tool

**Version 1.0.0**

A tool to track down statistics of COVID-19 via command line interface 
 ---
 ## License and Copyright 
 This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
---
## Contributors 
-  Jonathan Angeles <jangelesg@gangsecurity.com>
-  Odi mathdroid https://github.com/mathdroid
## Resources 
- https://services7.arcgis.com/4RQmZZ0yaZkGR1zy/arcgis/rest/services/COV19_Public_Dashboard_ReadOnly/
- https://alpublichealth.maps.arcgis.com/
- https://covid19.mathdro.id/api/

---
## Installation

user@CS38:~/cov1d19-cli$ python setup.py install --user

---
## Usage 
- python c0v1d19-cli-tracker.py --cd italy 
- python c0v1d19-cli-tracker.py --cr usa
- python c0v1d19-cli-tracker.py --gs
- python c0v1d19-cli-tracker.py -h

usage: c0v1d19-cli-tracker.py [-h] [--gs] [--gc] [--gr] [--gd] [--d] [--dt DT] [--c] [--cs CS] [--cc CC] [--cr CR] [--cd CD] [--ac]

optional arguments:
  -h, --help  show this help message and exit
  --gs        Show global Summary
  --gc        Global cases per region sorted by confirmed cases
  --gr        Global cases per region sorted by recovered cases
  --gd        Global cases per region sorted by death toll
  --d         Global cases per day
  --dt DT     Detail of updates in a (e.g. python3 c0v1d19-cli-tracker.py --dt 2-14-2020)
  --c         All countries and their ISO codes
  --cs CS     A [country] Summary (e.g. python3 c0v1d19-cli-tracker.py --sc JAPAN)
  --cc CC     A [country] Cases per region sorted by confirmed cases (e.g. python3 c0v1d19-cli-tracker.py --cc JAPAN)
  --cr CR     A cases per region sorted by recovered cases (e.g. python3 c0v1d19-cli-tracker.py --cr JAPAN)
  --cd CD     A cases per region sorted by death toll (e.g. python3 c0v1d19-cli-tracker.py --cd JAPAN)
  --ac        Alabama region sorted by counties, and Summary

Email: jangeles@gangsecurity.com
Code: https://github.com/jangelesg/cov1d19-cli
Better Safe, than Sorry!!
It's Covit19 Virus not a Chinese Virus 

## Screen Shoot 

![](https://github.com/jangelesg/cov1d19-cli/blob/master/tools/covid19_1.gif)

