
def timeToTuple(duration):
    """Converts time float to tuple
    
    Args:
        duration (float): converts duration to a tuple
    Returns:
        tuple: Duration split into hours, minutes, and seconds
    """
    hours, rem = divmod(duration, 3600)
    minutes, rem2 = divmod(rem, 60)
    seconds, mseconds = divmod(rem2, 1)
    return int(hours), int(minutes), int(seconds), round(mseconds * 1000)


def sizeStr(size):
    """Returns formatted string of a byte size
    Args:
        size (int): size in bytes
    Returns:
        string: Size with appropriate byte suffix
    
    """
    prefixes = ["B", "KB", "MB", "GB", "TB"]
    exponent = 0
    while size > 1024:
        size /= 1024
        exponent += 1
    precision = 3 - len(str(int(size)))
    form = "{:0." + str(precision) + "f} {}"
    return form.format(size, prefixes[exponent])
    