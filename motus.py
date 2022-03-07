#%%
# Import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options

import argparse
import unidecode
import numpy as np 
import pandas as pd
import time
import re
import random

from utils import SolveMotus



def main():


    #Open file with the list of words
    file = open("lexique.txt", "r", encoding='utf8')
    #Delete all accents and special characters (é, è, ê, ç, à, â, etc.)
    words = [unidecode.unidecode(line.strip()) for line in file]
    #Lowercase every word
    words8 = [word.lower() for word in words if len(word)==8]

    solver = SolveMotus()
    it = 1

    #We keep only the words of length 8 and send our first word
    words8 = [word for word in words8 if word[0] == solver.first_letter]
    solver.send_first_word(words8)        
    

    #Now we can iterate until we find (or not) the solution
    result = ''
    while  result != "" or it < 9:

        output = solver.get_result_pred(it)
        print(output)
        words8 = solver.new_prediction(output, words8)

        #print(words8)

        if len(words8) == 0:
            print('The word is not in the database, please try again.')
            #solver.driver.close()
            break
        
        #Select a new word in the remaining possibilities
        word =  words8[random.randint(0, len(words8)-1)]
        print(f"{len(words8)} words remaining !")
        print(f'Word selected is : "{word.upper()}"')

        #Try it
        solver.send_word(word)
        start = time.time()
        while "n'est pas accepté comme un mot valide" in solver.driver.page_source and time.time()-start<5:
            words8.pop(words8.index(word))
            word =  words8[random.randint(0, len(words8)-1)]
            print(f'Previous word is not valid, new word selected is : "{word.upper()}"')
            solver.send_word(word)

        it+=1
        time.sleep(0.2)

        if "Bravo" in solver.driver.page_source:
            result = "win"
            print(f"\nWell done, you won in {it} tries ! (solution : {word.upper()})\n")
            #solver.driver.close()
            break

        else:
            words8.pop(words8.index(word))
        


if __name__ == "__main__":
    question = input("Do you want to play Motus ? (y/n) : ")

    while question == 'y':
        main()
        question = input("Do you want to play again ? (y/n) : ")



