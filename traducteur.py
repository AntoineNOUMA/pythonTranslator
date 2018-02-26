# -*-coding:utf-8 -*-
"""
DESCRIPTION
Ce web service écrit en Python vous permet de traduire une chaîne de caractère saisi au clavier dans
la langue de votre choix. Pour ce faire, une fois que vous avez saisie votre chaîne de caractère,
que vous avez sélectionné la langue de traduction et que vous cliquez sur traduire, ce web service
va intéroger l'API Google translate en lui envoyant en paramètre dans une URL la chaîne de
caractère que vous avez saisie ainsi que la langue de traduction. Si la requête a bien été prise en
compte par l'API de Google, elle nous renvoie une réponse contenant le texte traduit en format JSON.
Nous récupérons donc cette information et nous enregistrons : la date de la traduction, l'heure de
la traduction, la chaîne de caractère saisie, la langue de traduction ainsi que la chaîne de
caractère traduite dans un fichier CSV. Ceci dans le but de vous restituer la traduction de votre
saisie, mais aussi pour vous fournir un historique de toutes vos traductions. Ensuite, nous
convertissons ce fichier CSV en un fichier HTML qui nous servira à vous afficher l'historique de vos
traductions.
"""

def debug(my_text):
    """[Fonction permettant le debugage de l'application. Equivalente à un print, cette fonction donne
    des informations au technicien sur les éventuelles erreurs générées]
    
    Arguments:
        my_text {[str]} -- [Message à l'attention du technicien]
    """

    if debug:
        print my_text

try:
    import config
except ImportError:
    debug("Le module config n'a pas été trouvé.")

try:
    from bottle import get
except ImportError:
    debug("Le module get de bottle n'a pas été trouvé.")

try:
    from bottle import post
except ImportError:
    debug("Le module post de bottle n'a pas été trouvé.")

try:
    from bottle import redirect
except ImportError:
    debug("Le module redirect de bottle n'a pas été trouvé.")

try:
    from bottle import request
except ImportError:
    debug("Le module request de bottle n'a pas été trouvé.")

try:
    from bottle import route
except ImportError:
    debug("Le module route de bottle n'a pas été trouvé.")

try:
    from bottle import run
except ImportError:
    debug("Le module run de bottle n'a pas été trouvé.")

try:
    import csv
except ImportError:
    debug("Le module csv n'a pas été trouvé.")

try:
    import datetime
except ImportError:
    debug("Le module datetime n'a pas été trouvé.")

try:
    import requests
except ImportError:
    debug("Le module requests n'a pas été trouvé.")

try:
    import json
except ImportError:
    debug("Le module json n'a pas été trouvé.")

try:
    import os
except ImportError:
    debug("Le module os n'a pas été trouvé.")

try:
    import sys
except ImportError:
    debug("Le module sys n'a pas été trouvé.")

#Permet de gérer l'encodage utf-8 pour éviter les problèmes d'accents etc...
reload(sys)
sys.setdefaultencoding('utf8')
#VARIABLE GLOBAL

##Dictionnaire permettant de stocker les variables du formulaire (chaîne de caractère à traduire et
# langue de traduction).
DICT1 = dict
##Dictionnaire permettant de stocker les variables du web service (date de traduction, heure de
# traduction, chaîne de caractère à traduire, langue de traduction, texte traduit).
DICT2 = dict
##Variable permettant de stocker un token.
TOKEN = ""

#Route par défaut
@route('/')

@route('/formulaire/')
@get('/formulaire')
def formulaire1():
    """[Fonction générant un formulaire en méthode get avec une case pour saisir du texte,
    une liste déroulante pour selectionner la langue à traduire et un
    bouton pour envoyer l'information.]
    
    Decorators:
        get
        route
    """

    open("historique.csv", "a")
    return'''
    <form action="/formulaire" method="post">
       
        Votre texte à traduire: <input name="texte" type="text" />

        <select name="langue" size="1">
            <option value="fr">Français</option>
            <option value="en">Anglais</option>
            <option value="de">Allemand</option>
            <option value="es">Espagnol</option>
            <option value="it">Italien</option>
            <option value="ko">Koréen</option>
        </select>

        <input type="submit" value="Traduire" />

    </form>''' + '''
    
    Historique de vos traduction :''' + affichage()

@route('/formulaire/')
@post('/formulaire')
def formulaire2():
    """[Fonction vérifiant le formulaire en méthode post avec une case pour saisir du texte,
    une liste déroulante pour selectionner la langue à traduire et un
    bouton pour envoyer l'information.]
    
    Decorators:
        post
        route
    
    Returns:
        [str] -- [Redirection vers mon_web_service]
    """

    if request.forms.get('texte') == "":

        return "Erreur : veuillez saisir quelque chose à traduire.<br><br>" + '''
        <form action="/formulaire" method="post">
                
            Votre texte à traduire: <input name="texte" type="text" />

            <select name="langue" size="1">
                <option value="fr">Français</option>
                <option value="en">Anglais</option>
                <option value="de">Allemand</option>
                <option value="es">Espagnol</option>
                <option value="it">Italien</option>
                <option value="ko">Koréen</option>
            </select>

            <input type="submit" value="Traduire" />

        </form>''' + '''
        
        Historique de vos traduction :''' + affichage()

    global TOKEN
    TOKEN = os.urandom(24).encode('hex')
    global DICT1
    DICT1 = {'texte':'', 'langue':''}
    DICT1['texte'] = request.POST['texte']
    DICT1['langue'] = request.POST['langue']
    return redirect("/mon_web_service/"+str(TOKEN))

@route('/mon_web_service/<token>')
def mon_web_service(token):
    """[Fonction qui interroge l'API Google translate.
    Récupération des informations au format JSON.]
    
    Decorators:
        route
    
    Arguments:
        token {[str]} -- [clé chiffrée]
    
    Returns:
        [str] -- [Message d'erreur si les deux clés chiffrées ne corespondent pas]
        [str] -- [Message d'erreur si il y à une erreur de connexion avec l'API Google translate]
        [str] -- [Redirection vers formulaire]
    """

    resp1 = request.url_args['token']
    if TOKEN != resp1:
        return "Error token"

    global DICT2

    DICT2 = {'date':'', 'heure':'', 'texte_original':'', 'langue':'', 'texte_traduit':''}

    date = datetime.datetime.now()

    DICT2['texte_original'] = DICT1['texte']
    DICT2['langue'] = DICT1['langue']
    DICT2['date'] = str(date.day) + '-' + str(date.month) + '-' + str(date.year)
    DICT2['heure'] = str(date.hour) + ':' + str(date.minute) + ':' + str(date.second)

    url = "https://translation.googleapis.com/language/translate/v2?key="
    key = config.api_key
    url = url + key + DICT2['texte_original'] + "&target=" + DICT2['langue']
    resp2 = requests.get(url)

    if resp2.status_code != 200:

        return "Erreur : connexion à l'API Google translate impossible." + formulaire1()

    traduction_json = resp2.json()
    DICT2['texte_traduit'] = traduction_json['data']['translations'][0]['translatedText']
    ecriture_csv()
    DICT1['texte'] = ""
    DICT1['langue'] = ""

    return redirect("/formulaire")

def ecriture_csv():
    """[Fonction qui permet l'écriture dans un fichier csv.]
    """

    with open("historique.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', dialect="excel")
        writer.writerow([DICT2['date'], DICT2['heure'], DICT2['texte_original'],
                         DICT2['langue'], DICT2['texte_traduit']])
        csvfile.close()

def affichage():
    """[Fonction qui permet l'affichage du fichier csv.]
    
    Returns:
        [str] -- [Chaîne de caractère contenant toutes les informations de la traduction]
    """

    filename = 'historique.csv'
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        try:
            chaine = ""
            for row in reader:
                chaine += "<tr>"
                for column in row:
                    chaine += "<td>"+str(column)+"</td>"
                chaine += "</tr>"
            if chaine != "":
                chaine = "<table>"+chaine+"</table>"
            return chaine
        except csv.Error as csverror:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, csverror))

run(host='localhost', port=8080, debug=True)

"""
TO DO
- Optimiser les boucles(complexité)
- faire des try except sur les flux (get, urlopen etc...)
"""
