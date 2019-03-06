import requests

artist = 'Modest_Mouse'
song = 'Jesus_Christ_Was_An_Only_Child'
apiOutURL = 'http://lyric-api.herokuapp.com/api/find/'
totalURL = apiOutURL + artist + '/' + song

response = requests.get(totalURL)
data = response.json()
print(data['lyric'])
