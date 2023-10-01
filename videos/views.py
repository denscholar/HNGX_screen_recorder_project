import os
from tempfile import NamedTemporaryFile
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
        operation_description="""
        """,
        request_body=RecordedVideoSerializer,
    )
    def post(self, request, *args, **kwargs):
        video_chunk = request.data.get("video_chunk")
        video_chunk = base64.b64decode(video_chunk)

        try:
            video_instance = RecordedVideo.objects.create()

            # Create a temporary file to store the video chunks
            temp_file = NamedTemporaryFile(delete=False)

            try:
                # Write the received video chunk to the temporary file
                temp_file.write(video_chunk.read())

                # Close the temporary file to flush the data to disk
                temp_file.close()

                # Check if all chunks have been received
                if request.data.get("final_chunk"):
                    # Concatenate all chunks into the final video file
                    final_video_path = os.path.join(
                        "media", f"{video_instance.id}_final.mp4"
                    )
                    with open(final_video_path, "ab") as final_video:
                        with open(temp_file.name, "rb") as temp_file_content:
                            final_video.write(temp_file_content.read())

                    # Update the video file field in the database
                    video_instance.video_file.name = final_video_path
                    video_instance.save()

                    # Clean up the temporary file
                    os.remove(temp_file.name)

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


# import base64
# import cloudinary.uploader
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import RecordedVideo
# from .serializers import RecordedVideoSerializer


# class VideoUploadAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             video_chunk_base64 = request.data.get("video_chunk")
#             video_chunk = base64.b64decode(video_chunk_base64)

#             video_instance = RecordedVideo.objects.create()

#             # Append the video chunk to the video_file URL
#             video_instance.video_file += video_chunk

#             # Check if all chunks have been received
#             if request.data.get("final_chunk"):
#                 # Upload the concatenated video to Cloudinary
#                 upload_result = cloudinary.uploader.upload(
#                     video_instance.video_file.read(), resource_type="video"
#                 )

#                 # Update the video_file field in the database with Cloudinary URL
#                 video_instance.video_file.name = upload_result[
#                     "public_id"
#                 ]  # Assuming you want to store Cloudinary public_id
#                 video_instance.save()

#                 return Response(
#                     {"message": "Video uploaded successfully."},
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response(
#                     {"message": "Video chunk uploaded successfully."},
#                     status=status.HTTP_200_OK,
#                 )
#         except Exception as e:
#             # Handle any errors (e.g., data corruption, incomplete chunks)
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
