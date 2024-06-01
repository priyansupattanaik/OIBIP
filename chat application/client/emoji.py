import emoji

def add_emoji(text):
    return emoji.emojize(text, use_aliases=True)
