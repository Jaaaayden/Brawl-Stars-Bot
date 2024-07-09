from typing import Final, Optional
import os 
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message, app_commands
import brawling
from responses import get_response
import random

# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN') # key
BRAWL_TOKEN: Final[str] = os.getenv('BRAWL_TOKEN') 
# print(TOKEN)
# print(BRAWL_TOKEN)

# bot setup
intents: Intents = Intents.default()
intents.message_content = True #NOQA

client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

brawlClient = brawling.Client(BRAWL_TOKEN, proxy=True)


nuzlockeSetup: bool = False
brawlersList: list[str] = ["8-bit", "amber", "angelo", "ash", "barley", 
                           "bea", "belle", "berry", "bibi", "bo", "bonnie", "brock", 
                           "bull", "buster", "buzz", "byron", "carl", "charlie", 
                           "chester", "chuck", "collete", "colt", "cordelius", "crow", 
                           "darryl", "doug", "dynamike", "edgar", "el primo", "emz", "eve", 
                           "fang", "frank", "gale", "gene", "gray", "griff", "grom", "gus",
                           "hank", "jacky", "janet", "jessie", "kit", "larry & lawrie", "leon",
                           "lola", "lou", "maisie", "mandy", "max", "meg", "melody", "mico", "mortis",
                           "mr. p", "nani", "nita", "otis", "pam", "pearl", "penny", "piper",
                           "poco", "r-t", "sam", "sandy", "shelly", "spike", "sprout", "squeak",
                           "stu", "surge", "tara", "tick", "willow"]

# message func
async def send_message(message: Message, user_message: str, channel: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return
    # walrus operator, declaration in expression
    if is_private := user_message[0] == '?':
        user_message = user_message[1:] # slice 
    
    try:
        response: str = get_response(user_message, channel)
        if is_private:
            await message.author.send(response) # sends to dms
        else:
            await message.channel.send(response)
    except Exception as e: # bad practice but it works
        print(e) # use logging later
        
@client.event
async def on_ready() -> None:
    await tree.sync(guild=discord.Object(id=959967546021380177))
    print(f'{client.user} is now running!')
    
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message, channel)
    
@tree.command(name = "profile", description = "Fetches a Brawl Stars player's profile.", guild=discord.Object(id=959967546021380177))
async def profile(interaction, tag: Optional[str] = None, username: Optional[str] = None) -> None:
    if tag is not None:
        if tag[:1] != "#":
            tag = "#" + tag
        player = brawlClient.get_player(tag)
    if username is not None:
        with open('tag.txt', 'r') as file:
            for line in file:
                temp: list[str] = line.split("=")
                if temp[0] == username:
                    player = brawlClient.get_player(temp[1])
                    break
    print(player)
    embed = discord.Embed(
        title = f"{player.name} ({player.tag})",
        description = f"Trophies: 🏆 {player.highest_trophies}\nTeam Victories: 🗿🗿🗿 {player.victories_3v3}\nDuo Victories: 🤡🤡 {player.victories_duo}\nSolo Victories: 🔄 {player.victories_solo}",
        )
    await interaction.response.send_message(embed = embed)
    
@tree.command(name = "nuzlocke", description = "Randomly chooses n brawlers.", guild=discord.Object(id=959967546021380177))
async def nuzlocke(interaction, number_of_brawlers: int, hide_msg: bool, tag: Optional[str] = None, username: Optional[str] = None) -> None:
    if tag is not None:
        if tag[:1] != "#":
            tag = "#" + tag
        player = brawlClient.get_player(tag)
    if username is not None:
        with open('tag.txt', 'r') as file:
            for line in file:
                temp: list[str] = line.split("=")
                if temp[0] == username:
                    player = brawlClient.get_player(temp[1])
                    break

    brawlersInfo: list[object] = player.brawlers
    brawlersList: list[str] = []

    brawlers: str = ""
    
    for brawler in brawlersInfo:
        brawler: object = brawler
        name: str = brawler.name.lower()
        brawlersList.append(name)
    
    if (number_of_brawlers > len(brawlersList)):
        number_of_brawlers = len(brawlersList) 

    for i in range(number_of_brawlers):
        rand: int = random.randint(0, len(brawlersList)-1)
        brawlers += brawlersList[rand]
        if (i != number_of_brawlers - 1):
            brawlers += ", "
        brawlersList.pop(rand)

    embed = discord.Embed(
        title = f"Nuzlocke",
        description = f"Random Brawlers: {brawlers}"
        )
    await interaction.response.send_message(embed = embed, ephemeral = hide_msg)

@tree.command(name = "link", description = "Link a nickname to Brawl Stars tag.", guild=discord.Object(id=959967546021380177))
async def link(interaction, username: str, tag: str) -> None:
    if tag[:1] != "#":
        tag = "#" + tag
    with open("tag.txt", 'a') as file:
        file.write(username + "=" + tag + "\n")

    embed = discord.Embed(
        title = f"Account Link",
        description = f"{username} is now linked to {tag}"
        )
    await interaction.response.send_message(embed = embed)

"""
@tree.command(name = "team", description = "Creates teams based on total wins (separate players by spaces)", guild=discord.Object(id=959967546021380177))
async def team(interaction, players: str) -> None:
    playerList: list[str] = players.split(" ")
    playerTags: list[str] = []
    playerProfiles: list[object] = []
    winCounts: list[int] = []
    for player in playerList:
        with open('tag.txt', 'a') as file:
            for line in file:
                tagFound: bool = False
                temp: list[str] = line.split("-")
                if temp[0] == player:
                    playerTags.append(temp[1])
                    tagFound = True
                    break
"""

def main() -> None:
    client.run(token = TOKEN)
    
if __name__ == '__main__': # useful when calling
    main()