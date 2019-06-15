from setuptools import setup

with open("README.md", "r") as ld:
    long_description = ld.read()

setup(
    name='PyProbe',
    packages=['pyprobe'],
    version="0.1.1",
    license='MIT',
    description='Extract metadata from video files using ffprobe or mediainfo',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Protinon',
    author_email='Protinon99@gmail.com',
    url='https://github.com/Protinon/PyProbe',
    keywords=['ffprobe', 'mediainfo', 'parser', 'video'],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Programming Language :: Python :: 3 :: Only',
],
)