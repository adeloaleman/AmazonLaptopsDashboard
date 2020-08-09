import nltk
import string
nltk.data.path.append('/home/adelo/.nltk/nltk_data')
# If we are in the server:
# nltk.data.path.append('/root/nltk_data')
# nltk.data.path.append('/home/ubuntu/nltk_data')
from nltk.corpus import stopwords

stopwords_brands_additionals = ['computer','computers','laptop','laptops','thing','things','machine','machines','im','dont','ive']
stopwords_total  = stopwords.words('english') + stopwords_brands_additionals

# The following function takes a string and an optional argument «tokenize»:
# * It removes punctuation and stopwords from the string entered
# * If the «tokenize» argument if not specified, the string will be tokenized so it will return 
#   a list of the word without punctuation or stopwords
# * If a tokenize argument is specified, the string will NOT be tokenized, so it will return
#   a string without punctuation or stopwords
def pre_processing(texto,tokenize=None):
    # Removing punctuation:
    text_process = ''.join([ char for char in texto if char not in string.punctuation ])
    # Removing Stopwords:
    text_process = ' '.join([ word for word in text_process.split() if word.lower() not in stopwords_total ])
    if tokenize == None:
        return [word for word in text_process.split()]
    else:
        return text_process
    

# Example of applying the function «pre_processing()»:
# display(my_reviews['title_text'].head())
# display(my_reviews['title_text'].head().apply(lambda val: pre_processing(val,'no_tokenize')))

# Here is how we would apply the function «pre_processing()» to a column over the entire dataframe.
# However, we won't do that in this stage because we need a raw text for the Sentiment Analysis
# my_reviews['title']      = my_reviews['title'].apply(lambda val: pre_processing(val,'no_tokenize'))
# my_reviews['text']       = my_reviews['text'].apply(lambda val: pre_processing(val,'no_tokenize'))
# my_reviews['title_text'] = my_reviews['title_text'].apply(lambda val: pre_processing(val,'no_tokenize'))
# display(my_reviews)