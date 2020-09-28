from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from .models import VideoData, Thumbnails
from FamYoutube.celery import app
from django.conf import settings
from django.db import IntegrityError
from .utils import fromIsoToDateTime, fromDateTimeToIso


def insert_video(videoId, rowData):
    """
    Function receives videoId, and other video details,
    Inserts them into the database.
    If video is successfully inserted, video thumbnails are inserted.
    Returns the instance created in database.
    """
    video = VideoData(
            id = videoId,
            title = rowData['title'],
            description = rowData['description'],
            channelTitle = rowData['channelTitle'],
            publishedAt = fromIsoToDateTime(rowData['publishedAt']),
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
    It inserts them into database and links thumbnails to it's parent video.
    Returns the instance of thumbnail object created
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
        return None

    return thumbnail

    

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
        Async task handled by celery and executed every 10 seconds.
        This function fetches all the videos published with specific term in there title/description
        for every 10 seconds in background and populates database with that data.
    """
    
    # Logging
    print("Fetching new data...")

    # Get current datetime, convert it to timestamp of 10 minutes before. 
    timestamp = datetime.now() - timedelta(minutes=10)
     
    # Try to fetch record with latest publishedAt.  
    try:
        # If found, we use it's timestamp to search for videos published after this
        timestamp = VideoData.objects.latest('publishedAt').publishedAt
        print(f"Got existing timestamp {timestamp}")
    except VideoData.DoesNotExist:
        # If not found, we use the default timestamp i.e 10 minute delta from current time
        print(f"Using default timestamp {timestamp}")

    timestamp = fromDateTimeToIso(timestamp)
        
    # Index of which API Key is being used
    curr_key_index = 0
    
    is_data_fetched = False
    total_api_call_fails = 0

    # A dummy response, in case all API request fail
    response = {'items':[]}

    # Loop to try out all keys until all have been exhausted
    while is_data_fetched == False:
        is_data_fetched = True

        print(f"Using key ({curr_key_index}) = {settings.YOUTUBE_API_KEY[curr_key_index]}")

        try:
            service = build(
                'youtube',
                'v3',
                developerKey=settings.YOUTUBE_API_KEY[curr_key_index], 
                cache_discovery=False
            )
            collection = service.search().list(
                maxResults=25,
                part=['id','snippet'],
                q='cricket',
                type='video',
                order='date',
                publishedAfter=timestamp
            )

            response = collection.execute()
        except HttpError as e:
            # Exception when either the key is wrong or API limit is exhausted
            print(f"!!!!DEBUG LOG!!!! {e}")
            curr_key_index = curr_key_index + 1 
            total_api_call_fails = total_api_call_fails + 1

            # If total keys is less than current index, take mod
            curr_key_index = curr_key_index % len(settings.YOUTUBE_API_KEY)
            is_data_fetched = False       
        
        # If all the keys have been tried, break the loop
        if total_api_call_fails == len(settings.YOUTUBE_API_KEY):
            print("API call limit exhausted for all keys")
            break

    print(f"Fetched {len(response['items'])} items")

    #If list contains items, populate database
    if len(response['items']) > 0:
        count = populate_data(response['items'])
        print(f"Successfully inserted {count} data")

    return False
