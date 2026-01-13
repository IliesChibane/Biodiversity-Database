import requests

def get_images(key):
    limit = 3
    images_response = requests.get(f"https://api.gbif.org/v1/occurrence/search?taxonKey={key}&mediaType=StillImage&limit={limit}")
    if images_response.status_code == 200:
        images_data = images_response.json()
        if 'results' in images_data and images_data['results']:
            #print(f"Found {len(images_data['results'])} images for species: {key}")
            for result in images_data['results']:
                if 'media' in result:
                    image_url = []
                    for media in result['media']:
                        if 'identifier' in media:
                            #print(f"Species: {key}, Image URL: {media['identifier']}")
                            image_url.append(media['identifier'])
                    return image_url
    return []
                            
                            
get_images(2480537)