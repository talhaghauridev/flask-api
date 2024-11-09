# controllers/__init__.py
from os.path import dirname, basename, isfile, join
import glob

# Get all .py files in the directory
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
