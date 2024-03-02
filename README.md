# Spectrum RGB

**_Essential REST API service to convert Spectrum to RGB & Colour Temperature to RGB_**

- Python REST API using [FastAPI](https://fastapi.tiangolo.com/)
- Docker image via github actions (arm and x86)
- Tailoured for frequences from [AdaFruti AS7341](https://learn.adafruit.com/adafruit-as7341-10-channel-light-color-sensor-breakout)
- Generate RGB values for specific colour temperature

## Theory

Firstly, colo[u]r(1) theory is a large and complex topic.  Add in how your brain perceives colours.  You have been warned! 

Overacall context for this was to take the the sprectrum values from the [Adafruit AS7341](https://www.adafruit.com/product/4698) and convert that to a RGB value that can be sent to a tri-colour LED or strip. There is a tri-colour LED strip in the office that I wanted to control. 

Idea being that the colour of the LED would reflect the outside colour; by adding in the ability to convert colour temperature to RGB is a bonus. 

Specifically the I'm aiming for 'emperically perceptually equivalent'. (_i.e._ it looked ok-ish). This will only ever be an aproximation; but this is not intended for serious scientific use. 

## AS7341

This outputs counts for a number of frequencies: 415nm, 445nm, 480nm, 515nm, 555nm, 590nm, 630nm, 680nm
In addition there near-ir counts, but I've stuck with the visible counts.

As an example here's the distribution of these frequencies currently getting. ![](./_docs/Screenshot%202023-03-11%20091356.png)

The sensor gets these values to a MQTT topic, so the Node-Red flow is processing these already; but it need to get the RGB value to send to the LEDs.

## Spectrum to RGB Conversion

A [superb post on the SciPython](https://scipython.com/blog/converting-a-spectrum-to-a-colour/) site provided the theory and also some python code that was very close to what was needed. This specifically calculates the RGB for given colour temperature; colour temperature was converted to a spectrum of wave lengths, and then to RGB.

The code here is to a very large extent taken from the code on that page; with two changes:

- The sprectrum it uses is frequencies from 380nm increase in 5nm increments. With only 8 entires in the AS7341 spectrum this need some changes. The `cie-cmf.txt` file was reduced to just the frequencies I had (the `abrdiged-cie-cmf.txt` file). Suspect that this is a source of loss of accuracy. How wide the frequency response of the sensor is I don't know.

- Some refectoring to make it easier to handle


## REST API

Using the [FastAPI](https://fastapi.tiangolo.com/) it was straightforward to create a simple Python REST api that would accept a simple JSON structure with the frequency counts. Process this via the algorithm above, and return RGB values (both in hex and int styles) in a JSON structure. 

Similarly the API can is also converting a colour temperature to a spectrum for conversion to RGB. This is using the full range as per the original code. 

That's it really, built into a docker image via github actions - ready to be deployed into my Portainer configuration.

## Deployment

Briefly, the system is configured as follows:

- Arduino captures sensor values, and sends via 433Mhz
- RaspberryPi I've called the 'EdgeController' receives the 433Mhz signal, and forwards on via MQTT
- Node-RED flow triggered by MQTT. This takes the spectrum count array, passes to this SpectrumRGB service, and then publishes on MQTT
- PicoW is subscribed to MQTT and does the LED strip control

## Development Notes

- Using [Poetry](https://python-poetry.org/) for handling the depdencies of the python project; currently seems to be leading tool and handles most situations well.
- As above, this is using FastAPI. Previously used [uvicorn](https://www.uvicorn.org/), but recently I've [had issues](https://stackoverflow.com/questions/76371195/how-to-make-a-json-post-request-from-java-client-to-python-fastapi-server/78076530#78076530) with that and HTTP/2, so using [hypercord](https://pgjones.gitlab.io/hypercorn/).  Purely a pragmatic decision.

## Notes

[^1]: Yes I'm British, so it will be spelt with a u from now on :-)
