import json
import subprocess

subprocess.call("./../ccv/bin/cnnclassify ig/926318230906423186_22097384.jpg ../ccv/samples/image-net-2012.sqlite3", shell=True)