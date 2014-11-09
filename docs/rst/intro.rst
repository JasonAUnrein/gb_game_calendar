Introduction
------------

Libdlm is a library and application for managing downloads.  The intent is to
provide a simple API that allows developers to quickly add a concurrent and
restartable download manager to an application.  There should be hooks to not
only start/stop/restart downloads but also receive download status updates such
as complete and X% done. 

Future versions enhancements could include support for different download
methods such as jigdo and torrents.

This is package will provide a minimalistic CLI interface as a proof of concept
and for testing purposes.  It should remain a small and light weight package
that makes it easy to incorporate into other projects

*Note*: The basis of this was forked/lifted from ade@pipe-devnull.com
http://pipe-devnull.com/2012/09/13/queued-threaded-http-downloader-in-python.html

Documentation
-------------

Documentation is hosted on [libdlm.readthedocs.org](http://libdlm.readthedocs.org/en/latest/)

Install
-------

Download the tarball and install with `pip install <package>`.

Usage
-----

See the unit tests for more in-depth examples. Here are the basics:
