class Node:
    '''
    Klasa tworząca wierzchołki
    '''

    def __init__(self, parents=[], node_cost=0, index=0, checked=False):
        self.parents = parents  # lista rodziców wierzchołka
        self.node_cost = node_cost  # koszt przejścia od początku drogi do wierzchołka
        self.index = index  # indeks wierzchołka
        self.children = []  # lista dzieci wierzchołka
        self.checked = checked  # stan sprawdzenia - odwiedzenia
        self.matrix = []  # macierz danego wierzchołka

    def __str__(self):
        '''
        Pomocnicze przeciążenie wyśiwetlające dane o konkretnym wierzchołku
        :return:
        '''
        return ("Wierzcholek: {}\nKoszt: {}\nDzieci: {}\nRodzice: {}\nMatrix: {}\n\n".format(self.index, self.node_cost,
                                                                                             self.children,
                                                                                             self.parents, self.matrix))
