#Importing libraries
from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
import nltk

#Ignore the warning messages
warnings.filterwarnings('ignore')

#Download the packages from nltk
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

#Get the article URL
article = Article(' ') #add the website link in the inverted commas
article.download()
article.parse()
article.nlp()
corpus = article.text

#Print the text
#print(corpus)

#Tokenization
text = corpus
sent_tokens = nltk.sent_tokenize(text) #conv text into a list of sentences
#print(sent_tokens)

#Create a dictionary to remove punctuations
remove_punct_dict = dict((ord(punkt), None) for punkt in string.punctuation)
#Print the punctuations
#print(string.punctuation)
#Print thedictionary
#print(remove_punct_dict)

#Create a function to return a list of lemmetized lower case words after removing punctuations
def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))
#Print the tokenized text
#print(LemNormalize(text))

#Key word matching:
#Greeting Inputs
GREETING_INPUTS = ['hi', 'hello', 'hiya', 'greetings', 'whats up', 'hey']
#Greeting responses back to the user
GREETING_RESPONSES = ['how are you doing', 'hi', 'hello', 'hey there', 'whats good']
#Random Greeting response to the user's greeting
def greeting(sentence):
#If the user's input is a greeting, returns should be a randomly chosen resonse
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    #User's response/query---------
    #user_response=''
    user_response = user_response.lower() #make the response lower case
    #Print the user's query/response------------
    print(user_response)
    #Set the bot's response to an empty string
    robo_response = ''
    #Append the user's response to the sentence list
    sent_tokens.append(user_response)
    #Print the sentence list after the user's response-------
    #print(sent_tokens)

    #Create a tfidfVectorizer object
    tfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')

    #Convert the text to matrix- TF-IDF features
    tfidf = tfidfVec.fit_transform(sent_tokens)
    #Print tfidf features -------
    #print(tfidf)

    #Get the measure of similarity
    vals = cosine_similarity(tfidf[-1], tfidf)
    #print(vals)     #Print the similarity score
    #Get the index of the most similar text to the user's response
    idx = vals.argsort()[0][-2]   #-1 the most similar- at the end of the list(response itself)
    vals.argsort()                        #hence -2 the next best resonse
    #  Reduce the dimentionality of vals
    flat = vals.flatten()
    flat.sort()     #Sorting in ascending order

    #Get the most similar score to the user's response
    score = flat[-2]
    #print(score)
    #If the vals score is 0 then there is no text similar to the user's response
    if score == 0:
        robo_response = robo_response+"I am sorry, I don't understand."
    else:
        robo_response = robo_response+sent_tokens[idx]
#print( robo_response)
    sent_tokens.remove(user_response)
    return robo_response


flag=True
print("Bot: I am a Bot, I will answer your queries about one plus 7. To quit type bye.")
while(flag==True):
    user_response = input("You: ")
    user_response = user_response.lower()
   # if user_response=='What are the reviews?' or user_response=='Reviews?' or user_response=='what are the reviews of one plus 7t':
 #Flag=Flase

    if(user_response!='bye'):
            if(user_response=='thanks' or user_response=='thank you'):
                flag = False
                print("You are welcome!")
            else:
                 if(greeting(user_response) != None):
                    print("Bot: "+ greeting(user_response))
                 else:
                     print("Bot: "+response(user_response))

    else:
        flag = False
        print('Bot: Chat with you later.')
