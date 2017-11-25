#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 01:08:51 2017

@author: chenhaoyu
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Created on Thu Nov  9 11:17:48 2017

@author: chenhaoyu
"""

# sumy summary library
from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

#UI library
import Tkinter as tk
from tkFileDialog import askopenfilename
from PIL import ImageTk, Image, ImageFile
from resizeimage import resizeimage
ImageFile.LOAD_TRUNCATED_IMAGES = True
import tkFont as tkfont  # python 2

#nltk library
from nltk import ngrams
from nltk import word_tokenize,pos_tag,FreqDist

#chinese keywords
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

#import numpy
###############

#import rake
import sys
sys.path.append('./related/')
from rake import load_stop_words, build_stop_word_regex, generate_candidate_keywords, split_sentences, calculate_word_scores, generate_candidate_keyword_scores

#other import
from pytldr.summarize.relevance import RelevanceSummarizer
import six
import operator
import io
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.summarization import summarize

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=30, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        startframe = tk.Frame(self)
        startframe.configure(background='white')
        startframe.grid(row=8, column=1)
        
        label = tk.Label(startframe, text="Welcome to use our Small Summerizer", font=controller.title_font)
        label.grid(row=0, column=0)
        
        self.path ='./image/1.png'
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.superimg = tk.Label(startframe, image = self.img)
        self.superimg.grid(row=1, column=0)
        
        #some  declarations
        self.filelabel = tk.Label(startframe, text="I've tried my best to be pretty!!", font=("Helvetica", 20))
        self.filelabel.grid(row=2, column=0)
        
        #select methods
        button1 = tk.Button(startframe, text="Go to Method 1", height = 2, width = 20 ,command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=3, column=0)
        self.label1 = tk.Label(startframe, text="LSA and PR", font=("Helvetica", 16))     
        self.label1.grid(row=4, column=0)
        button2 = tk.Button(startframe, text="Go to Method 2",  height = 2, width = 20 ,command=lambda: controller.show_frame("PageTwo"))
        button2.grid(row=5, column=0)
        self.label1 = tk.Label(startframe, text="Named Entity Recognition", font=("Helvetica", 16))     
        self.label1.grid(row=6, column=0)
        button3 = tk.Button(startframe, text="Go to Method 3",  height = 2, width = 20 ,command=lambda: controller.show_frame("PageThree"))
        button3.grid(row=7, column=0)  
        self.label1 = tk.Label(startframe, text="RAKE keywords", font=("Helvetica", 16))     
        self.label1.grid(row=8, column=0)
        
        self.filelabel = tk.Label(startframe, text="Design © Copyright 2017 by Wen yang and Haoyu Chen for NLP", font=("Helvetica", 13))
        self.filelabel.grid(row=9, column=0)
        
        
'''''''''''''''''''''''''''
  First sumarizer
  LSA and RP      
        
'''''''''''''''''''''''''''

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
#initialize frame and locate it
        self.controller = controller
        frame = tk.Frame(self)
        frame.configure(background='lightcyan')
        frame.grid(row=11, column=1)

#...........first column .......#
#entry link text headline
        #label of title1
        self.Label = tk.Label(frame, text="LSA/RP based text summerizer", font=("Helvetica", 30))
        self.Label.configure(background='lightcyan') 
        self.Label.grid(row=0, column=0)

#show a image 
        ##search and show the image
        ###
        self.path ='./image/2.jpg'
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.panel = tk.Label(frame, image = self.img)
        self.panel.configure(background='lightcyan')
        self.panel.grid(row=1, column=0)

#chose language
        #label
        self.languagelabel = tk.Label(frame, text="Select the text language", font=("Helvetica", 16))
        self.languagelabel.configure(background='lightcyan')       
        self.languagelabel.grid(row=2, column=0)

        #inite
        self.OPTIONS1 = ["english","chinese"] #etc
        self.language = tk.StringVar()
        self.language.set(self.OPTIONS1[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS1, key=len))
        #chose
        self.Language = tk.OptionMenu(frame, self.language, *self.OPTIONS1)
        self.Language.config(width=self.oMenuWidth)
        self.Language.configure(background='lightcyan')
        self.Language.grid(row=3, column=0)
        
#chose sentence number

        #label
        self.sentencelabel = tk.Label(frame, text="Select summary sentence number", font=("Helvetica", 16))
        self.sentencelabel.configure(background='lightcyan')
        self.sentencelabel.grid(row=4, column=0)
        
        #inite
        self.OPTIONS2 = ["30","150","230","300","400"] #etc
        self.sentencenum = tk.StringVar()
        self.sentencenum.set(self.OPTIONS2[3]) # default value
        self.oMenuWidth = len(max(self.OPTIONS2, key=len))
        #option
        self.SentenceNum = tk.OptionMenu(frame, self.sentencenum, *self.OPTIONS2)
        self.SentenceNum.configure(background='lightcyan')
        self.SentenceNum.grid(row=5, column=0)
        
#input file or link 
        #label of file
        self.filelabel = tk.Label(frame, text="You can select a local file or input web link:", font=("Helvetica", 16))
        self.filelabel.configure(background='lightcyan')
        self.filelabel.grid(row=6, column=0)

        #confirm button       
        self.filebutton = tk.Button(frame, text="Choose a file and summarize", width=20, command=self.callbackFile)
        self.filebutton.configure(background='lightcyan')
        self.filebutton.grid(row=8, column=0)

        #entry of link
        self.linkentry = tk.Entry(frame, width=50)
        url = "http://www.jingshu.org/jingangjing/23231.html"#chinese text        
        self.linkentry.insert(tk.END, url)
        self.linkentry.configure(background='lightcyan')
        self.linkentry.grid(row=9, column=0)
        
        #confirm button
        self.linkbutton = tk.Button(frame, text="Input a link and summarize(check the language)", width=40, command=self.callbackLink)
        self.linkbutton.configure(background='lightcyan')
        self.linkbutton.grid(row=10, column=0)
        
   
#...........second columns .......#
        
#label of title2
        self.Label = tk.Label(frame, text="The summaried story", font=("Helvetica", 20))
        self.Label.configure(background='lightcyan')
        self.Label.grid(row=0, column=1)
        
#print the summary text
        #welcome text
        #display the summary
        self.summarytext = tk.Text(frame, height=20, width=50)
        self.scroll = tk.Scrollbar(frame, command=self.summarytext.yview)
        self.summarytext.configure(yscrollcommand=self.scroll.set)
        self.quote = "Welcome to use our text summarizer!"
        self.summarytext.insert(tk.END, self.quote)
        self.summarytext.grid(row=1, column=1)
        self.scroll.grid(row=1, column=2)
        
#evaluation method
        #label of file
        self.evafilelabel = tk.Label(frame, text="You can select reference text to evaluate:", font=("Helvetica", 16))
        self.evafilelabel.configure(background='lightcyan')
        self.evafilelabel.grid(row=2, column=1)

        #confirm button       
        self.evafilebutton = tk.Button(frame, text="Choose a file and evaluate", width=20, command=self.checkResult)
        self.evafilebutton.configure(background='lightcyan')
        self.evafilebutton.grid(row=3, column=1)
        
#chose rouge n number

        #label
        self.Nlabel = tk.Label(frame, text="Select the N-gram number", font=("Helvetica", 16))
        self.Nlabel.configure(background='lightcyan')       
        self.Nlabel.grid(row=5, column=1)

        #inite
        self.OPTIONS3 = ["1","2","3","4","5"] #etc
        self.rougenum = tk.StringVar()
        self.rougenum.set(self.OPTIONS3[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS3, key=len))
        #chose
        self.Nnum = tk.OptionMenu(frame, self.rougenum, *self.OPTIONS3)
        self.Nnum.config(width=self.oMenuWidth)
        self.Nnum.configure(background='lightcyan')
        self.Nnum.grid(row=6, column=1)
        
#print the evaluation score 
        self.evascore = tk.StringVar()
        self.evascore.set("The current evaluation score is: 0")
        self.evascorelabel = tk.Label(frame, textvariable=self.evascore, font=("Helvetica", 16))
        self.evascorelabel.configure(background='lightcyan')
        self.evascorelabel.grid(row=7, column=1)
    
#the process statement
        #some copyright declarations
        self.processm = tk.StringVar()
        self.processm.set("Ready to process!")
        self.processM = tk.Label(frame, textvariable=self.processm, width=40, font=("Helvetica", 20))
        self.processM.configure(background='lightcyan')
        self.processM.grid(row=8, column=1)
        
        # button to go back
        button = tk.Button(frame, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=9, column=1)

#quit button
        self.quitbutton = tk.Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.quitbutton.configure(background='lightcyan')
        self.quitbutton.grid(row=10, column=1)
        
#some copyright declarations
        self.filelabel = tk.Label(frame, text="Design © Copyright 2017 by Wen yang and Haoyu Chen for NLP", font=("Helvetica", 13))
        self.filelabel.configure(background='lightcyan')
        self.filelabel.grid(row=11, column=1)

## do the summerizer
#analysis from website
    def callbackLink(self):

        url = self.linkentry.get()            
        LANGUAGE = self.language.get()
        SENTENCES_COUNT = int(self.sentencenum.get())
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        if parser:
            self.processm.set("Successfully connected!")
        else:
            self.processm.set("Can't open the website!")
        stemmer = Stemmer(LANGUAGE)
        
        ### offer different summerizer
#        from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer

        from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        # organize the sentences into summary
        self.sentences = ''
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            f = str(sentence).strip()
            self.sentences = self.sentences + '\n' + f
        
        self.processm.set("Summary is done!")
        self.starter = 'We summerized the most important '+ str(SENTENCES_COUNT) + ' sentences of the text: \n'
        
        #1.3 get the summarization, if needed, print it
        self.summarytext.delete("1.0", tk.END)
        self.summarytext.insert(tk.END, self.starter)
        self.summarytext.insert(tk.END, self.sentences)
        
#analysis from local file
    def callbackFile(self):
        self.filename = askopenfilename()
        localfile = self.filename
        print localfile
        
        LANGUAGE = self.language.get()
        parser = PlaintextParser.from_file(localfile, Tokenizer(LANGUAGE))
        if parser:
            self.processm.set("Successfully opened!")
        else:
            self.processm.set("File can't be analyzed!")
        stemmer = Stemmer(LANGUAGE)
        SENTENCES_COUNT = int(self.sentencenum.get())
        
        ### offer different summerizer
        
#        from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        self.sentences = ''
        # organize the sentences into an initial summarization using LSA
        for sentence in summarizer(parser.document, SENTENCES_COUNT):

            f = str(sentence).strip()
            self.sentences = self.sentences + '\n' + f
        
        self.processm.set("Summary is done!")
        self.starter = 'We summerized the most important '+ str(SENTENCES_COUNT) + ' sentences of the text: \n'
        
        #1.3 get the summarization, if needed, print it
        self.summarytext.delete("1.0", tk.END)
        self.summarytext.insert(tk.END, self.starter)
        self.summarytext.insert(tk.END, self.sentences)

    def checkResult(self):
        self.filename = askopenfilename()
        localfile = self.filename
        print localfile
        
        N_gram = self.rougenum.get()

        self.evaluates = ''
        with open(localfile, 'r') as myfile:
            reference=myfile.read().replace('\n', '')
            reference = reference.lower()
        
        summary = self.sentences
        
        processedsum = summary.split()
        processedref = reference.split()
        
        samplesRef = []
        samplesSum = []
        countsum = 0.0
        
        #get n grams of the text
        for ngram in ngrams(processedsum, int(N_gram)):
            samplesRef.append(' '.join(str(i) for i in ngram))
            countsum = countsum + 1
            
        for ngram in ngrams(processedref, int(N_gram)):
            samplesSum.append(' '.join(str(i) for i in ngram))
            
        count = 0.0
        countref = 0.0
        
        for gram in samplesRef:
            countsum = countsum + 1
        
        for gram in samplesRef:
            countref = countref + 1
            if gram in samplesSum:
                count =count + 1
                
        recall = count/countref
        precision= count/countsum
#        print countref
#        print countsum
        evaresult ='The N Rouge result is:'+ str(recall)+ '(recall)'+ str(precision)+ '(precision)'
        self.evascore.set(evaresult)

'''
  Second sumarizer
  NER    
        
'''
  
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
#initialize frame and locate it
        self.controller = controller
        self.frame2 = tk.Frame(self)
        self.frame2.configure(background='lightcyan')
        self.frame2.grid(row=11, column=1)

#...........first column .......#
#entry link text headline
        #label of title1
        self.Label = tk.Label(self.frame2, text="NER based text summerizer", font=("Helvetica", 30))
        self.Label.configure(background='lightcyan') 
        self.Label.grid(row=0, column=0)

#show a image 
        ##search and show the image
        ###
        self.path ='./image/3.png'
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.panel = tk.Label(self.frame2, image = self.img)
        self.panel.configure(background='lightcyan')
        self.panel.grid(row=1, column=0)

#chose topics
#        #label
#        self.languagelabel = tk.Label(self.frame2, text="Select the text language", font=("Helvetica", 16))
#        self.languagelabel.configure(background='lightcyan')       
#        self.languagelabel.grid(row=2, column=0)
#
#        #inite
#        self.OPTIONS1 = ["english","chinese"] #etc
#        self.language = tk.StringVar()
#        self.language.set(self.OPTIONS1[0]) # default value
#        self.oMenuWidth = len(max(self.OPTIONS1, key=len))
#        #chose
#        self.Language = tk.OptionMenu(self.frame2, self.language, *self.OPTIONS1)
#        self.Language.config(width=self.oMenuWidth)
#        self.Language.configure(background='lightcyan')
#        self.Language.grid(row=3, column=0)
        
                #label
        self.topiclabel = tk.Label(self.frame2, text="Select topic number", font=("Helvetica", 16))
        self.topiclabel.configure(background='lightcyan')
        self.topiclabel.grid(row=2, column=0)
        
        #inite
        self.OPTIONS1 = ["1","3","50","70","100","150"] #etc
        self.topicnum = tk.StringVar()
        self.topicnum.set(self.OPTIONS1[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS1, key=len))
        #option
        self.TopicNum = tk.OptionMenu(self.frame2, self.topicnum, *self.OPTIONS1)
        self.TopicNum.configure(background='lightcyan')
        self.TopicNum.grid(row=3, column=0)
#        
#chose sentence number

        #label
        self.sentencelabel = tk.Label(self.frame2, text="Select summary sentence number", font=("Helvetica", 16))
        self.sentencelabel.configure(background='lightcyan')
        self.sentencelabel.grid(row=4, column=0)
        
        #inite
        self.OPTIONS2 = ["30","150","230","300","400"] #etc
        self.sentencenum = tk.StringVar()
        self.sentencenum.set(self.OPTIONS2[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS2, key=len))
        #option
        self.SentenceNum = tk.OptionMenu(self.frame2, self.sentencenum, *self.OPTIONS2)
        self.SentenceNum.configure(background='lightcyan')
        self.SentenceNum.grid(row=5, column=0)
        
#input file or link 
        #label of file
        self.filelabel = tk.Label(self.frame2, text="You can select a local file or input web link:", font=("Helvetica", 16))
        self.filelabel.configure(background='lightcyan')
        self.filelabel.grid(row=6, column=0)

        #confirm button       
        self.filebutton = tk.Button(self.frame2, text="Choose a file and summarize", width=20, command=self.callbackFile)
        self.filebutton.configure(background='lightcyan')
        self.filebutton.grid(row=8, column=0)

        #entry of link
        self.linkentry = tk.Entry(self.frame2, width=50)
        url = "http://www.jingshu.org/jingangjing/23231.html"#chinese text        
        self.linkentry.insert(tk.END, url)
        self.linkentry.configure(background='lightcyan')
        self.linkentry.grid(row=9, column=0)
        
        #confirm button
        self.linkbutton = tk.Button(self.frame2, text="Input a link and summarize(check the language)", width=40, command=self.callbackLink)
        self.linkbutton.configure(background='lightcyan')
        self.linkbutton.grid(row=10, column=0)
        
   
#...........second columns .......#
        
#label of title2
        self.Label = tk.Label(self.frame2, text="The summaried story", font=("Helvetica", 20))
        self.Label.configure(background='lightcyan')
        self.Label.grid(row=0, column=1)
        
#print the summary text
        #welcome text
        #display the summary
        self.summarytext = tk.Text(self.frame2, height=20, width=50)
        self.scroll = tk.Scrollbar(self.frame2, command=self.summarytext.yview)
        self.summarytext.configure(yscrollcommand=self.scroll.set)
        self.quote = "Welcome to use our text summarizer!"
        self.summarytext.insert(tk.END, self.quote)
        self.summarytext.grid(row=1, column=1)
        self.scroll.grid(row=1, column=2)
        
#evaluation method
        #label of file
        self.evafilelabel = tk.Label(self.frame2, text="You can select reference text to evaluate:", font=("Helvetica", 16))
        self.evafilelabel.configure(background='lightcyan')
        self.evafilelabel.grid(row=2, column=1)

        #confirm button       
        self.evafilebutton = tk.Button(self.frame2, text="Choose a file and evaluate", width=20, command=self.checkResult)
        self.evafilebutton.configure(background='lightcyan')
        self.evafilebutton.grid(row=3, column=1)
        
#chose rouge n number

        #label
        self.Nlabel = tk.Label(self.frame2, text="Select the N-gram number", font=("Helvetica", 16))
        self.Nlabel.configure(background='lightcyan')       
        self.Nlabel.grid(row=5, column=1)

        #inite
        self.OPTIONS3 = ["1","2","3","4","5"] #etc
        self.rougenum = tk.StringVar()
        self.rougenum.set(self.OPTIONS3[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS3, key=len))
        #chose
        self.Nnum = tk.OptionMenu(self.frame2, self.rougenum, *self.OPTIONS3)
        self.Nnum.config(width=self.oMenuWidth)
        self.Nnum.configure(background='lightcyan')
        self.Nnum.grid(row=6, column=1)
        
#print the evaluation score 
        self.evascore = tk.StringVar()
        self.evascore.set("The current evaluation score is: 0")
        self.evascorelabel = tk.Label(self.frame2, textvariable=self.evascore, font=("Helvetica", 16))
        self.evascorelabel.configure(background='lightcyan')
        self.evascorelabel.grid(row=7, column=1)
    
#the process statement
        #some copyright declarations
        self.processm = tk.StringVar()
        self.processm.set("Ready to process!")
        self.processM = tk.Label(self.frame2, textvariable=self.processm, width=40, font=("Helvetica", 20))
        self.processM.configure(background='lightcyan')
        self.processM.grid(row=8, column=1)
        
        # button to go back
        button = tk.Button(self.frame2, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=9, column=1)

#quit button
        self.quitbutton = tk.Button(self.frame2, text="QUIT", fg="red", command=self.frame2.quit)
        self.quitbutton.configure(background='lightcyan')
        self.quitbutton.grid(row=10, column=1)
        
#some copyright declarations
        self.filelabel = tk.Label(self.frame2, text="Design © Copyright 2017 by Wen yang and Haoyu Chen for NLP", font=("Helvetica", 13))
        self.filelabel.configure(background='lightcyan')
        self.filelabel.grid(row=11, column=1)

## do the summerizer
#analysis from website
    def callbackLink(self):
        url = self.linkentry.get()            
        LANGUAGE = 'english'
        SENTENCES_COUNT = int(self.sentencenum.get())
        TOPICS_COUNT = int(self.topicnum.get())
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        if parser:
            self.processm.set("Successfully connected!")
        else:
            self.processm.set("Can't open the website!")
        stemmer = Stemmer(LANGUAGE)
        
        ### offer different summerizer
#        from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        self.pieces = ''
        # organize the sentences into an initial summarization using LSA
        for sentence in summarizer(parser.document, 100):

            f = str(sentence).strip()
            self.pieces = self.pieces + '\n' + f
            
        
            
        # process the summarization above
        segment = word_tokenize(self.pieces)
        names = ''
        
        #do a NER, Named Entity Rocgnition to the summarization
        for word,pos in pos_tag(segment):
            if pos == 'NNP' or 'NNS':
                names = names + ' '+ word
                #print word

        # process to the name list
        potnamelist = word_tokenize(names)
        namelist = [wrd for wrd in potnamelist if (len(wrd) >= 5)]
        
        # according to the name list, find the most common one
        fdist1 = FreqDist(namelist) 
        Mostname = fdist1.most_common(TOPICS_COUNT)#[('John', 17)]
        Heroinfo = Mostname[0]#('John', 17)
        Heroname = Heroinfo[0]
        
        Topics = []
        for Tname in Mostname:
            Topicname = Tname[0]#('John', 17)
            Topics.append(Topicname)
        
        self.oridocuments = ''
        for sentence in parser.document.sentences:
            #count = count + 1
            #sentences.append(f.encode('unicode_escape'))
            #print(sentence)
            f = str(sentence).strip()
            self.oridocuments = self.oridocuments + '\n' + f
        
        self.finalsum =''
        for doc in self.oridocuments.split('.'):
            for top in Topics:
                if top in doc:
                    f = doc+ '.'
                    self.finalsum =self.finalsum  + '\n' + f.lower()
                
        #self.results = summarize(self.finalsum,word_count=100)
#        orisize = 0.0
#        newsize=0.0
#        newsize = 50.0 *SENTENCES_COUNT
#        orisize = len(oridocuments)
#        comratio = newsize/orisize
        
        #self.results = summarize(self.finalsum,ratio= comratio)
        
        self.results = summarize(self.finalsum,word_count=50*SENTENCES_COUNT)
        
        self.processm.set("Summary is done!")
        self.starter = 'We summerized the most important '+ str(SENTENCES_COUNT) + ' sentences of the text: \n'
        self.Heroindex = 'We find the hero/topic of the story is '+ Heroname + '\n'
        
        #1.3 get the summarization, if needed, print it
        self.summarytext.delete("1.0", tk.END)
        self.summarytext.insert(tk.END, self.starter)
        self.summarytext.insert(tk.END, self.Heroindex)
        self.summarytext.insert(tk.END, self.results)

#analysis from local file
    def callbackFile(self):
        self.filename = askopenfilename()
        localfile = self.filename
        print localfile
        
        LANGUAGE = 'english'
        TOPICS_COUNT = int(self.topicnum.get())
        SENTENCES_COUNT = int(self.sentencenum.get())
        

#        from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
        parser = PlaintextParser.from_file(localfile, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        self.pieces = ''
        # organize the sentences into an initial summarization using LSA
        for sentence in summarizer(parser.document, 100):

            f = str(sentence).strip()
            self.pieces = self.pieces + ' ' + f
        self.clean_pieces = ''.join([c for c in self.pieces if ord(c) < 128])

        # process the summarization above
        segment = word_tokenize(self.clean_pieces)
        names = ''
        
        #do a NER, Named Entity Rocgnition to the summarization
        for word,pos in pos_tag(segment):
            if pos == 'NNP' or 'NNS':
                names = names + ' '+ word
                #print word

        # process to the name list
        potnamelist = word_tokenize(names)
        namelist = [wrd for wrd in potnamelist if (len(wrd) >= 5)]
        
        # according to the name list, find the most common one
        fdist1 = FreqDist(namelist) 
        Mostname = fdist1.most_common(TOPICS_COUNT)#[('John', 17)]
        Heroinfo = Mostname[0]#('John', 17)
        Heroname = Heroinfo[0]
        
        # search the heroname
        items = []
        search = Heroname
        pure_keyword = 'cute'
        url = 'https://www.google.com/search?q=' + search + '+' + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html =  (download_page(url))
        items = items + (_images_get_all_items(raw_html))
        
        from urllib2 import Request,urlopen
        
        req = Request(items[0], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        response = urlopen(req,None,15)
        output_file = open("./image/update.png",'wb')
        
        data = response.read()
        output_file.write(data)
        response.close();
        
        Topics = []
        self.keywords = 'Listed topics'
        for Tname in Mostname:
            Topicname = Tname[0]#('John', 17)
            Topics.append(Topicname)
            self.keywords = self.keywords  + ', ' + Topicname
            
        
        with open(localfile, 'r') as myfile:
            clean_oridocuments=myfile.read().replace('\n', '')     


        #resize the image   

        im_temp = open("./image/update.png",'r')
        img = Image.open(im_temp)
        img = resizeimage.resize_width(img, 180)
        img.save('./image/update.png', img.format)
        im_temp.close()
        
        self.finalsum =''
        for doc in clean_oridocuments.split('.'):
            for top in Topics:
                if top in doc:
                    f = doc+ '.'
                    self.finalsum =self.finalsum  + '\n' + f
                
        #self.results = summarize(self.finalsum,word_count=100)
#        orisize = 0.0
#        newsize=0.0
#        newsize = 50.0 *SENTENCES_COUNT
#        orisize = len(oridocuments)
#        comratio = newsize/orisize
        
        #self.results = summarize(self.finalsum,ratio= comratio)
        self.results = ''
        wdcoount = 50*SENTENCES_COUNT
        if wdcoount > len(self.finalsum):
            wdcoount =len(self.finalsum)
        else:
            self.results = summarize(self.finalsum,word_count=wdcoount)         
                
        #get n grams of the text
#        for ngram in ngrams(self.results, 3):
#            self.final_results.append(' '.join(str(i) for i in ngram))
#        
#        self.final_results = list(set(self.final_results))
#        
#        self.finalres =''
#        for res in  self.final_results:
#            f = str(res)
#            self.finalres =self.finalres  + ' ' + f.lower()
            
        
        self.processm.set("Summary is done!")
        self.starter = 'We summerized the most important '+ str(SENTENCES_COUNT) + ' sentences of the text: \n'
        self.Heroindex = 'We find the hero/topic of the story is '+ Heroname + '\n'
        self.wordstarter = '\nThe '+ str(SENTENCES_COUNT) + ' topic words are attached: \n'
        
        #1.3 get the summarization, if needed, print it
        self.summarytext.delete("1.0", tk.END)
        self.summarytext.insert(tk.END, self.starter)
        self.summarytext.insert(tk.END, self.Heroindex)
        self.summarytext.insert(tk.END, self.results)
        self.summarytext.insert(tk.END, self.wordstarter)
        self.summarytext.insert(tk.END, self.keywords)
        
                    
        imgnew = ImageTk.PhotoImage(Image.open("./image/update.png"))
        self.panel.destroy()
        self.panel = tk.Label(self.frame2, image = imgnew)
        self.panel.configure(background='lightcyan')
        self.panel.img=imgnew
        self.panel.grid(row=1, column=0)

    def checkResult(self):
        self.filename = askopenfilename()
        localfile = self.filename
        print localfile
        
        N_gram = self.rougenum.get()

        self.evaluates = ''
        with open(localfile, 'r') as myfile:
            reference=myfile.read().replace('\n', '')
            reference = reference.lower()
        
        summary = self.results
        summary = summary.replace('\n', '')
        
        processedsum = summary.split()
        processedref = reference.split()
        
        samplesRef = []
        samplesSum = []
        countsum = 0.0
        
        #get n grams of the text
        for ngram in ngrams(processedsum, int(N_gram)):
            samplesRef.append(' '.join(str(i) for i in ngram))
            countsum = countsum + 1
            
        for ngram in ngrams(processedref, int(N_gram)):
            samplesSum.append(' '.join(str(i) for i in ngram))
            
        count = 0.0
        countref = 0.0
        
        for gram in samplesRef:
            countsum = countsum + 1
        
        for gram in samplesRef:
            countref = countref + 1
            if gram in samplesSum:
                count =count + 1
                
        recall = count/countref
        precision= count/countsum
#        print countref
#        print countsum
        evaresult ='The N Rouge result is:'+ str(recall)+ '(recall)'+ str(precision)+ '(precision)'
        self.evascore.set(evaresult)


'''
  Third sumarizer
  Key-words based text summerizer   
        
'''
        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
#initialize frame and locate it
        self.controller = controller
        frame3 = tk.Frame(self)
        frame3.configure(background='lightcyan')
        frame3.grid(row=11, column=1)

#...........first column .......#
#entry link text headline
        #label of title1
        self.Label = tk.Label(frame3, text="Key-words based text summerizer", font=("Helvetica", 30))
        self.Label.configure(background='lightcyan') 
        self.Label.grid(row=0, column=0)

#show a image Flower
        ##search and show the image
        ###
        self.path ='./image/4.png'
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.panel = tk.Label(frame3, image = self.img)
        self.panel.configure(background='lightcyan')
        self.panel.grid(row=1, column=0)

#chose language
        #label
        self.languagelabel = tk.Label(frame3, text="Select the text language", font=("Helvetica", 16))
        self.languagelabel.configure(background='lightcyan')       
        self.languagelabel.grid(row=2, column=0)

        #inite
        self.OPTIONS1 = ["english","chinese"] #etc
        self.language = tk.StringVar()
        self.language.set(self.OPTIONS1[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS1, key=len))
        #chose
        self.Language = tk.OptionMenu(frame3, self.language, *self.OPTIONS1)
        self.Language.config(width=self.oMenuWidth)
        self.Language.configure(background='lightcyan')
        self.Language.grid(row=3, column=0)
        
#chose sentence number

        #label
        self.sentencelabel = tk.Label(frame3, text="Select summary sentence number", font=("Helvetica", 16))
        self.sentencelabel.configure(background='lightcyan')
        self.sentencelabel.grid(row=4, column=0)
        
        #inite
        self.OPTIONS2 = ["30","150","230","300","400"] #etc
        self.sentencenum = tk.StringVar()
        self.sentencenum.set(self.OPTIONS2[3]) # default value
        self.oMenuWidth = len(max(self.OPTIONS2, key=len))
        #option
        self.SentenceNum = tk.OptionMenu(frame3, self.sentencenum, *self.OPTIONS2)
        self.SentenceNum.configure(background='lightcyan')
        self.SentenceNum.grid(row=5, column=0)
        
#input file or link 
        #label of file
        self.filelabel = tk.Label(frame3, text="You can select a local file or input web link:", font=("Helvetica", 16))
        self.filelabel.configure(background='lightcyan')
        self.filelabel.grid(row=6, column=0)

        #confirm button       
        self.filebutton = tk.Button(frame3, text="Choose a file and summarize", width=20, command=self.callbackFile)
        self.filebutton.configure(background='lightcyan')
        self.filebutton.grid(row=8, column=0)

        #entry of link
        self.linkentry = tk.Entry(frame3, width=50)
        url = "http://www.jingshu.org/jingangjing/23231.html"#chinese text        
        self.linkentry.insert(tk.END, url)
        self.linkentry.configure(background='lightcyan')
        self.linkentry.grid(row=9, column=0)
        
        #confirm button
        self.linkbutton = tk.Button(frame3, text="Input a link and summarize(check the language)", width=40, command=self.callbackLink)
        self.linkbutton.configure(background='lightcyan')
        self.linkbutton.grid(row=10, column=0)
        
   
#...........second columns .......#
        
#label of title2
        self.Label = tk.Label(frame3, text="The summaried story", font=("Helvetica", 20))
        self.Label.configure(background='lightcyan')
        self.Label.grid(row=0, column=1)
        
#print the summary text
        #welcome text
        #display the summary
        self.summarytext = tk.Text(frame3, height=20, width=50)
        self.scroll = tk.Scrollbar(frame3, command=self.summarytext.yview)
        self.summarytext.configure(yscrollcommand=self.scroll.set)
        self.quote = "Welcome to use our text summarizer!"
        self.summarytext.insert(tk.END, self.quote)
        self.summarytext.grid(row=1, column=1)
        self.scroll.grid(row=1, column=2)
        
#evaluation method
        #label of file
        self.evafilelabel = tk.Label(frame3, text="You can select reference text to evaluate:", font=("Helvetica", 16))
        self.evafilelabel.configure(background='lightcyan')
        self.evafilelabel.grid(row=2, column=1)

        #confirm button       
        self.evafilebutton = tk.Button(frame3, text="Choose a file and evaluate", width=20, command=self.checkResult)
        self.evafilebutton.configure(background='lightcyan')
        self.evafilebutton.grid(row=3, column=1)
        
#chose rouge n number

        #label
        self.Nlabel = tk.Label(frame3, text="Select the N-gram number", font=("Helvetica", 16))
        self.Nlabel.configure(background='lightcyan')    
        self.Nlabel.grid(row=5, column=1)

        #inite
        self.OPTIONS3 = ["1","2","3","4","5"] #etc
        self.rougenum = tk.StringVar()
        self.rougenum.set(self.OPTIONS3[0]) # default value
        self.oMenuWidth = len(max(self.OPTIONS3, key=len))
        #chose
        self.Nnum = tk.OptionMenu(frame3, self.rougenum, *self.OPTIONS3)
        self.Nnum.config(width=self.oMenuWidth)
        self.Nnum.configure(background='lightcyan')
        self.Nnum.grid(row=6, column=1)
        
#print the evaluation score 
        self.evascore = tk.StringVar()
        self.evascore.set("The current evaluation score is: 0")
        self.evascorelabel = tk.Label(frame3, textvariable=self.evascore, font=("Helvetica", 16))
        self.evascorelabel.configure(background='lightcyan')
        self.evascorelabel.grid(row=7, column=1)
    
#the process statement
        #some copyright declarations
        self.processm = tk.StringVar()
        self.processm.set("Ready to process!")
        self.processM = tk.Label(frame3, textvariable=self.processm, width=40, font=("Helvetica", 20))
        self.processM.configure(background='lightcyan')
        self.processM.grid(row=8, column=1)
        
        # button to go back
        button = tk.Button(frame3, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=9, column=1)

#quit button
        self.quitbutton = tk.Button(frame3, text="QUIT", fg="red", command=frame3.quit)
        self.quitbutton.configure(background='lightcyan')
        self.quitbutton.grid(row=10, column=1)
        
#some copyright declarations
        self.filelabel = tk.Label(frame3, text="Design © Copyright 2017 by Wen yang and Haoyu Chen for NLP", font=("Helvetica", 13))
        self.filelabel.configure(background='lightcyan')
        self.filelabel.grid(row=11, column=1)

## do the summerizer
#analysis from website
    def callbackLink(self):

        url = self.linkentry.get()            

        #get the language
        LANGUAGE = self.language.get()
        #get the sentence number
        SENTENCES_COUNT = int(self.sentencenum.get())
        
        #organize the sentences into an initial summarization 
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        self.text = ''
        for sentence in parser.document.sentences:
            #count = count + 1
            #sentences.append(f.encode('unicode_escape'))
            #print(sentence)
            f = str(sentence).strip()
            self.text = self.text + '\n' + f
            
        if LANGUAGE == 'english':
    
            # initialize RAKE by providing a path to a stopwords file
            # generate candidate keywords
            stoppath = "./related/SmartStoplist.txt"
            stop_words_list = load_stop_words(stoppath)
            stopwordpattern = build_stop_word_regex(stop_words_list)
            
            # run on RAKE on a given text
            sentenceList = split_sentences(self.text)
            phraseList = generate_candidate_keywords(sentenceList, stopwordpattern, stop_words_list)
    
            # calculate individual word scores
            wordscores = calculate_word_scores(phraseList)
    
            # generate candidate keyword scores
            keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    
            # sort candidates by score to determine top-scoring keywords
            sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
            #totalKeywords = len(sortedKeywords)
            
            #get the scored text
            relevance = RelevanceSummarizer()
            summary = relevance.summarize(self.text, length=500)
            
            #record the sentences
            self.sentences = ''
            self.keywords = ''
            for sentence in summary[::-1]:
                for keyword in sortedKeywords[0:SENTENCES_COUNT]:
                    if keyword[0] in sentence :                 
                        f = str(sentence).strip()
                        g = str("\nKeyword: "+ str(keyword[0])+ ", score: "+str(keyword[1]))
                        self.sentences = self.sentences + '\n' + f.lower()
                        self.keywords = self.keywords + '\n' + g
        
        elif LANGUAGE == 'chinese':    
            self.chinesetext = unicode(self.text,"utf-8")
            #record the keywords
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=self.chinesetext, lower=True, window=2) 
            self.keywords = ''
            for item in tr4w.get_keywords(SENTENCES_COUNT, word_min_len=1):
                g = str("\nKeyword: "+ str(item.word)+ ", score: "+str(item.weight))
                self.keywords = self.keywords + '\n' + g
           
            #record the sentences  
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=self.chinesetext, lower=True, source = 'all_filters')
            self.sentences = ''
            for item in tr4s.get_key_sentences(num=SENTENCES_COUNT):
                print item.sentence
                f = str(item.sentence)
                self.sentences = self.sentences + '\n' + f
        else:
            self.processm.set("Something wrong with the language")        
       
        self.processm.set("Summary is done!")
        self.sumstarter = 'We summerized the most important '+ str(SENTENCES_COUNT) + ' sentences of the text: \n'
        self.wordstarter = '\nThe '+ str(SENTENCES_COUNT) + ' keywords are attached: \n'
        
        # get the summarization, if needed, print it
        self.summarytext.delete("1.0", tk.END)
        self.summarytext.insert(tk.END, self.sumstarter)
        self.summarytext.insert(tk.END, self.sentences)
        self.summarytext.insert(tk.END, self.wordstarter)
        self.summarytext.insert(tk.END, self.keywords)
        
#analysis from local file
    def callbackFile(self):
        self.filename = askopenfilename()
        localfile = self.filename
        print localfile
        
        #get the language
        LANGUAGE = self.language.get()
        #get the sentence number
        SENTENCES_COUNT = int(self.sentencenum.get())
        
        if LANGUAGE == 'english':
            #get the file 
            sample_file = io.open(localfile, 'r')
            text = sample_file.read()
    
            # initialize RAKE by providing a path to a stopwords file
            # generate candidate keywords
            stoppath = "./related/SmartStoplist.txt"
            stop_words_list = load_stop_words(stoppath)
            stopwordpattern = build_stop_word_regex(stop_words_list)
            
            # run on RAKE on a given text
            sentenceList = split_sentences(text)
            phraseList = generate_candidate_keywords(sentenceList, stopwordpattern, stop_words_list)
    
            # calculate individual word scores
            wordscores = calculate_word_scores(phraseList)
    
            # generate candidate keyword scores
            keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    
            # sort candidates by score to determine top-scoring keywords
            sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
            #totalKeywords = len(sortedKeywords)
            
            #get the scored text
            relevance = RelevanceSummarizer()
            summary = relevance.summarize(text, length=500)
            
            #record the sentences
            self.sentences = ''
            self.keywords = ''
            for sentence in summary[::-1]:
                for keyword in sortedKeywords[0:SENTENCES_COUNT]:
                    if keyword[0] in sentence :                 
                        f = str(sentence).strip()
                        g = str("\nKeyword: "+ str(keyword[0])+ ", score: "+str(keyword[1]))
                        self.sentences = self.sentences + '\n' + f
                        self.keywords = self.keywords + '\n' + g
        elif LANGUAGE == 'chinese':    
            text = codecs.open(localfile, 'r', 'utf-8').read()
            
            #record the keywords
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=text, lower=True, window=2) 
            self.keywords = ''
            for item in tr4w.get_keywords(SENTENCES_COUNT, word_min_len=1):
                g = str("\nKeyword: "+ str(item.word)+ ", score: "+str(item.weight))
                self.keywords = self.keywords + '\n' + g
           
            #record the sentences  
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=text, lower=True, source = 'all_filters')
            self.sentences = ''
            for item in tr4s.get_key_sentences(num=SENTENCES_COUNT):
                print item.sentence
                f = str(item.sentence)
                self.sentences = self.sentences + '\n' + f.lower
            
        else:
            self.processm.set("Something wrong with the language")        
        
        self.processm.set("Summary is done!")
        self.sumstarter = 'We summerized the most important '+ str(SENTENCES_COUNT) + ' sentences of the text: \n'
        self.wordstarter = '\nThe '+ str(SENTENCES_COUNT) + ' keywords are attached: \n'
        
        # get the summarization, if needed, print it
        self.summarytext.delete("1.0", tk.END)
        self.summarytext.insert(tk.END, self.sumstarter)
        self.summarytext.insert(tk.END, self.sentences)
        self.summarytext.insert(tk.END, self.wordstarter)
        self.summarytext.insert(tk.END, self.keywords)


    def checkResult(self):
        self.filename = askopenfilename()
        localfile = self.filename
        print localfile
        
        N_gram = self.rougenum.get()

        self.evaluates = ''
        with open(localfile, 'r') as myfile:
            reference=myfile.read().replace('\n', '')
        reference = reference.lower()
        
        summary = self.sentences
        
        self.processedsum = summary.split()
        self.processedref = reference.split()
        
        samplesRef = []
        samplesSum = []
        countsum = 0.0
        
        #get n grams of the text
        for ngram in ngrams(self.processedsum, int(N_gram)):
            samplesRef.append(' '.join(str(i) for i in ngram))
            
            countsum = countsum + 1
            
        for ngram in ngrams(self.processedref, int(N_gram)):
            samplesSum.append(' '.join(str(i) for i in ngram))
            
        count = 0.0
        countref = 0.0
        
        for gram in samplesRef:
            countsum = countsum + 1
        
        for gram in samplesRef:
            countref = countref + 1
            if gram in samplesSum:
                count =count + 1
                
        recall = count/countref
        precision= count/countsum
#        print countref
#        print countsum
        evaresult ='The N Rouge result is:'+ str(recall)+ '(recall)'+ str(precision)+ '(precision)'
        self.evascore.set(evaresult)
        
        


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"
            

#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    item, end_content = _images_get_next_item(page)
    items.append(item)     
    page = page[end_content:]
    return items
            

        
def main():
    
    #create a root window using Tk

    app = SampleApp()
    app.title('The small summarizer')
    app.mainloop()
    app.destroy() # optional; see description below

if __name__ == '__main__':
    main()  