"""A mocked win32api for when the application is run on linux."""


def GetVersionEx(_):
    """A mock of win32apiGetVersionEx."""
    return ['linux', 'linux', 'linux']
