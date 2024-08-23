import logging

from minio import Minio
from django.conf import settings
from minio.error import S3Error
import urllib3

logger = logging.getLogger(__name__)


class AvatarUploader:

    def __init__(self):
        self.client = Minio(
            settings.MINIO_STORAGE_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_STORAGE_USE_HTTPS
        )
        self.client._http = urllib3.PoolManager(cert_reqs='CERT_NONE')

    def get_avatar_url(self, user_id: str):
        logger.info("Getting avatar url for user {}".format(user_id))
        #filename = f"{user_id}.jpg"
        filename = settings.DEFAULT_AVATAR_PATH

        bucket_name = settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        minio_response = self.client.presigned_get_object(bucket_name, filename)
        if minio_response is None:
            minio_response = self.client.presigned_get_object(bucket_name, settings.DEFAULT_AVATAR_PATH)
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

