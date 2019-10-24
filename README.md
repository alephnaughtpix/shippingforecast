# The Shipping Forecast reader
https://github.com/alephnaughtpix/shippingforecast

v0.2 Michael James 2019-10-24

Output the latest Shipping Forecast as a spoken word MP3 file. 

This script uses the Met Office RSS feed for the forecast, XSLT to transform to readable text, and Google Text to Speech to
speak. Optionally, you can preface the forecast with a _[NOT INCLUDED]_ MP3 file containing the tune "Sailing By" (or indeed any theme).

You can configure the content of the output by editing the file `translate.xsl`. Theoretically, this could be the basis 
of a generic speech to text internet reader.

### Usage
```
python3 .\process.py
```

### Technologies used:
* Google Text to Speech
* PyRubberband: https://pyrubberband.readthedocs.io/
* PyDub: https://github.com/jiaaro/pydub/
* PySoundfile: https://pysoundfile.readthedocs.io/

The simplest way to install the requirements is to go to the root of this project in the command line and type:
```
pip install -r requirements.txt
```
