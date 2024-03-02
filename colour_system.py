#
# colour_system.py
# https://scipython.com/blog/converting-a-spectrum-to-a-colour/

import numpy as np

from enum import Enum


class MatchSpace(Enum):
    FULL = 1
    ABRIDGED = 2


# Return the vector (x, y, 1-x-y).
def xyz_from_xy(x, y):

    return np.array((x, y, 1 - x - y))


# A colour system defined by the CIE x, y and z=1-x-y coordinates of
# its three primary illuminants and its "white point".
class ColourSystem:

    #  Pass vectors (ie NumPy arrays of shape (3,)) for each of the
    #  red, green, blue  chromaticities and the white illuminant
    #  defining the colour system.
    def __init__(self, red, green, blue, white, matchSpace: MatchSpace):
        # The CIE colour matching function for 380 - 780 nm in 5 nm intervals
        if matchSpace == MatchSpace.FULL:
            self.cmf = np.loadtxt("cie-cmf.txt", usecols=(1, 2, 3))
        else:
            self.cmf = np.loadtxt("abridged-cie-cmf.txt", usecols=(1, 2, 3))

        # Chromaticities
        self.red, self.green, self.blue = red, green, blue
        self.white = white

        # The chromaticity matrix (rgb -> xyz) and its inverse
        self.M = np.vstack((self.red, self.green, self.blue)).T
        self.MI = np.linalg.inv(self.M)
        
        # White scaling array
        self.wscale = self.MI.dot(self.white)
        
        # xyz -> rgb transformation matrix
        self.T = self.MI / self.wscale[:, np.newaxis]

    # Transform from xyz to rgb representation of colour.
    #
    # The output rgb components are normalized on their maximum
    # value. If xyz is out the rgb gamut, it is desaturated until it
    # comes into gamut.
    #
    # By default, fractional rgb components are returned; if
    # out_fmt='html', the HTML hex string '#rrggbb' is returned.
    def xyz_to_rgb(self, xyz, out_fmt=None):
        rgb = self.T.dot(xyz)
        if np.any(rgb < 0):
            # We're not in the RGB gamut: approximate by desaturating
            w = -np.min(rgb)
            rgb += w
        if not np.all(rgb == 0):
            # Normalize the rgb vector
            rgb /= np.max(rgb)

        if out_fmt == "html":
            return self.rgb_to_hex(rgb)
        return rgb

    # Convert from fractional rgb values to HTML-style hex string.
    def rgb_to_hex(self, rgb):

        hex_rgb = (255 * rgb).astype(int)
        return "#{:02x}{:02x}{:02x}".format(*hex_rgb)

    # Convert a spectrum to an xyz point.
    # The spectrum must be on the same grid of points as the colour-matching
    # function, self.cmf: 380-780 nm in 5 nm steps.
    def spec_to_xyz(self, spec):
        XYZ = np.sum(spec[:, np.newaxis] * self.cmf, axis=0)
        den = np.sum(XYZ)
        if den == 0.0:
            return XYZ
        return XYZ / den

    # Convert a spectrum to an rgb value.
    def spec_to_rgb(self, spec, out_fmt=None):

        xyz = self.spec_to_xyz(spec)
        return self.xyz_to_rgb(xyz, out_fmt)

    @classmethod
    def HDTV(cls, matchSpace: MatchSpace):
        illuminant_D65 = xyz_from_xy(0.3127, 0.3291)
        return cls(
            red=xyz_from_xy(0.67, 0.33),
            green=xyz_from_xy(0.21, 0.71),
            blue=xyz_from_xy(0.15, 0.06),
            white=illuminant_D65,
            matchSpace=matchSpace,
        )

    @classmethod
    def SMPTE(cls, matchSpace: MatchSpace):
        illuminant_D65 = xyz_from_xy(0.3127, 0.3291)
        return cls(
            red=xyz_from_xy(0.67, 0.33),
            green=xyz_from_xy(0.21, 0.71),
            blue=xyz_from_xy(0.15, 0.06),
            white=illuminant_D65,
            matchSpace=matchSpace,
        )

    @classmethod
    def SRGB(cls, matchSpace: MatchSpace):
        illuminant_D65 = xyz_from_xy(0.3127, 0.3291)
        return cls(
            red=xyz_from_xy(0.64, 0.33),
            green=xyz_from_xy(0.30, 0.60),
            blue=xyz_from_xy(0.15, 0.06),
            white=illuminant_D65,
            matchSpace=matchSpace,
        )
