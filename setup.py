import codecs
import os
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


long_description = read('README.md')


setup(
    name='xpectacle',
    version=find_version('xpectacle', '__init__.py'),
    description='Dead-simple window resizing and positioning using xdotool, wmctrl and xwininfo',
    long_description=long_description,
    author='Beta Faccion',
    author_email='betafcc@gmail.com',
    packages=['xpectacle'],
    url='https://github.com/betafcc/xpectacle',
)
