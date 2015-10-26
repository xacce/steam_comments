# steam_comments
Simple comments parser from Steam community

# Install
    pip install steam_comments
    
    
# Usage:
    from steam_comments.post import Post
    url = "https://steamcommunity.com/groups/ns2rus/discussions/0/527273452871150509/"
    p = Post(url=url)
    print p.count_comments()
    
    for comment in p.comments():
        print comment
    # {'profile_url':'..', 'image_url'='..', 'text':'...', 'id'='..', 'author'='..'}
    
# Details
* profile_url - Absolute url to steam profile
* image_url - Absolute url to author avatar
* text - html code of  comment
* id - Steam id 
* author - Author of comment 
