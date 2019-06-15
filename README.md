## Features
 
* Formatted data from ffprobe/mediainfo
* Fallback data in case ffprobe/mediainfo cannot get data
* Identical data structure
* Full compatability with Python 3

## Install
 
 ```
 pip install PyProbe
 ```

## Usage

```python
import pyprobe
parser = pyprobe.VideoFileParser(ffprobe="/usr/bin/ffprobe", includeMissing=True, rawMode=False)
data = parser.parseFfprobe(inputFile)
```

This code will return a dictionary of values (as described below).

* **includeMissing** Will remove values where ffprobe/mediainfo does not return data
* **rawMode** Will make each value the raw output from ffprobe/mediainfo, which will be a string (except resolution, which is a tuple of strings).


There are also two helper functions provided to create more nicely formatted data -

```python
>>> import pyprobe
>>> pyprobe.timeToTuple(12345.44)
(3, 25, 45, 440)
>> pyprobe.sizeStr(12345678.99)
'11.8 MB'
```

# Data format

```python
{
    "path": str,
    "bit_rate": int,
    "duration": float,
    "size": int,
    "videos": [
        {
            "aspect_ratio": str,
            "bit_rate": int,
            "codec": str,
            "format": str,
            "framerate": float,
            "pixel_format": str,
            "resolution": (
                int # Width,
                int # Height
            )
        }
    ],
    "audios": [
        {
            "bit_rate": int,
            "channel_count": int,
            "channel_layout": str,
            "codec": str,
            "format": str,
            "sample_rate": int # Hz
        }
    ],
    "subtitles": [
        {
            "codec": str,
            "language": str
        }
    ],
    "chapters": [
        {
            "title": str,
            "start": float,
            "end": float,
        }
    ]
}
```
