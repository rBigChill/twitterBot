import requests
import settings

def grabFrontPage(limit):
    # Make an API call, and store the response
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)

    # Process information about each submission
    submission_ids = r.json()
    frontPage = {} 

    i = 0

    for submission_id in submission_ids[:limit]:
        # Make a separate API call for each submission
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        r = requests.get(url)
        response_dict = r.json()

        # Build a dictionary for each article
        try:
            frontPage[i] = {
                "title": response_dict["title"],
                "url": response_dict["url"],
            }
            i += 1
        except KeyError:
            i += 1

    settings.saveData(frontPage, settings.HNFRONT_PAGE)

if __name__ == "__main__":
    grabFrontPage()
