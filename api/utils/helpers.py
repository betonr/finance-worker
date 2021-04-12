import base64
import binascii
import os
import subprocess
import threading
import webbrowser
import contextlib
from sqlalchemy.inspection import inspect

class Serializer(object):
    @staticmethod
    def serialize(obj):
        return {c.key: str(getattr(obj, c.key)) for c in inspect(obj).mapper.column_attrs}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


def open_brower(url, time=1):
    """
    open new brower
    Args:
        url: url to open in brower
        time: time delay to open brower
    """
    threading.Timer(time, lambda: webbrowser.open(url)).start()


def random_string(size=16):
    """
    generate random string
    Args:
        size: string size
    """
    return (binascii.hexlify(os.urandom(size))).decode('ascii')


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.communicate()


def key_id_encode(the_bytes):
    source = base64.b32encode(the_bytes).decode('utf-8')
    result = []
    for i in range(0, len(source), 4):
        start = i
        end = start+4
        result.append(source[start:end])
    return ":".join(result)
    

@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit.
    Exceptions:
        FileNotFoundError when could not change to directory provided.
    Args:
        path (str): Directory to change
    Returns:
        str Path to the changed directory
    Example:
        >>> import os
        >>> from tempfile import gettempdir
        >>> from bdc_core.decorators.utils import working_directory
        ...
        ...
        >>> TEMP_DIR = gettempdir()
        >>> @working_directory(TEMP_DIR)
        ... def create_file(filename):
        ...     # Create file in Temporary folder
        ...     print('Current dir: {}'.format(os.getcwd()))
        ...     with open(filename, 'w') as f:
        ...         f.write('Hello World')
    """
    owd = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(owd)