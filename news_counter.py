import praw 
from pmaw import PushshiftAPI
import os 
import tldextract
import pickle 
from datetime import date 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
import csv 
import numpy 

class Article():
    def __str__(self):
        return str(self.author) + "\n" + str(self.domain) + "\n" + str(self.score) + "\n" + str(self.upvote_ratio) + "\n" + str(self.cross_posts) + "\n" + str(self.url)
         
    
    def __init__(self, author, domain, score, upvote_ratio, numComments, cross_posts, url, iden, title, comments):
        global count
        self.author = author 
        self.domain = domain 
        self.score = score 
        self.upvote_ratio = upvote_ratio
        self.numComments = numComments
        self.url = url 
        self.iden = iden 
        self.cross_posts = cross_posts
        self.title = title 
        self.comments = comments
        print("Created Article #" + str(count) + " With " + str(len(comments)) + " Comments")
        count = count + 1 

def __main__():
    reddit = praw.Reddit(client_id='iXk2rY1rxx7_jvWpJwnYBA', 
                        client_secret='Hwkrr1jTusfeWoPBcGsluyVH0BfBzQ', 
                        user_agent='News Recorder')
    limit = 400
    subreddits = ["news", "worldnews", "politics"]
    features = ["rising", "hot", "new"]
    today = date.today()
    for feature in features: 
        for sub in subreddits: 
            articles = []
            print("Parsing r/" + sub + "\n")
            filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
            filePath = filePath + str(today) + "_r_" + sub + "_" + feature + ".pickle"
            file = open(filePath, "wb")
            subreddit = reddit.subreddit(sub)
            posts = eval("subreddit." + feature + "(limit=" + str(limit) + ")")
            orgList = list() 
            orgSet = set()
            for p in posts:
                if (str(p.url).find("http") == 0) or (str(p.url).find("www") == 0):
                    domain = str(tldextract.extract(str(p.url)).domain)
                    orgList.append(domain)
                    orgSet.add(domain)
                    comments = p.comments.list() 
                    article = Article(p.author, domain, p.score, p.upvote_ratio, p.num_comments, p.num_crossposts, p.url, p.id, p.title, comments)
                    pickle.dump(article, file)
            counter(orgSet, orgList)
            file.close() 

def counter(orgSet, orgList): 
    for org in orgSet:
        print(org + " : " + str(orgList.count(org)))

def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

#Iter must be a list of article objects 
def isUniqueId(iter, id):
    for it in range(len(iter) - 1, 0, -1):  
        if str(iter[it].iden) == str(id): 
            return False 
        else:
            continue 
    return True 

def parseData():
    articles = []
    counter = 0 
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    for file in files: 
        if file.endswith(".pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen:
                if isUniqueId(articles, article.iden):
                    articles.append(article)
                    counter = counter + 1
                    print("Appending: " + str(counter))
    print("Done Appending")
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\uniqueData\\"
    file = filePath + "data.pickle"
    print("Writing To File")
    for article in articles: 
        with open(file, "ab") as f: 
            pickle.dump(article, f)
    print("Done Writing To File")

def getAuthorArticles(author):
    articles = []
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    counter = 0 
    for file in files: 
        if file.endswith(".pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen: 
                try:
                    if article.author == author:
                        articles.append(article.domain)
                except Exception: 
                    pass 
            counter = counter + 1 
            print(str(counter)) 
    return articles 

def authorFreq(): 
    authors = {}
    articles = {}
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    counter = 0 
    authorCounter = 0
    for file in files: 
        if file.endswith(".pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen: 
                if str(article.author) not in authors:
                    authors.update({str(article.author) : {}})
                    authors[str(article.author)].update({'count' : 0})
                    articles.update({article.author : {}})
                    #try:
                    #    authors[str(article.author)].update({'total karma / comment karma' : article.author.total_karma / article.author.comment_karma})
                    #    print(str(authorCounter))
                    #    authorCounter += 1 
                    #except Exception:
                    #    pass 
                if str(article.domain) not in articles[article.author]:
                    articles[article.author].update({str(article.domain) : 0})
                try:
                    authors[str(article.author)]['count'] = authors[str(article.author)]['count'] + 1 
                    articles[article.author][str(article.domain)] = articles[article.author][str(article.domain)] + 1 
                except Exception: 
                    pass 
            counter = counter + 1 
            print(str(counter)) 
    df = pd.DataFrame.from_dict(authors)
    df = df.transpose()
    df = df.drop("None")
    df.sort_values(by=['count'], ascending=False, inplace=True)
    articles = pd.DataFrame.from_dict(articles)
    return df, articles 

def processAuthorData(features):
    articles = {}
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    counter = 0 
    for file in files: 
        if file.endswith(".pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen:
                for feature in features: 
                    if str(article.author) not in articles:
                        articles.update({str(article.author) : {}})
                        articles[str(article.author)].update({"count" : 0})
                        for f in features: 
                            articles[str(article.author)].update({f : 0})
                    try:
                        articles[str(article.author)][feature] = articles[str(article.author)][feature] + (eval("article." + feature))
                    except Exception: 
                        pass  
                articles[str(article.author)]['count'] = articles[str(article.author)]['count'] + 1  
                counter = counter + 1 
                print(str(counter)) 

    for article in articles:
        for key in articles[article].keys():
            if key == "upvote_ratio":
                articles[article][key] = articles[article][key] / articles[article]['count']

    return articles

def processData(features):
    articles = {}
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    counter = 0 
    for file in files: 
        if file.endswith(".pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen:
                for feature in features: 
                    if str(article.domain) not in articles:
                        articles.update({str(article.domain) : {}})
                        articles[str(article.domain)].update({"count" : 0})
                        for f in features: 
                            articles[str(article.domain)].update({f : 0})
                    try:
                        articles[str(article.domain)][feature] = articles[str(article.domain)][feature] + (eval("article." + feature))
                    except Exception: 
                        pass  
                articles[str(article.domain)]['count'] = articles[str(article.domain)]['count'] + 1  
                counter = counter + 1 
                print(str(counter)) 

    for article in articles:
        for key in articles[article].keys():
            if key != "count":
                articles[article][key] = articles[article][key] / articles[article]['count']

    return articles

def sortData(file, feature = "count"):
    df = pd.read_csv(file)
    df = df.transpose()
    df = df[1:]
    df.columns = ["count", "score", "upvote_ratio", "numComments", "cross_posts"]
    df = df.sort_values(by=[feature], ascending=False)
    return df 
    

def getAverageScorePerDay():
    averageScore = []
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    counter = 0 
    filecounter = 0
    for file in files: 
        score = 0 
        counter = 0 
        if file.endswith("r_news_hot.pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen: 
                try:
                    score = score + article.score
                    counter = counter + 1 
                except Exception: 
                    pass
        try:
            averageScore.append(score / counter) 
        except Exception:
            pass 
        filecounter = filecounter + 1
        print(str(filecounter)) 
    return averageScore 

def getNumberOfCommentsPerDay():
    postCount = []
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    filecounter = 0
    for file in files: 
        counter = 0
        if file.endswith("r_worldnews_new.pickle") or file.endswith("r_worldnews_rising.pickle") or file.endswith("r_worldnews_hot.pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen: 
                try:
                    counter = counter + article.numComments
                except Exception: 
                    pass
        try:
            if counter > 0: 
                postCount.append(counter)
        except Exception:
            pass 
        filecounter = filecounter + 1
        print(str(filecounter)) 
    return postCount 

def getFeatureWRTCount(upper, feature, ascending=False): 
    df = sortData("articles.csv")
    print(str(df))
    df = df[1 : int(upper) + 1]
    df = df.sort_values(by=[feature], ascending=ascending)
    return df 

def getContributionPercent(ratios):
    percents = []
    authors = pd.read_csv("authors.csv")
    authors.columns = ['author', 'count']
    for ratio in ratios:
        total = sum(authors['count'].to_list())
        index = int(len(authors['count'].to_list()) * ratio)
        count = sum(authors['count'].to_list()[0 : index])
        percents.append(count / total)
    return percents

def getPercentArticles(data, feature, ratios):
    percents = []
    for ratio in ratios:
        total = sum(data[feature].to_list())
        index = int(len(data[feature].to_list()) * ratio)
        count = sum(data[feature].to_list()[0 : index])
        percents.append(count / total)
    return percents

def getNumberOfPostsPerDay():
    postCount = []
    filePath = r"C:\Users\thoma\Documents\Python Programs\News Counter\data\\"
    files = os.listdir(filePath)
    filecounter = 0
    for file in files: 
        counter = 0
        if file.endswith("new.pickle"):
            articleGen = loadall(filePath + file)
            for article in articleGen: 
                try:
                    counter = counter + 1 
                except Exception: 
                    pass
        try:
            postCount.append(counter)
        except Exception:
            pass 
        filecounter = filecounter + 1
        print(str(filecounter)) 
    return postCount 

def scorePerComment(start, stop, step):
    #score / comments 
    df = sortData("articles.csv")
    df = df[1 : ]
    orgs = df.index.values
    scorePerComment = []
    for i in range(0, len(df)):
        try:
            scorePerComment.append(df['score'][i] / df['numComments'][i])
        except ZeroDivisionError: 
            scorePerComment.append(-1)
    
    average = 0
    count = 0
    for i in range(start, stop, step):
        if scorePerComment[i] != -1:
            average += scorePerComment[i]
            count += 1 
    average = average / count
    print("Average Score/Comment: " + str(average))

if __name__ == "__main__":
    #authors, articles = authorFreq()
    #print(str(authors))
    #authors.to_csv("karma_ratio.csv")
    #d = {"News Org" : orgs, "Score Per Comment" : scorePerComment}
    #data = pd.DataFrame(d)
    #data.to_csv("scorepercomment.csv")
    #features = ["score", "upvote_ratio", "numComments", "cross_posts"]
    #articles = processAuthorData(features)
    #print(str(articles))
    #df = pd.DataFrame(articles)
    # df = getFeatureWRTCount(100, "score", True)
    #df.to_csv("authorStats.csv")
    df = sortData("authorStats.csv")
    # df = df[ : 10]
    # print(str(df))
    # #df = df.sort_values(by=["cross_posts"])
    # #print(str(df))
    # authors, articles = authorFreq()
    # # #print(str(authors))
    # # articles.columns = articles.columns.astype("str")
    # # ##print(type(articles[articles.columns[0]]))   
    # # with open("orgRatio.csv", 'w') as csvfile: 
    # #     csvwriter = csv.writer(csvfile) 
    # #     csvwriter.writerow(["Ratio"]) 
    # for i in range(0, 1500):
    #     series = articles[authors.index.values[i]].sort_values(ascending=False)
    #     series = series.dropna()
    #     print(str(series))
    #     os.abort()
    #         print("Ratio of top org: " + str(series[0] / series.sum()))
    #         # creating a csv writer object 
    #         csvwriter.writerow([str(series[0] / series.sum())])
            
        

    #authors.to_csv("authors.csv")
    #articles.to_csv("authorFreq.csv")
    #print(str(count / total))
    #articles = getAuthorArticles(str(authors['count'][0]))
    #print(str(articles))
    #print(str(getNumberOfPostsPerDay()))
    #arr = getContributionPercent()
    #print(str(arr))
    #x = numpy.arange(0, 1.001, .001)
    #feature = "numComments"
    #df = df[1 : ]
    #y = getPercentArticles(df, feature, x)
    #y = arr 
    # print(str(y))
    # #df.to_csv("percent.csv")
    #sns.set_theme(style="darkgrid")    
    #sns.lineplot(x = x, y = y)
    #plt.show()

    #Percent Significant
    # x = numpy.arange(0.001, 1.01, .001)
    # y = getContributionPercent(x)
    # #d = {"Ratios" : x, "Percent Of Total Submissions" : y}
    # #df = pd.DataFrame(d)
    # #df.to_csv("percent.csv")
    # sns.set_theme(style="darkgrid")

    # sns.lineplot(x = x, y = y)
    # plt.show()
    
