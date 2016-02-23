#Client ID 					826271aed029ec881f66f94611ea39db
#Client Secret 				0f1d9ee50c7a451216be87db205d6f2d
#Scrimshaw's ID 			8703641
#End User Authorization		https://soundcloud.com/connect
#Token						https://api.soundcloud.com/oauth2/token

import soundcloud as sc

#Can add username & password field for authentication to specific members
client = sc.Client(client_id = '826271aed029ec881f66f94611ea39db',
							client_secret = '0f1d9ee50c7a451216be87db205d6f2d')

#print (client.get('/me').username) 	Restricted without member login information
#users = client.get('/users', q = 'Scrimshaw', country = 'Canada')
#for user in users:
#	print ("%d %s %s %s", (user.id, user.username, user.country, user.permalink))


likes = client.get('users/8703641/favorites', limit=200)
for liked in likes:
	try:
		print (liked.title)
	except UnicodeEncodeError as e: #Catches error thrown by special characters
		print("Error: %s", e)

#tracks = client.get('/tracks', limit = 10)
#for track in tracks:
#	print (track.title)
#app = client.get('/apps/124')
#print (app.permalink_url)

#tracks = client.get('/resolve', url="https://soundcloud.com/dj-scrimshaw/likes")
#for track in tracks:
	#print(track.id)
	#print(tracks)

#Track data
'''
{
  "id": 13158665,
  "created_at": "2011/04/06 15:37:43 +0000",
  "user_id": 3699101,
  "duration": 18109,
  "commentable": true,
  "state": "finished",
  "sharing": "public",
  "tag_list": "soundcloud:source=iphone-record",
  "permalink": "munching-at-tiannas-house",
  "description": null,
  "streamable": true,
  "downloadable": true,
  "genre": null,
  "release": null,
  "purchase_url": null,
  "label_id": null,
  "label_name": null,
  "isrc": null,
  "video_url": null,
  "track_type": "recording",
  "key_signature": null,
  "bpm": null,
  "title": "Munching at Tiannas house",
  "release_year": null,
  "release_month": null,
  "release_day": null,
  "original_format": "m4a",
  "original_content_size": 10211857,
  "license": "all-rights-reserved",
  "uri": "http://api.soundcloud.com/tracks/13158665",
  "permalink_url": "http://soundcloud.com/user2835985/munching-at-tiannas-house",
  "artwork_url": null,
  "waveform_url": "http://w1.sndcdn.com/fxguEjG4ax6B_m.png",
  "user": {
    "id": 3699101,
    "permalink": "user2835985",
    "username": "user2835985",
    "uri": "http://api.soundcloud.com/users/3699101",
    "permalink_url": "http://soundcloud.com/user2835985",
    "avatar_url": "http://a1.sndcdn.com/images/default_avatar_large.png?142a848"
  },
  "stream_url": "http://api.soundcloud.com/tracks/13158665/stream",
  "download_url": "http://api.soundcloud.com/tracks/13158665/download",
  "playback_count": 0,
  "download_count": 0,
  "favoritings_count": 0,
  "comment_count": 0,
  "created_with": {
    "id": 124,
    "name": "SoundCloud iPhone",
    "uri": "http://api.soundcloud.com/apps/124",
    "permalink_url": "http://soundcloud.com/apps/iphone"
  },
  "attachments_uri": "http://api.soundcloud.com/tracks/13158665/attachments"
}'''