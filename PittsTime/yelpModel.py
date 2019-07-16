import requests

API_KEY = 'Dte0PqwjN_DoyR79RZeDIeTY4jlP-YMiQMg2sLd0VezZqu94XM6tdAIbLorBX8pQAAFT6vih1oY4gI3OVC1C6shIPfQVVoQ1T6HI8FaVKQtIndovD0zMFALjFqO8XHYx'


def Get_Info(term, location):
    # What you are searching for
    SEARCH_TERM = term
    # Business location
    SEARCH_LOCATION = location
    # Maximum number of results to return
    SEARCH_LIMIT = 1

    # Busines search end point
    url = 'https://api.yelp.com/v3/businesses/search'
    # Heahder should contain the API key
    headers = {'Authorization': 'Bearer {}'.format(API_KEY)}
    # Search parameters
    url_params = {
        'term': SEARCH_TERM,
        'location': SEARCH_LOCATION,
        'limit': SEARCH_LIMIT
    }

    # Call the API
    response = requests.request('GET', url, headers=headers, params=url_params)

    # To get a better understanding of the structure of
    # the returned JSON object refer to the documentation
    # For each business, print name, rating, location and phone
    info = {}
    try:
        for business in response.json()["businesses"]:
            info['name'] = business['name']
            info['rating'] = business['rating']
            info['location'] = business["location"]["display_address"][0]
            info['phone'] = business["display_phone"]
            try:
                info['price'] = business['price']
            except:
                info['price'] = 'Not found'
            info['image'] = business['image_url']
        # print("{:30}  {:5}  {:20}  {:10} {:30} {:30}".format(
        #     business["name"],
        #     business["rating"],
        #     business["location"]["display_address"][0],
        #     business['price'],
        #     business['image_url'],
        #     business["display_phone"]))
    except:
        info = None
    return info

# Get_Info('Acorn', 'Acorn, Walnut Street, Pittsburgh, PA, USA')