import numpy as np
from colour_system import cs_hdtv

cs = cs_hdtv



spec = np.array([154.,918.,806.,1156.,1496.,1498.,1270.,786.])


html_rgb = cs.spec_to_rgb(spec, out_fmt='html')
print(html_rgb)

