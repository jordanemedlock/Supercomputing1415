
# coding: utf-8

## Digital Aristotle

####### Modules

# In[48]:



# In[49]:

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

DEBUG = True
def debug(*s):
    global DEBUG
    if DEBUG:
        print s


# ###### Data Components

# In[50]:

class Serializable(object):
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
    #                 str  [Chapter] str         str
    def __init__(self,name,chapters,publish_date,isbn):
        self.name = name
        self.chapters = chapters
        self.publish_date = publish_date
        self.isbn = isbn

    @classmethod
    def fromJsonObj(cls,dictionary):
        return cls(dictionary['name'],[Chapter.fromJsonObj(obj) for obj in dictionary['chapters']],dictionary['publish_date'],dictionary['isbn'])

    def toJSONObj(self):
        return {'name' : self.name, 'chapters' : [obj.toJSONObj() for obj in self.chapters], 'publish_date': self.publish_date, 'isbn': self.isbn}
    
class Chapter(Serializable):
    #                 str  [Sub_Chapter] [Subject] 
    def __init__(self,name,subchapters,subjects,pages):
        self.name = name
        self.subchapters = subchapters
        self.subjects = subjects
        self.pages = set(pages)

    def toJSONObj(self):
        return {'name' : self.name, 'subchapters' : [x.toJSONObj() for x in self.subchapters], 'subjects': self.subjects, 'pages':list(self.pages)}
    
    
    
    @classmethod
    def fromJsonObj(cls,dictionary):
        return cls(dictionary['name'],[SubChapter.fromJsonObj(obj) for obj in dictionary['subchapters']],dictionary['subjects'],dictionary['pages'])

class SubChapter(Serializable):
    #                  str [Paragraph] [Subject]
    def __init__(self,name,text,subjects, pages):
        self.name = name
        self.text = text
        self.subjects = subjects
        self.pages = set(pages)

    @classmethod
    def fromJsonObj(cls,dictionary):
        return cls(dictionary['name'],
                   dictionary['text'],
                   dictionary['subjects'],
                   dictionary['pages'])

    def toJSONObj(self):
        return {'name' : self.name, 'text' : self.text, 'subjects': self.subjects, 'pages': list(self.pages)}
    
   
class Subject(object):
    def __init__(self,text):
        self.text = text

    @classmethod
    def fromJsonObj(cls,dictionary):
        return cls(dictionary['text'])


####### Data Creation

# In[51]:
def createNewMathOut():
    f = open("LinedMath.json")
    book = Book('A First Book in Algebra',[],"","")
    document = json.loads(f.read().encode('utf8'))
    chapter = None
    subchapter = None
    for (page_num, page) in enumerate(document):
        page_num += 1
        for line in page:
            if line[u'font'] == 5: # chapter
                chapter = Chapter(line[u'data'], [], [line[u'data']], [page_num])
                book.chapters.append(chapter)
                subchapter = None

            elif line[u'font'] == 3: # Subchapter
                subchapter = SubChapter(line[u'data'], '', [line[u'data']], [page_num])
                if chapter is None:
                    chapter = Chapter('No Name Chapter', [], [], [page_num])
                chapter.subchapters.append(subchapter)
                chapter.subjects.append(line[u'data'])
            
            elif subchapter is not None:
                subchapter.text += u'\n' + line[u'data']
                subchapter.pages.add(page_num)
                chapter.pages.add(page_num)
            
            else:
                subchapter = SubChapter("No Name", line[u'data'], [], [page_num])
                if chapter is None:
                    chapter = Chapter('No Name Chapter', [], [], [page_num])
                chapter.subchapters.append(subchapter)

    fout = open("newMathOut.json",'w')
    string = json.dumps(book.toJSONObj())
    fout.write(string)

def readBook():
    f = open('newMathOut.json')
    book = Book.fromJsonObj(json.loads(f.read()))
    return book
    for chapter in book.chapters:
        debug(type(chapter.subchapters))
####### Search Data (Functions)

# In[52]:

def levenshtein(source, target):
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


# In[53]:

def minimumChapter(xs):
    smallest = float("inf")
    smallestChapter = None
    for (value, chapter) in xs:
        if value < smallest:
            smallest = value
            smallestChapter = chapter
    return smallestChapter


# In[54]:

numberOfTimesRan = 0
filtered_words_global = []
def bestChapter(input_string, chapters):
    def countWordsInSubChapter(subchapter):
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
        index = levenshteinDistance(input_string, chapter.name)
        if type(chapter) is SubChapter:
            index += countWordsInSubChapter(chapter)
            debug('\t', chapter.name, index)
        elif type(chapter) is Chapter:
            accum = 0
            for subchapter in chapter.subchapters:
                accum += countWordsInSubChapter(subchapter)
            accum = accum/len(chapter.subchapters)
            index += accum
            debug(chapter.name, index)
            
        return (float(index), chapter)
    xs = map(chapterPlusIndex, chapters)
#     debug(map(lambda x: (x[0], x[1].name), xs))
    return minimumChapter(xs)


# In[55]:

def memoize(f):
    memory = dict()
    def memoizedFunction(x):
        if x in memory:
            return memory[x]
        else:
            memory[x] = f(x)
            return memory[x]
    return memoizedFunction


# In[56]:

def getChapter(input_string,book):
    return bestChapter(input_string, list(chain(*[c.subchapters for c in book.chapters])) + book.chapters)


# In[57]:

def levenshteinDistance(str1,str2):
    str1, str2 = unicode(str1), unicode(str2)
    return levenshtein(str1.lower().rstrip('.'),str2.lower().rstrip('.'))


# In[58]:

def isInt(string):
    string = [x for x in string if x in '0123456789']
    return len(string) > 0


####### Search Data

# In[59]:

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


# In[68]:
def search(input_string,book):
    filtered_words_global = []
    chapter = getChapter(input_string,book)
    debug("\n",chapter.name)
    debug("Page:",chapter.pages,"\n")
    return displayPages(chapter.pages)

# print  'Math6-%03d.png'%chapter.pages
def displayPages(pages):
    pages = sorted(list(pages))
    return [os.path.join('Math6-%03d.png'%(x)) for x in pages]

    
    
# display(Image(filename=os.path.join('Math6', 'Math6-%03d.png'%chapter.page)))
# display(Image(filename=os.path.join('Math6', 'Math6-%03d.png'%(chapter.page+1))))
# display(Image(filename=os.path.join('Math6', 'Math6-%03d.png'%(chapter.page+2))))


# In[ ]:
if __name__ == '__main__':
    createNewMathOut()
    book = readBook()
    search(u'substracting',book)