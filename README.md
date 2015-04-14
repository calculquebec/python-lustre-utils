# python-lustre-utils

## Summary
lustre-utils is a Python library to interface with Lustre through 
its /proc interface.  It is at an early stage of development and 
currently offers a set of classes to discover Lustre 'devices' on 
servers and clients as well as to read and parse stats files for 
those devices.

##Example usages

### MDS/MDT

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

### OSS/OST
On an OSSS, initialize a lustre_oss object and use it to get a
lustre_oss_stats object at regular interval.  Compare 2 lustre_oss_stats
to calculate the activity between the 2 timestamps.

Average request waittime would be:
(oss_stats2.req_waittime - oss_stats1.req_waittime) / (oss_stats2.req - oss_stats1.req)

```
>>> from lustre_util import *
>>> oss_stats = lustre_oss.get_OSS_stats()
>>> print "OSS nb threads={0}".format(oss_stats.nb_threads)
OSS nb threads=192
>>> print "OSS nb requests={0}".format(oss_stats.req)
OSS nb requests=86688783
>>> print "OSS request wait time={0}".format(oss_stats.req_waittime)
OSS request wait time=148960010965
>>> print oss_stats.timestamp
1429026158.35
>>>
```
Iterate over OSTs (lustre_ost) on that oss to get their state and IO 
counters through lustre_ost_stats. Compare 2 lustre_ost_stats object 
to calculate average IOPS over the delta of their respective timestamp.

With little changes, this could also be run on the MDS to have an easier 
aggregate of disk usage. For now, disk usage for the FS is the sum of 
KB_total on all OSTs.

```
>>> for ost in lustre_ost.get_OSTs():
...     print "OST={0}".format(ost.name)
...     (total, count) = ost.get_disk_usage()
...     print "KB_total={0}".format(total)
...     print "KB_used={0}".format(count)
...     (total, count) = ost.get_inode_usage()
...     print "inodes_total={0}".format(total)
...     print "inodes_used={0}".format(count)
...     stats = ost.get_stats()
...     print "read_bytes={0}".format(stats.read_bytes)
...     print "write_bytes={0}".format(stats.write_bytes)
...     print "read_count={0}".format(stats.read_count)
...     print "write_count={0}".format(stats.write_count)
...
OST=lustre1-OST0002
KB_total=30476265216
KB_used=24698989696
inodes_total=54089535
inodes_used=8954570
read_bytes=24153136496640
write_bytes=20812013882221
read_count=60069567
write_count=25409128
```
Additionnally, if running on ldiskfs, some brw_stats are available from
lustre_ost_stats.IO_size_KB


