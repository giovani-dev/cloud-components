from unittest.mock import Mock

from botocore.exceptions import ClientError

from cloud_components.infra.aws.resources.s3 import S3


class TestS3:
    connection_mock: Mock
    env_mock: Mock
    logger_mock: Mock
    bucket_mock: Mock

    def setup_method(self):
        self.connection_mock = Mock(name="connection")
        self.env_mock = Mock(name="env")
        self.logger_mock = Mock(name="logger")
        self.bucket_mock = Mock(name="bucket")

    def test_bucket__get_bucket_without_setting_its_name__expected_none_return(self):
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )

        assert not instance.bucket

    def test_bucket__get_bucket_setted__expected_bucket_object_returned(self):
        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )

        assert instance.bucket == self.bucket_mock

    def test_bucket__set_bucket_name__expected_bucket_method_call_from_connection(self):
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )
        instance.bucket = "my-bucket"

        self.connection_mock.Bucket.assert_called_once_with("my-bucket")

    def test_save_file__file_with_public_acl__expected_file_saved(self):
        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )

        is_saved = instance.save_file(
            data=b"pa\xc3\xa7oca de coco",
            file_path="test/file.txt",
            content_type="application/octet-stream",
            is_public=True,
        )

        assert is_saved
        self.logger_mock.info.assert_called_once_with(
            "Saving a file with public acl and content-type as 'application/octet-stream' in 'test/file.txt'"  # pylint: disable=C0301
        )
        self.bucket_mock.put_object.assert_called_once_with(
            Key="test/file.txt",
            Body=b"pa\xc3\xa7oca de coco",
            ACL="public-read",
            ContentType="application/octet-stream",
        )

    def test_save_file__file_with_private_acl__expected_file_saved(self):
        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )

        is_saved = instance.save_file(
            data=b"pa\xc3\xa7oca de coco",
            file_path="test/file.txt",
            content_type="application/octet-stream",
        )

        assert is_saved
        self.logger_mock.info.assert_called_once_with(
            "Saving a file with content-type as 'application/octet-stream' in 'test/file.txt'"
        )
        self.bucket_mock.put_object.assert_called_once_with(
            Key="test/file.txt",
            Body=b"pa\xc3\xa7oca de coco",
            ContentType="application/octet-stream",
        )

    def test_save_file__bucket_exception_when_save_a_file_with_public_acl__expected_bucket_raises_a_client_error(  # pylint: disable=C0301
        self,
    ):
        self.bucket_mock.put_object.side_effect = ClientError(
            operation_name="InvalidKeyPair.Duplicate",
            error_response={
                "Error": {"Code": "Duplicate", "Message": "This is a custom message"}
            },
        )
        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )

        is_saved = instance.save_file(
            data=b"pa\xc3\xa7oca de coco",
            file_path="test/file.txt",
            content_type="application/octet-stream",
            is_public=True,
        )

        assert not is_saved
        self.logger_mock.info.assert_called_once_with(
            "Saving a file with public acl and content-type as 'application/octet-stream' in 'test/file.txt'"  # pylint: disable=C0301
        )
        self.bucket_mock.put_object.assert_called_once_with(
            Key="test/file.txt",
            Body=b"pa\xc3\xa7oca de coco",
            ACL="public-read",
            ContentType="application/octet-stream",
        )
        self.logger_mock.error.assert_called_once_with(
            "An error occurred when try to save a file in S3. Error detail: An error occurred (Duplicate) when calling the InvalidKeyPair.Duplicate operation: This is a custom message"  # pylint: disable=C0301
        )

    def test_save_file__bucket_exception_when_save_a_file_with_private_acl__expected_bucket_raises_a_client_error(  # pylint: disable=C0301
        self,
    ):
        self.bucket_mock.put_object.side_effect = ClientError(
            operation_name="InvalidKeyPair.Duplicate",
            error_response={
                "Error": {"Code": "Duplicate", "Message": "This is a custom message"}
            },
        )
        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )

        is_saved = instance.save_file(
            data=b"pa\xc3\xa7oca de coco",
            file_path="test/file.txt",
            content_type="application/octet-stream",
        )

        assert not is_saved
        self.logger_mock.info.assert_called_once_with(
            "Saving a file with content-type as 'application/octet-stream' in 'test/file.txt'"
        )
        self.bucket_mock.put_object.assert_called_once_with(
            Key="test/file.txt",
            Body=b"pa\xc3\xa7oca de coco",
            ContentType="application/octet-stream",
        )
        self.logger_mock.error.assert_called_once_with(
            "An error occurred when try to save a file in S3. Error detail: An error occurred (Duplicate) when calling the InvalidKeyPair.Duplicate operation: This is a custom message"
        )

    def test_get_file__bucket_raises_an_exception__expected_client_error(self):
        self.bucket_mock.Object.side_effect = ClientError(
            operation_name="InvalidKeyPair.Duplicate",
            error_response={
                "Error": {"Code": "Duplicate", "Message": "This is a custom message"}
            },
        )
        S3._bucket = self.bucket_mock  # pylint: disable=W0212

        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )
        file = instance.get_file(file_path="test/file.txt")

        assert not file
        self.logger_mock.error.assert_called_once_with(
            "An error occurred when try to get a file in S3. Error detail: An error occurred (Duplicate) when calling the InvalidKeyPair.Duplicate operation: This is a custom message"  # pylint: disable=C0301
        )

    def test_get_file__read_file_with_content__expected_file_content(self):
        object_mock = Mock(name="object")
        file_buffer_mock = Mock(name="file_buffer")
        file_buffer_mock.read.return_value = b"pa\xc3\xa7oca de coco"
        object_mock.get.return_value = {"Body": file_buffer_mock}
        self.bucket_mock.Object.return_value = object_mock

        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )
        file = instance.get_file(file_path="test/file.txt")

        assert file == b"pa\xc3\xa7oca de coco"
        self.logger_mock.info.assert_called_once_with(
            "Getting file from 'test/file.txt'"
        )
        self.bucket_mock.Object.assert_called_once_with("test/file.txt")
        object_mock.get.assert_called_once()
        file_buffer_mock.read.assert_called_once()

    def test_get_file__read_file_without_content__expected_file_content(self):
        object_mock = Mock(name="object")
        file_buffer_mock = Mock(name="file_buffer")
        file_buffer_mock.read.return_value = b""
        object_mock.get.return_value = {"Body": file_buffer_mock}
        self.bucket_mock.Object.return_value = object_mock

        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )
        file = instance.get_file(file_path="test/file.txt")

        assert not file
        self.logger_mock.info.assert_called_once_with(
            "Getting file from 'test/file.txt'"
        )
        self.bucket_mock.Object.assert_called_once_with("test/file.txt")
        object_mock.get.assert_called_once()
        file_buffer_mock.read.assert_called_once()

    def test_get_file__object_raise_exception__expected_client_error(self):
        self.bucket_mock.Object.side_effect = ClientError(
            operation_name="InvalidKeyPair.Duplicate",
            error_response={
                "Error": {"Code": "Duplicate", "Message": "This is a custom message"}
            },
        )
        S3._bucket = self.bucket_mock  # pylint: disable=W0212
        instance = S3(
            connection=self.connection_mock, logger=self.logger_mock
        )
        file = instance.get_file(file_path="test/file.txt")

        assert not file
        self.logger_mock.info.assert_called_once_with(
            "Getting file from 'test/file.txt'"
        )
        self.logger_mock.error.assert_called_once_with(
            "An error occurred when try to get a file in S3. Error detail: An error occurred (Duplicate) when calling the InvalidKeyPair.Duplicate operation: This is a custom message"  # pylint: disable=C0301
        )
