import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "sample-san-francisco_california.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # find street type


expected = set(["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "West", "Mason", "Way", "Circle", "Alameda", "Highway",
             "Center", "Real", "Columbus", "East", "Embarcadero","A","Airport","Alley","Broadway",
             "Cumbre","D","3","A","Gardens","I-580","Las","Ic","Loop","Marina","Market/Noe","Ora",
             "Path","Plaza","Southgate","Steps","Terrace","Vallejo","Walk","I-580)"])

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd": "Road",
            "Rd.": "Road",
            "St.": "Street",
            "st": "Street",
            "avenue": "Avenue",
            "Plz": "Plaza",
            "Blvd": "Boulevard"
            }

'''
The update_name function takes a street name, 
determines if the name contains an incosistent street type, and if so, 
returns a cleaned version of the street type.
'''

def update_name(name, mapping):
        m = street_type_re.search(name)
        if m.group() not in expected:
            try:
                name = re.sub(m.group(), mapping[m.group()], name)
            except:
                print mapping, m.group(), len(m.group()), '|' + m.group() + '|'
                print type(m.group()), type(expected['Columbus'])
                exit()
        return name