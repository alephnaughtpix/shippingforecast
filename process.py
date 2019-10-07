import requests
import lxml.etree as ET
from gtts import gTTS 
import pyttsx3

USE_PYTTS = False

source_url = 'https://www.metoffice.gov.uk/public/data/CoreProductCache/ShippingForecast/Latest'
xml_filename = 'source.xml'
xsl_filename = 'translate.xsl'
script_filename = 'script.txt'

response = requests.get(source_url)
source_text = response.text

file = open(xml_filename,'w')
file.write(source_text)
file.close()

dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
output = " ".join(str(newdom).split())
output = output.replace('<?xml version="1.0"?>', '')
file = open(script_filename,'w')
file.write(output)
file.close()

if USE_PYTTS == True:
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()
else:
    engine = gTTS(text=output, lang='en', slow=False) 
    engine.save("output.mp3") 