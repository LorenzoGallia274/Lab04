# definisco la classe Espositore
class Espositore:
    # costruttore
    def __init__(self, codiceE, nome, cognome):
        # privatizzo gli attributi: codiceE, nome, cognome
        self.__codiceE = codiceE
        self.__nome = nome
        self.__cognome = cognome

    # getter per leggere codiceE dall'esterno
    @property
    def codiceE(self):
        return self.__codiceE
    # metodo per rappresentare l'oggetto (quando faccio print nel main)
    def __str__(self):
        # formattazione f string
        return f'Codice espositore: {self.__codiceE}, nome: {self.__nome}, cognome: {self.__cognome}'
    # metodo per stabilire come funziona l'uguaglianza
    def __eq__(self,other):
        # due espositori sono uguali se il loro codice è uguale
        if self.__codiceE == other.__codiceE:
            return True
        else:
            return False

# definisco la classe Stand
class Stand:
    # costruttore
    def __init__(self,codiceS, metratura, padiglione, prezzo_base):
        # privatizzo gli attributi
        self.__codiceS = codiceS
        self.__metratura = metratura
        self.__padiglione = padiglione
        self.__prezzo_base = prezzo_base
        self.__rif_E = None # lo stand inizia senza espositore

    # getter per leggere il prezzo_base dall'esterno
    @property
    def prezzo_base(self):
        return self.__prezzo_base
    # getter per leggere il rif_E dall'esterno
    @property
    def rif_E(self):
        return self.__rif_E

    # setter per poter modificare rif_E (l'espositore assegnato)
    @rif_E.setter
    def rif_E(self, nuovo_espositore):
        self.__rif_E = nuovo_espositore

    # getter per leggere il codiceS dall'esterno
    @property
    def codiceS(self):
        return self.__codiceS

    # metodo per calcolare il prezzo base, nello stand base ritorna il prezzo base
    def calcola_prezzo(self):
        return self.__prezzo_base

    # metodo per stampare lo stand
    def __str__(self):
        if self.__rif_E == None:
            stato = 'Disponibile'
        else:
            stato = 'Assegnato'
        return f'{self.__codiceS} | {self.__metratura} - {self.__padiglione} - {self.calcola_prezzo()} - {stato}'

    # metodo per stabilire come funziona l'uguaglianza tra stand
    def __eq__(self,other):
        # stand uguali se il codiceS è uguale
        if self.__codiceS == other.__codiceS:
            return True
        else:
            return False
    # metodo less than per
    def __lt__(self,other):
        # uno stand è 'minore' di un altro se il suo prezzo finale calcolato è più basso
        if self.calcola_prezzo() < other.calcola_prezzo():
            return True
        else:
            return False
# definisco la classe figlia: StandPremium di Stand
# eredita tutti gli attributi della classe padre
class StandPremium(Stand):
    # costruttore della classe figlia (parametri padre + specifico del figlio (posizione))
    def __init__(self, codiceS, metratura, padiglione, prezzo_base, posizione):
        # passo i primi 4 parametri al costruttore della classe padre
        super().__init__(codiceS, metratura, padiglione, prezzo_base)
        self.__posizione = posizione

    # metodo che calcola il prezzo finale per la classe StandPremium
    # override del metodo precedente calcola_prezzo, però questo è specifico per gli stand premium
    def calcola_prezzo(self):
        prezzo_base = super().calcola_prezzo() # prezzo base
        prezzo_finale = prezzo_base * 1.30 # prezzo finale, maggiorato del 30 percento
        return prezzo_finale

    # override stampa per gli stand premium
    def __str__(self):
        # passiamo la stampa (stringa) dello stand base (padre)
        base = super().__str__()
        # 'aggiungo' l'attributo del premium (posizione)
        return f'{base} - Stand Premium - posizione: {self.__posizione})'

# classe figlia di Stand: StandPreseExtra
class StandPreseExtra(Stand):
    # costruttore
    def __init__(self, codiceS, metratura, padiglione, prezzo_base, num_prese):
        super().__init__(codiceS, metratura, padiglione, prezzo_base)
        self.__num_prese = num_prese

    # getter di num_prese
    @property
    def num_prese(self):
        return self.__num_prese

    # override del calcola_prezzo
    def calcola_prezzo(self):
        prezzo_base = super().calcola_prezzo() # prezzo base
        prezzo_finale = prezzo_base * (1 + 0.07 * self.__num_prese) # prezzo finale (formula specifica)
        return prezzo_finale

    # override stampa per gli stand con prese extra
    def __str__(self):
        # passiamo la stampa (stringa) dello stand base (padre)
        base = super().__str__()
        # 'aggiungo' l'attributo dello stand prese extra (num_prese)
        return f'{base} - Stand Prese Extra - prese aggiuntive: {self.__num_prese}'

# definisco la classe LingottoFiere
class LingottoFiere:
    # costruttore
    def __init__(self, nome):
        self.__nome = nome # privatizzo il nome (e lo salvo)
        self.__stand = {} # creo un dizionario vuoto per gli stand
        self.__espositori = {} #creo un dizionario vuoto per gli espositori

        """Aggiungere setter e getter se necessari"""
    # getter per leggere il nome dall'esterno (main)
    @property
    def nome(self):
        return self.__nome
    # setter per poter modificare il nome del centro (main)
    @nome.setter
    def nome(self,nuovo):
        self.__nome = nuovo

    # metodo per caricare il file
    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        # gestione delle eccez.
        try:
            # apro il file in mod lettura con with (chiusa automatica)
            with open(file_path, 'r', encoding='utf-8') as file:
                # scorro il file riga per riga
                    for riga in file:
                        # lo 'pulisco'
                        campi = riga.rstrip().split(',')
                        # se il codice inizia con 'ES'
                        if campi[0].startswith('ES'):
                            # allora è un espositore
                            nuovo_espositore = Espositore(campi[0],campi[1],campi[2])
                            # creo l'oggetto e inserisco nel diz usando il codice come chiave
                            self.__espositori[campi[0]] = nuovo_espositore
                        # se non è un espositore ed è lungo 4 caratteri
                        elif len(campi)==4:
                            # allora è uno stand base
                            nuovo_stand = Stand(campi[0],int(campi[1]),campi[2],float(campi[3]))
                            # creo l'oggetto e inserisco nel diz usando il codice come chiave
                            self.__stand[campi[0]] = nuovo_stand
                        # se è lungo 5 caratteri è uno stand speciale
                        elif len(campi)==5:
                            # se il quinto è un numero (num_prese), è uno stand con prese extra
                            if campi[4].isdigit():
                                nuovo_standPE = StandPreseExtra(campi[0],int(campi[1]),campi[2],float(campi[3]),int(campi[4]))
                                self.__stand[campi[0]] = nuovo_standPE
                            # sennò è uno stand premium
                            else:
                                nuovo_standPR = StandPremium(campi[0],int(campi[1]),campi[2],float(campi[3]),(campi[4]))
                                self.__stand[campi[0]] = nuovo_standPR

        # se il comando open fallisce
        except FileNotFoundError:
            # scateno eccez.
            raise

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        # verifico che la chiave codice_stand esista tra le chiavi del dizionario degli stand
        if codice_stand not in  self.__stand.keys():
            raise ValueError("lo stand non esiste!")
        # verifico che la chiave codice_espositore esista tra le chiavi del dizionario degli espositori
        if codice_espositore not in self.__espositori.keys():
            raise ValueError("l'espositore non esiste!")
        # estraggo l'oggetto stand per usarlo più comodamente
        stand_scelto = self.__stand[codice_stand]
        # controllo se l'attributo rif_E dello stand contiene già qualcosa (occupato)
        if stand_scelto.rif_E != None:
            raise ValueError('lo stand non è disponibile!')
        # scorro per ogni stand gli oggetti del diz. degli stand
        for s in self.__stand.values():
            # se l'espositore ne ha già uno (codice dentro un altro stand)
            if s.rif_E == codice_espositore:
                raise ValueError('espositore già assegnato!')
        # se sono stati superati tutti gli if, assegno lo stand all'espositore (modifico rif_E)
        stand_scelto.rif_E = codice_espositore



    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        # scorro per ogni espositore gli oggetti del diz. degli espositori
        for e in self.__espositori.values():
            print(e) # python chiama e.__str__() e lo stampa
            # scorro tutti gli elementi dello stand
            for s in self.__stand.values():
                # se il riferimento dentro lo stand è uguale al codice dell'espositore
                if s.rif_E == e.codiceE:
                    print(f'assegnato allo stand: {s.codiceS}')
                    break # interrompo il ciclo perché può averne uno solo


    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        # ordinati dal più economico al più costoso
        # converto i valori del diz. in una lista (più facilmente ordinabile)
        lista_stand = list(self.__stand.values())
        # la ordino con sorted (metodo) e la 'ritorno'
        return sorted(lista_stand)
