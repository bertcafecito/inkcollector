from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("inkcollector")
except PackageNotFoundError:
    __version__ = "unknown"
