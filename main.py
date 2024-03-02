# SPDX Apache:2.0

from pydantic import BaseModel
from fastapi import FastAPI
from colour_system import *
import numpy as np
from scipy.constants import h, c, k

app = FastAPI()


# Spretrum and RGB are the two objects pased as JSON into and
# out of the REST API
# Use pydantic to handle these by extending from BaseModel
class Spectrum(BaseModel):
    freq: list = []


class RGB(BaseModel):
    hdtv_hex: str
    srgb_hex: str
    hdtv_rgb: list = []
    srgb_rgb: list = []


## Utility to convert text HEX values to RGB int values
def hex_to_rgb(hexa):
    hexa = hexa.lstrip("#")
    rgb = []
    for i in (0, 2, 4):
        rgb.append(int(hexa[i : i + 2], 16))
    return rgb


# Returns the spectral radiance, B(lam, T), in W.sr-1.m-2 of a black body
# at temperature T (in K) at a wavelength lam (in nm), using Planck's law.
#
# Algorthm here is clear by inspection so no need for comments :-)
def planck(lam, T):
    lam_m = lam / 1.0e9
    fac = h * c / lam_m / k / T
    B = 2 * h * c**2 / lam_m**5 / (np.exp(fac) - 1)
    return B


@app.post("/spectrum/")
def read_item(spec: Spectrum) -> RGB:
    spec = np.array(spec.freq)
    print(spec)

    # use the abridge set of colour frequencies here
    hdtv = ColourSystem.HDTV(MatchSpace.ABRIDGED).spec_to_rgb(spec, out_fmt="html")
    srgb = ColourSystem.SRGB(MatchSpace.ABRIDGED).spec_to_rgb(spec, out_fmt="html")

    r = RGB(
        hdtv_hex=hdtv,
        srgb_hex=srgb,
        hdtv_rgb=hex_to_rgb(hdtv),
        srgb_rgb=hex_to_rgb(srgb),
    )
    print(r)
    return r


@app.post("/temperature/")
def colour_temp(temp: int) -> RGB:

    # full range of frequencies here
    lam = np.arange(380.0, 781.0, 5)
    spec = planck(lam, temp)

    hdtv = ColourSystem.HDTV(MatchSpace.FULL).spec_to_rgb(spec, out_fmt="html")
    srgb = ColourSystem.SRGB(MatchSpace.FULL).spec_to_rgb(spec, out_fmt="html")

    r = RGB(
        hdtv_hex=hdtv,
        srgb_hex=srgb,
        hdtv_rgb=hex_to_rgb(hdtv),
        srgb_rgb=hex_to_rgb(srgb),
    )
    print(r)
    return r
