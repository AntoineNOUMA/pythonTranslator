# Technical documentation

## Table of Contents

* [Description](#description)
* [Dependencies and prerequisites of the application](#dependancies)
  * [How to install application components](#process)
  * [Exhaustive list of native Python packages to install](#native_list)
  * [Exhaustive list of non-native Python packages to install](#non_native_list)
* [Input parameters](#inputs)
* [Possible outputs](#outputs)
* [Error management](#errors)
* [Architecture diagrams](#architecture)
  * [Flow chart](#chart)
  * [Flow matrix](#matrix)

<a name="description"></a>

## Description

This web service written in Python allows you to translate a string into the language of your choice.

To do this, we ask you to fill out a form containing 2 inputs:

    - An input to write a string.
    - An input to select the language of translation.

Once you have written your string, selected the language of translation and clicked on translate, this web service will interoperate with the Google translate API by sending as a parameter in the URL the string you have written and the language of translation. If the request has been taken by the Google API, it sends back to the web service a response containing the translated text in a JSON format.

The web service retrieves this information and records: the date and time of the translation, the string written, the language of translation and the string translated into a CSV file. This in order to give you the translation of your input but also to provide you an history of all your translations.

As a result, the web service redirects you to the form. The latter re-displays the translation form as well as the information contained in the CSV file which will give you the history of your translations and offer you the possibility to perform several successive translations.

<a name="dependancies"></a>

## Dependencies and prerequisites of the application

<a name="process"></a>

### How to install application components

In what follows, you will have to make installations via the terminal. If you are connected to a corporate network, some commands, especially for downloading, may not work. That's why I advise you to disconnect the ethernet cable from your PC and put you in connection sharing via your mobile during the installation phase.

To make this web service written in Python work, you need **Python** first!

There are 2 versions of Python, Python 2 and Python 3. The code of this web service was coded and tested under Python 2, so it is guaranteed that it works in this version.

To find out if Python is already installed on your machine, just open a terminal and run the `python` command. If the terminal shows you something like this:

_Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)] on win32_

_Type "help", "copyright", "credits" or "license" for more information._

Python is already installed on your machine!

If this is not the case, or if you want to install the latest version of Python 2 or Python 3, click on the following link: <https://www.python.org/downloads/>.

Once Python is installed, you need to install several Python packages whose exhaustive list with a short description of each one is in the two tables below. The first group contains native Python packages, ie those that can be imported by just installing Python. The second one groups, non-native Python packages, ie they must be installed via pip before importing them.

To install these non-native packages, you will use the `pip install` packageName command in the terminal. In order for this to work, you must first install the **pip**!

Pip is already installed if you are working in a virtual environment created by virtualenv or pyvenv or if you are using Python binaries from versions 2.7.9 and 3.4 downloaded from python.org, but you will need to update pip!

To install pip, simply go to the following download page: <https://pip.pypa.io/en/stable/installing/>. Once the download is complete, run the following command in your terminal: `python get-pip.py`

This web service interacts with the Google translate API. To make this interaction possible, you must have an API key.

To begin, you need to create a **config.py** file and copy this piece of code into `api_key = "key"`. Then save this file to the folder where there is the main program **translator.py**.

In the piece of code given previously, it is necessary of course that the **key** word is replaced by the original key of the Google Translate API. To do that, you must have a Gmail account. If you don't have one, you can create once at this link: <https://accounts.google.com/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default>.

After that, click on the following link and log in with your Gmail IDs: <https://console.developers.google.com/cloud-resource-manager?Authuser=0>.

Then click on **Create Project**.

Create a project name and click **Create**. Once the project is created, the **Developers Console** window opens by increasing the name of your project at the top left.

Click on **APIs & Auth** and then on **APIs**.

Find in the **Translate API** list which is under **Other Popular APIs**.

Click on **Enable API**. Wait a few moments for the API activation.

Then click on **Project Billing Settings**.

Click on **Accept and start the free trial**. You will be redirected to the **Developers Console** window.

In the menu, click on **APIs & Auth** then **Credentials**.

Click on **Add crendentials API Key**.

Click **Server Key** and click **Create**.

Your API key is now displayed! Copy it and paste it into your `config.py` file using Ctrl + V.

The translator is now operational!

<a name="native_list"></a>

### Exhaustive list of native Python packages to install

| Packages   | Description   |
|------------|---------------|
| csv        | Used to extract and display the translation data in CSV format for historical purposes. |
| datetime   | Used to get the date and time of the translation. |
| json       | Used to manage the json format. |
| os         | Used to generate a random number. |
| sys        | Used to manage the encoding (special characters). |

<a name="non_native_list"></a>

### Exhaustive list of non-native Python packages to install

| Packages | Description |
|----------|-------------|
| bottle   | Used as a web application framework. |
| config   | Used to access the Google translate API key. |
| requests | Used to access the different variables returned by the pages. |

<a name="inputs"></a>

### Input parameters

* A string written by the user on "/form".
* A translation language chosen from the drop-down list by the user on "/form".

<a name="outputs"></a>

### Possible outputs

* If all runs properly
  * The form to make a new translation.
  * An HTML table composed of:
    * the date and time of the translation.
    * the original text.
    * the language of translation.
    * the translated text.
    * the translation history.
* If the answer from Google's server is different from 200:
  * An error message.
  * The form.
* If you click on "translate" without first entering a string:
  * An error message.
  * The form.

<a name="errors"></a>

### Error management

| Error | Error management |
|-------|------------------|
| Send an empty string into "/ form" | The user is returned to "/ form" with the following message: _Error: Please enter something to translate._ |
| Google's server response different from 200 |  We send an error message to the user: _Error: Can not connect to the Google translate API._ |
| Time out | We send an error message to the user: _Error : to do._ |

<a name="architecture"></a>

### Architecture diagrams <a id="architecture"></a>

<a name="chart"></a>

#### Flow chart

![Flow chart](https://github.com/AntoineNOUMA/pythonTranslator/blob/master/Capture.PNG "Flow chart")
![Flow chart](C:\Users\QS5611\Desktop\pythonTranslator\Capture.png "Flow chart")

<a name="matrix"></a>

#### Flow matrix

| Actors | user | show_form () (method="get") | post_form () (method="post") | translator() | google\_translate\_api |
| :----: | :--: | :-------------------------: | :--------------------------: | :----------: | :--------------------: |
| user | - | Fill form | - | - | - |
| show_form() (method="get")| - | - | Send form_data | - | - |
| post_form() (method="post")| return form | - | - | Send form_data | - |
| translator() | - | - | Display translator_data | Extract JSON_data + Write data in CSV | Send translator_data |
| google\_translate\_api | - | - | - | Send api_data | - |