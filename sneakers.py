import requests
import discord
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

source = requests.get('https://sneakernews.com/release-dates/').text

soup = BeautifulSoup(source, 'lxml')

release_section = soup.find('div', {'class': 'sneaker-con-main'})

releases = release_section.findAll('div', {'class': 'releases-box'})

cleaned_releases = []

for release in releases:
    image = release.find('img', {'alt': 'Release page image'})
    h2 = release.find('h2')
    if not image:
        continue
    cleaned_releases.append({
        'page': h2.find('a')['href'],
        'image_url': image['src'],
        'release_date': release.find('span', {'class': 'release-date'}).text.strip() or 'n/a',
        'name': h2.text.strip(),
        'price': release.find('span', {'class': 'release-price'}).text.strip(),
        'color': release.find('div', {'class': 'post-data'}).findAll('p')[1].text.strip().split(':')[1]
    })

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to Discord')

@client.event
async def on_message(message):
    for shoe in cleaned_releases:
        if message.content == 'lil sneaker bby':
            embed = discord.Embed(title=shoe['name'], description=shoe['color'], url=shoe['page'])
            embed.set_image(url=shoe['image_url'])
            await message.channel.send('-------------------')
            await message.channel.send(embed=embed)
            await message.channel.send('Releases on ' + shoe['release_date'] + ' for ' + shoe['price'])

client.run(TOKEN)
