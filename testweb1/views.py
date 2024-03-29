from django.shortcuts import render
from django.http import HttpResponse
from testweb1.forms import audioAccept
import os
from django.conf import settings
from django.http import JsonResponse
from .forms import VideoIdForm  # Import your VideoIdForm
import requests
import time
import re

def sample(request):
    if request.method == 'POST':
        form = audioAccept(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['audioFile']
            
            # Determine the path to save the uploaded file
            save_path = os.path.join(settings.MEDIA_ROOT, 'accepted_Audio')  # 'accepted_Audio' is the subdirectory where you want to save the files
            os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
            
            # Construct the full file path
            file_name = uploaded_file.name
            file_path = os.path.join(save_path, file_name)
            
            # Save the uploaded file to the desired location
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Handle the uploaded file processing here, if needed
            
    else:
        form = audioAccept()
    
    context = {'form': form}
    return render(request, 'uiDesign.html', context)




def convert_mp3(request):

    form = VideoIdForm(request.POST)
    if form.is_valid():
        video_id = form.cleaned_data['video_id']
            
        if not video_id:
            return render(request, 'uiDesign.html', {'success': False, 'message': 'Please enter a video ID'})
            
        api_key = settings.YOUTUBE_API_KEY
        api_host = settings.YOUTUBE_API_HOST
            
        response = requests.get(f'https://{api_host}/dl?id={video_id}', 
                                headers={"x-rapidapi-key": api_key, "x-rapidapi-host": api_host})
            
        fetch_response = response.json()
            
        if fetch_response.get('status') == 'ok':
            return render(request, 'uiDesign.html', {'success': True, 
                                                    'song_title': fetch_response.get('title'), 
                                                    'song_link': fetch_response.get('link')})
        else:
            return render(request, 'uiDesign.html', {'success': False, 'message': fetch_response.get('msg')})
    



def mp3_conversion(video_id, api_key, api_host):
    api_key = settings.API_KEY
    api_host = settings.API_HOST
    url = f"https://{api_host}/dl?id={video_id}"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }

    while True:
        response = requests.get(url, headers=headers)
        fetch_response = response.json()

        if fetch_response["status"] == "processing":
            time.sleep(1)
        else:
            return fetch_response

def extract_video_id(url):
    # Define the regular expression pattern to match YouTube video IDs
    pattern = r"(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|&v=)([\w-]+)"

    # Use re.search to find the video ID in the URL
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None

def convert_mp3(request):
    form = VideoIdForm(request.POST)
    if form.is_valid():
        youtube_url = form.cleaned_data['video_id']  # Get the YouTube URL from the form


        # Extract the video ID from the URL using the updated function
        video_id = extract_video_id(youtube_url)
        
        if video_id:
            api_key = settings.API_KEY
            api_host = settings.API_HOST

            response = mp3_conversion(video_id, api_key, api_host)

            if response.get('status') == 'ok':
                return render(request, 'uiDesign.html', {'success': True,
                                                         'song_title': response.get('title'),
                                                         'song_link': response.get('link')})
            else:
                return render(request, 'uiDesign.html', {'success': False, 'message': response.get('msg')})
        else:
            return render(request, 'uiDesign.html', {'success': False, 'message': 'Invalid YouTube URL'})

    return render(request, 'uiDesign.html', {'form': form})
             
