"""
Written by Varshini Ramaraj
Written on: 09/21/2016

Functional code starts here
Go to line 141 for the non-functional code

This code basically takes in a corpus and a statement from the user as arguments. It then calculates
the bigram counts and probabilities of the bigrams in the statement. It does this without smoothing,
with add-one smoothing and good-turing smoothing.
"""


# calculate the count for each combo:
def createcount(corpus_divided,statement_divided, count_table):
    for ax in range(0, len(statement_divided)):
        list1 = []
        word1st = statement_divided[ax]
        for bx in range(0, len(statement_divided)):
            word2st = statement_divided[bx]
            # add a list here and keep appending to that. At end of for loop append it to main list in probability_table
            list1.append(0)
            for ell in range(0, len(corpus_divided) - 1):  # loop to  check if both words are consecutive in the corpus
                word1co = corpus_divided[ell]
                word2co = corpus_divided[ell + 1]
                if word1co == word1st and word2co == word2st:
                    list1[bx] += 1
        count_table.append(list1)  # basically probability_table becomes a list of lists
    return count_table


# to print the probability table
def printcount(count_table,statement):
    el = 0
    print("\nThis is the table with bigram counts: ")
    header = statement
    print tabulate(count_table,header,tablefmt="pipe")


#count occurrences of each word
def countword(statement_divided,corpus_divided):
    word_count = []
    for word in statement_divided:
        word_count.append(corpus_divided.count(word))
    #prints out word_count, just while testing
    return word_count

# to print bigram table
def printbigram(bigram_table,statement):
    print("\nThis is the table with bigram probabilities: ")
    header = statement
    print tabulate(bigram_table,statement,tablefmt="pipe")

"""
These functions are for the normal smoothing
"""
# to calculate the bigram probability table
def createbigram(word_count,statement_divided,count_table):
    # take the first word, calculate the first list from it, and then increment the list value
    bigram_table = []
    ax = 0
    for word in word_count:
        list1 = []
        for bx in range(0, len(statement_divided)):
            value=count_table[ax][bx] / float(word)
            list1.append(format(value, '.4f'))
        bigram_table.append(list1)
        ax += 1
    return bigram_table

#to calculate the probability of a sentence using the conditional probabilities
def probsentence(bigram_table):
    #addprobability of first word IMPORTANT
    length = len(bigram_table[0])
    probability = 1
    for ax in range(0,length-1):
        probability*=float(bigram_table[ax][ax+1])
    return probability

"""
These functions are for add-one smoothing
"""

#get number of unique words in the whole corpus
def getvalueV(corpus_divided):
    uniqueList=[]
    for word in corpus_divided:
        if word not in uniqueList:
            uniqueList.append(word)
    return len(uniqueList)

#changing count_table by adding one to each
def addOne(change_count_table):
    for lis in change_count_table:
        for value in range(0,len(lis)):
            lis[value]+=1
    return change_count_table

# calculates bigram table by dividing prob by count + unique words
def createbigramAdd(word_count,statement_divided,count_table,countV):
    bigram_table = []
    ax = 0
    for word in word_count:
        list1 = []
        for bx in range(0, len(statement_divided)):
            value = (count_table[ax][bx]) / float(word + countV)
            list1.append(format(value, '.4f'))
        bigram_table.append(list1)
        ax += 1
    return bigram_table

"""
These functions are for good-turing smoothing
"""
#this basically  gets the count of count of bigrams
def getcounts(dict_freq,bigram_table):
    for lis in bigram_table:
        for value in lis:
            check = dict_freq.get(value,0)      #checks in dictionary to see if the frequency value has already been met before
            if check==0:
                dict_freq[value]=1
            else:
                dict_freq[value]+=1
    return dict_freq

#basically updates the count_table from 0,1 and so on to the new values calculated using the dict_freq and new_freq values
def newCount(new_freq,count_table):
    for key in new_freq.keys():
        newVal = new_freq.get(key)
        newVal = float(format(newVal,'.4f'))        #formats it to 4 decimals, otherwise goes to like 15 decimals
        for lis in count_table:
            for val in range(0,len(lis)):
                if lis[val]==key:
                    lis[val]=newVal         #changes list values if less than 20 only
    return count_table

#used to change the values less than 20 to the new values
def changeTuringValue(dict_freq,new_freq):
    n1 = dict_freq.get(1)
    n = 0
    for key in dict_freq.keys():
        n += (float(key) * dict_freq.get(key))
    substitute = float(n1 / n)  # check today
    for key in dict_freq.keys():  # takes the frequency of frequencies and updates them
            new_freq[key] = (float(key + 1) * dict_freq.get(key + 1, substitute)) / float(dict_freq.get(key))   #basically if the value is 0, uses N1/N
    return new_freq

"""
Non-function code starts here
"""
import sys
from tabulate import tabulate

args=[]
for arg in sys.argv:    #takes in statement through command line
    args.append(arg)

file1 = open(args[1],"r")
corpus = file1.read()   #read in the corpus from textfile
corpus_divided = corpus.replace(".","").replace("\'"," \'").replace("\n"," ").split(" ")  #split the corpus based on spaces
for word in corpus_divided:
    if (word==" "):
        corpus_divided.remove(word)

count_table = []  # to store probability table of every combination of word
statement = args[2] #takes in statement
statement_divided = statement.replace(".", "").replace("\'"," \'").split(" ")
for word in statement_divided:
    if word == " ":
        statement_divided.remove(word)

print("\n*****************THIS IS WITHOUT ANY SMOOTHING***********************")
count_table = createcount(corpus_divided, statement_divided,count_table)  # calculate the probability for each combo:
printcount(count_table,statement_divided)  # prints probability table
word_count = countword(statement_divided, corpus_divided)  # count occurrences of each word
bigram_table = createbigram(word_count, statement_divided,count_table)  # calculates bigram table by dividing prob by count
printbigram(bigram_table,statement_divided)  # to print bigram table
probability = probsentence(bigram_table)
print("\nThe probability of the sentence \'%s\' is %s" % (statement, probability))

print("\n\n*****************THIS IS WITH ADD-ONE SMOOTHING***********************")
countV = getvalueV(corpus_divided)      #get number of unique words in the whole corpus
change_count_table = addOne(count_table)        #changing count_table by adding one to each
printcount(change_count_table,statement_divided)          #prints probability table
change_bigram_table = createbigramAdd(word_count,statement_divided,change_count_table,countV)  # calculates bigram table by dividing prob by count + unique words
printbigram(change_bigram_table,statement_divided)
probability = probsentence(change_bigram_table)
print("\nThe probability of the sentence \'%s\' is %s" % (statement, probability))


print("\n\n*****************THIS IS WITH GOOD-TURING SMOOTHING***********************")

dict_freq={}
dict_freq=getcounts(dict_freq,count_table)  #get frequencies for N0, N1 and so on
new_freq={}                                 #to pass on the new values and change in the table
new_freq = changeTuringValue(dict_freq,new_freq)
new_count_table = newCount(new_freq,count_table)    #changing count_table by replacing value with new_freq  values
printcount(new_count_table,statement_divided)         #prints the bigram count
new_bigram_table = createbigram(word_count,statement_divided,new_count_table)
printbigram(new_bigram_table,statement_divided)       #prints the probability count
probability=probsentence(new_bigram_table)      #calculates the probability
print("\nThe probability of the sentence \'%s\' is %s" % (statement, probability))





