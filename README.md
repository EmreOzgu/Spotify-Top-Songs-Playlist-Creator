# Spotify-Top-Songs-Playlist-Creator
This is a simple Python script to create a playlist of the top 25th percentile of most popular songs (decided by the 'popularity' rating provided by the Spotify API) on Spotify for songs that revolve around a keyword. (like Star Wars, World of Warcraft, Lord of the Rings, etc.)

Update (6/20/2018): 
   - Can now choose to skip recent songs (within last 2 months)
   - Skips (most) duplicate songs.
   
# Setup
The script requires the installation of the Spotipy library. (See [here](https://github.com/plamere/spotipy) for installation)

It also requires users to register this application through their Spotify account.
This can be done by following the steps [here.](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app)
A redirect URI should be set from Edit Settings at [My Dashboard.](https://developer.spotify.com/dashboard/applications)
The redirect URI can be any website, simplest is http://localhost/.

Once you have the Client ID, Client Secret, and Redirect URI you can either:
1. Type in these commands in the command line:
   - export SPOTIPY_CLIENT_ID=your-spotify-client-id
   - export SPOTIPY_CLIENT_SECRET=your-spotify-client-secret
   - export SPOTIPY_REDIRECT_URI=your-app-redirect-url
   
2. Change util.prompt_for_user_token(username, scope) in the source code, to util.prompt_for_user_token(username,scope,client_id='your-app-redirect-url',client_secret='your-app-redirect-url',redirect_uri='your-app-redirect-url')
(All of these arguments are string arguments)
