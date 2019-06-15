import xml.etree.ElementTree as ET
from os import path
import re
import traceback

from pyprobe.baseparser import BaseParser


class DataParser(BaseParser):
    @staticmethod
    def get_element(xml_data, index):
        """Searches for element, returns default if not found"""
        element = xml_data.find(index)
        if element == None:
            return None
        elif type(element) == ET.Element:
            return element.text
        return None

    @staticmethod
    def codec(cls, data):
        """Returns a string"""
        info = cls.get_element(data, "CodecID")
        return info, info or "null"

    @staticmethod
    def format(cls, data):
        """Returns a string"""
        info = cls.get_element(data, "Format")
        return info, info or "null"

    @staticmethod
    def bit_rate(cls, data):
        """Returns an int"""
        info = cls.get_element(data, "BitRate")
        try:
            return info, int(float(info))
        except (ValueError, TypeError):
            return info, 0


class VideoStreamParser(BaseParser):
    @staticmethod
    def get_element(xml_data, index):
        return DataParser.get_element(xml_data, index)

    @classmethod
    def value_codec(cls, data):
        return DataParser.codec(cls, data)

    @classmethod
    def value_format(cls, data):
        return DataParser.format(cls, data)

    @classmethod
    def value_bit_rate(cls, data):
        return DataParser.bit_rate(cls, data)

    @classmethod
    def value_resolution(cls, data):
        """Returns a tuple of ints (width, height)"""
        width = cls.get_element(data, "Width")
        height = cls.get_element(data, "Height")
        try:
            return (width, height), (int(width), int(height))
        except (ValueError, ZeroDivisionError, TypeError):
            return (width, height), (0, 0)

    @classmethod
    def average_framerate(cls, data):
        """Returns a float"""
        frames = cls.get_element(data, "FrameCount")
        duration = cls.get_element(data, "Duration")
        combined = "Frames: {}, Duration: {}".format(frames or "", duration or "")
        try:
            return combined, int(float(frames)) / float(duration)
        except (ValueError, TypeError, ZeroDivisionError):
            return combined, 0.0

    @classmethod
    def value_framerate(cls, data):
        """Returns a float"""
        fallback = cls.average_framerate(data)
        info = cls.get_element(data, "FrameRate")
        try:
            return info, float(info)
        except (ValueError, TypeError):
            return info, fallback[1]

    @classmethod
    def value_aspect_ratio(cls, data):
        """Returns a string"""
        info = cls.get_element(data, "DisplayAspectRatio")
        return info, info or "null"

    @classmethod
    def value_pixel_format(cls, data):
        """Returns a string"""
        info = cls.get_element(data, "ColorSpace")
        return info, info or "null"


class AudioStreamParser(BaseParser):
    @staticmethod
    def get_element(xml_data, index):
        return DataParser.get_element(xml_data, index)

    @classmethod
    def value_codec(cls, data):
        return DataParser.codec(cls, data)

    @classmethod
    def value_format(cls, data):
        return DataParser.format(cls, data)

    @classmethod
    def value_bit_rate(cls, data):
        return DataParser.bit_rate(cls, data)

    @classmethod
    def value_sample_rate(cls, data):
        """Returns an int - audio sample rate in Hz"""
        info = cls.get_element(data, "SamplingRate")
        try:
            return info, int(float(info))
        except (ValueError, TypeError):
            return info, 0

    @classmethod
    def value_channel_count(cls, data):
        """Returns an int"""
        info = cls.get_element(data, "Channels")
        try:
            return info, int(float(info))
        except (ValueError, TypeError):
            return info, 0

    @classmethod
    def value_channel_layout(cls, data):
        """Returns a string"""
        info = cls.get_element(data, "ChannelLayout")
        return info, info or "null"


class SubtitleStreamParser(BaseParser):
    @staticmethod
    def get_element(xml_data, index):
        return DataParser.get_element(xml_data, index)

    @classmethod
    def value_codec(cls, data):
        return DataParser.codec(cls, data)

    @classmethod
    def value_language(cls, data):
        """Returns a string"""
        info = cls.get_element(data, "Language")
        return info, info or "null"


class ChapterParser(DataParser):
    @staticmethod
    def time_to_int(time):
        time_raw = 0.0
        exponent = 2
        for i in range(0, 3):
            time_raw += time[i] * 60 ** exponent
            exponent -= 1
        time_raw += time[3] / 1000
        return time_raw

    @classmethod
    def value_start(cls, data):
        """Returns an int"""
        time = data.tag.split("_")[1:]
        try:
            return data.tag, cls.time_to_int(tuple(map(int, time)))
        except (ValueError, ZeroDivisionError):
            return data, 0

    @staticmethod
    def value_title(data):
        """Returns a string"""
        time = data.text.split(":", 1)
        return data.text, time[-1]

    @classmethod
    def addEndTimes(cls, chapters, duration):
        """Add end times to chapters based on subsequent chapter start times
        Mediainfo only gives start times for each chapter

        Args:
            chapters (list): The parsed chapter info
            duration (int): Full video duration 

        """
        start_prev = duration
        for i in reversed(range(0, len(chapters))):
            chapters[i]["end"] = start_prev
            start_prev = chapters[i]["start"]


class RootParser(BaseParser):
    @staticmethod
    def get_element(xml_data, index):
        return DataParser.get_element(xml_data, index)

    @classmethod
    def value_duration(cls, data):
        """Returns an int"""
        info = cls.get_element(data, "Duration")
        try:
            return info, float(info)
        except (ValueError, TypeError):
            return info, 0.0

    @classmethod
    def value_size(cls, data):
        """Returns an int"""
        info = cls.get_element(data, "FileSize")
        try:
            return info, int(float(info))
        except (ValueError, TypeError):
            return info, 0

    @classmethod
    def value_bit_rate(cls, data):
        """Returns an int"""
        info = cls.get_element(data, "OverallBitRate")
        if info == None:
            size = cls.value_size(data)
            duration = cls.value_duration(data)
            info = size / (duration / 60 * 0.0075) / 1000
        try:
            return info, int(float(info))
        except (ValueError, TypeError):
            return info, 0
