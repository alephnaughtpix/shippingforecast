'''
THE SHIPPING FORECAST READER
https://github.com/alephnaughtpix/shippingforecast

v0.2 Michael James 2019-10-24

Output the latest Shipping Forecast as a spoken word MP3 file. 

This script uses the Met Office RSS feed for the forecast, XSLT to transform to readable text, and Google Text to Speech to
speak. Optionally, you can preface the forecast with an MP3 file containing the tune "Sailing By" (or indeed any theme).

You can configure the content of the output by editing the file 'translate.xsl'. Theoretically, this could be the basis 
of a generic speech to text internet reader.

Technologies used:
* Google Text to Speech
* PyRubberband: https://pyrubberband.readthedocs.io/
* PyDub: https://github.com/jiaaro/pydub/
* PySoundfile: https://pysoundfile.readthedocs.io/
'''
from datetime import datetime
from gtts import gTTS 
import lxml.etree as ET
import numpy as np
import os
import os.path
from pydub import AudioSegment
import pyrubberband as pyrb
import pyttsx3
import soundfile as sf
import requests
import time

start = time.time()
print('''
THE SHIPPING FORECAST READER
https://github.com/alephnaughtpix/shippingforecast
v0.2 Michael James 2019-10-24
''')
print("Creating shipping forecast at:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print()

THEME_TUNE = True           # OPTIONAL: Include the unofficial theme tune "Sailing By" before the forecast. (If you have an MP3 of it.)
REMOVE_TEMP_FILES = True    # Remove temp files after processsing
PITCH_SHIFT = True          # Pitch shift voice down
COMPRESS_DYNAMICS = False    # Compress overall result (Takes much longer)

# Trying with examples from https://pythonprogramminglanguage.com/text-to-speech/
USE_PYTTS = False
USE_WATSON = False

source_url = 'https://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest'    # URL of Shipping Forecast feed
xml_filename = 'source.xml'         # Saved RSS of Shipping Forecast
xsl_filename = 'translate.xsl'      # Translates RSS to human readable text
script_filename = 'script.txt'      # Human readable version of Shipping Forecast
source_mp3 = "speech.mp3"           # Text to speech result
pitch_file = "output_pitch.flac"    # Pitch-shifted Text to speech result
theme_mp3 = "sailingby.mp3"         # "Sailing By" by Ronald Binge - Used by Radio 4 late night Shipping Forecast broadcast.
                                    # ^^^ You'll need to supply this yourself!!!
combined_file = "output_with_theme.mp3"
output_file = "output.mp3"
if PITCH_SHIFT:
    speech_file = pitch_file
else:
    speech_file = source_mp3

# Get Shipping Forecast RSS
print('Calling Met Office for latest Shipping Forecast.')
response = requests.get(source_url)
source_text = response.text

# Save on local system
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
print('Downloaded shipping forecast data, converting to speech')

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
        print('Converted to speech.')
        if PITCH_SHIFT:
            print('Changing pitch')
            word_src = AudioSegment.from_mp3(source_mp3)
            sample_rate = word_src.frame_rate
            samples = np.array(word_src.get_array_of_samples())
            pitched_down = pyrb.pitch_shift(samples, sample_rate, n_steps=-4)
            sf.write(pitch_file, pitched_down, sample_rate)
            if REMOVE_TEMP_FILES:
                os.remove(source_mp3)
            print('Changed pitch')
                
if os.path.exists(output_file):
    os.remove(output_file)
        
if THEME_TUNE:
    print('Adding theme tune')
    theme_src = AudioSegment.from_mp3(theme_mp3).normalize()        # Get theme tune
    feature_src = AudioSegment.from_file(speech_file).normalize()   # Get spoken word
    programme_start = len(theme_src) - (6 * 1000)                   # Speech starts 6 seconds before the theme is complete
    programme_length = programme_start + len(feature_src)           # Combined programme is the combined length of the two files minus 6 seconds
    playlist = AudioSegment.silent( duration=programme_length )     # Make new blank segment with the combine programme length
    programme = playlist.overlay(theme_src).overlay(feature_src, position=programme_start)  # Overlay theme and speech onto blank segment
    if COMPRESS_DYNAMICS:
        print('Compressing result')
        programme = programme.compress_dynamic_range()
    programme.export(combined_file, format="mp3")
    if REMOVE_TEMP_FILES:
        os.rename(combined_file, output_file)
    print('Added theme tune')
else:
    if REMOVE_TEMP_FILES:
        os.rename(speech_file, output_file)
        
if REMOVE_TEMP_FILES:
    os.remove(speech_file)
    os.remove(script_filename)
    os.remove(xml_filename)

duration = round(time.time() - start)
print('Shipping Forecast created in', duration, 'seconds.')
