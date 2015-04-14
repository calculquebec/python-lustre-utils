# Copyright (c) 2014 . All rights reserved.
# Use of this source code is governed by the APACHE 2.0 license that can be
# found in the LICENSE file.
# Author: Frederick Lefebre <frederick.lefebvre@calculquebec.ca>

import copy

class lustre_client_stats :
    #Operation counters
    counter_list = ["open",
                    "close",
                    "readdir",
                    "setattr",
                    "truncate",
                    "getattr",
                    "create",
                    "unlink",
                    "mkdir",
                    "rmdir",
                    "rename",
                    "statfs",
                    "alloc_inode",
                    "getxattr",
                    "inode_permission"]


    def __init__(self) :
        self.timestamp    = 0.0
        self.counters = {}

        #Byte sums
        self.read_bytes     = 0
        self.write_bytes    = 0
        self.osc_read_bytes = 0
        self.osc_write_bytes= 0

        #Operation counters
        self.read_count    = 0
        self.write_count   = 0
        self.osc_read_count  = 0
        self.osc_write_count = 0

    def set_counter(self, field, value) :
        #print "Setting counter : {0} = {1}".format(field,value)
        self.counters[field] = value 

    def get_counter(self, field) :
        if field in self.counters :
            return self.counters[field]
        else :
            return 0

    def clone(self) :
        new_copy = copy.deepcopy(self)
        new_copy.counters = copy.deepcopy(self.counters)
        return new_copy
