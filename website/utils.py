from defer import return_value
from google_images_search import GoogleImagesSearch
import requests

class WeatherConfig:
    def __init__(self):
        self.API_KEY = "9a00260af2814c1b8c1182732220310"

class WeatherAPI:
    def __init__(self) -> None:
        self.config = WeatherConfig()

    def getCurrentWeather(self, latitude=None, longitude=None, city = None):
        url = "http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no".format(city=city, API_KEY=self.config.API_KEY)
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code != 200:
            raise Exception("Weather API failed : response code : {code}".format(code = response.status_code))
        jsonResponse = response.json()
        if 'current' in jsonResponse and 'condition' in jsonResponse['current'] and 'text' in jsonResponse['current']['condition']:
            return jsonResponse['current']['condition']['text']
        return ''

class ImageConfig:
    def __init__(self) -> None:
        self.API_KEY = "AIzaSyDAm6ijCQKVo9w75JroZnU5nFMjI3SVP2Y"
        self.PROJ_CX = "525f979309bbd4a07"

class QueryBuilder:
    def __init__(self) -> None:
        pass

    def getQueryString(self, queries):
        return_query_string = ''
        for q in queries:
            return_query_string += q + ' '

        return "suggested dress for " + return_query_string

class SearchImages:
    def __init__(self) -> None:
        self.config = ImageConfig()
        self.gis = GoogleImagesSearch(self.config.API_KEY, self.config.PROJ_CX)
        self.default_num_of_records = 10
        self.query_builder = QueryBuilder()

    # gives the list of urls for a search
    def image_search(self, query_keywords, num_of_records = None):
        if not num_of_records:
            num_of_records = self.default_num_of_records

        query = self.query_builder.getQueryString(query_keywords)
        print ("Searchingy ", query)
        _search_params = {
            'q': query,
            'num' : num_of_records
        }
        self.gis.search(search_params=_search_params)

        image_urls = []
        for image in self.gis.results():
            image_urls.append(image.url)
        return image_urls