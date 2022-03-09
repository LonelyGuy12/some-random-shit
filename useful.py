from io import BytesIO
import os
import json
import aiohttp
import requests

class get:
    def get(self, url, content_type = None):
        url = str(url)
        try:
            resp = requests.get(url)
            try:
                res = resp.json()
            except:
                res = resp.content
            return str(res)
        except:
            raise TimeoutError

    def genius_lyrics(self, query, api_key):
        query = str(query)
        api_key = str(api_key)
        try:
            url = "https://api.genius.com/search?access_token=" + api_key + "&q=" + query.replace("&",
                                                                                                  "and").replace(
                "by", "-").replace(" ", "%20")
            details = urllib.request.urlopen(url).read().decode()
            json_results = json.loads(details)

            title = str(json_results["response"]["hits"][0]["result"]["title"])
            artist = str(json_results["response"]["hits"][0]["result"]["primary_artist"]["name"])
            genius_url = str(json_results["response"]["hits"][0]["result"]["url"])
            url1 = genius_url
            r = requests.get(url1)
            htmlcontent = r.content
            html_content = BeautifulSoup(htmlcontent.decode("utf-8").replace("<br/>", "\n"), "html.parser")

            lyrics = str(html_content.find("div", class_=re.compile("^lyrics$|Lyrics__Root")).get_text())
            lyrics = re.sub(r"(\[.*?])*", "", lyrics).replace("\n\n", "\n")

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = "Genius"  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = api_key  # API Key provided by the user
            self.url = url1
        except:
            raise TimeoutError

    def musixmatch_lyrics(self, query):
        query = str(query)
        try:
            url = 'https://www.musixmatch.com/search/' + query.replace(" ", "%20")  # +'/lyrics'
            http = urllib3.PoolManager(ca_certs=certifi.where())
            resp = http.request('GET', url)
            r = resp.data.decode('utf-8')
            html_content = BeautifulSoup(r, "html.parser")
            href = str(html_content.find("a", class_="title")).split("href=")[1].split('''"''')[1]
            new_link = "https://www.musixmatch.com/" + href
            http = urllib3.PoolManager(ca_certs=certifi.where())
            url = new_link
            resp = http.request('GET', url)
            r = resp.data.decode('utf-8')
            html_content = BeautifulSoup(r, "html.parser")

            artist = str(html_content.find("a", class_="mxm-track-title__artist mxm-track-title__artist-link"))
            artist = re.sub(r"(<.*?>)*", "", artist)

            title = str(html_content.find("h1", class_="mxm-track-title__track").getText("//")).split("//")[-1]
            title = re.sub(r"(<.*?>)*", "", title)

            lyrics = html_content.findAll("span", class_="lyrics__content__ok")
            lyrics = str(lyrics[0]) + "\n" + str(lyrics[1])
            lyrics = re.sub(r"(<.*?>)*", "", lyrics)

            self.title = title  # Name of the track
            self.artist = artist  # Name of the artist
            self.lyrics = lyrics  # Lyrics of the track
            self.source = "Musixmatch"  # Source of the lyrics
            self.query = query  # Query requested by the user
            self.api_key = None  # API Key provided by the user
            self.url = new_link
        except:
            raise TimeoutError