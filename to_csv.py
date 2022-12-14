#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 2.7.X

# Aide : python to_csv.py --help

import xml.etree.ElementTree as Xet
import pandas as pd
import argparse, os

parser = argparse.ArgumentParser(description='XML to CSV')
parser.add_argument("-f", "--file", required=True, help="Chemin du fichier XML de métadonnées GeoNetwork")
parser.add_argument("-o", "--output_name", required=True, help="Nom du fichier de sortie CSV")
args = parser.parse_args()

cols = ["col", "type", "alias", "liste_valeurs"]
rows = []

namespaces = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gco': 'http://www.isotc211.org/2005/gco' }
### XML method
tree = Xet.parse(args.file)
root = tree.getroot()
nodes = root.findall('gmd:contentInfo/gmd:MD_FeatureCatalogue/gmd:featureCatalogue/gmd:FC_FeatureCatalogue/gmd:featureType/gmd:FC_FeatureType/gmd:carrierOfCharacteristics', namespaces)
for i in nodes:
    column_name = i.find('gmd:FC_FeatureAttribute/gmd:memberName', namespaces).text
    column_alias = i.find('gmd:FC_FeatureAttribute/gmd:definition/gco:CharacterString', namespaces).text
    column_type = i.find('gmd:FC_FeatureAttribute/gmd:valueType/gco:TypeName/gco:aName/gco:CharacterString', namespaces).text
    if i.find('gmd:FC_FeatureAttribute/gmd:listedValue', namespaces):
        column_list_values = []
        for v in i.findall('gmd:FC_FeatureAttribute/gmd:listedValue', namespaces):
            column_list_values.append(v.find('gmd:FC_ListedValue/gmd:code/gco:CharacterString', namespaces).text + ' : ' + v.find('gmd:FC_ListedValue/gmd:label/gco:CharacterString', namespaces).text)
    else:
        column_list_values = ''
    rows.append({ 
        "col": column_name,
        "type": column_type,
        "alias": column_alias,
        "liste_valeurs": column_list_values 
    })
df = pd.DataFrame(rows, columns=cols)
df.to_csv(args.output_name, sep=";", header=True, encoding='utf-8')

"""
# JSON method
import xmltodict
with open('C:\data\metadata\metadata-iso19139.xml', 'r') as f:
    data = xmltodict.parse(f.read(), encoding='utf-8')
    dataContent = data['gmd:MD_Metadata']['gmd:contentInfo']['gmd:MD_FeatureCatalogue']['gmd:featureCatalogue']['gmd:FC_FeatureCatalogue']['gmd:featureType']['gmd:FC_FeatureType']['gmd:carrierOfCharacteristics']
for i in dataContent:
    column_name = i['gmd:FC_FeatureAttribute']['gmd:memberName']
    column_alias = i['gmd:FC_FeatureAttribute']['gmd:definition']['gco:CharacterString']
    rows.append({"col": column_name,
                 "alias": column_alias })
df = pd.DataFrame(rows, columns=cols)
df.to_csv('C:\data\metadata\metadata.csv', sep=";", header=True, encoding='utf-8')
"""