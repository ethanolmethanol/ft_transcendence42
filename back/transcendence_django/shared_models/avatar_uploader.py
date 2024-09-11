import logging

import urllib3
from django.conf import settings
from minio import Minio
from minio.commonconfig import CopySource
from minio.error import S3Error

logger = logging.getLogger(__name__)


class AvatarUploader:

    def __init__(self):
        self.client = Minio(
            settings.MINIO_STORAGE_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_STORAGE_USE_HTTPS,
        )
        self.client._http = urllib3.PoolManager(cert_reqs="CERT_NONE")
        logger.info("AvatarUploader: Started")

    def get_file_name(self, username):
        return "%s_avatar.jpg" % username

    def get_bucket_name(self):
        return settings.MINIO_STORAGE_MEDIA_BUCKET_NAME

    def upload_avatar(self, file, username):
        bucket_name = self.get_bucket_name()
        filename = self.get_file_name(username)
        self.client.put_object(
            bucket_name,
            filename,
            file,
            length=file.size,
            content_type=file.content_type,
        )

    def update_avatar_filename(self, former_username, new_username):
        try:
            former_filename = self.get_file_name(former_username)
            new_filename = self.get_file_name(new_username)
            bucket_name = self.get_bucket_name()

            self.client.copy_object(
                bucket_name,
                new_filename,
                CopySource(bucket_name, former_filename),
            )
            self.client.remove_object(bucket_name, former_filename)
        except S3Error:
            logger.info("Avatar file not found (not set yet)")

    def delete_avatar(self, username):
        bucket_name = self.get_bucket_name()
        filename = self.get_file_name(username)
        self.client.remove_object(bucket_name, filename)
