import os
from tempfile import NamedTemporaryFile
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RecordedVideo
from .serializers import RecordedVideoSerializer
from drf_yasg.utils import swagger_auto_schema
import base64


class VideoUploadAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="This endpoint is responsible for getting the video in chunks",
        operation_description="",
        request_body=RecordedVideoSerializer,
    )
    def post(self, request, *args, **kwargs):
        video_chunk = request.data.get("video_chunk")
        video_chunk = base64.b64decode(video_chunk)

        try:
            video_instance = RecordedVideo.objects.create()

            # Create a temporary file-like object to store the video chunks
            temp_file = BytesIO(video_chunk)

            try:
                # Check if all chunks have been received
                if request.data.get("final_chunk"):
                    # Concatenate all chunks into the final video file
                    final_video_path = os.path.join(
                        "media", f"{video_instance.id}_final.mp4"
                    )
                    with open(final_video_path, "ab") as final_video:
                        temp_file.seek(0)  # Move the cursor to the beginning
                        final_video.write(temp_file.read())

                    # Update the video file field in the database
                    video_instance.video_file.name = final_video_path
                    video_instance.save()

                    return Response(
                        {"message": "Video uploaded successfully."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Video chunk uploaded successfully."},
                        status=status.HTTP_200_OK,
                    )
            except Exception as e:
                # Handle any errors (e.g., data corruption, incomplete chunks)
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
