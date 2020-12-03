class Liste:
    """
    Implémentation partielle d'une liste chaînée.
    
    Exemples d'utilisation:
    >>> l = Liste() 
    >>> for jour in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']:
    >>>     l.prepend(jour)
    """
    def __init__(self, element=None, sublist=None):
        self.tete = element
        self.queue = sublist
        
    def is_empty(self):
        return self.tete == None
        
    def has_next(self):
        """
        Teste si la liste possède une sous-liste.
        """
        return self.queue is not None
        
    def next(self):
        """
        Retourne la (sous-)liste suivante 
        (à n'utiliser que si has_next() retourne vrai)
        """
        return self.queue
    
    def prepend(self, element):
        """
        Insérer un élément au début de la liste
        """
        self.queue = Liste(self.tete, self.queue)
        self.tete = element
        
    def value(self):
        """
        Retourne l'élément en tête de liste
        """
        return self.tete
    
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
            s += str(liste.tete)
            liste = liste.next()
            idx += 1
        return '<List: '+s+'>'
    
    def __str__(self):
        """
        Retourne une chaîne représentant la tête.
        """
        return str(self.tete)
    
l1 = Liste()
l2 = Liste()
for j in ['dimanche', 'samedi', 'vendredi', 'jeudi', 'mercredi', 'mardi', 'lundi']:
    l2.prepend(j)
    
class Arbre:
    """
    Implémentation partielle d'arbre binaire dans une structure chaînée.
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
    
    def value(self):
        """
        Retourne l'élément à la racine de l'arbre
        """
        return self.root
    
arbre1 = Arbre('A', 
              Arbre('L', 
                    Arbre('G', Arbre('O', None, None), None), 
                    Arbre('R', None, None)), 
              Arbre('I', 
                    Arbre('T', Arbre('H', None, None), None), 
                    Arbre('M', None, Arbre('E', None, None))))
arbre2 = Arbre()