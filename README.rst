Chat bot for Livecoding.tv
--------

This is chat bot for Livecoding.tv that connect to chat via XMPP.
I create this bot from Ubuntu and all commands will work corectly only in Ubuntu.
Run bot with command:
    python3 errbot/err.py

Features
--------

- Notification when viewer join the stream or left it. (Desktop and chat notification)
- Greet and say goodbye to viewers with custom messages.
- Bot can ask viewers some questions when they join the room.
- Bot tell some custom text with custom interval.
- VIP users system.
- Full control with Stream music and song requests
- Voice messages via chat command

Commands
--------

!favorite_language
!favorite_framework
!favorite_ide
!favorite_viewer
!favorite_music
!streamingguide
!support
!newfeatures
!tools
!current task - What I`m doing now
!say [message] - Bot say your message
!uptime - Stream time
!viewers - List of viewers with their current online time
!vip list - List of VIP users

!song - Show current song name
!song next - Skip to next song (only VIP)
!song previous - Skip to previous song (only VIP)
!song search [query] - Show songs list by query
!song last - Show last song search
!song request [Number] - Add song from !song search to playlist
!song favorite - Songs list of songs that requested more than others

!ball8 - Ask question to magic 8 ball

Admin commands:
!song enable - Enable song request for all users
!song disable - Enable song request only for VIP users
!vip [add|remove] - Control of VIP users
!offline - Bot say goodbye for all viewers and make them offline

If you have any ideas write me a private message.

Prerequisites
--------

Python 3.3+

Ubuntu 14.04 or above

Spotify

Installation
--------

First you need to register new user in `Livecoding <https://livecoding.tv/>`.
Sign Up only with Email and Password.

**Bot configuration**
Edit file config.py:
    BOT_DATA_DIR and BOT_EXTRA_PLUGIN_DIR - paths to storage and plugins

    BOT_LOG_FILE - you can edit this line if you want

Next enter your bot username and password in BOT_IDENTITY

    BOT_ADMINS - list of bot admins usernames

    CHATROOM_PRESENCE - enter your chat room

    CHATROOM_FN - bot name

**Storage configuration**
Create file lctv.db with CHMOD 777 in storage folder.
Uncomment in the plugins/lctv_orm.py lines with:
    # db.connect()
    # db.create_tables([User, Songs, SongsSearch])
And run this file and then comment or delete this lines.
If you get error change path to lctv.db file in SqliteDatabase.

**Bot data**
    channel - your channel
    bot - your bot login
    owner - your username
    task - Your current task

**Custom messages**
If you want to add, edit or remove some custom messages edit next variables:
    new_visitors_online - Custom messages for greet new viewer
    visitors_online - Custom messages for greet old viewer
    donate_visitors_online - Custom messages for greet VIP viewer
    visitors_greets - Custom messages for bot when somebody say hello to bot
    visitors_offline - Custom messages when viewer left chat or when somebody say goodbye to bot
    visitors_questions - Custom questions that bot can ask to viewers
    simple_commands_messages - Answers to chat bot commands
    poller_messages_data - list of messages that bot say every 10 minutes (time you can change)

**Spotify**
- If you want to use !song commands you can create new App in https://developer.spotify.com/
- Create new playlist for song requests and get Playlist ID.

Then edit this code in /plugins/lctv.py: 

spotify_data = {
    'username': 'Your username',
    'playlist_id': 'Playlist ID',
    'token': '',
    'client_id': 'Client App ID',
    'client_secret': 'Client App Secret',
    'redirect_uri': 'http://localhost:8888/callback',
    'scope': 'playlist-modify-public'
}

**Support**
If you have any problems or ideas write me email at yaroslav@molchan.me
