#Digital Aristotle

####### Modules Begin 

import json
from matplotlib.pylab import *
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import random
import time
from itertools import chain
import nltk
import os.path

####### Modules End

###### Data Components Begin

class Serializable(object):
    '''
    Creates a class that allow for the creation of a 
    JSON database while still being able to be used in Python
    '''
    @classmethod
    def fromJsonFile(cls,fname):
        f = open("Math6")
        document = json.loads(f.read().encode('utf8'))
        return cls.fromJsonObj(document)

    @classmethod
    def fromJsonObj(cls,obj):
        pass
    
    def toJSONObj(self):
        pass
    
    def __str__(self):
        return (json.dumps(self.toJSONObj(), indent=2))

class Book(Serializable):
    '''
    Creates a class that will contain major components 
    (book's name, chapters, isbn, and publish_date) of 
    the database based on the math book
    '''
    #                 str  [Chapter] str         str
    def __init__(self,name,chapters,publish_date,isbn):
        self.name = name
        self.chapters = chapters
        self.publish_date = publish_date
        self.isbn = isbn

    @classmethod
    def fromJsonObj(cls,dictionary):
        '''
        Creates a dictionalry with components of the book
        '''
        return cls(dictionary['name'],[Chapter.fromJsonObj(obj) for obj in dictionary['chapters']],dictionary['publish_date'],dictionary['isbn'])

    def toJSONObj(self):
        '''
        Adds information to dictionary based on dictionary 
        values created in the "fromJSONObj" function
        '''
        return {'name' : self.name, 'chapters' : [obj.toJSONObj() for obj in self.chapters], 'publish_date': self.publish_date, 'isbn': self.isbn}
    
class Chapter(Serializable):
    '''
    Makes a class which will contain the a chapter's name, 
    SubChapter object, and the number of pages in the entire chapter
    '''
    #                 str  [Sub_Chapter] 
    def __init__(self,name,subchapters,pages):
        self.name = name
        self.subchapters = subchapters
        self.pages = set(pages)
    
    '''
    Next two functions do the same JSON creation as in the "Book"
    class, except it uses dictionary values for the chapter's name.
    subchter, and pages
    '''
    def toJSONObj(self):
        return {'name' : self.name, 'subchapters' : [x.toJSONObj() for x in self.subchapters], 'pages':list(self.pages)}
    
    @classmethod
    def fromJsonObj(cls,dictionary):
        return cls(dictionary['name'],[SubChapter.fromJsonObj(obj) for obj in dictionary['subchapters']],dictionary['pages'])

class SubChapter(Serializable):
    '''
    Makes a class which will contain a subchapter's name, the 
    text in the subchapter, and the amount of pages in the SubChapter
    '''
    #                  str [Paragraph] 
    def __init__(self,name,text,pages):
        self.name = name
        self.text = text
        self.pages = set(pages)

    '''
    The next two fucntions do the same JSON database creation as in the 
    "Book" class, except it uses dictionary values  for the SubChapter's 
    name, text in the SubChapter, and the number of pages in the subchpter
    '''
    @classmethod
    def fromJsonObj(cls,dictionary):
        return cls(dictionary['name'],
                   dictionary['text'],
                   dictionary['pages'])

    def toJSONObj(self):
        return {'name' : self.name, 'text' : self.text, 'pages': list(self.pages)}

###### Data Components End

####### Data Creation Begin 

def createNewMathOut():
    '''
    Function to use classes in "Data components" to create the JSON database
    by searching through each page of the book, and using the font to determine
    where the type of object, chapter, subchapters, or text, the information belongs 
    '''
    f = open("LinedMath.json")
    book = Book('A First Book in Algebra',[],"","")
    document = json.loads(f.read().encode('utf8'))
    chapter = None
    subchapter = None
    for (page_num, page) in enumerate(document):
        page_num += 1
        for line in page: # Searches by each line of text on a single page
            if line[u'font'] == 5: # chapter
                chapter = Chapter(line[u'data'], [], [page_num])
                book.chapters.append(chapter)
                subchapter = None

            elif line[u'font'] == 3: # Subchapter
                subchapter = SubChapter(line[u'data'], '', [page_num])
                if chapter is None:
                    chapter = Chapter('No Name Chapter', [], [page_num])
                chapter.subchapters.append(subchapter)
            
            elif subchapter is not None:
                subchapter.text += u'\n' + line[u'data']
                subchapter.pages.add(page_num)
                chapter.pages.add(page_num)
            
            else:
                subchapter = SubChapter("No Name", line[u'data'], [page_num])
                if chapter is None:
                    chapter = Chapter('No Name Chapter', [], [page_num])
                chapter.subchapters.append(subchapter)

    fout = open("newMathOut.json",'w')  
    string = json.dumps(book.toJSONObj())
    fout.write(string) # Creates the database as a text file

def readBook():
    '''
    Function used to search through the JSON in python
    database created in the fucntions
    '''
    f = open('newMathOut.json')
    book = Book.fromJsonObj(json.loads(f.read()))
    return book

####### Data Creation End  

####### Search Data Begin (Functions)

def levenshtein(source, target):
    '''
    Function used to compare two strings for their similarity by comparing
    the individual characters in the strings, and finding what is needed to 
    make them the same (i.e. insertion, substitution, or deletion). Returns 
    a number based on the changes required; the smaller the number, the closer 
    the two strings are to eachother. 
    '''
    if len(source) < len(target):
        return levenshtein(target, source)
 
    if len(target) == 0:
        return len(source)
    source = np.array(tuple(source))
    target = np.array(tuple(target))
 
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion 
        current_row = previous_row + (0.1)
 
        # Substitution or matching:
        current_row[1:] = np.minimum(current_row[1:],np.add(previous_row[:-1], (target != s) * (3)))
 
        # Deletion 
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + (1))
        previous_row = current_row
 
    return previous_row[-1]
levenshtein = np.vectorize(levenshtein)

def minimumChapter(xs):
    '''
    Function used to find the chapter with the least amount of difference
    between the input and a (sub)chpter's text and name given an index where
    the smallest index is the (sub)chapter with the least difference
    '''
    smallest = float("inf")
    smallestChapter = None
    for (value, chapter) in xs:
        if value < smallest:
            smallest = value
            smallestChapter = chapter
    return smallestChapter

numberOfTimesRan = 0
filtered_words_global = []
def bestChapter(input_string, chapters):
    '''
    Function used to return the chapter or subchapter withe the smallest 
    difference between the input. It compares all of the chapters and
    subchapters to the input
    '''
    def countWordsInSubChapter(subchapter):
        '''
        Function that changes a subchapters text into a lost of individual
        words, and then removest irrelevant words, stop words, from this list.
        It then creates a negative accumulator where one is subtracted from it 
        if the word matches the input. The sum of levenshtein distance of a word 
        divided by every word is then added to this accumulator. 
        '''
        global numberOfTimesRan, filtered_words_global
        numberOfTimesRan += 1
        accum = 0
        text = subchapter.text
        words = text.split()
        filtered_words = [w.lower() for w in words if not w.lower() in stopWords and not isInt(w) and w.isalpha() and len(w) > 2]
        accum -= len([w for w in filtered_words if w == input_string])
        filtered_words_global += filtered_words
        for word in filtered_words:
            comp = levenshteinDistance(input_string,word)
            accum += float(comp) / len(words)
        return accum
    
    countWordsInSubChapter = memoize(countWordsInSubChapter)
    
    def chapterPlusIndex(chapter):
        '''
        Function used to return the (sub)chapter with the name and text closest to the 
        input by comparing their levenshtein distances with a created index which is more
        accurate than the other chapters or SubChapters
        '''
        index = levenshteinDistance(input_string, chapter.name)
        if type(chapter) is SubChapter:
            index += countWordsInSubChapter(chapter)
        elif type(chapter) is Chapter:
            accum = 0
            for subchapter in chapter.subchapters:
                accum += countWordsInSubChapter(subchapter)
            accum = accum/len(chapter.subchapters)
            index += accum
            
        return (float(index), chapter)
    xs = map(chapterPlusIndex, chapters)
    return minimumChapter(xs)

def memoize(f):
    '''
    Function used to make searching the database quicker in the "bestChapter" function by repeating
    a code that has been ran before in the same way so it takes less time to run it again for another
    chapter
    '''
    memory = dict()
    def memoizedFunction(x):
        if x in memory:
            return memory[x]
        else:
            memory[x] = f(x)
            return memory[x]
    return memoizedFunction

def getChapter(input_string,book):
    '''
    Function used to find the chapter or subchapter that is closet to the input by comparing the input 
    to every chapter and SubChapter with the "bestChapter" function
    '''
    return bestChapter(input_string, list(chain(*[c.subchapters for c in book.chapters])) + book.chapters)

def levenshteinDistance(str1,str2):
    '''
    A function which takes two string and converts them into unicode, and then compares them with the "levenshtein"
    function after making them lowercase and removing periods from the strings
    '''
    str1, str2 = unicode(str1), unicode(str2)
    return levenshtein(str1.lower().rstrip('.'),str2.lower().rstrip('.'))

def isInt(string):
    '''
    A function used to test if a string contains numbers and returns a list of those strings.
    This is used to remove numbers from the comparison of the input to the text in SubChapters 
    '''
    string = [x for x in string if x in '0123456789']
    return len(string) > 0

####### Search Data End (Functions)

####### Search Data Begin

# These stop words are words that are not related to data seach, but used in spoken and written English
stopwords = """ 
a about above after again agains all am an and any are aren't as at be because been before being below between both but by can't cannot 
could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he 
he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me
more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll 
she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're
they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where 
where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves first
second twice third fourth - + one two three four five six seven eight nine ten john many times much will can miles years cent men hours 
exercise man must 
"""
stopWords = stopwords.split()

def search(input_string,book):
    '''
    Main function which uses the functions above to compare an input to the 
    book's chapters and subchapter, and returns the chapter with the closest 
    related information
    '''
    filtered_words_global = []
    chapter = getChapter(input_string,book)
    return displayPages(chapter.pages)

def displayPages(pages):
    '''
    Function used to return the chapter's pages file names which are
    used to find the file locations of the book's pictures
    '''
    pages = sorted(list(pages))
    return [os.path.join('Math6-%03d.png'%(x)) for x in pages]

####### Search Data End
'''
Statement used by server to run the search using an input sent 
from the webpage
'''
if __name__ == '__main__':
    createNewMathOut()
    book = readBook()
    search(u'',book)