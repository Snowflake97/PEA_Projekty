import os
from read_data import read_data
from random import randint
import datetime
import time


class Menu:
    '''
    Klasa zajmująca się sterowaniem i interfejsem użytkownika
    '''

    def __init__(self):
        self.data = read_data()  # stworzenie obiektu klasy zajmującej się przeprowadzeniem algorytmów
        self.printMenu()  # wywołanie metody wyświetlającą menu
        self.data_name = ''  # przechowywanie nazwy pliku z danymi
        self.counter = 0

    def date_txt(self):
        '''
        Funkcja zwracająca stringa z datą i godziną wywołania
        :return:
        '''
        now = datetime.datetime.today()  # użycie biblioteki datetime
        date_str = now.strftime("%Y.%m.%d_%H-%M-%S")  # formatowanie pobranych zmiennych
        return date_str  # zwrócenie stringa

    def print_txt_files_in_current_directory(self):
        '''
        Wyświetlenie plików tekstowych z folderu danych wejściowych ( folder files->inputs )
        :return:
        '''
        for entry in os.scandir('./files/inputs'):
            if entry.is_file() and entry.name[-4:] == ".txt":
                print(entry.name)

    def try_open_file(self, file_name):
        '''
        Sprawdzenie możliwości otworzenia pliku do odczytu
        Później wykorzystane do sprawdzenia czy podany plik juz istnieje
        :param file_name:
        :return:
        '''
        try:
            open("./files/inputs/{}".format(file_name), "r")
            return 1
        except IOError:
            return 0

    def read_file(self):
        '''
        Czytanie danych z pliku
        :return:
        '''
        print("------ PLIKI TEKSTOWE Z DANYMI ------\n")
        self.print_txt_files_in_current_directory()  # wyswietlenie plikow z danymi
        file_name = input("Podaj nazwe pliku: ")  # wybranie pliku po nazwie
        if file_name[-4:] != ".txt":  # jezeli nie wprowadzono rozszerzenia dodanie koncówki .txt
            file_name += ".txt"

        if self.try_open_file(file_name) == 1:  # jeżeli udało się otworzyć plik pomyślnie
            print("Sukces!\n")
            self.data_name = file_name  # ustalenie nazwy pliku obecnie wybranego
            self.data.__init__()  # wyzerowanie danych w obiekcie liczącym
            self.data.file_name = file_name  # nadanie obiektu nazwy pliku z danymi
            self.data.prep_data()  # przygotowanie danych ( wczytanie z pliku, przygotowanie poprawnej macierzy)
            self.printMenu()  # wyświetlenie menu
        else:
            print("Niestety nie ma takiego pliku!")  # informacja o braku takiego pliku

    def generateData(self):
        '''
        Generowanie losowych danych przejsc dla wybranej ilości miast
        :return:
        '''
        check_file = True
        while check_file:  # ustalenie nazwy pliku z danymi, tak długo aż nazwa będzie inna od istniejących
            file_name = input("Podaj nazwe pliku dla nowych danych: ")
            if file_name[-4:] != ".txt":
                file_name += ".txt"
            if self.try_open_file(file_name) == 1:
                print("Plik o takiej nazwie juz istnieje")
            else:
                check_file = False  # nowy plik, unikatowa nazwa

        check_size = True
        while check_size:  # wymagane wprowadzenie inta
            size = input("Podaj ilosc miast: ")
            try:
                size = int(size)
                check_size = False
            except:
                print("Wprowadz liczbe")
                check_size = True

        check_matrix = True
        while check_matrix:
            current_matrix = self.generate_random_matrix(
                size)  # wygenerowanie i wyswietlenie macierzy dla określonej wielkości
            print("Aktualna macierz: \n")
            self.data.print_nicely(current_matrix)  # wyswietlenie macierzy używjąc metody klasy read_data
            print("\n")
            choise = input(
                "Wygenerowac inna macierz? (t/n): ")  # decyzja o podjęciu aktualnej macierzy bądź wygenerowaniu innej
            if choise.lower() == 't':
                continue
            elif choise.lower() == 'n':
                check_matrix = False

        # zapisanie wygenerowanej i zaakceptowanej macierzy w pliku o ustalonej nazwie
        with open("./files/inputs/{}".format(file_name), mode='w') as file:
            file.write("{}\n".format(size))
            for lists in current_matrix:
                for element in lists:
                    file.write("{} ".format(element))
                file.write("\n")
        file.close()

        question = input(
            "Czy zaladowac wygenerowane dane? (t/n):")  # decyzja o załadowaniu wygenerowanych danych jako obecnych
        if question.lower() == 't':
            self.data.__init__()  # wyczyszczenie poprzednich danych
            self.data_name = file_name  # ustalenie nazwy pliku
            self.data.file_name = file_name
            self.data.prep_data()  # przygotowanie danych

        self.printMenu()  # wyświetlenie menu

    def generate_random_matrix(self, size):
        '''
        Generowanie losowych wartości macierzy dla podanego rozmiaru
        :param size:
        :return:
        '''
        number_of_rands = int(size * (size - 1) / 2)  # wyliczenie ilości potrzebnych losowych wartości
        rand_list = []  # lista przechowywująca losowe wartości
        for i in range(0, number_of_rands):
            rand_list.append(randint(1, 128))  # losowanie wartości z przedziału <1,128>
        matrix = []
        help_list = []
        index = 0

        # wypełnienie lewej dolnej częsci macierzy o losowe wartości i przekątnej
        for columns in range(0, size):
            for rows in range(0, columns + 1):
                if rows == columns:
                    help_list.append(0)
                else:
                    help_list.append(rand_list[index])
                    index += 1
            matrix.append(help_list)
            help_list = []

        # wypełnienie prawej górnej częsci macierzy stosując odbicie lustrzane
        for index, list in enumerate(matrix):
            for i in range(size - index - 1):
                list.append(matrix[i + index + 1][index])
        return matrix

    def bruteMenu(self):
        '''
        Menu dla bruteforcea
        :return:
        '''

        print("1. Wykonaj pojedynczy test")
        print("2. Wykonaj serie testow")
        print("0. Powrot do menu\n")
        choise = int(input("Wybor: "))  # decyzja o wyborze testu

        try:
            choise = int(choise)  # wymagana liczba
        except:
            self.bruteMenu()
        self.counter = 0
        if choise == 1:  # pojedyńcze wykonanie algorytmu
            proccess_time = time.clock()  # pobranie aktualnego czasu
            self.data.doBruteForce()  # wykonanie bruteforca
            proccess_time = time.clock() - proccess_time  # pobranie aktualnego czasu i wyliczenie różnicy miedzy poprzednim
            brute_result = self.data.returnBrute()  # pobranie stringa z rożwiazaniem
            self.data.__init__()  # wyczyszczenie danych
            self.data.file_name = self.data_name  # przypisanie nazwy pliku
            self.data.prep_data()  # przygotowanie danych, możliwośc wywołania następnego algorytmu
            print(brute_result)  # wyświetlenie wyników
            print("\nCzas dla pojedynczego wykonania algorytmu: {} sekund\n".format(proccess_time))
            # przygotowanie pełnego stringa z wynikami
            info = brute_result + ("\nCzas dla pojedynczego wykonania algorytmu: {} sekund".format(proccess_time))
            self.save_file("bruteforce", "single", info)  # zapisanie wyników do pliku

        if choise == 2:
            whole_time = 0
            helper_time = 0
            # wykonanie 150 razy algorytmu. czas zliczany dopiero po pierwszych 50 razach
            for i in range(0, 151):
                if i == 0:
                    proccess_time = time.clock()
                    self.data.doBruteForce()  # wykonanie bruteforca
                    proccess_time = time.clock() - proccess_time
                    helper_time += proccess_time
                    brute_result = self.data.returnBrute()  # pobranie stringa z wynikami
                    self.data.__init__()  # wyczyszczenie danych
                    self.data.file_name = self.data_name  # nadanie nazwy pliku
                    self.data.prep_data()  # przygotowanie danych
                    self.counter = i

                    # takie same kroki + zliczanie czasu każdej iteracji i sumowanie go
                elif i >= 50:
                    proccess_time = time.clock()
                    self.data.doBruteForce()
                    proccess_time = time.clock() - proccess_time
                    whole_time += proccess_time
                    self.data.__init__()  # wyczyszczenie danych
                    self.data.file_name = self.data_name
                    self.data.prep_data()
                    self.counter = i
                    if whole_time > 300:
                        break
                else:
                    proccess_time = time.clock()
                    self.data.doBruteForce()
                    proccess_time = time.clock() - proccess_time
                    helper_time += proccess_time
                    self.data.__init__()
                    self.data.file_name = self.data_name
                    self.data.prep_data()
                    if helper_time > 300:
                        self.counter = i
                        break
            print(brute_result)  # wyswietlenie wyników
            print("\nCzas dla serii 100 razy wykonania algorytmu: {} sekund".format(whole_time))
            print("Usredniony czas - pojedyncze wykonanie: {} sekund\n".format(whole_time / 100))
            # przygotowanie płenego stringa z wynikami i czasami
            info = "Sprawdzono {} iteracji (na 150) \n".format(self.counter) + brute_result + (
                "\nCzas dla pojedynczego wykonania algorytmu: {} sekund".format(proccess_time)) + (
                       "\nUsredniony czas - pojedyncze wykonanie: {} sekund\n".format(whole_time / 100))
            self.save_file("bruteforce", "multiple", info)  # zapis danych do plików
        self.printMenu()

    def branchMenu(self):
        # wyswietlenie opcji
        print("1. Wykonaj pojedynczy test")
        print("2. Wykonaj serie testow")
        print("0. Powrot do menu\n")
        choise = int(input("Wybor: "))

        try:
            choise = int(choise)  # wymagana liczba
        except:
            self.branchMenu()

        self.counter = 0
        if choise == 1:  # jednorazowe wykonanie algorytmy
            proccess_time = time.clock()  # aktualny czas
            self.data.doBranchAndBound()  # wykonanie algorytmu
            proccess_time = time.clock() - proccess_time  # aktualny czas i roznica miedzy czasami
            branch_result = self.data.determine_path()  # pobranie stringa z wynikiem
            self.data.__init__()  # wyzerowanie danych
            self.data.file_name = self.data_name  # przypisanie nazwy pliku
            self.data.prep_data()  # przygotowanie danych do wykonania algorytmu
            print(branch_result)  # wyświetlenie wyniku
            print(
                "\nCzas dla pojedynczego wykonania algorytmu: {} sekund\n".format(proccess_time))  # wyświetlenie czasu
            # przygotowanie stringa z wszystkimi danymi
            info = branch_result + ("\nCzas dla pojedynczego wykonania algorytmu: {} sekund".format(proccess_time))
            self.save_file("branch&bound", "single", info)  # zapis do pliku

        if choise == 2:  # seria wykonania algorytmu
            whole_time = 0  # czas całkowity
            for i in range(0, 151):
                if i == 0:
                    self.data.doBranchAndBound()  # wykonanie algorytmu
                    branch_result = self.data.determine_path()  # pobranie wyniku
                    self.data.__init__()  # wyzerowanie danych
                    self.data.file_name = self.data_name  # przypisanie nazwy pliku
                    self.data.prep_data()  # przygotowanie danych do następnego wywołania algorytmu
                elif i >= 50:
                    proccess_time = time.clock()  # pobranie aktualnego czasu
                    self.data.doBranchAndBound()  # wywołanie algorytmu
                    proccess_time = time.clock() - proccess_time  # pobranie aktualnego czasu i wyliczenie różnicy
                    whole_time += proccess_time  # dodanie czasu kolejnych iteracji do całkowitego czasu
                    self.data.__init__()  # wyzerowanie danych
                    self.data.file_name = self.data_name  # przypisanie nazwy pliku
                    self.data.prep_data()  # przygotowanie danych do następnego wywołania algorytmu
                else:
                    self.data.doBranchAndBound()  # wywołanie algorytmu
                    self.data.__init__()  # wyzerowanie danych
                    self.data.file_name = self.data_name  # przypisanie nazwy pliku
                    self.data.prep_data()  # przygotowanie danych do następnego wywołania algorytmu
            print(branch_result)  # wyświetlenie wyników
            print("\nCzas dla serii 100 razy wykonania algorytmu: {} sekund".format(
                whole_time))  # czas dla serii 100 wywołan
            print("Usredniony czas - pojedyncze wykonanie: {} sekund\n".format(whole_time / 100))  # uśredniony czas
            # przygotowanie stringa z wszystkimi danymi
            info = branch_result + ("\nCzas dla pojedynczego wykonania algorytmu: {} sekund".format(proccess_time)) + (
                "\nUsredniony czas - pojedyncze wykonanie: {} sekund\n".format(whole_time / 100))
            self.save_file("branch&bound", "multiple", info)  # zapis do pliku

        self.printMenu()  # wyświetlenie menu

    def printMenu(self):
        '''
        Proste menu wyboru
        :return:
        '''
        print("------ MENU ------\n")
        print("1. Wczytaj dane")
        print("2. Wygeneruj dane")
        print("3. Brute Force")
        print("4. Branch and Bound")
        print("5. Wyswietl aktualne dane")
        print("0. Koniec\n")

        choise = input("Wybor: ")

        try:
            choise = int(choise)
        except:
            self.printMenu()

        if choise == 1:
            self.read_file()
        elif choise == 2:
            self.generateData()
        elif choise == 3:
            self.bruteMenu()
        elif choise == 4:
            self.branchMenu()
        elif choise == 5:
            print("Aktualne dane: \n")
            self.data.print_nicely(self.data.matrix)
            print("\n")
            self.printMenu()
        elif choise == 0:
            pass

    def save_file(self, algorithm, quantity, info):
        '''
        Zapisanie pliku z wynikami
        :param algorithm: rodzaj algorytmu - bruteforce albo branch&bound
        :param quantity: ilość czyli pojedyńcze wykonanie albo seria
        :param info: string z wynikami
        :return:
        '''
        number_of_cities = str(self.data.size)  # liczba miast jako string
        # przygotowanie unikatowej nazwy pliku zapisu (rok.miesiac.dzien_godzina-minuta-sekunda_rodzaj algorytmu_ilosc miast_ilosc)
        file_name = self.date_txt() + "_" + algorithm + "_" + number_of_cities + "cities" + "_" + quantity + ".txt"
        with open("./files/outputs/{}".format(file_name), mode="w") as file:
            if quantity == "single":  # jezeli test pojdeyńczy
                # zapisanie danych wybieralnych
                file.write(
                    "Algorytm: {}\nIlosc miast: {}\nPojedyncze wykonanie\n\n".format(algorithm, number_of_cities))
                for i in self.data.matrix:  # zapisanie macierzy dla której został wykonany algorytm
                    for j in i:
                        file.write("{} ".format(j))
                    file.write("\n")
                file.write("\n\n")
                file.write(info)  # zapisanie wyników testu
            if quantity == "multiple":  # jeżeli seria testów
                file.write("Algorytm: {}\nIlosc miast: {}\nSeria wykonan(150 lacznie, czas liczony dla 100)\n\n".format(
                    algorithm, number_of_cities))  # zapisanie danych wybieralnych
                for i in self.data.matrix:  # zapisanie macierzy dla której został wykonany algorytm
                    for j in i:
                        file.write("{} ".format(j))
                    file.write("\n")
                file.write("\n\n")
                file.write(info)  # zapisanie wyników testu
        file.close()
