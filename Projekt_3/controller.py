import copy
import time
import random
from operator import itemgetter


class Controller:
    def __init__(self, weights=[], cross_lvl=0.8, mutation_lvl=0.01):

        self.weights = weights  # wagi przejsc
        self.size = len(self.weights)  # ilosc wierzchołków
        self.population = self.generate_population()  # wygenerowanie pierwszej populacji
        self.population_size = len(self.population)  # wielkosc populacji
        self.max_time = 120  # czas maksymalny trwania algorytmu
        self.helper_time = 0  # czas pomocniczny do obiegu 10 sekundowego
        self.current_time = 0  # czas akutalny
        self.best_time = 0  # czas w ktorym znaleziono najlepsze rozwiązanie
        self.costs = []  # najlepsze koszty w odstepach 10 sekundowych
        self.init_first_cost()  # znalezienie pierwszego najlepszego kosztu
        self.best_path = []  # najlepsza droga
        self.best_cost = 99999999  # najlepszy koszt
        self.cross_lvl = cross_lvl  # wspolczynnik krzyzowania
        self.mutation_lvl = mutation_lvl  # wspolczynnik mutacji

    def generate_population(self, population_size=20):
        """
        Generowanie pierwszej populacji - domyslnie 20 osobnikow
        Kazdy osobnik generowany metoda zachlanna - start od innego wierzcholka
        :param population_size:
        :return:
        """
        node_list = []  # pomocnicza lista wierzcholkow
        while len(node_list) != population_size:
            node = random.randint(0, self.size - 1)
            if node not in node_list:
                node_list.append(node)  # wypelnienie tablicy roznymi wierzcholkami

        population_list = []
        # dla kazdego wierzcholka wygenerowanie drogi metoda zachlanna
        for node in node_list:
            path = self.first_path(node)
            population_list.append(path)

        return population_list  # zwrocenie populacji pierwtonej

    def order_crossover(self, p1, p2):
        """
        Order crossover - metoda krzyzowania
        :param p1: rodzic 1
        :param p2: rodzic 2
        :return:
        """
        descentand = []  # potomek
        for i in range(0, len(p1) - 1):
            descentand.append('X')  # inicjacja "X"'ami potomka

        cross_size = round(len(p1) / 2)  # wielkosc fragmentu powielalnego rowna polowie
        cross_pos = random.randint(0, len(p1) - 1)  # wybranie losowej pozycji
        slice = p1[cross_pos:cross_pos + cross_size]  # pobranie wycinka do powielenia
        slice_size = len(slice) - 1  # wielkosc wycinka

        descentand[cross_pos:cross_pos + slice_size] = slice  # wklejenie wycinka do potomka w odpowiednie miejsce

        position = cross_pos + slice_size + 1  # ustawienie sie na nastepnej pozycji
        if position >= len(p2):  # jezeli pozycja przekracza dlugosc ustawienie sie na poczatku
            position = 0

        helper = p2[position:] + p2[
                                 :position]  # sklejenie czesci rodzica 2 w kolejnosci ustawionej do kopiowania do potomka

        for i in descentand:  # usuniecie juz istniejacych elementow(wierzcholkow)
            if i in helper:
                helper.remove(i)

        while 'X' in descentand:  # dopki sa "X"
            if position >= len(p1):  # jezeli pozycja przekracza wielkosc ustawienie się na początku
                position = 0

            descentand[position] = helper.pop(0)  # pobranie pozycji, wyrzucenie jej i wklejenie potomkowi
            position += 1  # zwiekszenie pozycji

        return descentand  # zwrocenie potomka po krzyzowaniu rodzicow p1,p2

    def inversion_mutation(self, p1):
        """
        Mutacja przez inwersje
        :param p1:
        :return:
        """
        size = len(p1) - 1  # wielkosc osobnika
        first_edge = random.randint(0, size)  # losowanie pierwszej pozycji
        second_edge = first_edge
        while second_edge == first_edge:
            second_edge = random.randint(0, size)  # losowanie drugiej pozycji, innej niz pierwsza
        if first_edge > second_edge:  # ustawienie w kolejnosci mniejsza - wieksza
            first_edge, second_edge = second_edge, first_edge

        slice = p1[first_edge:second_edge]  # pobranie wycinka
        slice = slice[::-1]  # odwrocenie go - inwersja
        descendent = copy.deepcopy(p1)
        descendent[first_edge:second_edge] = slice  # wkelejenie odwroconego wycinka

        return descendent  # zwrocenie osobnika po mutacji

    def pop_worst(self):
        """
        Wyrzucenie najgorszego osobnika z populacji
        :return:
        """
        max_path = 0
        for position, path in enumerate(self.population):  # szukanie osobnika z najwiekszym kosztem
            if self.calculate_path(path) > max_path:
                max_path = self.calculate_path(path)
                index = position
        self.population.pop(index)  # wyrzcenie osobnika z populacji

    def find_best(self):
        """
        Znajdowanie najlepszego osobnika z populacji
        :return:
        """
        min_cost = 9999999
        for position, path in enumerate(self.population):
            if self.calculate_path(path) < min_cost:
                min_cost = self.calculate_path(path)
        return min_cost  # zwrocenie najmniejszego kosztu z populacji

    def find_worst(self):
        """
        Znalezienie najgorszego osobnika z populacji
        :return:
        """
        max_cost = 0
        for position, path in enumerate(self.population):
            if self.calculate_path(path) > max_cost:
                max_cost = self.calculate_path(path)
        return max_cost

    def init_first_cost(self):
        cost = self.find_best()
        self.costs.append(cost)

    def find_best_in_population(self, population):
        """
        Zwrocenie posortowanej listy o wielkosci populacji od najlepszych odosbnikow do najgorszych
        :param population:
        :return:
        """
        tup_list = []
        for position, i in enumerate(population):
            cost = self.calculate_path(i)
            if cost < self.find_worst():
                my_tup = (cost, position)
                tup_list.append(my_tup)
        tup_list.sort(key=itemgetter(0))
        cut_list = tup_list[:self.population_size]
        candidate_list = []
        for i in cut_list:
            cost, pos = i
            candidate = population[pos]
            candidate_list.append(candidate)
        return candidate_list

    def doAlgorithm(self):
        help_counter = 0

        while self.current_time < self.max_time:  # dopóki czas aktualny mniejszy od ustawianego
            proccess_time = time.clock()  # pobranie czasu

            helper_list = copy.deepcopy(self.population)  # pomocnicza lista populacji
            size = len(self.population) - 1  # wiekosc
            for i in range(0, size):  # kazdy z kazdym
                for j in range(0, size):
                    if i != j:  # jeżeli osobnik nie jest soba
                        rand = random.random()  # liczba losowa z przedzialu <0,1>
                        if rand < self.cross_lvl:  # jezeli dochodzi do krzyzowania
                            p1 = helper_list[i]  # wybranie rodzica 1
                            p2 = helper_list[j]  # wybranie rodzica 2
                            descendant = self.order_crossover(p1, p2)  # potomek po krzyzowaniu
                            descendant_cost = self.calculate_path(descendant)  # koszt potomka
                            if descendant_cost < self.best_cost:  # jezeli koszt jest mniejszy niz dotychczasowy najlepszy
                                self.best_cost = descendant_cost  # nadpisanie najlepszego kosztu
                                self.best_path = copy.deepcopy(descendant)  # nadpisanie najlepszej drogi
                                self.best_time = self.current_time  # nadpisanie czasu znalezienia najlepszego osobnika
                            if descendant_cost < self.find_worst():  # jezeli potomek jest lepszy niz najgorszy w aktualnej populacji
                                self.population.append(descendant)  # dodanie do populacji potomka
                                self.pop_worst()  # usuniecie nagorszego osobnika z populacji

            for position, i in enumerate(self.population):  # dla kazdego osobnika w populacji
                rand = random.random()  # losowanie liczby <0,1>
                if rand < self.mutation_lvl:  # jezeli ma dojsc do mutacji
                    self.population[position] = self.inversion_mutation(
                        self.population[position])  # nadpisanie osobnika w populacji

            proccess_time = time.clock() - proccess_time  # kalkulacja czasu wykonania pojdeynczej iteracji
            self.current_time += proccess_time  # dodanie czasu pojedynczej iteracji do czasu działania algorytmu
            self.helper_time += proccess_time  # zliczenie pomocniczego czasu
            if self.helper_time > 10:  # jezeli czas pomocniczy wiekszy niz 10 sekund
                self.costs.append(self.best_cost)  # dodanie najlepszego dotychczasowgo kosztu
                self.helper_time = 0  # wyzerowanie pomocniczego kosztu
                help_counter += 1  # zwiekszenie licznika
        if help_counter * 10 < self.max_time:  # przypadek ostatniego kosztu, poza glowna petla
            self.costs.append(self.best_cost)

    def first_path(self, first_node=0):
        '''
        Generowanie pierwszej drogi metodą zachłanną
        :return:
        '''
        help_weights = copy.deepcopy(self.weights)  # kopia macierzy wag
        visited = []  # lista odwiedzonych wierzchołków

        next_node = first_node  # wylosowanie pierwszego wierzchołka
        for i in range(0, self.size - 1):
            help_weights[i][
                next_node] = 9999999999  # ustawienie wartości uniemożliwiającej powrotu; rozpratrywany jest najmniejszy koszt

        while len(visited) < self.size:  # dopoki lista nie jest zapełniona wszystkimi wierzchołkami
            visited.append(next_node)  # dodanie wierzchołka do listy
            min_value = min(
                help_weights[next_node])  # znalezienie najniższej wartości przejścia do następnego wierzchołka
            next_node = help_weights[next_node].index(
                min_value)  # na podstawie wartości znalezienie pozycji wierzchołka - znalezienie indeksu wierzchołka i wybranie go na następnego
            for i in range(0, self.size - 1):
                help_weights[i][
                    next_node] = 9999999999  # ustawienie wartości uniemożliwiającej powrotu; rozpratrywany jest najmniejszy koszt

        return visited  # zwrócenie pierwszej drogi metodą zachłanną

    def generate_random_path(self):
        '''
        Generowanie losowej drogi
        :return:
        '''
        help_list = []  # pusta lista do przeszukiwania drogi
        while len(help_list) != self.size:  # poki lista nie wypełniona
            rand = random.randint(0, self.size - 1)  # wylosowanie wierzchołka
            if rand not in help_list:  # jeżeli wylosowany wierzchołek nie znajduje sie w liście
                help_list.append(rand)  # dodanie tego wierzchołka

        return help_list  # zwrócenie losowej drogi

    def set_time(self, value):
        '''
        ustawienie czasu o wielkości value
        :param value: czas podawany przesz użytkownika
        :return:
        '''
        self.max_time = value

    def calculate_path(self, path):
        '''
        Kalkulacja kosztu wybranej drogi
        :param path: wybrana droga
        :return:
        '''
        help_path = copy.deepcopy(path)  # kopia drogi
        help_path.append(help_path[0])  # dodanie powrotu do miasta startowego
        cost = 0  # poczatkowy koszt
        for i in range(0, self.size):
            v1 = help_path[i]  # pobranie wierzchołka 1
            v2 = help_path[i + 1]  # pobranie wierzchołka 2
            cost += self.weights[v1][v2]  # doliczenie kosztu przejscia między wierzchołkami
        return cost  # zwrócenie kosztu drogi
