import datetime
from django.utils.timezone import make_aware

def fromIsoToDateTime(isoDate):
    """
        Converts ISO formatted time to Python DateTime object 
    """
    timestamp = datetime.datetime.strptime(isoDate, "%Y-%m-%dT%H:%M:%SZ")
    timestamp = make_aware(timestamp)
    return timestamp


def fromDateTimeToIso(DateTime):
    """
        Converts Python DateTime object to ISO formatted time
    """
    timestamp = DateTime.strftime('%Y-%m-%dT%H:%M:%SZ')
    return timestamp