import twitterBot
import settings
import random
import time

settings.clear()
api = twitterBot.loginToTwitter()

while True:

    t = time.localtime()

    if t.tm_hour >= 20 or t.tm_hour < 9:
        frontPage = {}
        settings.saveData(frontPage, settings.FRONT_PAGE)
        settings.saveData(frontPage, settings.HNFRONT_PAGE)
        twitterBot.checkFollowers(api)
        when = settings.printTime()
        print(f"{when} <<< SLEEPING >>>")
        
        while t.tm_hour >= 20 or t.tm_hour < 9:
            settings.clear()
            settings.pause(1)
            t = time.localtime()
            if t.tm_hour < 20 and t.tm_hour >= 9:
                break
    else:
        for x in range(4):

            settings.clear()
            y = random.randrange(10)

            if x == 0:
                twitterBot.tweetReddit(api, 25)
            elif x == 1 and y % 2 == 0:
                twitterBot.angelTweets(api)
            elif x == 2 and y % 3 == 0:
                twitterBot.tweetFavFollow(api)
            elif x == 3:
                twitterBot.tweetHackerNews(api, 25)
