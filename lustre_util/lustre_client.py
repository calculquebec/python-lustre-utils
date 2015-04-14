
from __future__ import division
import os.path
import glob
import re

from lustre import lustre
from lustre_client_stats import lustre_client_stats

class lustre_client :
    fs_name = ""
    name    = ""
    proc_llite_path = ""
    # List of Lustre filesystems mounted

    def __init__(self) :    
        #FS is a dict 
        #ex:
        # lustre2-3jdfkdf384 : lustre2
        # fs1-fkljfsdjie     : fs1
        self.FS = {}
        self.proc_llite_path = lustre.proc_path+"/llite"
        self._load_FS()

    def _load_FS(self) :
        _r = re.compile(r"(.*?)-.*")
        paths = glob.glob(self.proc_llite_path+"/*")
        for path in paths :
           hashed_name = os.path.basename(path)
           self.FS[hashed_name] = _r.sub(r"\1", hashed_name) 
      
        #Check that we have mounted filesystems
        if not len(self.FS) :
            #throw an exception
            raise IOError("No Lustre FS mounted")


    # Returns a lustre_oss_stats object containing
    # stats for a point in time
    def get_stats(self, fs) :
        stats = lustre_client_stats()
        raw_stats = lustre.read_stats(self.proc_llite_path+"/"+fs+"/stats")
        stats.timestamp    = raw_stats["timestamp"]

        (stats.read_count, stats.read_bytes)   = \
            lustre.get_stats_field(raw_stats, "read_bytes", "SUM")
        (stats.write_count, stats.write_bytes) = \
            lustre.get_stats_field(raw_stats, "write_bytes", "SUM")

        #https://jira.hpdd.intel.com/browse/LUDOC-220
        (stats.osc_read_count, stats.osc_read_bytes)   = \
            lustre.get_stats_field(raw_stats, "osc_read", "SUM")
        (stats.osc_write_count, stats.osc_write_bytes) = \
            lustre.get_stats_field(raw_stats, "osc_write", "SUM")

        #Don't assume a stat is present
        for field in stats.counter_list:
            stats.set_counter(
                field, 
                lustre.get_stats_field(raw_stats, field, "COUNT")
            )

        return stats

