import configparser
import facebook
import pprint
import requests

from collections import defaultdict

config = configparser.ConfigParser()
config.read('config.conf')

ACCESS_TOKEN = config.get('facebook', 'TOKEN')

graph = facebook.GraphAPI(access_token=ACCESS_TOKEN, version='2.5')

photos_args = {'fields':
                'likes'}

like_counts = defaultdict(int)
shutter_count = 0

def count_likes(likes):
    for like in likes['data']:
        like_counts[like['name']] += 1

    try:
        count_likes(get_next(likes['paging']['next']))
    except KeyError:
        pass



def count_likes_in_photos(photos):
    global shutter_count
    for photo in photos['data']:
        shutter_count += 1
        try:
            likes = photo['likes']
            count_likes(likes)
        except KeyError:
            pass


def get_next(url):
    return requests.get(url).json()


def main():
    photos = graph.get_connections(id='me',
                                   connection_name='photos',
                                   **photos_args)

    count_likes_in_photos(photos)

    while True:
        try:
            photos = get_next(photos['paging']['next'])
            count_likes_in_photos(photos)
        except KeyError:
            break

    pprint.pprint(like_counts)
    print(shutter_count)


if __name__ == '__main__':
    main()
