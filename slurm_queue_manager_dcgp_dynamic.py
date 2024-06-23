#!/bin/python
import os
import io
import subprocess
import re
import time
from datetime import datetime
import json

def getSlurmStatus(slurm_command):
  mydict = [] 
  # probe slurm
  command_list = slurm_command.split()

  proc = subprocess.Popen(command_list, stdout=subprocess.PIPE)
  for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):  # or another encoding
    # do something with line
#    print("got line ",line)
    line=line.replace("(ReqNodeNotAvail, Reserved for maintenance)","Maintenance")
    if (len(line.split())!=9):
#            print("DISCARDING LINE",line)
            continue
    if (re.search("PARTITION",line) != None and re.search("STATE",line) != None):
#            print("DISCARDING LINE",line)
            continue
#    print (line.split())
    (number,partition,name,user,state,time,time_limit,nodes,nodelist) = line.split() 
    job = {}
    job["jobid"]=int(number)
    job["partition"] = partition
    job["name"]=name
    job["user"]=user
    job["state"]=state
    job["time"]=time
    job["time_limit"]=time_limit
    job["numnodes"]=int(nodes)
    job["nodelist"] = nodelist
    mydict.append(job)
  return (mydict)

def analyze_jobs(jdict):
    running=0
    pending=0

    for d in jdict:
  #      print (jdict)
        if (d['state'] == "RUNNING"):
                running = running + 1
        if (d['state'] == "PENDING"):
#                print ("add pending")
                pending = pending + 1
    return (running, pending)
# read json
f = open('dcgp.json') 

# returns JSON object as  
# a dictionary 
conf = json.load(f) 
f.close()

#print ("CONF ", conf)

#command to get list of job
slurm_command = "squeue -l -n "+conf["jobname"]+" --me"

print ("===== Initially configured with:")
print ("Slurm command",slurm_command)
print ("Max_Running",conf["max_running"])
print ("Max_Pending",conf["max_idle"])
print ("Job Executor",conf["jobexecutor"])
print ("Log Prefix",conf["log_prefix"])
print ("Operate at max for hours ",conf["max_hours"])
print ("SLURM Job Name",conf["jobname"])

count=0

while (count < conf["max_hours"]*(3600./20)):

 count = count + 1
 
 jobs_dict = getSlurmStatus(slurm_command)

 (running,pending) = analyze_jobs(jobs_dict)
 
 print ("=== Date: "+str(datetime.now()))
 print ("(running, pending) = ("+str(running)+","+str(pending)+")")
 if (running < conf["max_running"] and pending< conf["max_idle"]):
        # start new jobs 
        jobs_to_start = min(conf["max_running"]-running,conf["max_idle"]-pending)
        print ("Starting "+ str(jobs_to_start)+ " jobs.")
        for j in range(0,jobs_to_start):
            num = int(time.time())
            jname = conf["log_prefix"]+str(num)
            cmd = conf["jobexecutor"] + " >& " + jname
            os.system(cmd+ " &")
#            subprocess.Popen(cmd.split(), close_fds=True)

            print ('Submitted job '+jname)
            time.sleep(1.2)
 time.sleep(20)
 #reload conf!
 # read json
 f = open('dcgp.json')

 # returns JSON object as
 # a dictionary
 conf = json.load(f)
 print ("Current Max_Running",conf["max_running"])
 print ("Current Max_Pending",conf["max_idle"])
 f.close() 
 #


