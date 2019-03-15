import math
import time
from pprint import pprint
import stale as c
import sys, os


def timeit(func):
    """
    Dekorator funkcji to po prostu funkcja ktora przyjmuje jako argument funkcje.
    Dzieki niemu mozemy 'udekorowac' funkcje, zmierzyc czas i wypisac ja na ekran.
    """
    def wrapper(*args,**kwargs): #args to wszystkie argumenty wymagane, kwargs to wszystkie argumenty opcjonalne
        t0 = time.time()
        result = func(*args,**kwargs)
        print(f"Czas wykonania algorytmu to %.10f" % (time.time()-t0))
        return result
    return wrapper

def wyczysc_ekran():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
  
@timeit
def dijkstra(graf, start, koniec, logika):
    """
    Do funkcji nalezy podać:
        - graf, ktory jest slownikiem slownikow. Dzieki takiej prezentacji mozemy jasno
        okreslic, ile dany wierzcholek ma krawedzi z pozostalymi i jakie maja wagi
       np.
       graf = {
            'A': {'B':3,'C':4,'D':5},
            'B': {'E':5},
            'C': {'E':7},
            'D': {'E':9},
            'E': {},
       }
       - start, ktory jest wierzcholkiem startowym/zrodlowym dla algorytmu
       - koniec, ktory jest wierzcholkiem koncowym
        - logika, true lub false decydujacy czy aplikujemy dodatkowa logike do algorytmu
    Wierzcholek A ma 3 krawedzie, A->B (waga 3), A->C (waga 4), A->D (waga 5),
    B, C i D maja odpowiednio po jednej krawedzi B->E,C->E,D->E o nastepujacych wagach (5,7,9).
    Wierzcholek E ma trzy skierowane na siebie krawedzie od wierzcholkow B, C i D,
    ale zadna krawedz nie idzie wprost od niego.

    Algorytm Dijkstry opracowany przez Edsgera Dijkstre sluzy do znajdowania najkrosztej 
    sciezki z pojedynczego zrodla w grafie o nieujemnych wagach krawedzi.
    Ponizej prezentuje zwiezla implementacje tego algorytmu bez dzielenia jej na podfunkcje.

    """
    przeanalizowane = [] # lista przeanalizowanych wezlow

    D = {}   # tablica odleglosci
    P = {}   # tablica poprzednikow
    
    for wierzcholek in graf.keys():
        D[wierzcholek] = sys.maxsize           # definiujemy tablice odleglosci wartoscia domyslna (nieskonczonosc)
        P[wierzcholek] = ""                    # definiujemy tablice poprzednikow pustą
        
    D[start] = 0        #startujemy od źródła, więc jej dystans równy jest 0
    
    wierzcholki_do_przejscia = list(graf.keys())    # definiujemy wierzcholki do przejscia
    
    while wierzcholki_do_przejscia:                 # dopoki lista jest nie pusta wykonaj
        min_waga = None                          # zdejmij min wage              
        wezel = ""                                 
        for temp_wezel in wierzcholki_do_przejscia: # szukamy węzła o najmniejszej wadze krawędzi
            if min_waga == None:
                min_waga = D[temp_wezel]
                wezel = temp_wezel
            elif D[temp_wezel] < min_waga:
                min_waga = D[temp_wezel]
                wezel = temp_wezel
                
        wierzcholki_do_przejscia.remove(wezel) # wyrzucamy ten wierzcholek z listy
        
        for wezel_pochodny, pochodny_koszt in graf[wezel].items():  # sprawdzamy wagi krawedzi od wybranego wierzcholka
            if D[wezel_pochodny] > D[wezel] + pochodny_koszt:       # wybieramy najmniejszy
                if logika and P[koniec] and D[koniec] < D[wezel] + pochodny_koszt: # na bazie kosztu albo rezygnujemy z analizy tego wierzcholka
                    wierzcholki_do_przejscia.remove(wezel_pochodny)                #albo kontynuujemy analize
                    break
                else:
                    D[wezel_pochodny] = D[wezel] + pochodny_koszt
                    P[wezel_pochodny] = wezel  # i wstawiamy go do tablicy poprzedników o najmniejszej wadze
        przeanalizowane.append(wezel) # dodajemy przeanalizowany wierzcholek
    
    sciezka = []    # pusta lista po wykonaniu algorytmu wskazujaca najkrotsza sciezke
    wezel = koniec  # zaczniemy wypelnianie najkrotszej sciezki od konca i odpowiednio bedziemy ja wypelniac uzywajac tablicy poprzednikow
    koszt = D[koniec]
    while not (wezel == start): # wypelniamy sciezke kolejno wierzcholkami o najmniejszej wadze przejscia
        if sciezka.count(wezel) == 0: 
            sciezka.insert(0, wezel)
            try: 
                wezel = P[wezel]
            except KeyError:
                print(f"Nie mozna w zaden sposob dostac sie do {koniec}. Nalezy poprawic krawedzie.")
                return (None, None, None)
        else:
            break
            
    sciezka.insert(0, start)
    
    return sciezka, koszt, przeanalizowane

def start_aplikacja():
    """
    Glówna funkcja aplikacji
    """
    aktywna = True
    logika = False
    graf = c.GRAF_DOMYSLNY
    print(c.AUTOR,c.TYTUL,sep='\n')
    while aktywna:
        print(*c.OPCJE_APLIKACJI,sep='\n')
        wybor = str(input("Wybieram opcje: "))
        wyczysc_ekran()
        if wybor == 'a':
            graf = wprowadz_graf()
        elif wybor == 'b':
            graf = c.GRAF_DOMYSLNY
        elif wybor == 'c':
            start, koniec = wprowadz_dane(graf)
            sciezka, koszt, przeanalizowane = dijkstra(graf, start, koniec, logika)
            if sciezka is not None and koszt is not None:
                
                print(f"(i) Najkrotsza droga od wierzcholka {start} do {koniec} to {sciezka}.")
                print(f"(ii) Jej koszt to {koszt}.")
                print(f"(iii) Liczba wezlow przeanalizowanych to {len(przeanalizowane)}.")
                print(f"(iv) Logika zaaplikowana? {logika}")
                print(f"Sa one nastepujace {przeanalizowane}.")
        elif wybor == 'd':
            pprint(graf)
        elif wybor == 'e':
            wypisz_krawedzie(graf)
        elif wybor == 'f':
            logika = not logika
            if logika:
                print("Dodatkowa logika została włączona!")
            else:
                print("Dodatkowa logika została wyłączona!")
        elif wybor == 'g':
            print(c.KONIEC)
            sys.exit(0)

def wypisz_krawedzie(graf):
    """
    Funkcja wypisujaca wszystkie krawedzie w grafie
    """
    for i in graf.keys():
        for j in graf[i].keys():
            print(f"{i}->{j} o wadze {graf[i][j]}")


def wprowadz_graf():
    """
    Funkcja pozwalajaca wprowadzic graf/kreator grafu
    """
    wybieram = True
    graf = {}
    while wybieram:
        print(*c.OPCJE_KREATORA_GRAFU,sep='\n')
        wybor = str(input("Wybieram opcje: "))
        wyczysc_ekran()
        if wybor == 'a':
            graf = dodaj_wierzcholek(graf)
        elif wybor == 'b':
            if graf:
                graf = dodaj_krawedz(graf)
            else:
                print("Graf jest pusty, dodaj jakis wierzcholek")
        elif wybor == 'c':
            graf = usun_wierzcholek(graf)
        elif wybor == 'd':
            wybieram = False

    return graf

def wprowadz_dane(graf):
    """
    Funkcja pozwalajaca wprowadzic wierzcholek startowy i koncowy
    """
    start = str(input("Wprowadz wierzcholek startowy: "))
    if not start in graf.keys():
        wyczysc_ekran()
        print(f"{start} nie ma w grafie! Sprobuj jeszcze raz")
        pprint(graf)
        wprowadz_dane(graf)
    koniec = str(input("Wprowadz wierzcholek do ktorego mamy pokazac najkrotsza sciezke: "))
    if not koniec in graf.keys():
        wyczysc_ekran()
        print(f"{start} nie ma w grafie! Sprobuj jeszcze raz")
        pprint(graf)
        wprowadz_dane(graf)
    return start, koniec

def dodaj_wierzcholek(graf):
    """
    Funkcja pozwalajaca dodac wierzcholek do grafu
    """
    n = int(input("Ile chcesz wprowadzic wierzcholkow?"))
    for i in range(1,n+1):
        nazwa_wierzcholka = str(input(f"Podaj nazwe {i}-ego wierzcholka: "))
        graf[nazwa_wierzcholka] = {}
        wyczysc_ekran()
        print("Pomyslnie dodano.")
        pprint(graf)
    print(f"Pomyslnie dodano {n} wierzchołkow o nastepujacych nazwach {list(graf.keys())}")
    return graf

def dodaj_krawedz(graf):
    """
    Funkcja pozwalajaca dodac krawedz do grafu
    """
    pprint(graf)
    p = str(input("Od ktorego wierzcholka chcesz poprowadzic krawedz?: "))
    if p not in graf.keys(): 
        pprint(graf)
        print(f"{p} nie ma w grafie! Sprobuj jeszcze raz")
        dodaj_krawedz(graf)
    n = int(input("Ile chcesz wprowadzic krawedzi?: "))
    for i in range(1,n+1):
        print(graf)
        k = str(input(f"Wprowadz drugi wierzcholek krawedzi {p}-> "))
        if k not in graf.keys():
            pprint(graf)
            print(f"{k} nie ma w grafie! Sprobuj jeszcze raz")
            i-=1
        waga = int(input(f"Podaj wage krawedzi {p}->{k}: "))
        graf[p][k] = waga
        wyczysc_ekran()
        print(graf)
        print("Pomyslnie dodano krawedz.")
    return graf


def usun_wierzcholek(graf):
    """
    Funkcja pozwalajaca usunac wierzcholek z grafu
    """
    w = str(input("Ktory wierzcholek chcesz usunac z grafu?: "))
    if w in graf.keys():
        graf.pop(w)
        print(f"Pomyslnie usunieto wierzcholek {w}")
    else:
        wyczysc_ekran()
        print(graf)
        print(f"Graf nie posiada wierzcholka {w}")
        usun_wierzcholek(graf)
    return graf


if __name__ == "__main__":
    
    wyczysc_ekran()
    start_aplikacja()