# Import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from difflib import get_close_matches 

import numpy as np 
import pandas as pd
import time
import re
import random


class SolveMotus():

    def __init__(self):
        """
        Initialization of the Solver :
            - create driver, start the game and scrap the first letter of the word
            - create letter lists 
        """
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')         
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


        self.driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        self.driver.get("https://motus.absolu-puzzle.com/index.php")
        self.driver.execute_script("document.body.style.zoom='zoom %'")
        self.path_letter = "/html/body/div[1]/div[1]/div[2]/div[1]/table/tbody/"
        self.first_letter = self.driver.find_element(By.XPATH, f'{self.path_letter}tr[1]/td[1]').text.lower()

        self.enter = self.driver.find_element(By.CLASS_NAME, 'form-control')   
        self.letters_out = []
        self.letters_misplaced = [] 
        self.well_placed = []

        time.sleep(0.5)
        #We have to accept cookies in order to play
        while True :
            try :
                cookies = self.driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[2]/div[2]/button[1]")
                cookies.click()
                break
            except :
                pass


    def send_first_word(self, words8):  
        """
        Function which sends a first word based on most used letter in French
        """
        best_first_word = ['azulejos', 'byzantin', 'cypriote', 'dynastie', 'exutoire', 'fuyantes', 'gypseuse', 'hysterie', 'ivrognes', 'juvenile', 'kystique', 'lyonnais', 'mystifie',
        'nympheas', 'oxygenes', 'pyromane', 'quotient', 'rythmera', 'systemes', 'tziganes', 'utopiste', 'vulvaire', 'wishbone', 'xiphoide', 'yearling', 'zestames']

        first_word = [word for word in best_first_word if word[0]==self.first_letter][0]

        new_words = get_close_matches(first_word, words8, n=5, cutoff=0)

        # for let in common_letter:
        #     if len(first_word) < 8 or self.first_letter!=let:
        #         first_word += let

        #print(f"Words selected for the first step are : {new_words}")

        self.send_word(new_words[0], )

        i=1
        while "n'est pas accepté comme un mot valide" in self.driver.page_source:
            self.send_word(new_words[i])
            i+=1


    def get_result_pred(self, it):
        """
        Function which scraps result of the try n° it and updates letter lists

        INPUT :
            - it : iteration rank (int)
        OUTPUT :
            - result : list of info concerning try it [[letter, color of the letter], ...]
        """

        self.well_placed = []
        self.letters_misplaced = []
        result = []
        path_letter = "/html/body/div[1]/div[1]/div[2]/div[1]/table/tbody/"

        for i in range(1,9):
            try :
                result.append(  [self.driver.find_element(By.XPATH, f'{path_letter}tr[{it}]/td[{i}]').text.lower(),
                                self.driver.find_element(By.XPATH, f'{path_letter}tr[{it}]/td[{i}]').get_attribute("bgcolor")] )
            except :
                print(f"An error occured due to {self.driver.find_element(By.XPATH, f'{path_letter}tr[{it}]/td[{i}]').text}")
                break    
            
            #If letter not in word, we append it to unwanted letters
            if result[i-1][1] == '#36c':
                self.letters_out.append(result[i-1][0])
                if result[i-1][0] in self.well_placed or result[i-1][0] in self.letters_misplaced :
                    self.letters_out.pop(self.letters_out.index((result[i-1][0])))

            #It it is misplaced, we update letters missplaced
            elif result[i-1][1] == '#f60':
                self.letters_misplaced.append(result[i-1][0])
                if result[i-1][0] in self.letters_out:
                    self.letters_out.pop(self.letters_out.index((result[i-1][0])))


            #If the letter is well-placed, we try to pop it out from missplaced
            elif result[i-1][1] == '#008a05':
                self.well_placed.append(result[i-1][0])
                if result[i-1][0] in self.letters_out:
                    self.letters_out.pop(self.letters_out.index((result[i-1][0])))

                # try :
                #     self.letters_misplaced.pop(self.letters_misplaced.index(result[i-1][0]))
                # except:
                #     pass
                
        self.letters_out = list(set(self.letters_out))
        print(self.letters_out, self.letters_misplaced, self.well_placed)
        return result


    def new_prediction(self, previous_result, words8):
        """
        Function which uses result of the try n° it-1 to update the list of possible words

        INPUT :
            - previous_result : list of info concerning try it-1 [[letter, color of the letter], ...]
            - words8 : list of available words to solve the Motus
        OUTPUT :
            - words8 updated
        """

        architecture = '(?='

        #Add first condition concerning letters well-placed
        for idx, info in enumerate(previous_result) :
            if info[1] == '#008a05':
                architecture += info[0]
            else:
                architecture += '.'
        architecture += ')'

        #Add second condition about missplaced letters
        for letter in self.letters_misplaced:
            architecture += f"(?=[a-zA-Z]*{letter}[a-zA-Z]*)"

        #Add third condition about eliminated letters
        for letter in self.letters_out:
            architecture += f'(?=^((?!{letter}).)*$)'

        #print(architecture)
        #Use RegEx condition 
        r = re.compile(architecture)
        words8 = list(filter(r.match, words8))
        return words8


    def send_word(self, word):
        """
        Function which sends a word in the online game
        INPUT :
            - word : string chosen to be sent
        """

        #To prevent selenium.common.exceptions.StaleElementReferenceException
        # It may happen because the element to which I have referred is removed from the DOM structure. [https://stackoverflow.com/a/18226139]
        try : 
            self.enter.click()
            self.enter.send_keys(word)
            self.enter.send_keys(Keys.RETURN)

        except :
            self.enter = self.driver.find_element(By.CLASS_NAME, 'form-control') 
            self.enter.click()
            self.enter.send_keys(word)
            self.enter.send_keys(Keys.RETURN)

        # try :
        #     self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/form/div/button').click()
        # except :
        #     self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/form/div/button').click()

            
