class StoryBody():
    def __init__(self, key, headline, story_cat, story_region, author, story_date, story_details):
        self.key = key
        self.headline = headline
        self.story_cat = story_cat
        self.story_region = story_region
        self.author = author
        self.story_date = story_date
        self.story_details = story_details

class AuthorBody():
    def __init__(self, id, name, user, password):
        self.id = id
        self.name = name
        self.user = user
        self.password = password

class AuthorLoginBody():
    def __init__(self, username, password):
        self.user = username
        self.password = password