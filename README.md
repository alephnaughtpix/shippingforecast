# The Shipping Forecast reader
https://github.com/alephnaughtpix/shippingforecast

v0.1 Michael James 2019-10-18

Output the latest Shipping Forecast as a spoken word MP3 file. 

This script uses the Met Office RSS feed for the forecast, XSLT to transform to readable text, and Google Text to Speech to
speak. Optionally, you can preface the forecast with a _[NOT INCLUDED]_ MP3 file containing the tune "Sailing By" (or indeed any theme).

You can configure the content of the output by editing the file `translate.xs`. Theoretically, this could be the basis 
of a generic speech to text internet reader.

### Technologies used:
* Google Text to Speech
* PyRubberband: https://pyrubberband.readthedocs.io/
* PyDub: https://github.com/jiaaro/pydub/
* PySoundfile: https://pysoundfile.readthedocs.io/
