'''
THE SHIPPING FORECAST READER
https://github.com/alephnaughtpix/shippingforecast

v0.1 Michael James 2019-10-18

Output the latest Shipping Forecast as a spoken word MP3 file. 

This script uses the Met Office RSS feed for the forecast, XSLT to transform to readable text, and Google Text to Speech to
speak. Optionally, you can preface the forecast with an MP3 file containing the tune "Sailing By" (or indeed any theme).

You can configure the content of the output by editing the file 'translate.xsl'. Theoretically, this could be the basis 
of a generic speech to text internet reader.
'''

import requests
import lxml.etree as ET
from gtts import gTTS 
from pydub import AudioSegment
import pyttsx3

THEME_TUNE = True       # OPTIONAL: Include the unofficial theme tune "Sailing By" before the forecast. (If you have an MP3 of it.)

# Trying with examples from https://pythonprogramminglanguage.com/text-to-speech/
USE_PYTTS = False
USE_WATSON = False

source_url = 'https://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest'    # URL of Shipping Forecast feed
xml_filename = 'source.xml'         # Saved RSS of Shipping Forecast
xsl_filename = 'translate.xsl'      # Translates RSS to human readable text
script_filename = 'script.txt'      # Human readable version of Shipping Forecast
source_mp3 = "output.mp3"           # Text to speech result
theme_mp3 = "sailingby.mp3"         # "Sailing By" by Ronald Binge - Used by Radio 4 late night Shipping Forecast broadcast.
                                    # ^^^ You'll need to supply this yourself!!!

response = requests.get(source_url)
source_text = response.text

# Get Shipping Forecast RSS
file = open(xml_filename,'w')
file.write(source_text)
file.close()

# Translate Shipping forecast RSS to human readable text for Text to Speech
dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
output = " ".join(str(newdom).split())                  # Strip extra spaces
output = output.replace('<?xml version="1.0"?>', '')    # Remove XML header.
file = open(script_filename,'w')
file.write(output)
file.close()

# PyTTS - In case we don't have internet access. Sounds a bit robotic and US-ian
if USE_PYTTS == True:
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()
else:
    # Watson - TODO
    if USE_WATSON == True:
        engine = pyttsx3.init()
        engine.say(output)
        engine.runAndWait()
    else:
        # Google Text to speech
        engine = gTTS(text=output, lang='en-UK', slow=False) 
        engine.save(source_mp3)
        if THEME_TUNE:
            theme_src = AudioSegment.from_mp3(theme_mp3)
            feature_src = AudioSegment.from_mp3(source_mp3)
            programme_start = len(theme_src) - (6 * 1000)
            programme_length = programme_start + len(feature_src)
            playlist = AudioSegment.silent( duration=programme_length )
            programme = playlist.overlay(theme_src).overlay(feature_src, position=programme_start)
            programme.export("output_with_theme.mp3", format="mp3")

