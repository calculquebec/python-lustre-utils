# Copyright (c) 2014 . All rights reserved.
# Use of this source code is governed by the APACHE 2.0 license that can be
# found in the LICENSE file.
# Author: Frederick Lefebre <frederick.lefebvre@calculquebec.ca>

from __future__ import division
import os
import sys
import glob
import copy
from lustre import lustre

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

    # A dict with the read/write count per IO size (4K, 8K, 16K, etc)
    # The key is the IO size in 'KB'
    IO_size_KB = {}
    

    #Returns of full deep copy of self
    def clone(self) :
        newcopy = copy.deepcopy(self) 
        newcopy.IO_size_KB = copy.deepcopy(self.IO_size_KB)
        return newcopy
    


class lustre_ost :
    name = ""
    proc_path = ""

    def __init__(self, name, path) :
        self.name = name
        self.proc_path = path

    # Returns a list of devices of a given type
    # Supported types: OSC, OST, MDT
    # returns a list of lustre_device object
    @staticmethod
    def get_OSTs() :
        path = lustre.proc_path+"/obdfilter/*-OST*"
        devices = []

        for (device_name, device_path) in lustre.get_devices(type="OST") :
            devices.append(lustre_ost(name=device_name,
                                      path=device_path))
        return devices

    ##
    # return a lustre_ost_stats object filled from the /proc
    def get_stats(self) :
        stats = lustre_ost_stats()

        # Num exports
        with open(self.proc_path+"/num_exports", "r") as fd:
            stats.nb_exports = int(fd.readline())

        # Basic OST stats
        raw_stats = lustre.read_stats(self.proc_path+"/stats")
        stats.timestamp_rw = raw_stats['timestamp']
        (stats.read_count, stats.read_bytes)   = \
            lustre.get_stats_field(raw_stats, "read_bytes", "SUM")
        (stats.write_count, stats.write_bytes) = \
            lustre.get_stats_field(raw_stats, "write_bytes", "SUM")
            
        # Block IO OST stats
        try:
            with open(self.proc_path+"/brw_stats", "r") as fd:
                #This file has 7 sections
                # 1: "pages per bulk r/w"
                # 2: "discontiguous pages"
                # 3: "discontiguous blocks"
                # 4: "disk fragmented I/Os"
                # 5: "disk I/Os in flight"
                # 6: "I/O time (1/1000s)"
                # 7: "disk I/O size"
                sectionNo = 0
                data = {}
                for line in fd.readlines() :
                    #if len(line) == 0 or line.startswith('') : continue
                    if not line.strip() : continue
                    line_parts = line.split()

                    #If a line begins with a number, we assume we are in a section
                    #and we store in the appropriate array
                    if line[0].isdigit() :
                        #print "Ligne({0}): {1}".format(len(line),line)
                        #Build an array with the data from this section
                        if sectionNo not in data: data[sectionNo] = []
                        data[sectionNo].append(line_parts)
                    #Otherwise, First grab the timestamp
                    elif line_parts[0] == "snapshot_time:" :
                        stats.timestamp_brw = float(line_parts[1])
                    #Next, Identify if we are beginning a new section
                    elif line_parts[0] == "pages" :
                        sectionNo = 1
                        continue
                    elif line_parts[0] == "discontiguous" :
                        if line_parts[1] == "pages" :
                            sectionNo = 2
                        elif line_parts[1] == "blocks" :
                            sectionNo = 3
                        continue
                    elif line_parts[0] == "disk" :
                        if line_parts[1] == "fragmented" :
                            sectionNo = 4
                        elif line_parts[1] == "I/Os" :
                            sectionNo = 5
                        elif line_parts[1] == "I/O" :
                            sectionNo = 7
                        continue
                    elif line_parts[0] == "I/O" :
                        sectionNo = 6
                        continue

                #Parse actual data
                for line_parts in data[7] :
                    #Disk I/O size
                    size = int(line_parts[0][:-2])
                    if line_parts[0][-2:][:1] == 'M' :
                        size = size * 1024
                    stats.IO_size_KB[size] = {}
                    stats.IO_size_KB[size]["read"]  = long(line_parts[1])
                    stats.IO_size_KB[size]["write"] = long(line_parts[5])   
        except IOError :
            #brw_stats not found. 
            #Assume ZFS
            stats.has_brw_stats = 0
            pass

        return stats
                
    def get_disk_usage(self) :
        total = 0
        free  = 0

        #Get the total capacity from /proc
        with open(self.proc_path+"/kbytestotal", "r") as fd:
            total = long(fd.readline())

        #Get the free space from /proc
        with open(self.proc_path+"/kbytesfree", "r") as fd:
            free  = long(fd.readline())
            
        #calculate
        #return  100 - free/total*100 
        return  [total,total - free] 
            
    def get_inode_usage(self) :
        total = 0
        free  = 0

        #Get the total capacity from /proc
        with open(self.proc_path+"/filestotal", "r") as fd:
            total = long(fd.readline())

        #Get the free space from /proc
        with open(self.proc_path+"/filesfree", "r") as fd:
            free  = long(fd.readline())
            
        #calculate
        #return  100 - free/total*100 
        return  [total,total - free] 
            

