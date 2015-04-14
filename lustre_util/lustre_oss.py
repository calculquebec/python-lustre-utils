
from __future__ import division

from lustre import lustre
from lustre_oss_stats import lustre_oss_stats

class lustre_oss :
    proc_path = "/proc/fs/lustre"

    # Returns a lustre_oss_stats object containing
    # stats for a point in time
    @staticmethod
    def get_OSS_stats() :
        oss_stats = lustre_oss_stats()
        raw_stats = lustre.read_stats(lustre.proc_path+"/ost/OSS/ost_io/stats")
        oss_stats.timestamp    = raw_stats["timestamp"]
        (oss_stats.req, oss_stats.req_waittime) = \
            lustre.get_stats_field(raw_stats, "req_waittime", "SUM")

        # Get the number of running threads
        with open(lustre.proc_path+"/ost/OSS/ost_io/threads_started", "r") as fd:
            oss_stats.nb_threads = int(fd.readline())
        return oss_stats
    
