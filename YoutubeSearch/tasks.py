from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from .models import VideoData, Thumbnails
from FamYoutube.celery import app
from django.conf import settings
from urllib3.exceptions import HTTPError 
from django.db import IntegrityError

def insert_video(videoId, rowData):
    """
    Function receives videoId, and other video details,
    Inserts them into the database.
    Returns the instance created in database.
    """
    video = VideoData(
            id = videoId,
            title = rowData['title'],
            description = rowData['description'],
            channelTitle = rowData['channelTitle'],
            publishedAt = rowData['publishedAt'],
        )
    
    try:
        video.save()
    except IntegrityError as e:
        return None

    insert_thumbnail(rowData['thumbnails']['default'],'DE',video)
    insert_thumbnail(rowData['thumbnails']['medium'],'ME',video)
    insert_thumbnail(rowData['thumbnails']['high'],'HI',video)

    return video


def insert_thumbnail(thumbnail, thumbnail_type, video):
    """
    Function receives thumbnail data, thumbnail type and instance of parent video,
    It inserts them into database and links the item to it's parent video.
    """
    thumbnail = Thumbnails(
            thumbnail_type = thumbnail_type,
            video = video,
            height = thumbnail['height'],
            width = thumbnail['width'],
            url = thumbnail['url']
        )
    try:
        thumbnail.save()
    except IntegrityError as e:
        return False

    

def populate_data(itemsData):
    """
        Input: List of video data response from youtube
        This function receives list of video data and inserts them into the database 
        Returns count of successful insertions
    """
    count = 0
    for item in itemsData:
        video = insert_video(item['id']['videoId'], item['snippet'])
        if video is not None:
            count = count + 1

    return count


@app.task
def fetch_data():
    """
        Input: None
        This function fetches all the videos published with specific term in there title/description
        for every 10 seconds in background.
    """
    #Logging
    print("Fetching new data...")

    #Get current datetime, convert it to timestamp of 30 seconds before.
    # obj= Model.objects.filter(testfield=12).latest('testfield')

    now = datetime.now() - timedelta(minutes=10)
    timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    try:
        timestamp = VideoData.objects.latest('publishedAt').publishedAt
        print(f"Got existing timestamp {timestamp}")
    except VideoData.DoesNotExist:
        print(f"Using default timestamp {timestamp}")
    
    print(timestamp)

    curr_key_index = 0
    
    is_data_fetched = False
    total_api_call_fails = 0

    #Loop to try out all keys until all have been exhausted
    response = {'items':[]}

    while is_data_fetched == False:
        is_data_fetched = True

        #Debug log (Which key is currently being used)
        print(f"Using key ({curr_key_index}) = {settings.YOUTUBE_API_KEY[curr_key_index]}")

        service = build('youtube','v3',developerKey=settings.YOUTUBE_API_KEY[curr_key_index], cache_discovery=False)
        collection = service.search().list(maxResults=25,part=['id','snippet'],q='cricket', type='video', order='date', publishedAfter=timestamp)
        
        try:
            response = collection.execute()
        except HttpError as e:
            print(e)
            curr_key_index = curr_key_index + 1 
            total_api_call_fails = total_api_call_fails + 1
            curr_key_index = curr_key_index % len(settings.YOUTUBE_API_KEY)
            is_data_fetched = False       

        if total_api_call_fails == len(settings.YOUTUBE_API_KEY):
            print("API call limit exhausted for all keys")
            break

    print(f"Fetched {len(response['items'])} items")

    #If list contains items, populate database
    if len(response['items']) > 0:
        count = populate_data(response['items'])
        print(f"Successfully inserted {count} data")

    return False
