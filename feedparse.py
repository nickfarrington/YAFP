import feedparser,sys,urllib,os
feedparser.PREFERRED_XML_PARSERS.remove("drv_libxml2")

if sys.version[0] == "2":
    input = raw_input

def getInputFile():
    if os.name == "posix":
        path = os.path.expanduser("~") + "/.config/YAFP"

    if os.name == "nt":
        path = os.path.join(os.path.expanduser("~"), "Documents", "YAFP")

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(path, "feeds.txt")

def loadURLs():
    '''
    Opens an input file.
    Each entry in the file is formatted: "Title;url"
    '''
    INPUTFILE = getInputFile()
    try:
        o = open(INPUTFILE)
    except IOError:
        o = open(INPUTFILE,"a+")
    lines = o.readlines()
    o.close()
    feeds = {line.split(";")[0]:line.split(";")[1] for line in lines}
    return feeds

def downloadMedia(podcast,limit=10):
    sample = podcast['entries'][0]['links']
    key = None
    for i in range(len(sample)):
        if sample[i]['type'] == "audio/mpeg":
            key = i
            break

    for i in range(len(podcast['entries'])):
        if i == limit:
            break
        episode = podcast['entries'][i]
        url = episode['links'][key]['href']
        print(url)
        print("Downloading podcast {} of {}".format(i + 1,limit))
        urllib.urlretrieve(episode['links'][key]['href'],episode['title']+".mp3")
        print("Download complete.")

def displayTitles(feed, limit = 10):
    print('\n\n' + feed['feed']['title'] + '\n------------------------\n')
    for entry in feed['entries']:
        if limit == 0:
            break
        limit -= 1
        print(entry['title'])
    print("\n")

def openSubreddit(limit = 10,sub = None,output=displayTitles):
    """Similar to loadURLs but gets input directly from user.
    Defaults to displayTitles, but can use different output"""
    if sub == None:
        sub = input("Enter the name of a subreddit: /r/")
    url = "https://www.reddit.com/r/{}/.rss".format(sub)
    feed = feedparser.parse(url)
    return output(feed)

def addFeed(url = None, name = None):
    """Writes a feed to feeds.txt in the format specified in loadURLs"""
    f = open(getInputFile(),"a")
    if url == None or name == None:
        url = input("Please enter the URL of a new feed: ")
        name = input("Enter a nickname for this feed: ")
    f.write(name + ";" + url + "\n")
    f.close()

def removeFeed(name):
    """Removes a feed from feeds.txt"""
    f = open(getInputFile(),"r")
    newlines = []
    for line in f.readlines():
        if line.split(";")[0] != name:
            newlines.append(line)
    f.close()
    f = open(getInputFile(),"w")
    for line in newlines:
        f.write(line)

def browse():
    """Provides a CLI browsing mode for feedparse"""
    urls = loadURLs()
    l = []
    for title in urls.keys():
        print(str(len(l) + 1) + ": " + title)
        l.append(urls[title])
    key = int(input("Enter a number to go to the corresponding feed: "))
    displayTitles(feedparser.parse(l[key - 1]),limit=10)
        
def helpDownloadPodcast():
    url = input("Enter the URL of a podcast: ")
    feed = feedparser.parse(url)
    downloadMedia(feed)

def displayHelp():
    print("browse: Browse your feeds\nreddit: Open a subreddit\nadd: Add a new feed\nmedia: Load audio files from a podcast RSS")


if __name__ == "__main__":
    funcs = {"browse":browse,"reddit":openSubreddit,"add":addFeed,"media":helpDownloadPodcast,"help":displayHelp}
    if len(sys.argv) > 1:
        funcs[sys.argv[1]]()
    else:
        displayHelp()
