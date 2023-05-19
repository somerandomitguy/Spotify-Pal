import discord
import os
import spotipy.oauth2 as oauth2
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Load the environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_USERNAME = os.getenv('SPOTIFY_USERNAME')
SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')

# Initialize the Discord bot and Spotify client
bot = discord.Client()
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope='playlist-modify-private',
    username=SPOTIFY_USERNAME
))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!addsong'):
        # Get the song name and artist from the message content
        song_data = message.content.split(' ', 1)[1]
        song_name, song_artist = song_data.split(' by ', 1)

        # Search for the song on Spotify
        results = spotify.search(q=f'track:{song_name} artist:{song_artist}', type='track')

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']

            # Add the song to the Spotify playlist
            spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, SPOTIFY_PLAYLIST_ID, [track_uri])

            await message.channel.send('Song added to the Spotify playlist!')
        else:
            await message.channel.send('Song not found on Spotify.')

# Start the Discord bot
bot.run(TOKEN)