
from __future__ import division

from lustre import lustre
from lustre_mdt_stats import lustre_mdt_stats

class lustre_mdt :
    name    = ""
    proc_path = ""
    proc_osd_path = ""
    kbytes_total  = 0
    kbytes_used   = 0
    inodes_total  = 0
    inodes_used   = 0

    def __init__(self, name) :    
        self.name    = name
        self.proc_path = lustre.proc_path+"/mdt/"+self.name
        self.proc_osd_path = lustre.proc_path+"/osd-ldiskfs/"+self.name

        #Get total capacity (kbytes & inodes) from /proc
        #KBytes
        with open(self.proc_osd_path+"/kbytestotal", "r") as fd:
            self.kbytes_total = long(fd.readline())
        with open(self.proc_osd_path+"/kbytesfree", "r") as fd:
            self.kbytes_used  = self.kbytes_total - long(fd.readline())

        #Inodes
        #Get the total and free capacity from /proc
        with open(self.proc_osd_path+"/filestotal", "r") as fd:
            self.inodes_total = long(fd.readline())
        #Get the free space from /proc
        with open(self.proc_osd_path+"/filesfree", "r") as fd:
            self.inodes_used  = self.inodes_total - long(fd.readline())

    def get_stats(self) :
        mdt_stats = lustre_mdt_stats()
        raw_stats = lustre.read_stats(lustre.proc_path+"/mdt/"+self.name+"/md_stats")
        #We care about :  open, close, mknod, unlink, mkdir, rmdir, 
        #                 rename, getattr, setattr, getxattr, link, statfs
        mdt_stats.timestamp   = raw_stats["timestamp"]

        mdt_stats.nb_open     = lustre.get_stats_field(raw_stats, "open")
        mdt_stats.nb_close    = lustre.get_stats_field(raw_stats, "close")
        mdt_stats.nb_mknod    = lustre.get_stats_field(raw_stats, "mknod")
        mdt_stats.nb_unlink   = lustre.get_stats_field(raw_stats, "unlink")
        mdt_stats.nb_mkdir    = lustre.get_stats_field(raw_stats, "mkdir")
        mdt_stats.nb_rmdir    = lustre.get_stats_field(raw_stats, "rmdir")
        mdt_stats.nb_rename   = lustre.get_stats_field(raw_stats, "rename")
        mdt_stats.nb_getattr  = lustre.get_stats_field(raw_stats, "getattr")
        mdt_stats.nb_setattr  = lustre.get_stats_field(raw_stats, "setattr")
        mdt_stats.nb_getxattr = lustre.get_stats_field(raw_stats, "getxattr")
        mdt_stats.nb_link     = lustre.get_stats_field(raw_stats, "link")
        mdt_stats.nb_statfs   = lustre.get_stats_field(raw_stats, "statfs")

        return mdt_stats
      

    def get_disk_usage(self) :
        return  [self.kbytes_total, self.kbytes_used]

    def get_inode_usage(self) :
        return  [self.inodes_total, self.inodes_used]
    
