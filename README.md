# python-lustre-utils

## Summary
lustre-utils is a Python library to interface with Lustre through 
its /proc interface.  It is at an early stage of development and 
currently offers a set of classes to discover Lustre 'devices' on 
servers and clients as well as to read and parse stats files for 
those devices.

##Example usages

### MDS

On a MDS, initialize a lustre_mds object and use it to get a
lustre_mds_stats object at regular interval.  Compare 2 lustre_mds_stats
to calculate the activity between the 2 timestamps.

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

Iterate over MDTs (lustre_mdt) on that node to get their state and IO 
counters through lustre_mdt_stats. Compare 2 lustre_mdt_stats object 
to calculate average IOPS over the delta of their respective timestamp.
```
>>> for mdt in mds.MDTs :
...     (total, count) = mdt.get_disk_usage()
...     print "KB_total={0}".format(total)
...     print "KB_used={0}".format(count)
...     mdt_stats = mdt.get_stats()
...     print mdt_stats.timestamp
...     print "nb_open={0}".format(mdt_stats.nb_open)
...     print "nb_close={0}".format(mdt_stats.nb_close)
...     print "nb_mknod={0}".format(mdt_stats.nb_mknod)
...     print "nb_unlink={0}".format(mdt_stats.nb_unlink)
...     print "nb_mkdir={0}".format(mdt_stats.nb_mkdir)
...     print "nb_rmdir={0}".format(mdt_stats.nb_rmdir)
...     print "nb_rename={0}".format(mdt_stats.nb_rename)
...     print "nb_getattr={0}".format(mdt_stats.nb_getattr)
...     print "nb_setattr={0}".format(mdt_stats.nb_setattr)
...     print "nb_link={0}".format(mdt_stats.nb_link)
...     print "nb_statfs={0}".format(mdt_stats.nb_statfs)
...
KB_total=1463928360
KB_used=15095456
1429025597.42
nb_open=246819413
nb_close=229597234
nb_mknod=15776
nb_unlink=38180836
nb_mkdir=1155283
nb_rmdir=1545186
nb_rename=49329740
nb_getattr=452232913
nb_setattr=37349033
nb_link=358
nb_statfs=875795
```
