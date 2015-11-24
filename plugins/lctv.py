from errbot import BotPlugin, botcmd, re_botcmd, arg_botcmd
import spotipy
import spotipy.util as util
import lctv_orm as orm
import random
import subprocess
import re
from time import sleep
from datetime import datetime
from errbot.utils import format_timedelta


class LCTV(BotPlugin):

    channel = 'jadson@chat.livecoding.tv'
    bot = 'LCTV'
    owner = 'jadson'
    task = 'Working'
    # if 0 - enable for all users
    # if 1 - enable only for donators
    song_request_status = 0

    spotify_data = {
        'username': 'yaroslavmolchan',
        'playlist_id': 'playlist_id',
        'token': '',
        'client_id': 'client_id',
        'client_secret': 'client_secret',
        'redirect_uri': 'http://localhost:8888/callback',
        'scope' : 'playlist-modify-public'
    }

    new_visitors_online = [
        "Hey @%s – welcome.",
        "We have a new visitor %s",
        "Hello @%s!"
    ]

    visitors_online = [
        "%s is back!",
        "Hello @%s!",
        "%s is here again!"
    ]

    visitors_questions = [
        "@%s, have you built any project like this before?",
        "Where are you from @%s?",
        "What brings you here today @%s?",
        "How are you @%s?"
    ]

    donate_visitors_online = [
        "VIP %s is in da house!"
    ]

    visitors_offline = [
        "Goodbye @%s",
        "See you later @%s",
        "@%s come back soon"
    ]

    visitors_greets = [
        "Hello @%s",
        "Hey @%s"
    ]

    simple_commands_messages = {
        'current_task': task,
        'favorite_language': 'PHP',
        'favorite_framework': 'Yii',
        'favorite_ide': 'PhpStorm',
        'favorite_music': 'ASOT',
        'streamingguide': ['Livecoding.tv streaming guide for Mac, Windows and Linux is here:', 'https://www.livecoding.tv/streamingguide/'],
        'support': 'Livecoding.tv support page is here: http://support.livecoding.tv/hc/en-us/',
        'newfeatures': ['Here is a list of new features Livecoding.tv released:', '1. Hire a Streamer & Pay', '2. Reddit stream announcement'],
        'tools': 'JetBrains Tools and Spotify'
    }

    poller_messages_data = [
        "My current task: " + task,
        "If you have any ideas about a bot write me a private message.",
        "Donate and you get VIP status and may control Stream sound"
    ]

    def activate(self):
        super(LCTV, self).activate()

        orm.db.connect()
        # every 55 min update spotify tokens
        self.start_poller(55 * 60, self.spotify_refresh)
        # every 10 min tell any messages (task or adv)
        self.start_poller(10 * 60, self.poller_message)

    def poller_message(self):
        message = random.choice(self.poller_messages_data)
        self.send(
            self.channel,
            message,
            message_type="groupchat"
        )

    def spotify_refresh(self):
        token = util.prompt_for_user_token(self.spotify_data['username'], self.spotify_data['scope'], self.spotify_data['client_id'], self.spotify_data['client_secret'], self.spotify_data['redirect_uri'])
        if token:
            self.spotify_data['token'] = token
        else:
            self.send(
                self.channel,
                "Can't get token",
                message_type="groupchat"
            )

    def callback_room_joined(self, room):
        self.send(
            self.channel,
            "I am in action!",
            message_type="groupchat"
        )

        token = util.prompt_for_user_token(self.spotify_data['username'], self.spotify_data['scope'], self.spotify_data['client_id'], self.spotify_data['client_secret'], self.spotify_data['redirect_uri'])
        if token:
            self.spotify_data['token'] = token
        else:
            self.send(
                self.channel,
                "Something wrong with Spotify",
                message_type="groupchat"
            )

    def callback_presence(self, presence):
        # greets visitors
        if presence.nick not in [None, self.bot, self.owner] and presence.status is 'online':
            try:
                user = orm.User.get(orm.User.username == presence.nick)
                user.is_online = True
                user.views += 1
                user.save()
                if user.views > 2:
                    is_vip = orm.User.select().where(
                        (orm.User.username == presence.nick) & (orm.User.is_vip == True)
                    ).count()
                    if is_vip:
                        message = random.choice(self.donate_visitors_online)
                    else:
                        message = random.choice(self.visitors_online)
                    self.send(
                        self.channel,
                        message % presence.nick,
                        message_type="groupchat"
                    )
            except orm.User.DoesNotExist:
                orm.User.create(username=presence.nick)
                message = random.choice(self.new_visitors_online)
                self.send(
                    self.channel,
                    message % presence.nick,
                    message_type="groupchat"
                )
            subprocess.Popen(['notify-send', self.bot, presence.nick + " join the chat"])

            # with chance 50% add some questions for visitors
            if random.randint(1, 100) > 50:
                sleep(2)
                message = random.choice(self.visitors_questions)
                self.send(
                    self.channel,
                    message % presence.nick,
                    message_type="groupchat"
                )
        elif presence.nick not in [None, self.bot, self.owner] and presence.status is 'offline':
            user = orm.User.get(orm.User.username == presence.nick)
            user.is_online = False
            user.save()
            message = random.choice(self.visitors_offline)
            self.send(
                self.channel,
                message % presence.nick,
                message_type="groupchat"
            )
            subprocess.Popen(['notify-send', self.bot, presence.nick + " left the chat"])

    def callback_message(self, msg):
        # TODO: create with re module matching
        # TODO: Add more words
        # if msg.body.find(self.bot) != -1:
        #     self.send(
        #         self.channel,
        #         "Who calling me?",
        #         message_type="groupchat"
        #     )
        pass

    @re_botcmd(pattern=r"(^| )([Gg]oodbye|bb|bye-bye|[Bb]ye)( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_leave(self, msg, match):
        if msg.nick not in [self.bot] and (msg.body.find(self.bot) != -1 or msg.body.find(self.owner) != -1):
            message = random.choice(self.visitors_offline)
            yield message % msg.nick

    @re_botcmd(pattern=r"(^| )([Hh]ello|[Hh]i|[Hh]allo|[Hh]ey)( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_greet(self, msg, match):
        if msg.nick not in [self.bot] and (msg.body.find(self.bot) != -1 or msg.body.find(self.owner) != -1):
            message = random.choice(self.visitors_greets)
            yield message % msg.nick

    # some commands
    simple_commands_string = '|'.join(simple_commands_messages)

    @re_botcmd(pattern=r"^(" + simple_commands_string + ")")
    def tools(self, msg, args):
        # get command name
        command = msg.body[1:]
        # find answer in array
        answer = self.simple_commands_messages[command]
        # if answer is array then return all messages in answer, else answer is string return it
        if isinstance(answer, list):
            for message in answer:
                yield message
        else:
            yield answer

    @botcmd()
    def favorite_viewer(self, msg, args):
        try:
            user = orm.User.select().order_by(orm.User.views.desc()).get()
            self.send(
                self.channel,
                user.username + " (" + str(user.views) + " times)",
                message_type="groupchat"
            )
        except orm.User.DoesNotExist:
            self.send(
                self.channel,
                "Nobody :(",
                message_type="groupchat"
            )

    @botcmd()
    def song_favorite(self, msg, args):
        if orm.Songs.select().count() > 0:
            search_list = orm.Songs.select().order_by(orm.Songs.requests.desc()).limit(5)
            self.send(
                self.channel,
                "TOP 5 requested songs",
                message_type="groupchat"
            )
            for i, search in enumerate(search_list):
                sp = spotipy.Spotify()
                track = sp.track(search.id)
                artists = []
                for artist in track['artists']:
                    artists.append(artist['name'])
                artists_str = ', '.join(artists)
                self.send(
                    self.channel,
                    str(i) + ". " + artists_str + " - " + track['name'] + " (" + str(search.requests) + " times)",
                    message_type="groupchat"
                )
        else:
            self.send(
                self.channel,
                "List is empty",
                message_type="groupchat"
            )

    @botcmd()
    def song(self, msg, args):
        output = subprocess.check_output("dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata'", shell=True)
        string = output.decode('unicode_escape')
        m = re.search('spotify:track:(.*?)\\n', string)
        id = m.group(0)[:-2]
        urn = 'spotify:track:' + id
        sp = spotipy.Spotify()
        track = sp.track(urn)
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
        artists_str = ', '.join(artists)
        yield artists_str + " - " + track["name"]

    @botcmd()
    def song_enable(self, msg, args):
        if msg.nick == self.owner and self.song_request_status == 1:
            self.song_request_status = 0
            yield "Song request enable for all viewers"

    @botcmd()
    def song_disable(self, msg, args):
        if msg.nick == self.owner and self.song_request_status == 0:
            self.song_request_status = 1
            yield "Song request enable only for VIP viewers"

    @botcmd()
    def song_search(self, msg, args):
        is_vip = orm.User.select().where(
            (orm.User.username == msg.nick) & (orm.User.is_vip == True)
        ).count()
        if self.song_request_status == 1 and is_vip == 0 and msg.nick != self.owner:
            yield "You are not a VIP user"
            return

        if len(args) == 0:
            yield "Type song name like !song search [Song name]"
        else:
            sp = spotipy.Spotify()
            results = sp.search(args, limit=10)
            if results['tracks']['total'] > 0:
                orm.SongsSearch.create(username=msg.nick, requested_name=args, requested_limit=10)
                yield "@" + msg.nick + ": Please choose your song and type !song request [Number of song]"
                for i, t in enumerate(results['tracks']['items']):
                    number = i+1
                    artists = []
                    for artist in t['artists']:
                        artists.append(artist['name'])
                    artists_str = ', '.join(artists)
                    message = str(number) + ": " + artists_str + ": " + t['name']
                    yield message
            else:
                yield "No results found"

    @botcmd()
    def song_last(self, msg, args):
        request = orm.SongsSearch.select().order_by(orm.SongsSearch.created_at.desc()).get()
        sp = spotipy.Spotify()
        results = sp.search(request.requested_name, limit=request.requested_limit)
        if results['tracks']['total'] > 0:
            yield "@" + msg.nick + ": Please choose your song and type !song request [Number of song]"
            for i, t in enumerate(results['tracks']['items']):
                number = i+1
                artists = []
                for artist in t['artists']:
                    artists.append(artist['name'])
                artists_str = ', '.join(artists)
                message = str(number) + ": " + artists_str + ": " + t['name']
                yield message

    @arg_botcmd('number', type=int, default=1)
    def song_request(self, msg, number):
        is_vip = orm.User.select().where(
            (orm.User.username == msg.nick) & (orm.User.is_vip == True)
        ).count()
        if self.song_request_status == 1 and is_vip == 0 and msg.nick != self.owner:
            yield "You are not a VIP user"
            return

        request = orm.SongsSearch.select().order_by(orm.SongsSearch.created_at.desc()).get()
        number = int(number) - 1
        sp = spotipy.Spotify()
        result = sp.search(request.requested_name, limit=request.requested_limit)
        urn = 'spotify:track:' + result['tracks']['items'][number]['id']
        sp = spotipy.Spotify()
        track = sp.track(urn)
        username = self.spotify_data['username']
        playlist_id = self.spotify_data['playlist_id']
        track_ids = [urn]
        sp = spotipy.Spotify(auth=self.spotify_data['token'])
        sp.trace = False
        sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        artists = []
        for artist in track['artists']:
            artists.append(artist['name'])
        artists_str = ', '.join(artists)
        try:
            user = orm.Songs.get(orm.Songs.id == urn)
            user.requests += 1
            user.save()
        except orm.Songs.DoesNotExist:
            orm.Songs.create(id=urn, artist=artists_str, name=track['name'])
        title = "New song request by " + msg.nick
        message = artists_str + " - " + track['name']
        subprocess.Popen(['notify-send', title, message])
        yield "@" + msg.nick + " add song \"" + artists_str + " - " + track['name'] + "\" to playlist"

    @botcmd()
    def song_next(self, msg, args):
        is_vip = orm.User.select().where(
            (orm.User.username == msg.nick) & (orm.User.is_vip == True)
        ).count()
        if msg.nick == self.owner or is_vip:
            subprocess.call(["./spotify-remote.sh", "next"])
            return
        else:
            yield "@ " + msg.nick + " this command only for VIP users"

    @botcmd()
    def song_previous(self, msg, args):
        is_vip = orm.User.select().where(
            (orm.User.username == msg.nick) & (orm.User.is_vip == True)
        ).count()
        if msg.nick == self.owner or is_vip:
            # skip to the track start
            subprocess.call(["./spotify-remote.sh", "previous"])
            # skip to previous track
            subprocess.call(["./spotify-remote.sh", "previous"])
            return
        else:
            yield "@ " + msg.nick + " this command only for VIP users"

    @botcmd()
    def ball8(self, msg, args):
        if len(args) == 0:
            yield "Ask me a question like !ball8 [Question]"
        else:
            answers = [
                "It is certain",
                "It is decidedly so",
                "Outlook good",
                "You may rely on it",
                "Ask again later",
                "Concentrate and ask again",
                "Reply hazy, try again",
                "My reply is no",
                "My sources say no"
            ]

            self.send(
                self.channel,
                random.choice(answers),
                message_type="groupchat"
            )

    @botcmd()
    def say(self, msg, args):
        subprocess.call(["espeak", args, "-s 100"])
        return

    @botcmd()
    def vip_list(self, msg, args):
        if orm.User.select().where(orm.User.is_vip == True).count() > 0:
            vip_list = orm.User.select().where(orm.User.is_vip == True).order_by(orm.User.views.desc())
            self.send(
                self.channel,
                "List of VIP users",
                message_type="groupchat"
            )
            for i, user in enumerate(vip_list):
                self.send(
                    self.channel,
                    str(i) + ". " + user.username + " (" + str(user.views) + " times)",
                    message_type="groupchat"
                )
        else:
            self.send(
                self.channel,
                "List is empty",
                message_type="groupchat"
            )

    @botcmd()
    def vip_add(self, msg, args):
        if msg.nick == self.owner:
            try:
                user = orm.User.get(orm.User.username == args)
                user.is_vip = True
                user.save()
                self.send(
                    self.channel,
                    "We have new VIP - %s" % args,
                    message_type="groupchat"
                )
            except orm.User.DoesNotExist:
                self.send(
                    self.channel,
                    "%s is not your viewer" % args,
                    message_type="groupchat"
                )
            return
        else:
            yield "@ " + msg.nick + " this command only for " + self.owner

    @botcmd()
    def vip_remove(self, msg, args):
        if msg.nick == self.owner:
            try:
                user = orm.User.get(orm.User.username == args)
                user.is_vip = False
                user.save()
                self.send(
                    self.channel,
                    "%s no longer VIP" % args,
                    message_type="groupchat"
                )
            except orm.User.DoesNotExist:
                self.send(
                    self.channel,
                    "%s is not your viewer" % args,
                    message_type="groupchat"
                )
            return
        else:
            yield "@ " + msg.nick + " this command only for " + self.owner

    @botcmd()
    def viewers(self, msg, args):
        if orm.User.select().where(orm.User.is_online == True).count() > 0:
            online_list = orm.User.select().where(orm.User.is_online == True).order_by(orm.User.updated_at.asc())
            for i, user in enumerate(online_list):
                self.send(
                    self.channel,
                    str(i) + ". " + user.username + " (%s %s)" % (args, format_timedelta(datetime.now() - user.updated_at)),
                    message_type="groupchat"
                )
        else:
            self.send(
                self.channel,
                "List is empty",
                message_type="groupchat"
            )
        return

    @botcmd()
    def offline(self, msg, args):
        if msg.nick == self.owner:
            try:
                online_list = orm.User.select().where(orm.User.is_online == True).order_by(orm.User.views.desc())
                for i, user in enumerate(online_list):
                    message = random.choice(self.visitors_offline)
                    self.send(
                        self.channel,
                        message % user.username,
                        message_type="groupchat"
                    )
                    user.is_online = False
                    user.save()
                self.send(
                    self.channel,
                    "Follow to my channel and see you next time :good:",
                    message_type="groupchat"
                )
            except orm.User.DoesNotExist:
                self.send(
                    self.channel,
                    "List is empty",
                    message_type="groupchat"
                )
            return
        else:
            yield "@ " + msg.nick + " this command only for " + self.owner