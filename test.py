#%%
from platform import architecture
import pandas as pd
import numpy as np
import unidecode
import re
from difflib import get_close_matches 
from utils import SolveMotus

file = open("lexique.txt", "r", encoding='utf8')
words = [unidecode.unidecode(line.strip()) for line in file]
words8 = [word.lower() for word in words if len(word)==8]

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
premiers_mots = []

for letter in alphabet:
    first_word = [letter + "eaisnrto"]
    words_letter = [word for word in words8 if word[0] == letter]
    new_words = get_close_matches(first_word, words_letter, n=3, cutoff=0)
    premiers_mots.append(new_words)

print(premiers_mots)

['azulejos', 'byzantin', 'cypriote', 'dynastie', 'exutoire', 'fuyantes', 'gypseuse', 'hysterie', 'ivrognes', 'juvenile', 'kystique', 'lyonnais', 'mystifie',
'nympheas', 'oxygenes', 'pyromane', 'quotient', 'rythmera', 'systemes', 'tziganes', 'utopiste', 'vulvaire', 'wishbone', 'xiphoide', 'yearling', 'zestames']

























# words8 = [word for word in words8 if word[0]=="f"]
# print(words8[:10])


# word = "fearsnrto"
# print(get_close_matches(word, words8, n=1, cutoff=0.3))


# arch = "(?=^((?!r).)*$)(?=^((?!i).)*$)(?=^((?!n).)*$)"
# r = re.compile(arch)
# words8 = list(filter(r.match, words8))

# print("monergol" in words8)



# df = pd.read_csv('lexique.csv', on_bad_lines='skip', sep=';')



# df = df[['1_ortho']]
# df = df.loc[~(df['1_ortho'].str.contains(' ') | df['1_ortho'].str.contains('-'))]
# df.drop_duplicates(inplace=True)
# df.columns = ['words']
# df.head(10)

# df = df.to_numpy()
# np.savetxt("lexique.txt", df, fmt='%s')

#df.to_csv("lexique_clean.csv", sep=';', index=False)

# %%
