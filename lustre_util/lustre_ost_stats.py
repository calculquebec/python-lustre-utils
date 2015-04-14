# Copyright (c) 2014 . All rights reserved.
# Use of this source code is governed by the APACHE 2.0 license that can be
# found in the LICENSE file.
# Author: Frederick Lefebre <frederick.lefebvre@calculquebec.ca>

import copy

class lustre_ost_stats :
    timestamp_rw = 0.0
    timestamp_brw  = 0.0
    read_bytes     = 0
    write_bytes    = 0
    nb_exports     = 0
    
    #Operation counters
    read_count    = 0
    write_count   = 0
    create_count  = 0
    destroy_count = 0
    setattr_count = 0
    punch_count   = 0
    statfs_count  = 0

    
    def __init__(self) :
        # ZFS systems are missing brw_stats (for now)
        # https://jira.hpdd.intel.com/browse/LU-4259
        self.has_brw_stats = "yes"

        # A dict with the read/write count per IO size (4K, 8K, 16K, etc)
        # The key is the IO size in 'KB'
        self.IO_size_KB = {}
    

    #Returns of full deep copy of self
    def clone(self) :
        newcopy = copy.deepcopy(self) 
        newcopy.IO_size_KB = copy.deepcopy(self.IO_size_KB)
        return newcopy
    


