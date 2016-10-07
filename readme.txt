Points to note:

1A) Way to run code:

Go to given folder
run - python bigrams.py corpus.txt "Statement"
E.g. python bigrams.py corpus.txt "I like listening to Muse."

This is done with tabulate py file.

I've made my file so you get the count and probability for each type one at a time, so you'll get 6 tables for each statement.
1) python bigrams.py corpus.txt "The president has relinquished his control of the company's board."
2) python bigrams.py corpus.txt "The chief executive officer said the last year revenue was good."

or

1B) Potential installation
I have installed tabulate on my computer in order to print out the tables in a good format.
In case you do not have it/do not want to install it, I have a separate py file called normal_bigrams.py that you can use with the method in A
i.e. python normal_bigrams.py corpus.txt "I like listening to Muse."

C) About code:

1) Replaced periods with nothing. Split based on spaces. If there is a blank in the list, it was removed.
	For e.g.: I feel great . I feel good.
	Removing periods and separating on spaces gives you
	I, feel, great, _, I, feel, good
	So I remove the space from there.
2) Replaced new lines with spaces. This was causing an issue where it was joining  last word from one line and the first word from the next, so I did this.
3) For add-one smoothing, V is the number of unique words in the corpus.
4) For Good-turing smoothing, if N(c) is 0, I gave it the value N1/N, where N1 is the number of bigrams occuring once, and N is the total number of bigrams in the statement.
5) For probabilities - I decided to ignore the probability of the first word in each test case. Thus, the probability is essentially the product of each bigram.

