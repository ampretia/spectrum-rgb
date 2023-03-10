
from pydantic import BaseModel
from fastapi import FastAPI
from colour_system import *
import numpy as np

app = FastAPI()

class Spectrum(BaseModel):
    freq: list = []

class RGB(BaseModel):
    hdtv_hex: str
    srgb_hex: str
    hdtv_rgb: list = []
    srgb_rgb: list = []

def hex_to_rgb(hexa):
    hexa = hexa.lstrip('#')
    rgb = []
    for i in (0,2,4):
        rgb.append(int(hexa[i:i+2], 16))
    return rgb

@app.post("/spectrum/")
def read_item(spec: Spectrum) -> RGB:
    spec = np.array(spec.freq)
    print(spec)
    hdtv = cs_hdtv.spec_to_rgb(spec, out_fmt='html')
    srgb = cs_srgb.spec_to_rgb(spec, out_fmt='html')
    
    r = RGB(hdtv_hex=hdtv, srgb_hex=srgb, hdtv_rgb=hex_to_rgb(hdtv),srgb_rgb=hex_to_rgb(srgb))
    print(r)
    return r