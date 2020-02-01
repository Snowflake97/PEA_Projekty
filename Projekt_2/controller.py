import copy
import time
import random
import operator
import math


class Controller:
    def __init__(self, weights=[]):

        self.costs = []
        self.weights = weights  # wagi przejsc
        self.size = len(self.weights)  # ilosc wierzchołków
        self.tabu_number = self.size  # kadencja tabu

        self.path = self.first_path()  # wygenerowanie pierwszej drogi metodą zachłanną
        self.tabu = self.init_tabu()  # zainicjowanie pustej listy tabu

        self.current_time = 0  # aktualny czas
        self.helper_time = 0
        self.best_time = 0  # czas znalezienia najlepszego rozwiązania
        self.max_time = 60  # domyślny maksymalny czas działania algorytmu
        self.best_path = copy.deepcopy(self.path)  # pierwsza droga jest najlepszą drogą
        self.best_cost = self.calculate_path(self.path)  # koszt pierwszej drogi jest najlepszy
        self.edges = self.make_all_edges()  # lista krotek przejść - krawędzi

        self.counter = 0  # licznik iteracji bez poprawy

        self.temperature = self.size * 100  # temperatura startowa
        self.cooler_const = 0.9  # współczynnik chłodzenia

        self.current_cost = self.calculate_path(self.path)  # aktualny koszt drogi

    def swap(self, value_1, value_2, path):
        '''
        Funkcja podmieniająca pozycje wierzchołków w określonej drodze
        :param value_1: wierzchołek 1
        :param value_2: wierzchołek 2
        :param path: droga
        :return:
        '''
        path[value_1], path[value_2] = path[value_2], path[value_1]  # podmiana

    def init_tabu(self):
        '''
        Funckcja tworząca macierz o wymiarach NxN gdzie N jest równe ilości wierzchołków
        :return:
        '''
        help_list = []
        for i in range(0, self.size):
            row = []
            for j in range(0, self.size):
                row.append(0)
            help_list.append(row)

        return help_list

    def set_tabu(self, verticle_1, verticle_2):
        '''
        Ustawienie kadencji zakazu przejsc z wierzchołka 1 do wierzchołka 2
        :param verticle_1: wierzchołek 1
        :param verticle_2: wierzchołek 2
        :return:
        '''
        self.tabu[verticle_1][verticle_2] = self.tabu_number

    def decrement_tabu(self):
        '''
        Funkcja iterująca po macierzy zakazów - dekrementująca wartości dodatnie o 1
        :return:
        '''
        for x, rows in enumerate(self.tabu):
            for y, i in enumerate(rows):
                if type(i) == int and i > 0:
                    self.tabu[x][y] = i - 1

    def first_path(self):
        '''
        Generowanie pierwszej drogi metodą zachłanną
        :return:
        '''
        help_weights = copy.deepcopy(self.weights)  # kopia macierzy wag
        visited = []  # lista odwiedzonych wierzchołków

        next_node = 0  # wylosowanie pierwszego wierzchołka
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

        self.costs.append(self.calculate_path(visited))

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

    def set_temperature(self, value):
        '''
        ustawienie temperatury o wielkości value
        :param value: temperatura podawana przesz użytkownika
        :return:
        '''
        self.temperature = value

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

    def make_all_edges(self):
        '''
        Tworzenie krawędzi przejść nie uwzględniając przejść na samego siebie
        :return:
        '''
        tuple_list = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if i != j:
                    tuple_list.append((i, j))
        return tuple_list

    def generate_best_moves(self, node):
        '''
        Wygenerowanie najlepszych przejsc dla określonego wierzchołka
        :param node: wybrany wierzchołek
        :return:
        '''
        best_moves = {}  # pusty słownik
        for tup in self.edges:  # iteracja po wszystkich krawedziach
            v1, v2 = tup  # "tuple unpacking"
            if v1 == node:  # jeżeli wierzchołek 1 jest tym wybranym
                help_path = copy.deepcopy(self.path)  # bezpieczna kopia aktualnej drogi
                self.swap(v1, v2, help_path)  # wykonanie podmiany pozycji wierzchołków
                help_cost = self.calculate_path(help_path)  # kalkulacja drogi
                best_moves = {**best_moves, **{(v1,
                                                v2): help_cost}}  # sposób na aktualizacje słownika o przejscie i wartość nowej drogi jakie przejscie zapewni

        sorted_best_moves = sorted(best_moves.items(), key=operator.itemgetter(
            1))  # sortowanie słownika w zależności od wartości dróg (od najmniejszej wartości do największej)
        # items w słowniku odwołuję się do par {klucz;wartosc}
        # ustawienie parametru sortowania = itemgetter(1) jakos wartość
        return sorted_best_moves  # zwrócenie posortowanego słownika

    def tabu_search(self):
        '''
        Przeprowadzenie przeszukiwania z zakazami
        :return:
        '''
        help_counter = 0

        while self.current_time < self.max_time:  # dopóki czas aktualny mniejszy od ustawianego
            proccess_time = time.clock()  # pobranie czasu
            if self.counter > self.size * 10:  # jeżeli licznik iteracji bez poprawy jest większy niż dzisieciokrotna ilosc wierzchołków
                self.path = self.generate_random_path()  # wygenerowanie nowej sciezki metodą zachłanną
                self.counter = 0  # licznik iteracji bez poprawy wyzerowany
                self.init_tabu()  # zerowanie tabu

            v1 = random.randint(1, self.size - 1)  # wybranie losowego wierzchołka
            best_moves = self.generate_best_moves(v1)  # wygenerowanie najlepszych ruchów przejść z wierzchołka v1
            nodes_tuple, path_cost = best_moves[0]  # rozpakowanie krawędzi przejscia i kosztu najlepszego przejscia
            v1, v2 = nodes_tuple  # rozpakowanie krawędzi przejcia na pojedyńcze wierzchołki

            if path_cost < self.best_cost:  # jeżeli koszt przejścia jest lepszy niż dotychczasowy
                self.best_time = self.current_time  # ustawienie aktualnego czasu znalezienia najlepszej drogi
                self.counter = 0  # zerowanie licznika iteracji bez poprawy
                self.swap(v1, v2, self.path)  # podmiana wierzchołków w drodze
                self.best_cost = path_cost  # nadpisanie najlepszego kosztu
                self.best_path = self.path  # nadpisanie najlepszej drogi
                self.set_tabu(v1, v2)  # ustawienie kadencji tabu przjeścia
            elif self.tabu[v1][
                v2] > 0:  # jeżeli przejście nie jest lepsze niż dotychczasowe i znajduje sie na liście tabu
                continue  # pomijamy ruch
            else:  # przejście gorsze
                self.counter += 1  # zwiększenie iteracji bez poprawy
                self.swap(v1, v2, self.path)  # podmiana
                self.set_tabu(v1, v2)  # ustawienie kadencji

            self.decrement_tabu()  # zmniejszenie wszystkich kadencji o 1
            proccess_time = time.clock() - proccess_time  # kalkulacja czasu wykonania pojdeynczej iteracji
            self.current_time += proccess_time  # dodanie czasu pojedynczej iteracji do czasu działania algorytmu
            self.helper_time += proccess_time
            if self.helper_time > 10:
                self.costs.append(self.best_cost)
                self.helper_time = 0
                help_counter += 1
        if help_counter * 10 < self.max_time:
            self.costs.append(self.best_cost)

    def annealing(self):

        help_counter = 0

        while self.current_time < self.max_time:  # dopóki czas aktualny mniejszy od ustawianego
            proccess_time = time.clock()  # pobranie czasu
            if self.counter > self.size * 10:  # jeżeli licznik iteracji bez poprawy jest większy niż podwojona ilosc wierzchołków
                self.path = copy.deepcopy(self.best_path)  # powrót do najlepszej drogi
                self.temperature = self.size * 10  # zwiększenie temperatury do wartości = ilość wierzchołków * 10
                self.counter = 0  # licznik iteracji bez poprawy wyzerowany

            v1 = random.randint(1, self.size - 1)  # wybranie losowego wierzchołka
            best = self.generate_best_moves(v1)  # wygenerowanie najlepszych ruchów przejść z wierzchołka v1
            tup, path_cost = best[0]  # rozpakowanie krawędzi przejscia i kosztu najlepszego przejscia
            v1, v2 = tup  # rozpakowanie krawędzi przejcia na pojedyńcze wierzchołki

            if path_cost < self.best_cost:  # jeżeli koszt przejścia jest lepszy niż dotychczasowy
                self.best_time = self.current_time  # ustawienie aktualnego czasu znalezienia najlepszej drogi
                self.counter = 0  # zerowanie licznika iteracji bez poprawy
                self.swap(v1, v2, self.path)  # podmiana wierzchołków w drodze
                self.best_cost = path_cost  # nadpisanie najlepszego kosztu
                self.best_path = copy.deepcopy(self.path)  # nadpisanie najlepszej drogi6
            else:  # przejście gorsze
                self.counter += 1  # zwiększenie iteracji bez poprawy
                delta = abs(path_cost - self.best_cost)  # obliczenie różnicy między aktualna droga a najlepszą
                p = math.exp(-delta / self.temperature)  # wyliczenie prawdopodobieństwa
                if (random.random() < p):  # akceptacja gorszej drogi z prawdopodobieństwem p
                    self.swap(v1, v2, self.path)  # podmiana wierzchołków w drodze

            self.temperature *= self.cooler_const  # zmniejszenie temperatury o stałą chłodzenia
            proccess_time = time.clock() - proccess_time  # kalkulacja czasu wykonania pojdeynczej iteracji
            self.current_time += proccess_time  # dodanie czasu pojedynczej iteracji do czasu działania algorytmu
            self.helper_time += proccess_time
            if self.helper_time > 10:
                self.costs.append(self.best_cost)
                self.helper_time = 0
                help_counter += 1
        if help_counter * 10 < self.max_time:
            self.costs.append(self.best_cost)
