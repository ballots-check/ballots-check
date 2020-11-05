import requests
import json
import os
from pathlib import Path
import pandas as pd
import subprocess
import sys
import time

PATH = Path(__file__).parent.resolve()
NUMBER_OF_THREADS = 5
#Call the scrapers in a number of parallel subprocesses
subs = []
for i in [1850, 1870, 1890, 1910, 1930]:
    subs.append(subprocess.Popen('"{0}" parallel.py {1}'.format(sys.executable, i), shell=True))
    
#If all scrapers are finished, merge the temp files again in main output file and save
while True:
    if all([False if x.poll() == None else True for x in subs]):
        print('all finished')
        break
    else:
        time.sleep(10)
