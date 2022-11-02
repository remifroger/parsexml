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

cols = ["col", "alias"]
rows = []

namespaces = {'gmd': 'http://www.isotc211.org/2005/gmd', 'gco': 'http://www.isotc211.org/2005/gco' }
tree = Xet.parse('C:\data\metadata\metadata-iso19139.xml')
root = tree.getroot()
nodes = root.findall('gmd:contentInfo/gmd:MD_FeatureCatalogue/gmd:featureCatalogue/gmd:FC_FeatureCatalogue/gmd:featureType/gmd:FC_FeatureType/gmd:carrierOfCharacteristics', namespaces)
for i in nodes:
    column_name = i.find('gmd:FC_FeatureAttribute/gmd:memberName', namespaces).text.strip()
    column_alias = i.find('gmd:FC_FeatureAttribute/gmd:definition/gco:CharacterString', namespaces).text.strip()
    rows.append({"col": column_name,
                 "alias": column_alias })
df = pd.DataFrame(rows, columns=cols)
df.to_csv('C:\data\metadata\metadata.csv', sep=";", header=True, encoding='utf-8')