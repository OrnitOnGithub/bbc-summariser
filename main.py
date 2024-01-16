import os
import requests
from bs4 import BeautifulSoup


articleAmount = 1


#setup
url = "https://www.bbc.com/news"
response = requests.get(url)
results = BeautifulSoup(response.content, "html.parser")

Summariser_Key = os.getenv("Summariser_Key")

articleLinks = []
articleTitles = []

def Summarise(text):
    """
    link: https://rapidapi.com/oneai-oneai-default/api/summarize-texts/
    also i forgot what my account is
    """
    
    url = "https://summarize-texts.p.rapidapi.com/pipeline"
    
    payload = { "input": text }
    headers = {
    	"content-type": "application/json",
    	"X-RapidAPI-Key": Summariser_Key,
    	"X-RapidAPI-Host": "summarize-texts.p.rapidapi.com"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()
    return (data['output'][0]['text'])
    


#article previews on the first page are always under h3
#find the article text and the link to the article with href element
#also one day rewrite to only search for href instead of first searching for h3 and then href, whould work imo
articles = results.find_all('h3')
for article in articles:
    if (article.text):
        link = article.parent.get('href')
        if (link):
            #"if" to make sure there is indeed a link. if there is then the article's a real one :fire:.
            print(article.text)
            print(link)
            print("----------")
            articleLinks.append(link)
            articleTitles.append(article.text)
#get rid of duplicates
articleLinks = [x for i, x in enumerate(articleLinks) if x not in articleLinks[:i]]
articleTitles = [x for i, x in enumerate(articleTitles) if x not in articleTitles[:i]]



#just a variable used to know the index of an article in the "for" loop. used for titles.
articleNumber = 0
for articleLink in articleLinks[:articleAmount]:
    #Idk why but there's still random shit in the links. This should only keep links to actual articles.
    if (articleLink[:5] == "/news"):
        #setup
        url = "https://www.bbc.com" + articleLink
        response = requests.get(url)
        article = BeautifulSoup(response.content, "html.parser")


        #all articles are inside a <p> tag
        textElements = article.find_all('p')
        text = ""
        for textElement in textElements:
            if (textElement.text):
                #for some reason all relevant text in an article is child of a <div> tag
                if (textElement.parent.name == 'div'):
                    text += textElement.text
        print("--------------------------")
        print(articleTitles[articleNumber])
        print("--------------------------")
        print(Summarise(text))
    articleNumber += 1
