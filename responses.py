from random import choice, randint

def get_response(user_input: str, channel: str) -> str:
    lowered: str = user_input.lower() # lowercase everything bc python is case-sensitive
    print(channel) 
    if lowered[:11]== "brawl stars":
        return "https://tenor.com/view/brawl-stars-nerd-cactus-morph-face-gif-26790147"
    elif lowered[:10] == "nah id win":
        return "https://tenor.com/view/nah-i%27d-win-gif-7220010602787901432"
    elif lowered[:4] == "i am":
        return "hi " + lowered[5:] +  " im justin"
    elif lowered[:3] == "i'm":
        return "hi " + lowered[4:] +  " im justin"
    elif lowered[:2] == "im":
        return "hi " + lowered[3:] +  " im justin"