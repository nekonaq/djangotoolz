import os
from django.core.files import storage as django_storage


class FileSystemStorage(django_storage.FileSystemStorage):
    # - 存在するファイルに上書きする

    OS_OPEN_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, 'O_BINARY', 0)

    def get_available_name(self, name, max_length=None):
        return name

    def get_or_create_folder(self, name):
        directory = self.path(name)
        if not os.path.exists(directory):
            try:
                if self.directory_permissions_mode is not None:
                    # os.makedirs applies the global umask, so we reset it,
                    # for consistency with file_permissions_mode behavior.
                    old_umask = os.umask(0)
                    try:
                        os.makedirs(directory, self.directory_permissions_mode)
                    finally:
                        os.umask(old_umask)
                else:
                    os.makedirs(directory)
            except FileExistsError:
                # There's a race between os.path.exists() and os.makedirs().
                # If os.makedirs() fails with FileExistsError, the directory
                # was created concurrently.
                pass
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        # Store filenames with forward slashes, even on Windows.
        return name.replace('\\', '/')
