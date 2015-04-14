# Copyright (c) 2014 . All rights reserved.
# Use of this source code is governed by the APACHE 2.0 license that can be
# found in the LICENSE file.
# Author: Frederick Lefebre <frederick.lefebvre@calculquebec.ca>

from __future__ import division
import os
import glob

lustre_KB = 1000

class lustre :
    proc_path = "/proc/fs/lustre"

    # Generic function to read Lustre stats files
    # Returns a dict of dict
    @staticmethod
    def read_stats(filepath) :
        stats = {}
        with open(filepath, "r") as stats_fd :
            for line in stats_fd.readlines() :
                line_parts = line.split()
                #line_parts[0] = name
                #line_parts[1] = count
                #line_parts[6] = sum
                if line_parts[0] == "snapshot_time":
                    #ignore
                    stats["timestamp"] = float(line_parts[1])
                    continue
                else:
                    if len(line_parts) > 4 :
                        stats[line_parts[0]] = { 'count': long(line_parts[1]), 'unit': line_parts[3], 'sum':long(line_parts[6]) }
                    else :
                        # We only have the count
                        stats[line_parts[0]] = { 'count': long(line_parts[1]), 'unit': line_parts[3] }
        return stats

    # Generic function to return a counter or a counter & sum
    # from raw_stats returned by lustre.read_stats (above)
    # @field : string with name of line element to read
    # @type  : COUNTER, SUM
    #         if 'SUM' an array is returned in the form [COUNTER,SUM]
    #         if 'COUNTER' only the count is returned
    @staticmethod
    def get_stats_field(raw_stats, field, type="COUNT") :
        ret = None
        try:
            if type == "COUNT" :
                ret = raw_stats[field]["count"]
            elif type == "SUM" :
                ret = (raw_stats[field]["count"], raw_stats[field]["sum"])
            else :
                raise ValueError("Unknown stats field type: {0}".format(type))
        except KeyError:
            if type == "COUNT" :
                ret = 0
            elif type == "SUM" :
                ret = (0, 0)
            pass
        return ret

    # Returns a list of devices of a given type
    # Supported types: OSC, OST, MDT
    # returns a list of lustre_device object
    @staticmethod
    def get_devices(type=None, fs=None) :
        path = ""
        if not fs or len(fs) == 0 :
            fs = "*"
        if type == "OST":
            path = lustre.proc_path+"/obdfilter/*-OST*"
        elif type == "MDT":
            path = lustre.proc_path+"/mdt/*-MDT*"
        else:
            raise ValueError("Unknown Lustre device type: {0}".format(type))
        devices = []

        for device_path in glob.glob(path):
            devices.append([os.path.basename(device_path), device_path])
        return devices
            
    @staticmethod
    def get_version():
        with open(lustre.proc_path+"/version", "r") as fd:
            return fd.readline().split()[1]

    @staticmethod
    def get_nb_clients(dev_proc_path) :
        nb_exports = 0
        non_clients = 0
        with open(dev_proc_path+"/num_exports", "r") as fd :
            nb_exports = int(fd.readline())
        # The number of exports contains OSTs and MDTs...
        # We should count and substract them
        #uuid_files = glob.glob(dev_proc_path+"/exports/*/uuid")
        #for uuid_file in uuid_files :
        #    with open(uuid_file, "r") as fd :
        #        client_uuid = fd.readline()
        #    print "client_uuid = {0}".format(client_uuid)

        return nb_exports - non_clients
                


        

        

