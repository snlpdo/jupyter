from PIL import Image, ImageDraw, ImageFont
from turtle import *

def detection_mur(image, x1, y1, x2, y2,seuil=100):
    '''
    Teste s'il existe un mur dans l'image entre les points (x1,y1) et (x2,y2).
    
    Un 'mur' correspond a une variation de luminance supérieure à un certain seuil.
    '''
    lmin = float('inf')
    lmax = -1
    for x in range(max(0,min(x1,x2)),min(image.width,max(x1,x2)+1)):
        for y in range(max(0,min(y1,y2)),min(image.height,max(y1,y2)+1)):
            luminance = sum(image.getpixel((x,y)))
            if luminance<lmin:
                lmin = luminance
            if luminance>lmax:
                lmax = luminance
    return True if lmax-lmin>seuil else False

def analyse(image, nb_col, nb_ligne):
    '''
    Détecter des contours (=murs) de toutes les cases et générer le graphe.
    
    Valeur dans chaque case: 1 octet au format binaire 0bxxxxhdbg
    où 
    x : valeur irrélévante
    h: mur en haut
    d: mur à droite
    b: mur en bas
    g: mur à gauche
    '''
    contours = [[0 for i in range(nb_col)] for j in range(nb_ligne)]
    graphe = {}
    
    BLANC = (255,255,255)
    NOIR = (0,0,0)
    ROUGE = (255,0,0)
    sz_h = image.width/nb_col
    sz_v = image.height/nb_ligne
    
    for i in range(nb_ligne):
        for j in range(nb_col):
            graphe[(i,j)] = []
            x = sz_h/2+j*sz_h
            y = sz_h/2+i*sz_v
            
            # Bordure haute
            if detection_mur(image,int(x),int(y),int(x),int(y-sz_v)):
                contours[i][j] += 1
            else:
                if i>0: 
                    graphe[(i,j)].append((i-1,j))
                
            # Bordure droite
            if detection_mur(image,int(x),int(y),int(x+sz_h),int(y)):
                contours[i][j] += 2
            else:
                if j<nb_col-1:
                    graphe[(i,j)].append((i,j+1))
                    
            # Bordure basse
            if detection_mur(image,int(x),int(y),int(x),int(y+sz_v)):
                contours[i][j] += 4
            else:
                if i<nb_ligne-1:
                    graphe[(i,j)].append((i+1,j))
                    
            # Bordure gauche
            if detection_mur(image,int(x),int(y),int(x-sz_h),int(y)):
                contours[i][j] += 8
            else:
                if j>0:
                    graphe[(i,j)].append((i,j-1))
                    
    return graphe, contours

def dessiner_labyrinthe(bordures, sz=40):
    # Dessiner le labyrinthe
    penup()
    speed("fastest")
    home()
    backward(len(bordures[0])/2*sz)
    right(90)
    backward(len(bordures)/2*sz)
    left(90)

    # Lignes horizontales (depuis le côté supérieur haut) correspondant aux bordures
    # supérieures de chaque cellule
    # - les lignes paires (0,2...): dessinées de gauche vers la droite
    # - les lignes impaires (1,3...) sont dessinées de la droite vers la gauche
    # Une itération supplémentaire permet de dessiner la bordure inférieure d'uniquement
    # la dernière ligne.
    pair = True
    decalage = 0
    for i in range(len(bordures)+1):
        i2 = i
        if i==len(bordures): # Refaire la dernière ligne pour bordure inférieure
            i = i-1
            decalage = 2

        if pair: # Ligne paire: gauche vers droite
            for j in range(0,len(bordures[i]),1): # -> vers la droite
                if ((bordures[i][j]>>decalage)&1)==1: # baisser le stylo
                    pendown()
                else: # lever le stylo
                    penup()
                forward(sz)

            # Demi-tour en fin de ligne à droite (sauf pour la dernière)
            if i2!=len(bordures):
                penup()
                right(90)
                forward(sz)
                right(90)

        else: # Ligne impaire: de droite vers gauche
            for j in range(len(bordures[i])-1,-1,-1): # -> vers la gauche
                if ((bordures[i][j]>>decalage)&1)==1:
                    pendown()
                else:
                    penup()
                forward(sz)

            # Demi-tour en fin de ligne à gauche (sauf pour la dernière)
            if i2!=len(bordures):
                penup()
                left(90)
                forward(sz)
                left(90)

        pair = not(pair)
    ### Fin traits horizontaux

    if pair:
        backward(len(bordures[0])*sz)
        right(90)
        pair = False
    else:
        penup()
        left(90)

    # Lignes verticales (depuis le côté inférieur droit) correspondant aux bordures
    # droites de chaque cellule
    # - les colonnes paires: dessinées de gauche vers la droite
    # - les colonnes impaires: dessinées de la droite vers la gauche
    # Une itération supplémentaire permet de dessiner la bordure gauche d'uniquement
    # la dernière colonne.
    pair = not(pair)
    decalage = 1
    for j in range(len(bordures[0])-1, -2, -1): # Depuis la dernière colonne
        j2 = j
        if j==-1: # côté droit première colonne
            j = j+1
            decalage = 3

        if pair:
            for i in range(len(bordures)-1,-1,-1): # -> vers le haut
                if ((bordures[i][j]>>decalage)&1)==1:
                    pendown()
                else:
                    penup()
                forward(sz)

            # Fin de colonne en haut
            if j2!=-1:
                penup()
                left(90)
                forward(sz)
                left(90)

        else:
            for i in range(0,len(bordures),1): # -> vers le bas
                if ((bordures[i][j]>>decalage)&1)==1:
                    pendown()
                else:
                    penup()
                forward(sz)

            # Fin de colonne en bas
            if j2!=-1:
                penup()
                right(90)
                forward(sz)
                right(90)

        pair = not(pair)
    # Fin traits verticaux
    penup()
    right(90)

def depart_tortue(ligne, colonne, bordures, direction='droite', sz=40):
    penup()
    home()
    backward(len(bordures[0])/2*sz)
    right(90)
    backward(len(bordures)/2*sz)
    left(90)
    
    color('red')
    forward(colonne*sz+sz/2)
    right(90)
    forward(ligne*sz+sz/2)
    left(90)
    if direction=='droite':
        pass
    elif direction=='gauche':
        left(180)
    elif direction=='haut':
        left(90)
    else:
        right(90)
    pendown()

def dessiner_parcours(bordures, parcours, direction='droite', sz=40):
    dessiner_labyrinthe(bordures, sz)
    
    depart = parcours[0]
    depart_tortue(depart[0], depart[1], bordures, direction, sz)
    
    speed('slow')
    i_prev, j_prev = parcours[0]
    for pos in parcours:
        i,j = pos
        if i==i_prev-1: # monter
            if direction=='haut':
                pass
            elif direction=='bas':
                right(180)
            elif direction=='droite':
                left(90)
            else: # gauche
                right(90)
            forward(sz)
            direction = 'haut'
        elif i==i_prev+1: # descendre
            if direction=='haut':
                right(180)
            elif direction=='bas':
                pass
            elif direction=='droite':
                right(90)
            else: # gauche
                left(90)
            forward(sz)
            direction = 'bas'
        elif j==j_prev-1: # aller à gauche
            if direction=='haut':
                left(90)
            elif direction=='bas':
                right(90)
            elif direction=='droite':
                left(180)
            else: # gauche
                pass
            forward(sz)
            direction = 'gauche'
        elif j==j_prev+1: # aller à droite
            if direction=='haut':
                right(90)
            elif direction=='bas':
                left(90)
            elif direction=='droite':
                pass
            else: # gauche
                right(180)
            direction = 'droite'
            forward(sz)
        i_prev, j_prev = i,j
