# Spectrum RGB

**_Essential REST API service to convert spectrum to RGB_**

- Python REST API using [FastAPI](https://fastapi.tiangolo.com/)
- Docker image via github actions (arm and x86)
- Tailored for frequencies from [AdaFruti AS7341](https://learn.adafruit.com/adafruit-as7341-10-channel-light-color-sensor-breakout)

## Theory

Firstly, colo[u]r theory is a large topic, very very large - you have been warned!

The idea was to take the spectrum values from the Adafruit AS7341 and convert that to a RGB value that can be sent to a tri-colour LED or strip.

This is link in with an outdoor light sensor and the WS8212B led strip in the office. 

### AS7341

This outputs counts for a number of frequencies: 415nm, 445nm, 480nm, 515nm, 555nm, 590nm, 630nm, 680nm
In addition there near-ir counts, but I've stuck with the visible counts.

As an example here's the distribution of these frequencies currently getting. ![](./_docs/Screenshot%202023-03-11%20091356.png)

The sensor gets these values to a MQTT topic, so the Node-Red flow is processing these already; but it need to get the RGB value to send to the LEDs.

### Spectrum to RGB Conversion

Being a photographer I knew that the theory here was immense, so knew to be careful looking for the conversion algorithm. Specifically the aim was to get a 'empirically perceptually equivalent'. (_i.e._ it looked ok-ish).

A [superb post on the SciPython](https://scipython.com/blog/converting-a-spectrum-to-a-colour/) site provided the theory and also some python code that was very close to what was needed. This specifically calculates the RGB for given colour temperature; colour temperature was converted to a spectrum of wave lengths, and then to RGB.

The code here is to a very large extent taken from the code on that page; with two changes:

- I didn't need the colour temperature to spectrum function
- The spectrum it uses is frequencies from 380nm increase in 5nm increments. With only 8 entires in the AS7341 spectrum this need some changes. The `cie-cmf.txt` file was reduced to just the frequencies I had (the `aprox.txt` file). 

### REST API

Using the [FastAPI](https://fastapi.tiangolo.com/) it was straightforward to create a simple Python REST api that would accept a simple JSON structure with the frequency counts. Process this via the algorithm above, and return RGB values (both in hex and int styles) in a JSON structure. 

That's it really, built into a docker image via github actions - ready to be deployed into my [Portainer](https://www.portainer.io/) configuration.

## Deployment

Briefly, the system is configured as follows:

- Arduino captures sensor values, and sends via 433Mhz
- RaspberryPi I've called the 'EdgeController' receives the 433Mhz signal, and forwards on via MQTT
- Node-RED flow triggered by MQTT. This takes the spectrum count array, passes to this SpectrumRGB service, and then publishes on MQTT
- PicoW is subscribed to MQTT and does the LED strip control
