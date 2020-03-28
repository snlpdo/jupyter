#!/usr/bin/env python3

''' 
Constantes et fonctions qui permettent de récupérer des tuiles d'images
du site Géoportail.

L'utilisation de certaines fonction nécessite l'obtention
d'une clé valide à récupérer sur http://professionnels.ign.fr/
et à stocker dans CLE_IGN.

R. Grosbois - Lycée de Vizille - 2019.
'''

import math
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS
import requests

R_TERRE = 6_378_137
CIRCONF = int(2 * math.pi * R_TERRE)

def wmts(latitude, longitude):
    '''
    Calcule les coordonnées WMTS (en mètres)
    d'une géolocalisation donnée (latitude et longitude en degrés)
    '''
    return (CIRCONF/2 + R_TERRE * math.radians(longitude),
        CIRCONF/2 - R_TERRE * math.log(math.tan(math.radians(latitude)/2 + math.pi/4)) )

def etendue_tuile(niveau):
    '''Calculer l'étendue (en m) couverte par chaque tuile d'un niveau donné.'''
    return (CIRCONF / (2**niveau))

def tuile_info(latitude, longitude, niveau=7):
    '''
    Calcule les indices de ligne et de colonne de la tuile
    contenant la géolocalisation ainsi que les coordonnées
    x et y (en pixel) de cette géolocalisation dans cette
    tuile.
    '''
    
    cote = etendue_tuile(niveau)
    coord = wmts(latitude, longitude)
    ligne, colonne = int(coord[1]/cote), int(coord[0]/cote)
    x = int(math.modf(coord[0]/cote)[0] * 256)
    y = int(math.modf(coord[1]/cote)[0] * 256)
    return ligne, colonne, x, y

def tuile(l, c, niveau=7, ortho=False, dispInfo=False):
    # Différents serveurs WMTS
    url = f"http://a.tile.openstreetmap.fr/hot/{niveau}/{c}/{l}.png"
    t = Image.open(requests.get(url, stream=True).raw)
    if dispInfo:
        t = t.convert("RGBA")
        draw = ImageDraw.Draw(t)
        draw.rectangle([0,0,255,255], outline=(0,0,0,255))
        draw.text((5,5), f"({l},{c})/{niveau}",fill=(0,0,0,255))
    return t

def geotuile(latitude, longitude, niveau=7, ortho=False, dispLoc=False, dispInfo=False):
    (l,c, x, y) = tuile_info(latitude, longitude, niveau)
    t = tuile(l, c, niveau, ortho,dispInfo)
    if dispLoc:
        t = t.convert("RGBA")
        draw = ImageDraw.Draw(t)
        draw.ellipse([(x-4, y-4), (x+4, y+4)], fill=(255,0,0,255))
    return t

def print_exif(exif):
    for key,value in exif.items():
        print(TAGS.get(key), ': ', value)
        
def extract_geoloc(exif):
    latRef, longRef = 1, 1
    latitude, longitude = 0, 0
    for key, value in exif.items(): # Boucler sur les données GPS
        if TAGS.get(key)=='GPSInfo':
            for k2, v2 in value.items():
                if k2==1: # GPSLatitudeRef
                    if v2=='S':
                        latRef = -1
                elif k2==2: # GPSLatitude (deg, min, sec)
                    latitude = v2[0][0]/v2[0][1] + (v2[1][0]/v2[1][1])/60 + (v2[2][0]/v2[2][1])/3600
                elif k2==3: # GPSLongitudeRef
                    if v2=='W':
                        longRef = -1
                elif k2==4: # GPSLongitude (deg, min, sec)
                    longitude = v2[0][0]/v2[0][1] + (v2[1][0]/v2[1][1])/60 + (v2[2][0]/v2[2][1])/3600

    latitude_photo, longitude_photo = (latRef*latitude, longRef*longitude)
    return (latitude_photo, longitude_photo)