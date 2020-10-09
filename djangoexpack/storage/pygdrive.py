import os
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.functional import cached_property

import pygdrive


class GoogleDriveStorage(Storage):
    def __init__(
            self,
            location=None,
            file_permissions_mode=None,
            directory_permissions_mode=None,
            credentials=None,
            client=None,
    ):
        self._location = location or ''
        self._file_permissions_mode = file_permissions_mode
        self._directory_permissions_mode = directory_permissions_mode
        self._custom_credentials = credentials
        if client:
            self.__dict__['client'] = client

    @cached_property
    def client(self):
        auth_params = {}

        if self._custom_credentials:
            auth_params['custom_credentials'] = self._custom_credentials
        else:
            auth_params['service_account_file'] = settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_FILE

        return pygdrive.authorize(**auth_params)

    @cached_property
    def files_api(self):
        return self.client.files

    def _value_or_setting(self, value, setting):
        return setting if value is None else value

    ''' #Not Implemented
    @property
    def base_location(self):
        return self._location

    @property
    def location(self):
        return self.base_location

    @cached_property
    def base_url(self):
        import pdb; pdb.set_trace()
        if self._base_url is not None and not self._base_url.endswith('/'):
            self._base_url += '/'
        return self._value_or_setting(self._base_url, settings.MEDIA_URL)

    @cached_property
    def file_permissions_mode(self):
        import pdb; pdb.set_trace()
        return self._value_or_setting(self._file_permissions_mode, settings.FILE_UPLOAD_PERMISSIONS)

    @cached_property
    def directory_permissions_mode(self):
        import pdb; pdb.set_trace()
        return self._value_or_setting(self._directory_permissions_mode, settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS)
    '''

    def path(self, name):
        return os.path.join(self._location, name) if name else self._location

    def exists(self, name):
        return self.files_api.exists(self.path(name))

    def get_or_create_folder(self, name):
        return self.files_api.get_or_create_folder(self.path(name))

    def size(self, name):
        return self.files_api.size(self.path(name))

    def get_accessed_time(self, name):
        return self.files_api.accessed_time(self.path(name))

    def get_created_time(self, name):
        return self.files_api.created_time(self.path(name))

    def get_modified_time(self, name):
        return self.files_api.modified_time(self.path(name))

    def url(self, name):
        url = self.files_api.url(self.path(name))
        if not url:
            raise ValueError("This file is not accessible via a URL.")
        return url

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        self.files_api.delete(self.path(name))

    def listdir(self, path):
        path = self.path(path)
        directories, files = [], []
        for entry in self.files_api.list(path):
            entry
            if entry['mimeType'] == self.files_api.FOLDER_MIME_TYPE:
                directories.append(entry['name'])
            else:
                files.append(entry['name'])
        return directories, files

    def _open(self, name, mode='rb'):
        # return File(open(self.path(name), mode))
        raise NotImplementedError(
            f'NYI: {self.__class__.__module__}.{self.__class_.__name__}._open()'
        )

    def _save(self, name, content):
        return self.files_api.upload(self.path(name), content)
