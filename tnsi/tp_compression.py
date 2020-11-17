class Liste:
    """
    Implémentation d'une liste chaînée.
    
    Exemples d'utilisation:
    >>> l = Liste() 
    >>> for jour in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']:
    >>>     l.insert(0,jour)
    >>> l2 = Liste() 
    >>> for jour in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']:
    >>>     l.append(jour)
    """
    def __init__(self, element=None, sublist=None):
        self.car = element
        self.cdr = sublist
        
    def has_next(self):
        """
        Teste si la liste possède une sous-liste.
        """
        return self.cdr is not None
        
    def next(self):
        """
        Retourne la (sous-)liste suivante 
        (à n'utiliser que si has_next() retourne vrai)
        """
        return self.cdr
    
    def insert(self, i, element):
        """
        Insérer un élément à un index spécifique
        """
        # Trouver le maillon d'index i
        liste = self
        idx = 0
        while liste.has_next():
            if idx==i: # trouvé sous-chaîne d'index i
                liste.cdr = Liste(liste.car, liste.cdr)
                liste.car = element
                return
            liste = liste.next()
            idx += 1
        # Sinon insérer en fin de chaîne
        liste.cdr = Liste(None, None)
        liste.car = element
        
    def replace(self, i, element):
        """
        Remplacer l'élément à un index spécifique
        """
        # Trouver le maillon d'index i
        liste = self
        idx = 0
        while liste.has_next():
            if idx==i: # trouvé sous-chaîne d'index i
                liste.car = element
                return
            liste = liste.next()
            idx += 1
        
    def remove(self, i):
        """
        Supprimer l'élément se trouvant à un index spécifique
        """
        liste = self
        # Trouver le maillon d'index i
        idx = 0
        while liste.has_next():
            if idx==i: # trouvée sous-chaîne d'index i
                n = liste.next()
                liste.cdr = n.cdr
                liste.car = n.car
                return
            liste = liste.next()
            idx += 1
        assert False, "L'élément demandé n'existe pas"
        
    def element(self, i=0):
        """
        Retourne l'élément du ième maillon
        """
        liste = self
        idx = 0
        while liste.has_next():
            if idx==i:
                return liste.car
            liste = liste.next()
            idx += 1
        return None
    
    def index(self, element):
        """
        Retourne la position d'un élément dans la liste (-1 s'il n'existe pas)
        """
        liste = self
        if liste.car == element:
            return 0
        idx = 0
        while liste.has_next():
            if liste.car == element:
                return idx
            liste = liste.next()
            idx += 1
        return -1
    
    def length(self):
        """
        Retourne la longueur de la liste
        """
        size = 0
        liste = self
        while liste.has_next():
            size += 1
            liste = liste.next()
        return size
    
    def append(self, element):
        """
        Ajouter l'élément en fin de liste.
        """
        self.insert(self.length(),element)
        
    def __repr__(self):
        """
        Retourne une représentation de la chaîne de tous les éléments.
        """
        s = ''
        idx = 0
        liste = self
        while liste.has_next():
            if idx>0:
                s += ' -> '
            s += str(liste.car)
            liste = liste.next()
            idx += 1
        return '<List: '+s+'>'
    
    def __str__(self):
        """
        Retourne une chaîne représentant la tête.
        """
        return str(self.car)
    
class Arbre:
    """
    Implémentation d'arbre binaire dans une structure chaînée.
    
    Exemple d'utilisation:
    >>> arbre = Arbre('A',None,None)
    >>> arbre.append_left('B')
    >>> arbre.append_right('C')
    >>> arbre.left().append_left('D')
    >>> arbre.left().append_right('E')
    >>> arbre.right().append_left('F')
    >>> arbre.right().append_right('G')
    """
    def __init__(self, element=None, gauche=None, droit=None):
        """
        Arbre = élément + sous-arbre gauche + sous-arbre droit
        """
        self.root = element
        self.l = gauche
        self.r = droit
        
    def is_empty(self):
        """
        Teste si l'arbre est vide (i.e. n'a pas d'élément à sa racine)
        """
        return self.root is None
    
    def has_left(self):
        """
        Teste s'il existe un sous-arbre gauche
        """
        return self.l is not None
    
    def left(self):
        """
        Retourne le sous-arbre gauche.
        """
        return self.l

    def has_right(self):
        """
        Teste s'il existe un sous-arbre droit.
        """
        return self.r is not None
    
    def right(self):
        """
        Retourne le sous-arbre droit.
        """
        return self.r
    
    def append_left(self, element):
        """
        Ajouter une feuille gauche (attention: n'insère pas mais écrase)
        """
        self.l = Arbre(element, None, None)
        
    def append_right(self, element):
        """
        Ajouter une feuille droite (attention: n'insère pas mais écrase)
        """
        self.r = Arbre(element, None, None)
        
    def value(self):
        """
        Retourne la valeur de l'élément à la racine de l'arbre
        """
        return self.root
        
    def height(self):
        """
        Retourne la hauteur de l'arbre (méthode récursive)
        """
        tg, td = 0,0
        if self.has_left():
            tg = self.left().height() + 1
        if self.has_right():
            td = self.right().height() + 1
        return max(tg, td)
    
    def size(self):
        """
        Retourne la taille de l'arbre (méthode récursive)
        """
        sg, sd = 0,0
        if self.has_left():
            sg = self.left().size()
        if self.has_right():
            sd = self.right().size()
        return sg + sd + 1

    def afficher(self, niv=0, prefix=''):
        """
        Afficher le contenu de l'arbre sous forme textuelle (méthode récursive)
        """
        if self.is_empty():
            return
        if niv==0:
            print(self)
        else:
            print(' '*5*(niv-1) + '|'+prefix+'-' + str(self))

        if self.has_left():
            self.left().afficher(niv+1, '(l)')
        if self.has_right():
            self.right().afficher(niv+1, '(r)')

    def __str__(self):
        """
        Retourne l'élément à la racine de l'arbre sous la forme d'une chaîne
        """
        return str(self.root)