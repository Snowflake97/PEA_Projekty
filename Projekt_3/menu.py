import os
from random import randint
from controller import Controller
import datetime
import re
import copy


class Menu:
    '''
    Klasa zajmująca się sterowaniem i interfejsem użytkownika
    '''

    def __init__(self):
        self.weights = []  # macierz wag przejsc
        self.time = 60  # czas dzialania algorytmu
        self.temperature = 0
        self.cooler = 0.9  # wspolczynnik chlodzenia
        self.file_picked = False  # czy plik zostal wybrany
        self.file_name = ''  # nazwa pliku wczytywanego
        self.mutation_lvl = 0.01
        self.cross_lvl = 0.8

        self.printMenu()  # wywołanie metody wyświetlającą menu

    def date_txt(self):
        '''
        Funkcja zwracająca stringa z datą i godziną wywołania
        :return:
        '''
        now = datetime.datetime.today()  # użycie biblioteki datetime
        date_str = now.strftime("%Y.%m.%d_%H-%M-%S")  # formatowanie pobranych zmiennych
        return date_str  # zwrócenie stringa

    def print_atsp_files_in_current_directory(self):
        '''
        Wyświetlenie plików atsp z folderu danych wejściowych ( folder data -> input )
        :return:
        '''
        for entry in os.scandir('./data/input'):
            if entry.is_file() and entry.name[-5:] == ".atsp":
                print(entry.name)

    def try_open_file(self, file_name):
        '''
        Sprawdzenie możliwości otworzenia pliku do odczytu
        Później wykorzystane do sprawdzenia czy podany plik juz istnieje
        :param file_name:
        :return:
        '''
        try:
            open("./data/input/{}".format(file_name), "r")
            return 1
        except IOError:
            return 0

    def read_weights(self, file_name):
        """
        Wczytanie danych z pliku
        :param file_name:
        :return:
        """
        weights = []
        help_list = []
        full_list = []
        #  pobranie wszystkich danych do listy
        with open("./data/input/{}".format(file_name), mode='r') as file:
            data = file.readlines()
        for i in data:
            if len(re.findall(r'\d+', i)) != 0:  # jezeli element listy zawiera liczby
                number_list = re.findall(r'\d+', i)  # pobranie liczb
                for i in number_list:
                    full_list.append(int(i))  # dodanie liczb to list liczb

        full_list.pop(0)  # liczba pobrana z nazwy pliku
        size = full_list.pop(0)  # liczba okreslajaca ilosc wierzcholkow

        #  podzielnie listy na podlisty o wielkosci size
        for position, i in enumerate(full_list):
            if position % size != 0:
                help_list.append(int(i))
            else:
                weights.append(help_list)
                help_list = []
                help_list.append(int(i))
        weights.append(help_list)
        weights.pop(0)  # wyrzucenie pustej lini
        self.weights = copy.deepcopy(weights)  # przypisanie wag
        self.file_name = file_name

    def read_file(self):
        '''
        Czytanie danych z pliku
        :return:
        '''
        print("------ PLIKI TEKSTOWE Z DANYMI ------\n")
        self.print_atsp_files_in_current_directory()  # wyswietlenie plikow z danymi
        file_name = input("Podaj nazwe pliku: ")  # wybranie pliku po nazwie

        if file_name[-5:] != ".atsp":  # jezeli nie wprowadzono rozszerzenia dodanie koncówki .atsp
            file_name += ".atsp"

        if self.try_open_file(file_name) == 1:  # jeżeli udało się otworzyć plik pomyślnie
            print("Sukces!\n")
            self.read_weights(file_name)  # wczytanie wag z pliku
            self.file_picked = True  # ustawienie wczytanego pliku
            self.printMenu()  # powrot do menu
        else:
            print("Niestety nie ma takiego pliku!")  # informacja o braku takiego pliku
            self.printMenu()  # powrót do menu

    def printMenu(self):
        '''
        Proste menu wyboru
        :return:
        '''
        print("------ MENU ------\n")
        print("1. Wczytaj dane")
        print("2. Ustaw czas")
        print("3. Ustaw wspolczynnik krzyzowania")
        print("4. Ustaw wspolcznnik mutacji")
        print("5. Wyswietl aktualne parametry")
        print("6. Wyswietl aktualne dane")
        print("7. Alogrytm Genetyczny")
        print("8. Alogrytm Genetyczny - 10 razy")
        print("9. Seria testow")
        print("0. Koniec\n")

        choise = input("Wybor: ")

        try:
            choise = int(choise)
        except:
            self.printMenu()

        if choise == 1:
            self.read_file()
        elif choise == 2:
            # ustawienie czasu wykonania algorytmu
            choise = input("Czas: ")
            try:
                choise = int(choise)
            except:
                print("Blad!")
                self.printMenu()
            self.time = choise
            print("\n")
            self.printMenu()
        elif choise == 3:
            # ustawienie wspolczynnika krzyzowania
            choise = input("Wspolczynnik krzyzwoania: ")
            try:
                choise = float(choise)
            except:
                print("Blad!")
                self.printMenu()
            self.cross_lvl = choise
            print("\n")
            self.printMenu()
        elif choise == 4:
            choise = input("Wspolczynnik mutacji: ")
            try:
                choise = float(choise)
            except:
                print("Blad!")
                self.printMenu()
            self.mutation_lvl = choise
            print("\n")
            self.printMenu()
        elif choise == 5:
            print(
                "Aktualnie ustawiony czas: {}\nAktualnie ustawiony wspolczynnik krzyzowania: {}\nWspolczynnik mutacji: {}\n".format(
                    self.time,
                    self.cross_lvl, self.mutation_lvl))
            self.printMenu()
        elif choise == 6:
            #  wyswietlenie wag
            print("Aktualne dane: \n")
            if len(self.weights) == 0:
                print("Brak danych!\n")
            else:
                for i in self.weights:
                    print(i)
                print("\n")
            self.printMenu()
        elif choise == 7:
            self.doGenetic()
        elif choise == 8:
            self.do10Genetic()
        elif choise == 9:
            self.doTests()
        elif choise == 0:
            pass

    def save_file(self, algorithm, info):
        '''
        Zapisanie pliku z wynikami
        :param algorithm: rodzaj algorytmu - tabu albo wyzarzanie
        :param info: string z wynikami
        :return:
        '''
        #  przygotowanie unikatowej nazwy pliku zapisu (rok.miesiac.dzien_godzina-minuta-sekunda_rodzaj algorytmu_ilosc miast_ilosc)
        file_name = self.date_txt() + "_" + algorithm + ".txt"
        with open("./data/output/{}".format(file_name), mode="w") as file:
            file.write(info)
        file.close()

    def doGenetic(self):
        if self.file_picked:  # jezeli wybrano plik
            results = self.build_string(None, True)  # wartość True -> pobranie nazwy pliku i czasu
            controller = Controller(copy.deepcopy(self.weights), self.cross_lvl,
                                    self.mutation_lvl)  # utworzenie obiektu klasy do przeprowadzania algorymtu
            controller.set_time(self.time)  # ustawienie czasu w obiekcie controller
            controller.doAlgorithm()  # wywolanie algorytmu genetycznego

            results += self.build_string(controller)  # budowanie stringa z wynikami
            print(results)
            self.save_file("Genetic", results)  # zapisanie wynikow w pliku
            print(controller.costs)

            self.printMenu()  # powrot do menu
        else:
            print("Nie wybrano pliku!\n")  # jezeli nie wybrano pliku
            self.printMenu()

    def do10Genetic(self, test=False):
        if self.file_picked:  # jezeli wybrano plik
            results = self.build_string(None, True)
            for i in range(10):
                controller = Controller(
                    copy.deepcopy(self.weights), self.cross_lvl,
                    self.mutation_lvl)  # utworzenie obiektu klasy do przeprowadzania algorymtu
                controller.set_time(self.time)  # ustawienie czasu w obiekcie controller
                controller.doAlgorithm()  # wywolanie algorytmu genetycznego
                results += "{} Iteracja:\n".format(i)
                results += self.build_string(controller)  # budowanie stringa z wynikami
                results += "\n\n"
            print(results)
            self.save_file("Genetic_10_times", results)  # zapisanie wynikow w pliku
            if test == False:
                self.printMenu()  # powrot do menu
        else:
            print("Nie wybrano pliku!\n")  # jezeli nie wybrano pliku
            self.printMenu()

    def build_string(self, controller, start=False):
        '''
        Budowanie string z wynikami
        :param controller: obiekt klasy controller
        "param start: domyślnie False, jeżeli True oznacza pobranie zwrócenie nazwy pliku i ustawionego czasu przeszukiwania
        :return:
        '''
        build_string = ''
        if start == True:
            build_string += "Plik z danymi: {}\nCzas przeszukiwania: {}\n\n".format(self.file_name, str(self.time))

        else:
            best_time = round(controller.best_time, 2)
            build_string += "Koszt: {} - znaleziony po {} sek\n".format(str(controller.best_cost),
                                                                        str(best_time))  # zapisanie najlepszego kosztu
            for i in controller.costs:
                build_string += "{}:".format(str(i))

            build_string += "\n"

            for i in controller.best_path:
                build_string += "{} -> ".format(str(i))  # zapisanie kolejnych wierzcholkow
            build_string += str(controller.best_path[0])  # zapisanie powrotu - miasta startowego

        return build_string  # zwrocenie pelnego stringa z wynikami

    def doTests(self):
        '''
        Automatyzacja testów
        :return:
        '''
        self.file_picked = True

        self.read_weights("ftv47.atsp")
        self.time = 120
        self.do10Genetic(test=True)

        self.read_weights("ftv170.atsp")
        self.time = 240
        self.do10Genetic(test=True)

        self.read_weights("rbg403.atsp")
        self.time = 360
        self.do10Genetic(test=True)
