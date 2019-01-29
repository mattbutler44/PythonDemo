# Matt Butler
# Dec 13, 2018
# Imports, manipulates, and encrypts text from an outside source; manipulates book cover


import math
import random
import sys
import turtle
from cImage import *


class BookManip:

    # constructor
    def __init__(self):
        self.wordsWithX = 0
        self.wordsWithQ = 0
        self.rareDict = {'x': 0, 'q': 0}
        self.myWin = ImageWin("Book Cover", 600, 400)
        self.myWin.configure(background="navy")

    # input the text from a text file
    def inputBook(self):
        self.bookFile = open("Book.txt", "r")
        for aline in self.bookFile:
            self.words = aline.split()
        self.removeSymbols(self.words)
        self.bookFile.close()

    # remove symbols such as .,"': and so on
    def removeSymbols(self, wordList):
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        for i in range (len(wordList)): # iterate over each word in the list
            word = wordList[i].lower()  # set all words lowercase to compare to alphabet
            letters = list(word)        # convert words to char arrays
            for j in range (len(letters)):      # iterate over char arrays
                if letters[j] not in alphabet:  # if the char at index is not in alphabet
                    letters[j] = ""     # replace it with blank
            word = "".join(letters)     # join char array back into a full word
            wordList[i] = word          # replace the word list at index with newly formed word
        self.words = wordList

    # Counts X and Q, updates a dictionary to store those values
    # I picked two uncommon letters just to see how many there were
    def countXandQ(self, wordList):
        for i in range (len(wordList)):
            if "x" in wordList[i]:
                self.wordsWithX += 1
                self.rareDict.update(x=self.wordsWithX)
            elif "q" in wordList[i]:
                self.wordsWithQ += 1
                self.rareDict.update(q=self.wordsWithQ)
        print("Rare letters and their counts:\n", self.rareDict)

    # encrypt the text from the file we previously took in
    def encryptBook(self, wordList):
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        # start with an empty string
        self.encryptedText = ""
        # random amount of shift (a shift of 1 makes a ->b, b ->c, etc)
        shift = random.randint(1, 25)
        # for every word in the list made from our de-symboled text:
        for word in wordList:
            # for every character in the above word:
            for ch in word:
                # find the character in the word, get its position (index)
                origIndex = alphabet.find(ch)
                # implement the shift
                # if the shift doesn't go past z, shift as-is:
                if origIndex + shift < len(alphabet):
                    encryptedIndex = origIndex + shift
                # if the shift is past z, wrap around to the start of the alphabet:
                # (this is actually implemented as a "mirrored" shift to the left but the result is the same)
                else:
                    encryptedIndex = origIndex - (len(alphabet) - shift)
                self.encryptedText += alphabet[encryptedIndex]
        self.outputBook()

    # Make a new file with the encrypted version of the text we input earlier
    def outputBook(self):
        self.encryptedBook = open("encryptedBook.txt", "w")
        self.encryptedBook.write(self.encryptedText)
        self.encryptedBook.close()

    # display some information about your computer system
    # (this was a requirement for the project)
    def displaySysInfo(self):
        self.opsys = sys.platform
        print("\nYour operating system:\n",self.opsys)
        if "win32" in self.opsys:
            print("Your Windows version:")
            print(sys.getwindowsversion())
        else:
            print("\nYou aren't using windows")

    # displays the original book cover
    def displayCover(self, imageString):
        cover = FileImage(imageString)
        cover.draw(self.myWin)

    # makes an inverted pixel
    def negativePixel(self, oldPixel):
        newRed = 255 - oldPixel.getRed()
        newGreen = 255 - oldPixel.getGreen()
        newBlue = 255 - oldPixel.getBlue()
        self.newPixel = Pixel(newRed, newGreen, newBlue)
        return self.newPixel

    # uses inverted pixel method above to invert the book cover's colors
    def invertImage(self, imageString):
        oldImage = FileImage(imageString)

        width = oldImage.getWidth()
        height = oldImage.getHeight()
        self.invertedImage = EmptyImage(width, height)

        # traverse through each row of pixels
        for row in range(height):
            # traverse through each pixel in each row
            for col in range(width):
                # take the old pixel
                originalPixel = oldImage.getPixel(col, row)
                # invert the colors
                newPixel = self.negativePixel(originalPixel)
                # set the pixel to the inverted variant
                self.invertedImage.setPixel(col, row, newPixel)

        # draw the inverted image next to the original
        self.invertedImage.setPosition(width+20, 0)
        self.invertedImage.draw(self.myWin)
        self.myWin.exitOnClick()

    # A silly example of recursion
    # (the project required certain techniques, I admit this is kind of just thrown in)
    # An L-System version of recursion (setting the structure)
    def lSystem(self, axiom, rules, n):
        for i in range(n):
            newString = ""
            for ch in axiom:
                newString += rules.get(ch, ch)
            axiom = newString
        return axiom

    # defining what will go into the L-System above
    def printBookTitle(self, title, depth):
        axiom = title
        # "space" becomes ! and ! becomes " !"
        myRules = {" ": "!", "!": " !"}
        for i in range(depth):
            res = self.lSystem(axiom, myRules, i)
            print("%3d %s" % (len(res), res))
    


bm = BookManip()
# trying to call this in my test app caused
# an infinite recursion but it works just fine here. 
bm.printBookTitle("Amulet of Samarkand", 5)


