# GeoNetwork XML parser

Manipulation de fichiers XML (iso19139)

## to_csv

Transforme un export XML des métadonnées (iso19139) en CSV  
*Le format iso19139 est accessible depuis l'export ZIP d'une fiche de métadonnées*

En savoir plus sur la norme ISO/TS 19139:2007 : https://www.iso.org/fr/standard/32557.html

### Aide

```shell
python main.py --help
```

```
usage: to_csv.py [-h] -f FILE -o OUTPUT_NAME

XML to CSV

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Chemin du fichier XML de métadonnées GeoNetwork
  -o OUTPUT_NAME, --output_name OUTPUT_NAME
                        Nom du fichier de sortie CSV
  -d DOMAINE, --domaine DOMAINE Si vous souhaitez exporter les domaines
```

### Exemple d'usage

Sans domaine
```shell
python "C:\xmlparser\to_csv.py" -f C:\data\metadata\metadata-iso19139.xml -o C:\data\metadata\metadata.csv
```

Avec domaines
```shell
python "C:\xmlparser\to_csv.py" -f C:\data\metadata\metadata-iso19139.xml -o C:\data\metadata\metadata.csv -d true
```