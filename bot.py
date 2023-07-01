import requests
from bs4 import BeautifulSoup
import time
import re
import urllib.parse
from discordwebhook import Discord

# Discord webhook URL
discord = Discord(url="REPLACE WITH YOUR WEBHOOK")
# The last commit id we've seen
last_commit_id = None

while True:
    # Request the page
    response = requests.get('https://commits.facepunch.com/r/rust_reboot')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first commit
    commit = soup.find('div', class_='commit columns')

    # Extract the commit id
    commit_id = commit.find('span', class_='changeset').text
    print(commit.find('span', class_='changeset').text)
    # If this is a new commit
    if commit_id != last_commit_id:
        # Update the last commit id
        last_commit_id = commit_id

        # Extract the commit details
        author = commit.find('div', class_='author').text
        repo = commit.find('span', class_='repo').text
        branch = commit.find('span', class_='branch').text
        changeset = commit.find('span', class_='changeset').text
        commit_message = commit.find('div', class_='commits-message').text
        avatar = commit.find('div', class_='avatar').fetchNextSiblings
        avtr = re.search("(?P<url>https?://[^\s]+)", str(avatar)).group("url")[:-3]

        # Create the message
        # Send the message to the Discord webhook
        discord.post(
            embeds=[
                {
                    "author": {
                        "name": str(author),
                        "url": "https://commits.facepunch.com/r/rust_reboot"
                    },
                    "title": str(repo)+str(branch)+str(changeset),
                    "description": str(commit_message),
                    "thumbnail": {"url": str(avtr)}
                    
                }
            ],
        )
        # Send the message to the Discord webhook

    # Wait for 50 seconds
    time.sleep(50)