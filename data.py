#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit import update_name, mapping, expected

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]



'''
The shape_element function returns a dictionary, containing the shaped data for that element.
- the function processes only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" are turned into key/value pairs, except for the a) "created" array,
 and b) the "pos" array
- problematic characters in the second level tag "k" are ignored
- second level tags with "k" value starting with "addr:" are added to a dictionary "address"
'''

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :      
        created = {}
        for e in element.attrib.keys():
            if e in CREATED:
                created[e] = element.attrib[e]                
            elif  element.attrib[e] == element.get('lat') or element.attrib[e] == element.get('lon'):
                pos = [] # create position list
                pos.append(float(element.get('lat')))
                pos.append(float(element.get('lon')))
                node['pos'] = pos
            else:
                node[e] = element.get(e)
                node['type'] = element.tag
        node['created'] = created
        node_refs = []
        address = {}
        for subtag in element:
            if subtag.tag == 'tag':
                if re.search(problemchars, subtag.get('k')):
                    pass
                elif re.search(r'\w+:\w+:\w+', subtag.get('k')):
                    pass
                elif subtag.get('k').startswith('addr:') and subtag.get('k')[5:] == "street":   
                    address[subtag.get('k')[5:]] = update_name(subtag.get('v'),mapping)     # run update_name function to clean street type
                    node['address'] = address
                elif subtag.get('k').startswith('addr:') and subtag.get('k')[5:] == "postcode" and len(subtag.get('v')) < 5:    # skip postcodes with fewer than 5 digits
                    print 'skipping ', subtag.get('v')
                    pass
                elif subtag.get('k').startswith('addr:'):
                    address[subtag.get('k')[5:]] = subtag.get('v')
                    node['address'] = address
                else:
                    node[subtag.get('k')] = subtag.get('v')
            else:
                if subtag.tag == 'nd':
                    node_refs.append(subtag.get('ref'))
                else:
                    pass
        if node_refs:
            node['node_refs'] = node_refs  
        return node
    else:
        return None


'''
This process_map function will parse the map file, and call the shape_element function
'''

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


'''
This load_data function calls teh process_map function and loads the output into a MongoDB collection.
'''

def load_data():
    # NOTE: with a larger dataset, call the process_map procedure with pretty=False. 
    # The pretty=True option adds additional spaces to the output, making it significantly larger.
    data = process_map('sample-san-francisco_california.osm', False)
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.sfosm
    db.sfosm.insert(data)

if __name__ == "__main__":
    load_data()



