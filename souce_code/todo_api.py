from flask import Flask, request
import requests

app = Flask(__name__)
liste :dict[str,dict[str,set[str]]] = {}

@app.route("/aggiungiOggetto/")
def aggiungi_oggetto():
    '''
    - aggiungere oggetto a lista
        - nome utente
        - lista della spesa
        - oggetto
    ''' 
    nome = request.args.get('nome')
    lista = request.args.get('lista')
    oggetto = request.args.get('oggetto')
    try:
        # provo ad aggiungere l'oggetto alla lista 
        # dando per scontato che esista sia nome che lista
        liste[nome][lista].add(oggetto)
    except:
        # se fallisce lo step di prima o manca solo la lista
        # o manca anche il nome
        try:
            # provo a vedere se manca solo la lista
            # creando una nuova lista
            liste[nome][lista]={oggetto}
        except:
            # se fallisce significa che manca anche il nome
            # e allora creo tutto
            liste[nome]={lista:{oggetto}}
    return "Oggetto aggiunto"

@app.route("/togliOggetto/")
def togli_oggetto():
    '''
    - togliere oggetto a lista
        - nome utente
        - lista della spesa
        - oggetto
    '''
    nome = request.args.get('nome')
    lista = request.args.get('lista')
    oggetto = request.args.get('oggetto')
    try:
        liste[nome][lista].remove(oggetto)
    except:
        return "Oggetto non trovato"
    return "Oggetto rimosso"

def temperatura_corrente_milano():
    lat = 45.4654219
    lon =  9.1859243
    params = {'latitude': lat,
            'longitude': lon,
            'current':'temperature_2m'}

    response = requests.get(url='https://api.open-meteo.com/v1/forecast', params=params)

    if response.ok:
        response_dictionary = response.json()
        return response_dictionary['current']['temperature_2m']
    else:
        raise ConnectionError

def suggerisci_ombrello():
    try:
        if temperatura_corrente_milano() < 30:
            return True
        else:
            return False
    except ConnectionError:
        return False

@app.route("/vediLista/")
def vedi_lista():
    '''
    - vedi lista della spesa
        - nome utente
        - lista della spesa
    '''
    nome = request.args.get('nome')
    lista = request.args.get('lista')
    try:
        if suggerisci_ombrello():
            lista_temp = liste[nome][lista].copy()
            lista_temp.add("<suggerimento> Ombrello")
            lista_temp = list(lista_temp)
            lista_temp.sort()
            return list(lista_temp)
        return list(liste[nome][lista])
    except:
        return "Lista non trovata"

@app.route("/rimuoviLista/")
def rimuovi_lista():
    '''
    - rimuovi lista della spesa
        - nome utente
        - lista della spesa
    '''
    nome = request.args.get('nome')
    lista = request.args.get('lista')
    try:
        del liste[nome][lista]
        return "Lista rimossa"
    except:
        return "Lista non trovata"

if __name__ == '__main__':
    app.debug = True
    app.run()