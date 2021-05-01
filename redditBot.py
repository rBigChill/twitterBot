import praw
import redditCreds as c
import settings

def loginToReddit():
    """
        Login to Reddit
    """
    reddit = praw.Reddit(
            client_id = c.CLIENT_ID,
            client_secret = c.CLIENT_SECRET,
            user_agent = c.USER_AGENT,
            username = c.USERNAME,
            password = c.PASSWORD,
            )
    #print(reddit.read_only)
    return reddit

def grabFrontPage(limit):
    """
        Saves Front Page Data
    """
    reddit = loginToReddit()

    frontPageData = {}

    i = 0

    for submission in reddit.front.hot(limit=limit):
        frontPageData[i] = {
            "title": submission.title,
            "sub": submission.subreddit.display_name,
            "url": submission.url,
                }
        i += 1

    settings.saveData(frontPageData, settings.FRONT_PAGE)
    
def printRedditData(limit):
    """
        Print Reddit Data
    """
    reddit = loginToReddit()

    data = {}

    i = 0

    try:
        for submission in reddit.front.hot(limit=limit):
            data[i] = {
                "title": submission.title,
                "sub": submission.subreddit.display_name,
                    }
            i += 1

        for info in data:
            title = data[info]['title']
            subreddit = data[info]['sub']
            print(f"\n{title}\n\n\tr/{subreddit}")
    except praw.exceptions as e:
        print(e)
