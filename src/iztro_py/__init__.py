"""
iztro-py: A pure Python implementation of iztro

A lightweight library for generating astrolabes for Zi Wei Dou Shu
(紫微斗数, Purple Star Astrology), an ancient Chinese astrology.

This is a pure Python reimplementation of the original JavaScript iztro library,
without any JavaScript interpreter dependencies.
"""

__version__ = "0.3.3"
__author__ = "iztro-py Contributors"
__license__ = "MIT"

# Re-export main modules for convenient imports
from iztro_py import astro, data, star, utils

# Re-export main API functions for easier access
from iztro_py.astro import by_solar, by_lunar

__all__ = ["astro", "data", "star", "utils", "by_solar", "by_lunar", "__version__"]
