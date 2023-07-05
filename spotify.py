@bot.command()
async def listening(ctx):
    # Authenticate and get access token
    auth_url = sp_oauth.get_authorize_url()
    await ctx.send(f'Please visit the following URL and authorize the bot: {auth_url}')
    response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    code = response.content.strip()
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info['access_token']

    # Set up Spotify API client
    sp = spotipy.Spotify(auth=access_token)

    # Get the user's current playback information
    current_track = sp.current_user_playing_track()
    if current_track is not None:
        track_name = current_track['item']['name']
        artists = [artist['name'] for artist in current_track['item']['artists']]
        artist_names = ', '.join(artists)
        await ctx.send(f'Currently listening to: {track_name} by {artist_names}')
    else:
        await ctx.send('Not currently listening to anything.')
