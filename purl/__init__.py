""""An immutable URL class for easy URL-building and manipulation"""
# flake8: noqa
from .url import URL
from .template import expand, Template

__version__ = "1.5"

__all__ = ["URL", "expand", "Template"]
