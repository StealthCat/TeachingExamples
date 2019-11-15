'''Make a new vocab checker and submitter for working documents
1. scan in document - Done-ish
    cannot be directly opened, must be imported word at a time
        work other services?
2. make list of all words - Done
3. make set of all words - Done
4. run set through "dictionary" - Done
5. create a python dictionary of words and definitions - Done
6. display words as key:value pairs - Done
    sorted by farsi alphabet
7. make list of words not found in "dictionary" - Done
8. tag new words with shop id 
    adds new column with tag
9. batch process words for upload to "dictionary"
    format based on upload requirements
10. upload words to "dictionary" for approval
    groups of 25 max'''

# python script.py text.txt - opens the python script and desired file in a single command

# Import needed packages
import os
import string
import time
import pandas as pd
from tabulate import tabulate
from google.cloud import translate

#Define global variables
alphabet = (string.ascii_letters +'\n' + '\r' + '.' + ' ' + '()' + ')' + '"')
#source_file = ''
#Setup for Google APK and Cloud API
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'My First Project-edb4fd6d1bf1.json'
client = translate.TranslationServiceClient()
parent = client.location_path('sodium-sublime-258916', 'global')


def file_info(): #Gets the needed file's info from the user and loads the file
    source_file = input("What is your file name with extension? ex: DocName.txt ")
    # Open file and name it source_text
    with open(source_file, 'r', encoding='utf-8-sig') as ft_open:
        source_text = ft_open.read().split(' ')
    return source_text

def process_file(source_text): #Processes the file into a list of unque words for translation
    # Removes all English letters by parsing the text into words, then check each word for English letters, and reassembles letters into words
    for index in range(len(source_text)):
        new_word = []
        for char_index in range(len(source_text[index])):
            if source_text[index][char_index] not in alphabet:
                new_word.append(source_text[index][char_index])
        source_text[index] = "".join(new_word)
    #removes all the empty places from the list
    source_text = [word for word in source_text if word]
    #sorts in place
    source_text.sort()
    #makes a set of unique words
    noduplist = []
    for element in source_text:
        if element not in noduplist:
            noduplist.append(element)
    return noduplist

def translator(noduplist): #Translator
    result = (client.translate_text(noduplist, 'en', parent))
    definitions = [translation.translated_text for translation in result.translations]
    return definitions

#Formats text and prints the list to the screen for debugging
#for index in range(len(noduplist)):
#   print('{} -> {}'.format(noduplist[index], definitions[index]))

def make_DF(noduplist, definitions):
    #Makes list into a dictionary into a pandas dataframe
    doc_dict = {'Source': noduplist, 'English': definitions}
    final_list = pd.DataFrame(doc_dict, columns = ['Source', 'English'])
    pprint_df(final_list)
    return final_list

def new_word_checker(final_list):
    #Checks to see if any words came back as unknown, and then places those words into a new list
    #will need to be changed when using new API inside
    new_words =[]
    definitions2 = ['NaN', 'test', 'blah','NaN', 'this','thing', 'is', 'NaN', 'boring']
    noduplist2 = ['1','2','3','4','5','6','7','8','9','10']
    for word in range(len(definitions2)):
        if definitions2[word] == 'NaN':
            new_words.append(noduplist2[word])
    return new_words

def tagger(new_words):
    #Tags new words with shop label, compiles them with their definition, and places it into a dictionary
    shop_tag = (['test']*len(new_words))
    definitions3 = ([' ']*len(new_words))
    new_word_dict ={'Source': new_words, 'English':definitions3,'Tag': shop_tag}
    final_new_words = pd.DataFrame(new_word_dict, columns = ['Source', 'English', 'Tag'])
    pprint_df(final_new_words)
    return new_word_dict

def export(new_word_dict):     #Converts dictionary to a dataframe and exports the file
    new_word_dict = pd.DataFrame(new_word_dict)
    new_word_dict.to_csv('new_word_dict.csv', header = True, index = None, sep = ',', encoding = 'utf-8', mode = 'a')
    print('File exported to working directory')

def pprint_df(dframe):
    print (tabulate(dframe, headers='keys', tablefmt='psql', showindex=False))

#Insert code from highside:

'''
9. batch process words for upload to "dictionary"
    format based on upload requirements
10. upload words to "dictionary" for approval 
    groups of 25 max
'''


if __name__ == '__main__':   
    file_info = file_info()
    process_file = process_file(file_info)
    translator = translator(process_file)
    make_DF = make_DF(process_file, translator)
    new_word_checker = new_word_checker(make_DF)
    tagger = tagger(new_word_checker)
    export(tagger)


#PLAYGROUND
'''# Imports translator package for translating through google translate
try:
    import translate
    print("translate loaded")
    from translate import Translator

except:
    try:
        import subprocess
        subprocess.call("pip install translator", shell=True)
        print("translator loaded")
        from translate import Translator
    except:
        print("Unable to install")
        exit()

#chunks list into 25 word segments, sends to google translate, pauses for 0.1 seconds, then sends the next chunk until all sent
results = []
chunksize = 1
for sourcechunk in range(0,len(source_text), chunksize):
    print("sending {} -> {}...".format(sourcechunk, sourcechunk + chunksize))
    results.extend([transresult for transresult in 
                    gs.translate(source_text[sourcechunk:sourcechunk + chunksize], 'en')])
    print("Recieved")
    time.sleep(0.5)


result = trans.translate([text for text in test])
for text in result:
    print(text)


final_text = {}
for index in range(len(source_text)):
    final_text.update({source_text[index]: result[index]})

#formatting example    update("native":orginal word, "english":translated word )
    print('{} -> {}'.format(source_text[index], result[index].text))
'''