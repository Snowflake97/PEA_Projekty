from itertools import *
import copy
from node import Node
import sys
import re

sys.setrecursionlimit(99999999)


class read_data:
    '''
    READ_DATA
    -wczytuje dane z pliku
    -wykonuje algorytmy
    -przechwouje dane
    -zwraca wyniki
    '''

    def __init__(self):
        self.matrix = []  # wczytywana macierz
        self.size = 0  # ilość miast, wielkość macierzy
        self.brute_cost = 0  # koszt drogi brute_force
        self.file_name = ''  # ustawienie nazwy pliku wczytywania danych
        self.startCity = 0  # ustawienie miasta startowego, początku drogi
        self.nodes_list = []  # lista przechowująca wierzhołki
        self.min = 999999999  # minimalny koszt - nadpisywany
        self.path = []  # aktualna droga
        self.min_path = []  # minimalna droga
        self.iterations = 0  # liczba wywolan funkcji
        self.sec_min = 0

    def prep_data(self):
        '''
        Przygotowanie danych
        '''

        self.fill_matrix()  # wypelnienie macierzy
        self.customize_matrix()  # usunięcie niepotrzebnych znaków z macierzy
        self.matrix_for_brute = copy.deepcopy(self.matrix)  # kopia macierzy startowej, dla bruteforca, bez redukowania
        self.matrix_with_minuses = self.change_zero(copy.deepcopy(self.matrix))  # zmiana przekątnej z 0 na -1
        self.main_cost, self.reduced_matrix = self.compute_brand(
            self.matrix_with_minuses)  # zredukowana macierz i koszt minimalny

    def fill_matrix(self):
        file = open("./files/inputs/{}".format(self.file_name), mode='r')  # otworzenie pliku
        with file as f:
            for position, line in enumerate(f):
                if position == 0:  # pierwsza linia to ilośc miast
                    size = line
                    self.size = int(size[:-1])
                else:
                    correct_line = re.sub("^\s+", "", line)  # regex usuwajacy spacje na poczatku lini
                    correct_line = re.sub("\s\s+", " ",
                                          correct_line)  # regex zamieniający wiele spacji na jedną, przerwy miedzy danymi
                    my_list = correct_line.split(" ")  # odzielenie i pobranie danych
                    self.matrix.append(my_list)  # wypełnienie macierzy
        f.close()  # zamknięcie pliku

    def customize_matrix(self):
        '''
        usuniecie endlinów
        usunięcie pustych elementów
        konwersja na inty
        '''
        for i in self.matrix:
            for position, item in enumerate(i):
                if "\n" in item:
                    replace_item = item.replace("\n", "")  # endliny
                    i[position] = replace_item

        for i in self.matrix:
            for position, item in enumerate(i):
                if item == '':
                    i.pop(position)  # puste elementy

        for i in self.matrix:
            for position, item in enumerate(i):
                item = int(item)  # rzutowanie na int ze string
                i[position] = item

    def print_nicely(self, mat):
        '''
        Wyświetlenie macierzy z wyszególnieniem na wierzchołki
        :param mat - macierz do wyświetlenia:
        :return:
        '''
        size = len(mat)
        row = '  |  '
        dash = '---'
        for i in range(0, size):
            row += str(i)
            row += '   '
            dash += "----"

        print(row)
        print(dash)

        for i in range(0, size):
            help_list = mat[i]
            print("{} | {}".format(i, help_list))

    def prep_for_brute(self):
        '''
        Przygotowanie do bruteforca
        :return:
        '''
        for i in range(0, self.size):
            self.nodes_list.append(Node([], 0, i, False))  # stworzenie listy zawierającej wierzchołki miast

    def calculate_path(self):
        '''
        Kalkulacja drogi do bruteforca
        Dla aktualnej drogi przeliczenie kosztow przejscia po kolei z wierzcholka na wierzcholek następny
        :return:
        '''
        helper_cost = 0
        for i in range(0, len(self.path) - 1):
            v1 = self.path[i]
            v2 = self.path[i + 1]
            helper_cost += self.matrix_for_brute[v1][v2]

        return helper_cost

    def bruteForce(self, current_node):
        '''
        Bruteforce
        :param current_node: wywołanie dla wybranego wierzchołka
        :return:
        '''
        self.iterations += 1  # zwiększenie liczby wywołań metody
        self.path.append(current_node.index)  # dodanie wierzchołka do listy aktualnej drogi
        if len(self.path) == self.size:  # jeżeli droga jest pełna
            self.path.append(self.startCity)  # dodanie do sciezki miasta początkowego
            self.brute_cost = self.calculate_path()  # wyliczenie kosztu całej drogi
            if self.brute_cost < self.min:  # jeżeli koszt danej drogi jest mniejszy niż wcześniejszy
                self.min = self.brute_cost  # nadpisanie poprzedniego kosztu
                self.min_path = copy.deepcopy(self.path)  # przekopiowanie aktualnie minimalnej drogi
            self.path.pop(-1)  # usunięcie miasta początkowego, drogi powrotu
        else:  # jeżeli droga nie jest jeszcze pełna
            index = self.nodes_list.index(current_node)  # pobranie indeksu listy aktualnego wierzchołka
            current_node.checked = True  # aktualny wierzchołek odwiedzony
            self.nodes_list[index] = current_node  # nadpisanie wierzchołka na liście
            for node in self.nodes_list:  # dla każdego wierzchołka
                if node.checked == True:  # jeżeli odwiedzony kolejny przebieg pętli
                    continue
                else:
                    self.bruteForce(node)  # jeżeli nieodwiedzony, wywołanie metody dla tego wierzchołka
            current_node.checked = False  # powrót i ustawienie wierzchołka na nieodwiedzony
            self.nodes_list[index] = current_node
        self.path.pop(-1)  # usunięcie poprzedniego wierzchołka z listy

    def change_zero(self, mat):
        '''
        zmienienie 0 na -1 w określonej macierzy
        :param mat:
        :return:
        '''
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i == j:
                    mat[i][j] = -1
        return mat

    def compute_brand(self, mat):
        min = 9999999
        reduced = 0
        # redukcja po wierszach, wyszukanie wartości minimalnej, odjęcie jej od każdej wartości, dodanie jej do kosztu redukcji
        for i in range(0, self.size):
            for j in range(0, self.size):
                if mat[i][j] < min and mat[i][j] != -1:
                    min = mat[i][j]
            if min != 9999999:
                reduced += min
            for k in range(0, self.size):
                if mat[i][k] != -1:
                    mat[i][k] -= min
            min = 9999999

        # redukcja po kolumnach, wyszukanie wartości minimalnej, odjęcie jej od każdej wartości, dodanie jej do kosztu redukcji
        for i in range(0, self.size):
            for j in range(0, self.size):
                if mat[j][i] < min and mat[j][i] != -1:
                    min = mat[j][i]
            if min != 9999999:
                reduced += min
            for k in range(0, self.size):
                if mat[k][i] != -1:
                    mat[k][i] -= min
            min = 9999999

        return reduced, mat  # zwrócenie zredukowanej macierzy i kosztu redukcji

    def matrix_inf(self, mat, v1, v2):
        '''
        Dla przejścia z v1 do v2, zaznaczenie calego wybranego wiersza i kolumny na wartości -1
        zaznaczenie wartościa -1 miejsce powrotu z v2 do v1
        :param mat: macierz
        :param v1: wierzchołek pierwszy - wiersz
        :param v2: wierzchołek drugi - kolumna
        :return:
        '''
        size = len(mat)
        for i in range(0, size):
            for j in range(0, size):
                if i == v1 or j == v2:
                    mat[i][j] = -1
        mat[v2][v1] = -1
        return mat

    def calculate_cost_from_verts(self, v1, v2, mat):
        '''
        Wyliczenie kosztu przejscia miedzy dwoma miastami
        :param v1: wierzchołek 1
        :param v2: wierzchołek 2
        :param mat: macierz
        :return:
        '''
        edge = mat[v1][v2]  # pobranie krawędzi miedzy miastami, zapisanie kosztu
        help_matrix = copy.deepcopy(mat)  # macierz pomocnicza
        help_matrix = self.matrix_inf(help_matrix, v1, v2)  # zaznaczenie kolumny i wiersza na -1
        cost, help_matrix = self.compute_brand(
            help_matrix)  # wyliczenie kosztu redukcji macierzy i zwrócenie macierzy zredukowanej
        whole_cost = cost + edge  # zliczenie całkowitego kosztu
        return whole_cost, help_matrix  # zwrócenie kosztu i macierzy

    def init_first_node(self):
        '''
        Stowrzenie pierwszego wierzchołka dla miasta początkowego
        :return:
        '''
        parents = []  # wierzchołek nie ma rodziców
        first_node_matrix = copy.deepcopy(self.reduced_matrix)  # macierzy dla wierzchołka
        first_node = Node(parents, self.main_cost, self.startCity, True)  # stworzenie obiektu
        first_node.matrix = first_node_matrix  # przypisanie macierzy
        children_list = []  # stowrzenie listy dla dzieci
        for i in range(0, self.size):
            if i != self.startCity:
                children_list.append(i)  # wypełnienie listy dzieci
        first_node.children = children_list  # przypisanie listy dzieci
        return first_node  # zwrócenie wierzchołka początkowego

    def bb(self, current_node):
        '''
        Branch&Bound
        :param current_node:
        :return:
        '''
        self.iterations += 1  # zwiększenie liczby wywołań metody
        if current_node in self.nodes_list:  # jeżeli wierzchołek już znajdował się na liście
            for node in self.nodes_list:
                if node == current_node:
                    node.checked = True  # wierzchołek odwiedzony
        else:  # jeżeli wierzchołek nie znajdował się na liście
            current_node.checked = True  # wierzchołek odwiedzony
            self.nodes_list.append(current_node)  # dodanie wierzchołka do listy

        # generowanie dzieci
        parents_list = copy.deepcopy(current_node.parents)  # kopia wierzchołków rodziców
        parents_list.append(current_node.index)  # dodanie aktualnego wierzchołka
        if len(current_node.children) != 0:  # jeżeli nie koniec gałęzi
            for child in current_node.children:  # dla każdego pozostałego dziecka
                current_matrix = copy.deepcopy(current_node.matrix)  # kopia macierzy aktualnego wierzchołka
                child_list = []  # stworzenie listy dzieci aktualnego wierzchołka
                for i in range(0, self.size):  # wyszukwanie dzieci
                    if child == i or i in parents_list:  # dodanie dzieci poza sobą
                        continue
                    else:
                        child_list.append(i)

                # wyliczenie kosztu przejścia do tworzonego wierzchołka i macierzy dla niego
                cost, node_matrix = self.calculate_cost_from_verts(current_node.index, child, current_matrix)
                cost += current_node.node_cost  # zliczenie kosztu całkowitego kosztu
                my_node = Node(parents_list, cost, child)  # tworzenie nowego wierzchołka
                my_node.children = child_list  # przypisywanie wartości
                my_node.matrix = node_matrix  # przypisywanie wartości
                self.nodes_list.append(my_node)  # dodanie utworzonego wierzchołka do listy

            min = 9999999  # koszt minimalny
            for position, node in enumerate(self.nodes_list):
                if node.node_cost < min and node.checked == False:  # jeżeli koszt wierzchołka znalezionego mniejszy niż poprzedni
                    min = node.node_cost  # zmiana kosztu minimalnego
                    node_position = position  # zapisanie pozycji w liście
                    self.min = min

            next_node = self.nodes_list[node_position]  # wybranie następnego wierzchołka, z najniższym kosztem

            min = 9999999  # koszt minimalny
            for position, node in enumerate(self.nodes_list):
                if node.node_cost > self.min and node.node_cost < min and node.checked == False:  # jeżeli koszt wierzchołka znalezionego mniejszy niż poprzedni
                    min = node.node_cost  # zmiana kosztu minimalnego
                    self.sec_min = min  # ustawienie drugiego minimalnego kosztu

            for pos, node in enumerate(self.nodes_list):
                if node.node_cost != self.min and node.node_cost != self.sec_min:
                    self.nodes_list.pop(pos)

            self.bb(next_node)  # wywołanie metody dla następnego wierzchołka

    def determine_path(self):
        '''
        wyszukanie wierzchołków dla minimalnego kosztu
        przygotowanie dróg do wyświetlenia
        zwrócenie stringa z danymi
        :return:
        '''
        paths = []
        result = ''
        for node in self.nodes_list:
            if node.node_cost == self.min and len(node.children) == 0:
                paths.append(node)
        for node in paths:
            path = copy.deepcopy(node.parents)  # pobranie rodziców
            path.append(node.index)  # dodanie swojego indeksu
            path.append(node.parents[0])  # dodanie wierzchołka startowego
            # całkowita droga
            result += "Sciezka : {}\nKoszt: {}\n".format(path, node.node_cost)  # string zawierający drogi, koszty
        result += "Iteracje : {}".format(self.iterations)  # dodanie do stringa liczby wywołań metody
        return result  # zwrócenie danych

    def doBruteForce(self):
        self.prep_for_brute()  # przygotowanie wierzchołków do bruteforca
        start = self.nodes_list[self.startCity]  # wybranie wierzchołka startowego - miasta pstartowego
        self.bruteForce(start)  # wykonanie bruteforca

    def returnBrute(self):
        '''
        Zwrócenie danych (stringa) z danymi wyjściowymi
        :return:
        '''
        return ("Sciezka : {}\nKoszt: {}\nIteracje: {}".format(self.min_path, self.min, self.iterations))

    def doBranchAndBound(self):
        first_node = self.init_first_node()  # stworzenie pierwszego wierzchołka dla branch&bound
        self.bb(first_node)  # wykonanie branch&bound
