# MotusSolver
The goal of this program is to find the word as quickly as possible on [Motus](https://www.google.com "Jeu du Motus"), the French version of *Lingo*.

![alt text](https://static.blog4ever.com/2013/03/731698/artfichier_731698_8197737_201905062337791.png)


***


#**History**

This online game is inspired by the **TV game Motus**, itself inspired by *Lingo*, the American version created by *Ralph Andrews* and broadcast since September 28, 1987 in the USA and Canada.


***


#**Rules**

The game is based on **finding words with a fixed number of letters**, here 8. 
The player must propose a word within a maximum of eight seconds and must spell it out. The word must contain the correct number of letters and **be spelled correctly**, otherwise it is rejected. The word then appears on a grid: the letters present and well placed are **colored in red**, the letters present but badly placed are **circled in yellow**. For a letter, you can only have the number of occurrences of this letter in the word colored (either in yellow or in red if some are well placed).


***


#**How my algo works**

I use a txt file containing more than **40 000 French words** of *exactly 8 letters*, it contains nouns, adverbs but also the conjugations of verbs (*manger : mangeions, mangerez, mangeais, etc*). 

First, I get the first letter of the word to guess. Then, I create a "*word*" with this letter followed by the 7 most common letters of the French language, for example if it's **'f' + 'esartin' = 'fesartin'**, then I look for the closest word in my database. This will be the first word I try on **Motus**.

Then, I scrap the result with the color of each letter (red, green or grey), I update the information on my letters and I take a word at random among those respecting these conditions.
I iterate in this way until I find (or not) the **correct word**.



##Example


![Alt Text](https://github.com/luceien/MotusSolver/blob/main/motus_cropped_speed.gif)



