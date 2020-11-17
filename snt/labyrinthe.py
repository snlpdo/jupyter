from turtle import *

def dessiner_labyrinthe():
    # Dessiner le labyrinthe
    lab = [
        [11, 9, 5, 5, 7, 9, 3, 9, 3, 8, 5, 3],
        [10, 8, 5, 5, 5, 6,12, 6,10,10, 9, 6],
        [10,10, 9, 5, 5, 5, 5, 3,10,10,12, 7],
        [10,10,10, 9, 5, 5, 5, 6,10, 8, 3,11],
        [ 8, 6,10,12, 5, 5, 5, 3,10,10,10,10],
        [12, 5, 4, 5, 3, 9, 3,10,10,10,10,10],
        [ 9, 5, 1, 3,10,10,12, 6,10, 8, 6,10],
        [10,11,10,10, 8, 4, 5, 3,10,12, 1, 6],
        [10, 8, 2, 8, 2, 9, 5, 6,10,13, 4, 3],
        [10,10, 8, 2,10,12, 5, 3,12, 5, 3,10],
        [10,10,10,10,10, 9, 5, 6, 9, 5, 6,10],
        [12, 6,10,12, 6,12, 5, 5, 4, 5, 5, 6]
          ]

    sz = 30
    penup()
    up = True

    # Aller au coin supérieur gauche du labyrinthe
    speed("fastest")
    home()
    backward(180)
    right(90)
    backward(180)
    left(90)

    # Traits horizontaux (côté haut)
    pair = True
    dec = 0
    for i in range(len(lab)+1):
        i2 = i
        if i==len(lab): # côté bas dernière ligne
            i = i-1
            dec = 2

        if pair: # Ligne paire 
            for j in range(0,len(lab[i]),1): # -> vers la droite
                if ((lab[i][j]>>dec)&1)==1:
                    if up:
                        pendown()
                        up = False
                else:
                    if not(up):
                        penup()
                        up = True
                forward(sz)

            # Fin de ligne à droite
            if i2!=len(lab):
                if not(up):
                    penup()
                    up = True
                right(90)
                forward(sz)
                right(90)

        else: # Ligne impaire 
            for j in range(len(lab[i])-1,-1,-1): # -> vers la gauche
                if ((lab[i][j]>>dec)&1)==1:
                    if up:
                        pendown()
                        up = False
                else:
                    if not(up):
                        penup()
                        up = True
                forward(sz)

            # Fin de ligne à gauche
            if i2!=len(lab):
                if not(up):
                    penup()
                    up = True
                left(90)
                forward(sz)
                left(90)

        pair = not(pair)

    if not(up):
        penup()
        up = True
    left(90)

    # Traits verticaux (côté gauche)
    pair = not(pair)
    dec = 1
    for j in range(len(lab[0])-1, -2, -1): # Depuis la dernière colonne
        j2 = j
        if j==-1: # côté droit première colonne
            j = j+1
            dec = 3

        if pair:
            for i in range(len(lab)-1,-1,-1): # -> vers le haut
                if ((lab[i][j]>>dec)&1)==1:
                    if up:
                        pendown()
                        up = False
                else:
                    if not(up):
                        penup()
                        up = True
                forward(sz)

            # Fin de colonne en haut
            if j2!=-1:
                if not(up):
                    penup()
                    up = True
                left(90)
                forward(sz)
                left(90)

        else:
            for i in range(0,len(lab),1): # -> vers le bas
                if ((lab[i][j]>>dec)&1)==1:
                    if up:
                        pendown()
                        up = False
                else:
                    if not(up):
                        penup()
                        up = True
                forward(sz)

            # Fin de colonne en bas
            if j2!=-1:
                if not(up):
                    penup()
                    up = True
                right(90)
                forward(sz)
                right(90)

        pair = not(pair)
        
    if not(up):
        penup()
        up = True
    backward(11.5*30)
    left(90)
    backward(2.5*30)
    right(90)
    pendown()
    up = False
    color('red')
    speed('slow')
