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
        logger.info("AvatarUploader: Started")

    def upload_avatar(self, file, user_id):
        bucket_name = settings.MINIO_STORAGE_MEDIA_BUCKET_NAME
        filename = "%s_avatar.jpg" % user_id
        self.client.put_object(
            bucket_name,
            filename,
            file,
            length=file.size,
            content_type=file.content_type
        )
