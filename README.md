# python-lustre-utils

## Summary
lustre-utils is a Python library to interface with Lustre through 
its /proc interface.  It is at an early stage of development and 
currently offers a set of classes to discover Lustre 'devices' on 
servers and clients as well as to read and parse stats files for 
those devices.

##Example usages

### MDS
```
>>> from lustre_util import *

# lustre1 is the FS nam
>>> mds = lustre_mds("lustre1")
>>> mds_stats = mds.get_stats()
>>> print mds_stats.timestamp
1429023634.66
>>> print mds_stats.req_waittime
322458150170
>>> print mds_stats.req
9316887436
>>> print mds_stats.nb_threads
192
```
