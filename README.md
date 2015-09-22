# steam_comments
Simple comments parser from Steam community

# Requirements
```pip install beautifulsoup4```
```pip install requests```

# Usage:
    url = "https://steamcommunity.com/groups/ns2rus/discussions/0/527273452871150509/"
    p = Post(url=url)
    print p.count_comments()
    
    for comment in p.comments():
        print comment
    
