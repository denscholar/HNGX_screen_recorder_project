from django.db import models


class Video(models.Model):
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"video created at {self.created_at}"
    

