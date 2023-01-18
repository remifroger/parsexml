#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 2.7.X

# Aide : python to_csv.py --help

import xml.etree.ElementTree as Xet
import pandas as pd
import argparse, os, sys

if not sys.version_info.major == 3 and sys.version_info.minor >= 6:
    print("Python 3.X ou plus est requis")
    print("Vous utilisez la version {}.{}".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)
else:
    print("Vous utilisez la version {}.{}".format(sys.version_info.major, sys.version_info.minor))
    print('Lancement')

parser = argparse.ArgumentParser(description='XML to CSV')
parser.add_argument("-f", "--file", required=True, help="Chemin du fichier XML de métadonnées GeoNetwork")
parser.add_argument("-o", "--output_name", required=True, help="Nom du fichier de sortie CSV")
parser.add_argument("-d", "--domain", required=False, help="Si vous souhaitez exporter les domaines")
args = parser.parse_args()

print("Fichier : {0}".format(args.file))

if (args.domain):
    cols = ["SHORT_NAME", "DESCRIPTION", "TYPE"]
    rows = []
    listDomaines = {}
    domainesCols = ["LABEL", "CODE", "DEFINITION"]
    domainesRows = []
else:
    cols = ["SHORT_NAME", "DESCRIPTION", "TYPE"]
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
    if i.find('gmd:FC_FeatureAttribute/gmd:listedValue', namespaces) and args.domain == "true":
        column_list_values = []
        listDomaines[column_name] = []
        for v in i.findall('gmd:FC_FeatureAttribute/gmd:listedValue', namespaces):
            column_list_values.append(v.find('gmd:FC_ListedValue/gmd:code/gco:CharacterString', namespaces).text + ' : ' + v.find('gmd:FC_ListedValue/gmd:label/gco:CharacterString', namespaces).text)
            column_domaine_code = v.find('gmd:FC_ListedValue/gmd:code/gco:CharacterString', namespaces).text 
            column_domaine_val = v.find('gmd:FC_ListedValue/gmd:label/gco:CharacterString', namespaces).text
            listDomaines[column_name].append({ 
                "LABEL": column_domaine_code,
                "CODE": column_domaine_val,
                "DEFINITION": ''
            })
    else:
        column_list_values = ''
    if (args.domain == "true"):
        rows.append({ 
            "SHORT_NAME": column_name,
            "DESCRIPTION": column_alias,
            "TYPE": column_type
            #"DOMAINES": column_list_values 
        })
    else:
        rows.append({ 
            "SHORT_NAME": column_name,
            "DESCRIPTION": column_alias,
            "TYPE": column_type
        })
    print('Ecriture de la colonne {0}'.format(column_name))
dirOutput = os.path.dirname(args.output_name)
if args.domain == "true":
    for x, y in listDomaines.items():
        fileName = "{0}.csv".format(x)
        pd.DataFrame(y, columns=domainesCols).to_csv(os.path.join(dirOutput, fileName), sep=";", header=True, encoding='utf-8', index=False)
df = pd.DataFrame(rows, columns=cols)
df.to_csv(args.output_name, sep=";", header=True, encoding='utf-8', index=False)

print('Terminé, métadonnées enregistrées dans {0}'.format(args.output_name))

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