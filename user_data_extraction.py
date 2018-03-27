import collections
import sys
import os
import subprocess

no_of_args = len(sys.argv) - 1 
default_output_file = "/home/atm423/merged_data.txt"


## ONLY FOR COMMAND LINE BASED ARGUMENTS ##
if no_of_args == 1:
 output_file = sys.argv[1]
else:
 output_file = default_output_file  

## check the python version info

if sys.version_info[0] == 2 and sys.version_info[1] < 6:  ## use only if using python version older than 2.6
 print ("detected version older than 2.6")
 input_1 = os.popen("ls -t /home/atm423/idm/iiqreports/  | head -n 1").read()
 input_2 = os.popen("ls -t /home/atm423/idm/hpc/reports/ | head -n 1").read()
else:
 print ("detected version > 2.6") ## use only if using version 2.7 or greater
 proc = subprocess.Popen("ls -t /home/atm423/idm/iiqreports/  | head -n 1", stdout=subprocess.PIPE, shell=True) 
 input_1 = proc.stdout.read()
 proc = subprocess.Popen("ls -t /home/atm423/idm/hpc/reports/ | head -n 1", stdout=subprocess.PIPE, shell=True)
 input_2 = proc.stdout.read()

if input_1 == "": ## check if input_1 is empty
 print("No file found in iiq_report folder")
 sys.exit()

if input_2 == "": ## check if input_2 is empty
 print("No file found in hpc folder")
 sys.exit()

### trim the leading newline
input_1 = input_1.strip()
input_2 = input_2.strip()


input_file1 = "/home/atm423/idm/iiqreports/" + str(input_1)
input_file2 = "/home/atm423/idm/hpc/reports/" + str(input_2)

file1 = open(input_file1,"r")
file2 = open(input_file2,"r");
file3 = open(output_file,"w")

data_map = ['nyuidn', 'Primary Affiliation', 'First Name', 'Last Name', 'HPC Sponsor NetID', 'Department1', 
            'HPC Start Date', 'HPC Disable Date', 'HPC Archive Date', 'HPC Delete Date', 'HPC End Date', 
            'HPC Status', 'Selected Shell', 'homeUnixUid', 'Univ ID', 'Lastname', 'Firstname', 'Affiliation', 
            'Account Sponsor NetID', 'Division or Affiliate Type', 'Department2', 'Affiliate Sponsor', 'HPC Account Create Date', 'HPC Account Expire Date']

file1_dict = collections.OrderedDict()
for line in file1:
 data = line.split('|')
 netid = data[0]
 data[-1] = data[-1].strip() ## remove trailing whitespaces
 file1_dict[netid] = data[1:]

file2_dict = collections.OrderedDict()
for line in file2:
 data = line.split('|')
 netid = data[0]
 data[-1] = data[-1].strip() ## remove trailing whitespaces
 file2_dict[netid] = data[1:-1]



merged_dict = collections.OrderedDict()

for key in file1_dict:
 merged_dict[key] = file1_dict[key] + file2_dict.get(key,["null","null","null","null","null","null","null","null","null","null"])

record_dict = collections.OrderedDict()

## all records are stored as a list in the dictionary, converting to dictionary of dictionaries
for key in merged_dict:
 simple_dict = collections.OrderedDict()
 record = merged_dict[key]
 for index in range( len(record) ):
   use_key = data_map[index]
   simple_dict[use_key] = record[index]
 record_dict[key] = simple_dict

## write the field manually for net id only
file3.write("NetID"  + "|")

## record write list, contains the list of record attributes we are interested in diplaying/analyzing therefore printing

record_list = [ "First Name", "Last Name" , "HPC Status", "HPC Sponsor NetID","Account Sponsor NetID" ,"Department1","Department2", "Division or Affiliate Type" ]

## write all the attributes at the top of the file [nyuid , primary affiliates , ..........]
for attributes in record_list:
 file3.write(attributes + "|")

## add a new line before writing records
file3.write("\n")

for key in record_dict:
    file3.write(key + "|")
    record = record_dict[key]
    for another_key in record_list:
        record_data = record[another_key]
	if record_data.strip() == "":
	 file3.write("null" + "|")
	else:
	 file3.write(record_data.strip() + "|")
    file3.write("\n")

print("SCRIPT SUCCESSFULLY RUN. OUTPUT WRITTEN TO " + output_file )
