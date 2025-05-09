from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("inkcollector")
except PackageNotFoundError:
    __version__ = "unknown"