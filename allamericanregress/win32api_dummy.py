"""A mocked win32api for when the application is run on linux."""


def GetVersionEx(_):
    """A mock of GetVersionEx from win32api."""
    return ['linux', 'linux', 'linux']
