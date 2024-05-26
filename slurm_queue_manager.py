#!/bin/python
import os
import io
import subprocess
import re
import time
from datetime import datetime

def getSlurmStatus(slurm_command):
  mydict = [] 
  # probe slurm
  command_list = slurm_command.split()

  proc = subprocess.Popen(command_list, stdout=subprocess.PIPE)
  for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):  # or another encoding
    # do something with line
#    print("got line ",line)
    if (len(line.split())!=9):
#            print("DISCARDING LINE",line)
            continue
    if (re.search("PARTITION",line) != None and re.search("STATE",line) != None):
#            print("DISCARDING LINE",line)
            continue
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
        if (d['state'] == "RUNNING"):
                running = running + 1
        if (d['state'] == "PENDING"):
                pending = pending + 1
    return (running, pending)


# single job executor
jobexecutor = "./slurm_glidein.job"

#logprefix
log_prefix = "job_log_"

#this is the name used to identify these jobs
jobname = "CMS_GLIDEIN"

#limits!
# max_runnig, max_idle, min_idle
max_running = 10
max_idle = 5

#command to get list of job
slurm_command = "squeue -l -n "+jobname+" --me"

print ("===== Configured with:")
print ("Slurm command",slurm_command)
print ("Max_Running",max_running)
print ("Max_Pending",max_idle)
print ("Job Executor",jobexecutor)
print ("Log Prefix",log_prefix)
print ("SLURMO Job Name",jobname)

while (True):
 jobs_dict = getSlurmStatus(slurm_command)

 (running,pending) = analyze_jobs(jobs_dict)
 
 print ("=== Date: "+str(datetime.now()))
 print ("(running, pending) = ("+str(running)+","+str(pending)+")")
 if (running < max_running and pending< max_idle):
        # start new jobs 
        jobs_to_start = min(max_running-running,max_idle-pending)
        print ("Starting "+ str(jobs_to_start)+ " jobs.")
        for j in range(0,jobs_to_start):
            num = int(time.time())
            jname = log_prefix+str(num)
            cmd = jobexecutor + " >& " + jname
            os.system(cmd+ " &")
#            subprocess.Popen(cmd.split(), close_fds=True)

            print ('Submitted job '+jname)
            time.sleep(1.2)
 time.sleep(20)
#


