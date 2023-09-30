from django.shortcuts import render

from videos.serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from .models import Video
from django.core.files.base import ContentFile


# views.py
import uuid


class ScreenRecorderAPIView(APIView):
    def post(self, request, format=None):
        video_chunk = request.data.get("video_chunk", None)

        if not video_chunk:
            return Response(
                {"error": "No video chunk provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Assuming your video data is a base64 encoded file
            video = Video.objects.last()  # Get the latest video record
            unique_filename = f"{str(uuid.uuid4())}.webm"  # Generate a unique filename
            video.video_file.save(unique_filename, ContentFile(video_chunk), save=False)
            video.save()
        except Exception as e:
            return Response(
                {"error": f"Error processing chunk: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Chunk received successfully"}, status=status.HTTP_200_OK
        )
