# YAFP
Yet Another Python Feedparser. Comes with a CLI version and a GUI version using PyQt5. Version agnostic

TO NOTE:
Depends on feedparser, requests and PyQt5 (gui version). "feedparser", "requests" and "PyQt5" can be obtained via pip, and PyQt5 requires additional libraries to be installed.

The CLI version will frequently crash windows command prompt because it does not filter out unicode (CMD seems to only support ASCII). In a later version I may implement sanitization either with a command line argument or some form of config file.
