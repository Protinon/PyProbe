from distutils.core import setup

setup(
  name='PyProbe',
  packages=['pyprobe'],
  version="0.1.0"
  license='MIT',
  description='Extract metadata from video files using ffprobe or mediainfo',
  author='Protinon',
  author_email='Protinon99@gmail.com',
  url='https://github.com/Protinon/PyProbe',
  keywords=['ffprobe', 'mediainfo', 'parser', 'video'],
  install_requires=[],
  python_requires='Python 3',
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