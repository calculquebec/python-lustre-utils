
from __future__ import division
import os.path

from lustre import lustre
from lustre_mds_stats import lustre_mds_stats
from lustre_mdt import lustre_mdt

class lustre_mds :
    fs_name = ""
    name    = ""
    proc_path = "/proc/fs/lustre"
    proc_lov_path = ""
    proc_osd_path = proc_path+"/osd-ldiskfs"
    MDTs = []

    def __init__(self, fs, name=None) :    
        self.fs_name = fs
        self.name    = name
        self.proc_lov_path = self.proc_path+"/lov/"+self.fs_name+"-mdtlov"
        self._load_MDTs()

        #Find the correct path for the MDS stats
        #It changed somewhere after 2.1
        #See: https://jira.hpdd.intel.com/browse/LU-2375
        if (os.path.exists(lustre.proc_path+"/mds/MDS")) :
            #current
            self.stats_dir = lustre.proc_path+"/mds/MDS/mdt"
        else :
            #older
            self.stats_dir = lustre.proc_path+"/mdt/"+self.MDTs[0].name+"/mdt"

    def _load_MDTs(self) :
        self.MDTs = []
        for device_name, device_path in lustre.get_devices("MDT", self.fs_name) :
            self.MDTs.append(lustre_mdt(device_name))
      
        #Check that we have local MDTs
        if not len(self.MDTs) :
            #throw an exception
            raise IOError("No MDTs configured")

    # Returns a lustre_oss_stats object containing
    # stats for a point in time
    def get_stats(self) :
        mds_stats = lustre_mds_stats()
        raw_stats = lustre.read_stats(self.stats_dir+"/stats")
        mds_stats.timestamp    = raw_stats["timestamp"]
        (mds_stats.req, mds_stats.req_waittime) = \
            lustre.get_stats_field(raw_stats, "req_waittime", "SUM")

        # Get the number of running threads
        with open(self.stats_dir+"/threads_started", "r") as fd:
            mds_stats.nb_threads = int(fd.readline())
        return mds_stats

