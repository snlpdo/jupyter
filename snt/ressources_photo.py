from PIL import Image
from IPython.display import display
import requests

# Image de départ
image = Image.new("RGB", (300,200))
# partie bleue
BLEU = (0,0,200)
for y in range(0,100):
    for x in range(0,150):
        image.putpixel((x,y),BLEU)
# partie grise
GRIS = (210,210,210)
for y in range(0,100):
    for x in range(150,300):
        image.putpixel((x,y),GRIS)
# partie rouge
ROUGE = (220,0,0)
for y in range(100,200):
    for x in range(0,150):
        image.putpixel((x,y),ROUGE)
# partie verte
VERT = (0,200,0)
for y in range(100,200):
    for x in range(150,300):
        image.putpixel((x,y),VERT)
        
img = image

def reset_image():
    global img
    img = image.copy()

def changer_image(url):
    global img
    
    # Télécharger dans un fichier temporaire
    fichier = None
    if url.lower().endswith('jpg'):
        fichier = 'tmp.jpg'
    elif url.lower().endswith('png'):
        fichier = 'tmp.png'
    assert fichier is not None, "Format d'image non supporté"
    f = open(fichier, 'wb')
    f.write(requests.get(url).content)
    f.close()
    # Retourner l'image
    img = Image.open(fichier)
    
def afficher_image():
    display(img)
    
def largeur():
    return img.size[0]

def hauteur():
    return img.size[1]

def consulter_pixel(x=0,y=0):
    return img.getpixel((x,y))

def modifier_pixel(x=0,y=0,r=0,v=0,b=0):
    img.putpixel((x,y),(r,v,b))
