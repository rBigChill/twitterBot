import tweepy
import twitterCreds as c
import settings
import redditBot
import random
import requests
import hackerNews

def loginToTwitter():
    """
        Return api, and me
    """
    # auth
    auth = tweepy.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
    auth.set_access_token(c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET)

    # api instance
    api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
            )

    return api

def angelTweets(api):
    """
        Like Angels Tweets
    """
    tweets = api.user_timeline("_angelplays_", count=1)
    
    if tweets[0].favorited != True:
        api.create_favorite(tweets[0].id)
        when = settings.printTime()
        title = "<<< ANGELS TWEET >>>"
        result = "[ FAVORITED ]"
        print(f"{when} {title} {result}")
        settings.pause(settings.LIMIT)

def tweetReddit(api, limit):
    """
        Tweet Reddit Data
    """
    frontPage = settings.openData(settings.FRONT_PAGE)
    frontPageLoop = settings.openData(settings.FRONT_PAGE)

    ignore = ["I ","thread ","THREAD ","my ","My ","OC ","ive ","I've ","reddit","Reddit","we ","We "]

    if frontPage == {}:
        redditBot.grabFrontPage(limit)
    else:
        for k in frontPageLoop:
            title = frontPageLoop[k]['title']
            link = frontPageLoop[k]['url']
            for i in ignore:
                if i in title or i in link:
                    del frontPage[k]
                    settings.saveData(frontPage, settings.FRONT_PAGE)
                    return False
            try:
                if "i.redd.it" in link or "i.imgur.com" in link:
                    pic = requests.get(link)
                    open("pic.jpg", "wb").write(pic.content)
                    status = f"{title}"
                    photo = api.media_upload("pic.jpg")
                    api.update_status(status, media_ids=[photo.media_id])
                    when = settings.printTime()
                    title = "<<< TWEET >>>"
                    result = "[ TWEET POSTED ]"
                    print(f"{when} {title} {result}")
                elif "twitter.com" in link:
                    api.update_status(link)
                    when = settings.printTime()
                    title = "<<< TWEET >>>"
                    result = "[ RE-TWEET ]"
                    print(f"{when} {title} {result}")
                else:
                    status = f"{title}\n{link}"
                    api.update_status(status)
                    when = settings.printTime()
                    title = "<<< TWEET >>>"
                    result = "[ TWEET POSTED ]"
                    print(f"{when} {title} {result}")
            except:
                when = settings.printTime()
                title = "<<< TWEET >>>"
                result = "[ FAILED ]"
                print(f"{when} Reddit {title} {result}")
                settings.pause(5)
                del frontPage[k]
                settings.saveData(frontPage, settings.FRONT_PAGE)
                return False

            del frontPage[k]
            settings.saveData(frontPage, settings.FRONT_PAGE)
            settings.pause(settings.LIMIT)
            break

def tweetHackerNews(api, limit):
    """
        Tweet Hacker News Data
    """
    frontPage = settings.openData(settings.HNFRONT_PAGE)
    frontPageLoop = settings.openData(settings.HNFRONT_PAGE)

    ignore = ["I ","my ","My ","ive ","I've ","we ","We "]

    if frontPage == {}:
        hackerNews.grabFrontPage(limit)
    else:
        for k in frontPageLoop:
            title = frontPageLoop[k]['title']
            link = frontPageLoop[k]['url']
            for i in ignore:
                if i in title:
                    del frontPage[k]
                    settings.saveData(frontPage, settings.HNFRONT_PAGE)
                    return False
            try:
                status = f"{title}\n{link}"
                api.update_status(status)
                when = settings.printTime()
                title = "<<< TWEET >>>"
                result = "[ TWEET POSTED ]"
                print(f"{when} {title} {result}")
            except:
                when = settings.printTime()
                title = "<<< TWEET >>>"
                result = "[ FAILED ]"
                print(f"{when} HackerNews {title} {result}")
                settings.pause(5)
                del frontPage[k]
                settings.saveData(frontPage, settings.HNFRONT_PAGE)
                return False

            del frontPage[k]
            settings.saveData(frontPage, settings.HNFRONT_PAGE)
            settings.pause(settings.LIMIT)
            break

def reTweet(api):
    """
        Re-Tweet HomeTimeline Tweet
    """
    me = api.me()

    tweets = api.home_timeline(count=1)

    for tweet in tweets:
        if tweet.retweeted != True and tweet.favorited != True and tweet.user.id != me.id:
            try:
                api.create_favorite(tweet.id)
            except tweepy.TweepError:
                print("Favorite Error")
            api.retweet(tweet.id)
            print("\n\t~ RETWEETED TWEET ~\n")
            settings.pause(settings.LIMIT)

def searchTweets(api):
    """
        Search & append to tweets list
    """
    q = random.choice(settings.QUERY)

    # search tweets
    tweet = api.search(q=q,lang="en",result_type="recent",count=1)

    return tweet

def tweetFavorite(api):
    """
        Search and Favorite Tweet
    """
    tweet = searchTweets(api)

    try:
        if tweet[-1].favorited != True:
            try:
                api.create_favorite(tweet[-1].id)
                print("\n\t~ FAVORITED TWEET ~\n")
                settings.pause(10)
            except (IndexError, tweepy.TweepError):
                print("Favorite Error Occured")
    except (IndexError, tweepy.TweepError):
        print("Favorite Error Occured")

def tweetFollow(api):
    """
        Search and Follow Tweet
    """
    tweet = searchTweets(api)

    try:
        if tweet[-1].user.following != True: 
            try:
                api.create_friendship(tweet[-1].user.id)
                friend = tweet[-1].user.id
                settings.saveDataTXT(friend, settings.NEW_FRIENDS)
                print("\n\t~ FRIENDSHIP CREATED ~\n")
                settings.pause(settings.LIMIT)
            except (IndexError, tweepy.TweepError):
                print("Friendship Error Occured")
    except (IndexError, tweepy.TweepError):
        print("Favorite Error Occured")

def tweetFavFollow(api):

    tweet = searchTweets(api)

    try:
        if tweet[-1].favorited != True:
            try:
                api.create_favorite(tweet[-1].id)
                when = settings.printTime()
                title = "<<< FAV >>>"
                result = "[ FAV ]"
                print(f"{when} {title} {result}")
                settings.pause(10)
            except (IndexError, tweepy.TweepError):
                when = settings.printTime()
                title = "<<< FAV >>>"
                result = "[ ERROR ]"
                print(f"{when} {title} {result}")
    except (IndexError, tweepy.TweepError):
        when = settings.printTime()
        title = "<<< FAV >>>"
        result = "[ ERROR ]"
        print(f"{when} {title} {result}")

    try:
        if tweet[-1].user.following != True: 
            try:
                api.create_friendship(tweet[-1].user.id)
                friend = tweet[-1].user.id
                settings.saveDataTXT(friend, settings.NEW_FRIENDS)
                when = settings.printTime()
                title = "<<< FOLLOW >>>"
                result = "[ FOLLOWED ]"
                print(f"{when} {title} {result}")
                settings.pause(settings.LIMIT)
            except (IndexError, tweepy.TweepError):
                when = settings.printTime()
                title = "<<< FOLLOW >>>"
                result = "[ ERROR ]"
                print(f"{when} {title} {result}")
                print("Friendship Error Occured")
    except (IndexError, tweepy.TweepError):
        when = settings.printTime()
        title = "<<< FOLLOW >>>"
        result = "[ ERROR ]"
        print(f"{when} {title} {result}")

def checkFollowers(api):
    """
        Check if following me, Unfollow if not
    """
    me = api.me()    

    data = settings.openDataTXT(settings.NEW_FRIENDS)

    fUnfollowed = 0
    nFollowedBack = 0
    
    print("Verifying Followed Profiles")
    for i in data:
        try:
            friend = api.show_friendship(source_id=me.id, target_id=i)
            if friend[0].followed_by != True:
                api.destroy_friendship(friend[1].id)
                settings.pause(3)
            else:
                nFollowedBack += 1
        except tweepy.TweepError:
            print("UnFriend Error")

    settings.deleteDataTXT(settings.NEW_FRIENDS)

    following = api.friends_ids()

    print("Verifying People I Follow")
    for i in following:
        try:
            friend = api.show_friendship(source_id=me.id, target_id=i)
            if friend[0].followed_by != True:
                api.destroy_friendship(friend[1].id)
                fUnfollowed += 1
                settings.pause(3)
        except tweepy.TweepError:
            print("UnFriend Error")

    print(f"Unfollowed Friends = {fUnfollowed}")
    print(f"New Friends = {nFollowedBack}")

def printHomeTimeline(api, count):
    """
        Print Twitter Home Timeline
    """
    try:
        tweets = api.home_timeline(count=count, tweet_mode="extended")

        for tweet in tweets:
            text = tweet.full_text
            name = tweet.user.name
            print(f"\n{text}")
            print(f"\n\t~ {name} ~")
    except tweepy.TweepError:
        print("Twitter Timeline Error")

