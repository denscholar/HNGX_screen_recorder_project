from django.shortcuts import render

from videos.serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from .models import Video
from django.core.files.base import ContentFile
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema


# views.py
import uuid


class ScreenRecorderAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="",
        operation_description="""
    """,
        request_body=VideoSerializer,
    )
    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)

        if serializer.is_valid():
            video_file = serializer.validated_data.get("video_file")

            if not video_file:
                return Response(
                    {"error": "No video file provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                # Create a new video record
                video = Video.objects.create()
                unique_filename = f"{str(uuid.uuid4())}.webm"

                # Save the uploaded file
                video.video_file.save(unique_filename, video_file, save=False)
                video.save()
            except Exception as e:
                return Response(
                    {"error": f"Error processing file: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": "File received and processed successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
