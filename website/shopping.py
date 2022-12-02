import requests
import json

class Shopping:
    def __init__(self):
        self.API_KEY="de711d79731e559c2229268ef91800bdce6db2a1fd6961e05284070cd673775a"
        self.url="https://cloudapi.lykdat.com/v1/global/search"
    
    def shopping_results(self,image_url):
        url = self.url
        payload = {
            "api_key": self.API_KEY ,
            "image_url": self.image_url,
        }
        response = requests.post(url, data=payload)
        json_response = response.json()
        data = json_response["data"]
        result_groups = data["result_groups"][0]
        similar_products = result_groups["similar_products"]
        results=[]
        for product in similar_products:
            if(product["currency"]== "USD"):
                results.append(product)
        return results