import logging

from minio import Minio
from django.conf import settings

logger = logging.getLogger(__name__)


class AvatarUploader:

    def __init__(self):
        self.client = Minio(
            settings.MINIO_STORAGE_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_STORAGE_USE_HTTPS
        )
        # load the clown image to the bucket

    def get_avatar_url(self, user_id: str):
        logger.info("Getting avatar url for user {}".format(user_id))
        filename: str = f"{user_id}.jpg"
        bucket_name = settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        minio_response = self.client.presigned_get_object(bucket_name, filename)
        logger.info('Minio response: {}'.format(minio_response))
        return minio_response

    def upload_avatar(self, file, user_id):
        bucket_name = settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        # filename = user_id
        filename = "%s_avatar.jpg" % user_id
        self.client.put_object(
            bucket_name,
            filename,
            file,
            length=file.size,
            content_type=file.content_type
        )
        return "https://%s/%s/%s" % (settings.MINIO_STORAGE_ENDPOINT, bucket_name, filename)

