# import base64
#
# client_id = '18c20566374e4616852ae682dcbfefb2'
# client_secret = '2621aa5eb47e48b7b1100d6ec36ab9cb'
# # encoded = client_id + client_secret
# # print(encoded)
# # encoded = 'MThjMjA1NjYzNzRlNDYxNjg1MmFlNjgyZGNiZmVmYjI6MjYyMWFhNWViNDdlNDhiN2IxMTAwZDZlYzM2YWI5Y2I='
# #
# headers = {'Authorization': 'Basic ' + encoded}
# r = requests.post('https://accounts.spotify.com/api/token', data={"grant_type": "client_credentials"}, headers=headers)
# #
# print (r.status_code)
# print(r.json())
# print (r.headers['content-type'])
# import pprint
# import sys
#
#
#
# # username = 'yaroslavmolchan'
# # playlist_id = '035jXnlCKDBarNlL6Eb1ZS'
# # track_ids = ['spotify:track:1zHlj4dQ8ZAtrayhuDDmkY']
#
# # scope = 'playlist-modify-public'
# # token = util.prompt_for_user_token(username, scope)
# # token = 'BQD-UnGhsB0ekkvTmVpE1vRGXEbENTEd3aqJ2VcjulZ3rWJdKufI0vq3APzMBwFgK8tz_6k9Oh3T_Ois48JyVO3ZDP7ka8VNneovDRv1Iud--BTUigRoFyOfeEtFA3FCX60Ikc7ue78wwXI0gOyu2dZ_iXtMfPPjAW4qkvkoq_HpQksR4O0-hR4u1BobmFpJGYH01feU7HVqb1w3_WrXFjAdSuzWqhOaWZtScx9LpuJHDOjV0kMEBQIApR7-h2Xy6Kcu2vNiOhW10U613Xr3MML1OHFeTSbRmsmCtpIuBvw9-lcsQQ'
#
# # sp = spotipy.Spotify()
# # result = sp.search('Hello', limit=1)
# # pprint.pprint(result)
#
# # sp = spotipy.Spotify()
# #
# # results = sp.search(q='Hello', limit=20)
# # for i, t in enumerate(results['tracks']['items']):
# #     print (' ', i,t['id'], t['name'])
#
# # id = '1MDoll6jK4rrk2BcFRP5i7'
# # urn = 'spotify:track:' + id
# # sp = spotipy.Spotify()
# # try:
# #     track = sp.track(urn)
# #     pprint.pprint(track)
# # except:
# #     print("Error")
#
# #
# #     12:46sipmanThe you can have like top5 request list, least5 request list - stuff like that or lsit of requests last hour - then you can do some really coll stuff like, never the same song twice with in 1 hour or 2 hour or what ever...
# # 12:47jadsonYes you are right, i need store request history
# # 12:50sipmani see alot of potentiel in this, liek you can do vote wars, say you put 2 songs up again each other, and then the viewers will vote wich one is the best and then the song with the most votes gets palyed and the other one gets an penalty(cant be palyed for 2 days or whatnot) - that opens up for a whole new way of interacting with your listeners... And it will be really easy becuase the bot will handle it all..
#
#
#
# # import lctv_orm as orm
# #
# # orm.db.connect()
# # orm.db.create_tables([orm.SongRequests, orm.User])



# import requests
# import json
#
# code = 'BQAlZ8TVqHNnuEXHQ0QJ20s2bCmUSXyNVJnA87EQAbG8ls_UQfBf6uwARjV9laMW5sPXOS18UTcv_6cjIaWtILyWOge4EvvshC2ttXqSZYAMJ7MZFF8H03h96Q653KFXQye6-9YMhMBOLhGxLbYiXPSQwfzZeyT7kL2e03gE9oL-t2RxiKI2mSnOMP23xMhlB5UxXg'
# encoded = 'MThjMjA1NjYzNzRlNDYxNjg1MmFlNjgyZGNiZmVmYjI6MjYyMWFhNWViNDdlNDhiN2IxMTAwZDZlYzM2YWI5Y2I='
# headers = {'Authorization': 'Basic ' + encoded}
# data = {
#     "grant_type": "authorization_code",
#     "code": code,
#     "redirect_uri": "http://localhost:8888/callback"
# }
# r = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
#
# print (r.status_code)
# print(r.json())
# response = r.json()
# print(response['access_token'])
# print(response['refresh_token'])

import sys
# import spotipy
# import spotipy.util as util
#
# username = 'yaroslavmolchan'
# scope = 'playlist-modify-public'
# client_id = '18c20566374e4616852ae682dcbfefb2'
# client_secret = '2621aa5eb47e48b7b1100d6ec36ab9cb'
# redirect_uri = 'http://localhost:8888/callback'
#
# token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
# print(token)
# import subprocess
# import re
# output = subprocess.check_output("dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata'", shell=True)
# string = output.decode('unicode_escape')
# m = re.search('spotify:track:(.*?)\\n', string)
# id = m.group(0)[:-2]
# print(id)