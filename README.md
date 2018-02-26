# Documentation technique

## Table des matières

* [Description](#description)
* [Dépendances et pré-requis de l'application](#dependances)
  * [Procédure d'installation des composants de l'application](#procedure)
  * [Liste exhaustive des paquets Python à installer](#liste_natif)
  * [Liste exhaustive des paquets Python non natif à installer](#liste_non_natif)
* [Paramètres en entrée](#entrees)
* [Sortie possible](#sorties)
* [Gestion des erreurs](#erreurs)
* [Schéma de l'architecture](#architecture)
  * [Diagramme des flux](#diagramme)
  * [Matrice des flux](#matrice)

<a name="description"></a>

## Description

Ce web service écrit en Python vous permet de traduire une chaîne de caractère saisi au clavier dans la langue de votre choix.

Pour ce faire, nous vous demandons de remplir un formulaire contenant 2 entrées :

    - Une entrée pour saisir une chaîne de caractère.
    - Une entrée pour selectionner la langue de traduction.

Une fois que vous avez saisie votre chaîne de caractère, que vous avez selectionné la langue de traduction et que vous avez cliqué sur traduire, ce web service va allé intéroger l'API Google translate en lui envoyant en paramètre dans une URL la chaîne de caractère que vous avez saisie ainsi que la langue de traduction. Si la requête à bien été prise en compte par l'API de Google, elle renvoie au web service une réponse contenant le texte traduit en format JSON.

Le web service récupère donc cette information et enregistre : la date de la traduction, l'heure de la traduction, la chaîne de caractère saisie, la langue de traduction ainsi que la chaîne de caractère traduite dans un fichier CSV. Ceci dans le but de vous restituer la traduction de votre saisie mais aussi de vous fournir un historique de toute vos traductions.

Par suite, le web service vous redirige vers le formulaire. Ce dernier vous ré-affiche le formulaire de traduction ainsi que les informations contenues dans le fichier CSV ce qui en somme vous donnera l'historique de vos traductions et vous offrira la possibilité d'effectuer plusieurs traductions successive.

<a name="dependances"></a>

## Dépendances et pré-requis de l'application

<a name="procedure"></a>

### Procédure d'installation des composants de l'application

Dans ce qui suit, vous allez devoir faire des installations via le terminal. Si vous êtes relié à un réseaux d'entreprise, il se peut que certaines commandes notamment pour réaliser un téléchargement, ne fonctionne pas. C'est pourquoi je vous conseil de débrancher le câble ethernet de votre PC est de vous mettre en partage de connexion via votre mobile durant la phase d'installation.

Pour faire fonctionner ce web service écris en Python, vous avez besoin premièrement de **Python**!

Il existe 2 versions de Python, Python 2 et Python 3. Le code de ce web service fût codé et testé sous Python 2, il est donc garantie qu'il fonctionne sous cette version.

Pour savoir si Python est déjà installé sur votre machine, il suffit d'ouvrir un termminal et d'exécuter la commande `python`. Si le terminal vous affiche quelques chose de ce style :

_Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)] on win32_

_Type "help", "copyright", "credits" or "license" for more information._

c'est que Python est déjà installé sur votre machine!

Si ce n'est pas la cas ou si vous souhaitez installer la dernière version de Python 2 ou Python 3, cliquez sur le lien suivant : **https://www.python.org/downloads/**.

Une fois Python installé, vous avez besoin d'installer plusieurs paquets Python dont la liste exhaustive avec une descriptinon succinte de chacun d'eux se trouve dans les deux tableaux ci-dessous. Le premier regroupe les paquets Python natif c'est à dire ceux que l'on peux importer en ayant juste installé Python. Le second regroupe les paquets Python non natif, c'est à dire qu'il faut les installer via pip avant de les importer.

Pour installer ces paquets non natif, vous utiliserez la commande `pip install` nomDuPaquet dans le terminal. Pour que cette dernière fonctionnne, vous devez préalablement installer le gestionnaire de paquets **pip**!

Pip est déjà installé si vous travaillez dans un environnement virtuel créé par virtualenv ou pyvenv ou si vous utilisez des binaires Python à partir des versions 2.7.9 et 3.4 téléchargés depuis python.org, mais vous devrez mettre à jour pip!

Pour installer pip, il suffit de se rendre sur la page de téléchargement suivante : **https://pip.pypa.io/en/stable/installing/**. Une fois le téléchargement éffectuer, exécuter la commande suivante dans votre terminal : `python get-pip.py`

<a name="liste_natif"></a>

### Liste exhaustive des paquets Python natif à installer

| Paquets   | Description   |
|-----------|---------------|
| csv       | Utilisé pour extraire puis pour afficher les données de la traduction au format CSV dans un but d'historisation.|
| datetime  | Utilisé pour obtenir la date et l'heure de la traduction.|
| random    | Utilisé pour générer un nombre aléatoire.|
| sys       | Utilisé pour géré l'encodage (caractères spéciaux).|

<a name="liste_non_natif"></a>

### Liste exhaustive des paquets Python non natif à installer

| Paquets | Description |
|---------|-------------|
| bottle  | Utilisé comme framework d'application web.|
| requests| Utilisé pour accéder au differentes variables retournée par les pages.|

<a name="entrees"></a>

### Paramètre en entrée

* Une chaîne de caractères saisie par l'utilisateur sur "/formulaire".
* Une langue de traduction choisie dans la liste déroulante par l'utilisateur sur "/formulaire".

<a name="sorties"></a>

### Sortie possible

* Si tous s'exécute correctement
  * Le formulaire pour effectuer une nouvelle traduction.
  * Un tableau HTML composé :
    * de la date de la traduction.
    * de l'heure de la traduction.
    * du texte original.
    * de la langue de traduction.
    * du texte traduit.
    * de l'historique des traductions.
* Si la réponse du serveur de Google est differente de 200 :
  * Un message d'erreur.
  * Le formulaire.
* Si vous cliquez sur "traduire" sans avoir préalablement saisie une chaine de caractère :
  * Un message d'erreur.
  * Le formulaire.

<a name="erreurs"></a>

### Gestion des erreurs

| Erreur | Gestion de l'erreur |
|--------|---------------------|
| Envoie d'une chaîne de caractères vide dans "/formulaire" | On renvoie l'utilisateur vers "/formulaire" avec le message suivant : _Erreur : veuillez saisir quelque chose à traduire._|
| Réponse du serveur de Google differente de 200 | On renvoie à l'utilisateur un message d'erreur : _Erreur : connexion à l'API Google translate impossible._|
| Time out | On renvoie à l'utilisateur un message d'erreur : _Erreur : à faire_|

<a name="architecture"></a>

### Schéma de l'architecture <a id="architecture"></a>

dépendances et pré-requis

* paramètres en entrée et les sorties possibles
* gestion des erreurs (paramètres incorrects, erreurs réseau tels que time out, absence de réponse du serveur Google,  panne réseau etc...)
* schéma de l'architecture : use case, diagramme de séquence, diagramme d'activité et matrice des flux reseaux (URL et ports en entrée et en sortie, en gros, qui communique avec qui/quoi)

<a name="diagramme"></a>

#### Diagramme des flux

![Diagramme des flux](https://github.com/AntoineNOUMA/pythonTranslator/blob/master/Capture.PNG "Diagramme des flux")

<a name="matrice"></a>

#### Matrice des flux

| Acteurs | utilisateur | formulaire () (method="get") | formulaire () (method="post") | mon\_web\_service () | api\_google\_translate |
| :-----: | :---------: | :--------------------------: | :---------------------------: | :------------------: | :--------------------: |
| utilisateurs | - | Remplir formulaire | - | - | - |
| formulaire1() (method="get")| - | - | Envoyer informations_formulaire | - | - |
| formulaire2() (method="post")| Retourner formulaire | - | - |Envoyer informations_formulaire | - |
| mon\_web\_service() | - | - | Afficher information\_mon\_web\_service | Extraire information JSON + Ecrire informations dans CSV | Envoyer information\_mon\_web\_service |
| api\_google\_translate | - | - | - | Envoyer information_api | - |