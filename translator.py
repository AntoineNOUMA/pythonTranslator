# -*-coding:utf-8 -*-
"""
DESCRIPTION
This web service written in Python allows you to translate a string into the language of your choice.
To do this, we ask you to fill out a form containing 2 inputs:
    - An input to write a string.
    - An input to select the language of translation.
Once you have written your string, selected the language of translation and clicked on translate, this 
web service will interoperate with the Google translate API by sending as a parameter in the URL the 
string you have written and the language of translation. If the request has been taken by the Google 
API, it sends back to the web service a response containing the translated text in a JSON format.
The web service retrieves this information and records: the date and time of the translation, the 
string written, the language of translation and the string translated into a CSV file. This in order 
to give you the translation of your input but also to provide you an history of all your translations.
As a result, the web service redirects you to the form. The latter re-displays the translation form as 
well as the information contained in the CSV file which will give you the history of your translations 
and offer you the possibility to perform several successive translations.
"""

def debug(my_text):
    """[Function allowing the debugging of the application. Equivalent to a print, this function gives
    information to the technician about any errors generated]
    
    Arguments:
        my_text {[str]} -- [Message to the technician]
    """
    if debug:
        print my_text

try:
    from bottle import get, post, redirect, request, route, run
except ImportError, e:
    debug("Bottle error")
    debug(e)
        
try:
    import csv, datetime, json, os, requests, sys
except ImportError, e:
    debug("Native error")
    debug(e)

try:
    import config
except ImportError, e:
    debug("Intern error")
    debug(e)
        
#Allows to manage the utf-8 encoding to avoid the problems of accents etc ...
reload(sys)
sys.setdefaultencoding('utf8')

#GLOBAL VARIABLE
#Dictionary to store the variables of the form (string to translate and
#language translation).
DICT1 = dict
#Dictionary allowing to store the variables of the web service (date and time of translation,
#string to translate, language of translation, translated text).
DICT2 = dict
##Variable to store a token.
TOKEN = ""

#Default route
@route('/')

@route('/form/')
@get('/form')
def display_form():
    """[Function generating a form in get method with a box to enter text,
    a drop-down list to select the language to be translated and a
    button to send the information.]
    
    Decorators:
        get
        route
    """
    open("history.csv", "a")
    return'''
    <form action="/form" method="post">
        Your text to translate: <input name="text" type="text" />
        <select name="language" size="1">
            <option value="fr">French</option>
            <option value="en">English</option>
            <option value="de">German</option>
            <option value="es">Spanish</option>
            <option value="it">Italian</option>
            <option value="ko">Korean</option>
        </select>
        <input type="submit" value="Translate" />
    </form>''' + '''Translation history :''' + show_history()

@route('/form/')
@post('/form')
def post_form():
    """[Function checking the form in post method with a box to enter text,
    a drop-down list to select the language to be translated and a
    button to send the information]
    
    Decorators:
        post
        route
    
    Returns:
        [str] -- [Redirection to translator]
    """
    if request.forms.get('text') == "":
        return "Error: Please enter something to translate.<br><br>" + '''
        <form action="/form" method="post">    
            Your text to translate: <input name="text" type="text" />
        <select name="language" size="1">
            <option value="fr">French</option>
            <option value="en">English</option>
            <option value="de">German</option>
            <option value="es">Spanish</option>
            <option value="it">Italian</option>
            <option value="ko">Korean</option>
        </select>
        <input type="submit" value="Translate" />
    </form>''' + '''Translation history :''' + show_history()
    global TOKEN
    TOKEN = os.urandom(24).encode('hex')
    global DICT1
    DICT1 = {'text':'', 'language':''}
    DICT1['text'] = request.POST['text']
    DICT1['language'] = request.POST['language']
    return redirect("/translator/"+str(TOKEN))

@route('/translator/<token>')
def translator(token):
    """[Function that queries the Google translate API.
    Retrieving information in JSON format.]
    
    Decorators:
        route
    
    Arguments:
        token {[str]} -- [encrypted key]
    
    Returns:
        [str] - [Error message if the two encrypted keys do not match]
        [str] - [Error message if there is a connection error with the Google translate API]
        [str] - [Redirect to form]
    """
    resp1 = request.url_args['token']
    if TOKEN != resp1:
        return "Error token"
    global DICT2
    DICT2 = {'date':'', 'original_text':'', 'language':'', 'translated_text':''}
    date = datetime.datetime.now().isoformat()
    DICT2['original_text'] = DICT1['text']
    DICT2['language'] = DICT1['language']
    DICT2['date'] = date
    url = "https://translation.googleapis.com/language/translate/v2?key="
    key = config.api_key
    url = url + key + DICT2['original_text'] + "&target=" + DICT2['language']
    resp2 = requests.get(url)
    if resp2.status_code != 200:
        return "Error: Can not connect to Google translate API" + display_form()
    traduction_json = resp2.json()
    DICT2['translated_text'] = traduction_json['data']['translations'][0]['translatedText']
    write_history()
    DICT1['text'] = ""
    DICT1['language'] = ""
    return redirect("/form")

def write_history():
    """[Function that allows writing to a csv file.]
    """
    with open("history.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', dialect="excel")
        writer.writerow([DICT2['date'], DICT2['original_text'], DICT2['language'], DICT2['translated_text']])
        csvfile.close()

def show_history():
    """[Function that allows the display of the csv file.]
    
    Returns:
        [str] -- [String containing all the information of the translation]
    """
    filename = 'history.csv'
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        try:
            string = ""
            for row in reader:
                string += "<tr>"
                for column in row:
                    string += "<td>"+str(column)+"</td>"
                string += "</tr>"
            if string != "":
                string = "<table>"+string+"</table>"
            return string
        except csv.Error as csverror:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, csverror))

run(host='localhost', port=8080, debug=True)
