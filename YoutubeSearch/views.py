from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from googleapiclient.discovery import build


@api_view(['GET'])
def getData(request):
    """
    Returns list of all the youtube videos that match the search criteria
    """
    
    return Response("construction-on-progress", status=status.HTTP_200_OK)  