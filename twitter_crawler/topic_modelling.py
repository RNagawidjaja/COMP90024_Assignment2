import re
import nltk
import json

class TopicModeller:
    def __init__(self):
        nltk.download('wordnet')
        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        self.word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()

    #reference: WSTA_N1_preprocessing.ipynb from Comp 90042 material
    def lemmatize(self, word):
        nouns_to_keep = ['running', 'swimming', 'jogging', 'cycling','golfing']
        if word not in nouns_to_keep:
            lemma = self.lemmatizer.lemmatize(word,'v')
            if lemma == word:
                lemma = self.lemmatizer.lemmatize(word,'n')
            return lemma
        else:
            return word
            


    # Given tweet text, return the topic(s) of the tweet. 
    def topic_of_tweet(self, text):
        
        # List of word related to exercise
        sloth_keywords = ['fitness', 'gym', 'exercise', 'workout', 'running', 'swimming', 'yoga', 
            'play tennis','cycling', 'play football', 'play basketball', 'play soccer', 'weight training'
            'golfing', 'aerobics', 'play golf']

        '''
        Reference: Which Fast Food Restaurant Is Australia's Favourite?
        https://www.lifehacker.com.au/2018/10/which-is-australias-favourite-fast-food-chain/
        Alcoholic Beverages: Beers, Wines, Spirits, Liqueurs
        http://www.nutrientsreview.com/alcohol/alcoholic-beverages-abv-calories.html
        '''
        gluttony_keywords = ['bigmac', 'kfc', 'mcdonalds', 'hungry jack','fried chicken', 
                'dominos', 'red rooster', 'nandos', 'maccas', 'fast food', 'rubbish food',
                'burger', 'french fries','pizza', 'nuggets', 'sweets', 'candy', 'ice cream',
                'alcohol', 'beer', 'wine', 'liqueur', 'liquor', 'cider', 'tequilla', 'vodka', 'brandy',
                'distilled beverage', 'whiskey', 'chips', 'alcopop']

        sin_keywrods = {'sloth': sloth_keywords, 'gluttony': gluttony_keywords}
        '''
        Reference: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/ 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        tokenized_text = self.word_tokenizer.tokenize(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text))
        #print(tokenized_text)
        lemmatized_words = []
        for word in tokenized_text:
            lemmatized_words.append(self.lemmatize(word.lower()))
        prossessed_text = ' '.join(lemmatized_words)
        
        topic = []
        for keyword in sin_keywrods:
            for word in sin_keywrods[keyword]:
                if len(re.findall(word, prossessed_text)) > 0:
                    topic.append(keyword)
                    break
        return topic

if __name__ == '__main__':
    nltk.download('wordnet')
    filename = r'C:\Users\reyna\Documents\Unimelb\COMP90024\Assignment_1\json_files\smallTwitter.json'
    topic_modeller = TopicModeller()
    with open(filename, encoding='UTF-8') as tf:
        count = 0
        topic = []
        next(tf)
        for i, line in enumerate(tf):
            if i <= 1000:
                tweet = json.loads(line[:-2])['doc']['text']
                topic = topic_modeller.topic_of_tweet(tweet)
                if len(topic) > 0:
                    count += 1
                print(topic)
            else:
                break
        print(count)