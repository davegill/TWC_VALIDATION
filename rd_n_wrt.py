from netCDF4 import Dataset

import os.path
import sys
import json
import numpy as np
import math
import random

	
if len(sys.argv) != 2:
	print " "
 	print 'Usage: ' + sys.argv[0] + ' <JSON_info_file> '
 	print " "
 	sys.exit(1)
 	
for file in range(1,len(sys.argv)):
	if os.path.exists(sys.argv[file]):
 		print 'Found ' + sys.argv[file]
 	else:
 		print " "
 		print 'File does not exist: ' + sys.argv[file]
 		print " "
 		sys.exit(file)

print ' '

#	Pull in the JSON info file

for file in range(1,len(sys.argv)):
	print 'File ' + str(file) + ': ' + sys.argv[file]
 	print " "

#	Get the setup for the ANOVA from the JSON input file

fp = sys.argv[file]
with open(fp, "r") as read_file:
	data = json.load(read_file)

#	Raw dump of the input JSON file, mostly for debugging

#print json.dumps(data, sort_keys=True, indent=4)

#	Print the initial comment, so we know what is going on

print data["_comment_"]
print ( " " )

#	Assignment of filenames from the input JSON file

out_files = data["mpas_output"][:]
root = data["mpas_root"]
tail = data["mpas_tail"]
ic = data["init_file"]
obs = data["observations"]

#	How many factors are we handling

factor = np.empty(len(data['design'][:])+1, dtype=str)

#	Each factor has a different number of levels, but they are all less than 10

lev = np.empty(10, dtype=int)

#	How many factors are we processing

max_fac = len(data['design'][:])
print ("Number of factors = " + str(max_fac) + "\n" )

#	For each factor, how many levels are we handling

for fac in range(0,max_fac):
	lev[fac] = len(data['design'][fac]['levels'])
	print ( "Factor #" + str(fac+1) + ": Number of levels = " + str(lev[fac] ))

#	Save the max number of levels that we need to process

max_lev = max(lev)

#	Another "larger than required" array of the levels
#	No more than 10 levels, and no more than 5 factors

levels = [[[] for j in range(10)] for i in range(5)]
lenny = np.empty([5, 10], dtype=int)

#	Loop over the max number of factors

for fac in range(0,max_fac):

	#	Assign the factor name

	print "\n" + data['design'][fac]['factor']
	factor[fac] = data['design'][fac]['factor']

	#	For this factor, loop over all levels

	for lev in range(0,len(data['design'][fac]['levels'][:])):
		print ("factor #" + str(fac+1) + " = " + data['design'][fac]['factor'] + \
		", level #" + str(lev+1) + " =  " + data['design'][fac]['levels'][lev])

		#	Assign the level name

		lenny[fac][lev] = len(data['design'][fac]['levels'][lev])
 		levels[fac][lev][0:lenny[fac][lev]] = data['design'][fac]['levels'][lev]
		print "".join(levels[fac][lev][0:lenny[fac][lev]])

print ("\nMPAS files")
#for inp_file in range(len(data["mpas_output"])): 
#	print data["mpas_output"][inp_file]
print ("Initialization file: " + data["init_file"] )
print ("MPAS root:           " + root )
print ("MPAS tail:           " + tail )

print ("Number of sampled measurements per geographical region = " + str(data["observations"]) + "\n" )

#	We difference with this IC file

o = Dataset(data["init_file"])

#	The IC has the lat lon fields, which we use to select boxes.
#	We need a separate lat/lon for u and theta.
#	The longitude is modifed to be degrees, -180 to 180

lat_theta = o.variables["latCell"][:] * 180. / math.pi
lon_theta = o.variables["lonCell"][:] * 180. / math.pi
for i in range(len(lon_theta)):
	if lon_theta[i] > 180:
		lon_theta[i] = lon_theta[i] - 360.

lat_u = o.variables["latEdge"][:] * 180. / math.pi
lon_u = o.variables["lonEdge"][:] * 180. / math.pi
for i in range(len(lon_u)):
	if lon_u[i] > 180:
		lon_u[i] = lon_u[i] - 360.

#	Get the local names for the regions we will be testing.

regions = len(data['design'][0]['names'])
names = np.empty((regions,100), dtype=str)
str_len = np.empty(regions, dtype=int)
r=0
while r < regions :
	str_len[r] = len(data['design'][0]['names'][r])
	s=0
	while s < str_len[r] :
		names[r][s] = data['design'][0]['names'][r][s]
		s = s + 1
	#print (str(r+1) + " " + "".join(names[r][0:str_len[r]]) )
	r = r + 1

#	Get the local region lat lon box limits.

min_lat = data["min_lat_box"]
max_lat = data["max_lat_box"]
min_lon = data["min_lon_box"]
max_lon = data["max_lon_box"]

#	We initialize our count of how many theta and u points
#	match our random number criteria, which is used for the
#	final selection.

count_theta = [ 0, 0, 0, 0, 0, 0, 0 ]
count_u     = [ 0, 0, 0, 0, 0, 0, 0 ]

#	We could first count these guys, but let's be expeditious
#	number of theta or u data points, respectively.

contains_in_each_theta = ( 109., 586., 184., 304., 166., 80., 125. )
contains_in_each_u     = ( 329., 1748., 559., 923., 501., 234., 380. )

#	We eventually want data[observation] number of measurements 
#	within each box. We first randomly thin down to "want_in_each".

want_in_each = 50.

#	We should get this out of the netcdf file instead

total_theta =  40962
total_u     = 122880

possible_indexes_theta = np.empty((7, 100),dtype=np.int)
possible_indexes_u     = np.empty((7, 100),dtype=np.int)
indexes_theta          = np.empty((7,  20),dtype=np.int)
indexes_u              = np.empty((7,  20),dtype=np.int)

#	Repeatable random sequences, PLEASE!

random.seed(9001)

#	Loop over all of the theta points

p=0
while p <= total_theta-1 :

	#	Loop over the number of locations

	l=0
	while l <= len(min_lat)-1 :

		#	For this data value, check to see if we are inside of the lat lon box for this location

		if ( lat_theta[p] >= min_lat[l] ) and ( lat_theta[p] < max_lat[l] ) and ( lon_theta[p] >= min_lon[l] ) and ( lon_theta[p] < max_lon[l] ) :
	
			#	Randomly decide: do we take this location based on 
			#	whether the random number is <= the ratio of values
			#	that we want to the number of values we have in this 
			#	lat lon box for this specific location. We have made the
			#	possible dimension twice what we want, to allow some 
			#	random slop.

			rr = random.uniform(0.,1.)
#		if random.uniform(0.,1.) <= want_in_each / contains_in_each_theta[l] :
			if rr <= want_in_each / contains_in_each_theta[l] :
				possible_indexes_theta[l,count_theta[l]] = p # +1 if fortran indexing
				count_theta[l] = count_theta[l] + 1
		l = l + 1
	p = p + 1

#	Loop over all of the u points, identical procedure

p=0
while p <= total_u-1 :
	l=0
	while l <= len(min_lat)-1 :
		if ( lat_u[p] >= min_lat[l] ) and ( lat_u[p] < max_lat[l] ) and ( lon_u[p] >= min_lon[l] ) and ( lon_u[p] < max_lon[l] ) :
			if random.uniform(0.,1.) <= want_in_each / contains_in_each_u[l] :
				possible_indexes_u[l,count_u[l]] = p # +1 if fortran indexing
				count_u[l] = count_u[l] + 1
		l = l + 1
	p = p + 1


#	Open up the file that has the region info explicitly detailed.

rfile = open("region_lat_lon.txt", "w")

#	We now have sufficient points that were randomly chosen, dimensioned to 100,
#	but we have approximately half that number by design, so we did not over run
#	our allocated space. From these "approximately half a hundred" points, we 
#	apply our second randomizer.

l=0
while l < len(min_lat) :
	rfile.write( "CHECK " + "".join(names[l][0:str_len[l]]) + "\n")

	#	First for theta

	rfile.write(str(count_theta[l]) + "\n")
	my_list = list(xrange(0,count_theta[l]))
	random.shuffle(my_list)

	#	From these super-duper random points, choose the first set that is
	#	the size of the sample of measurements per geophysical grid box location.

	i = 0
	while i < data["observations"] :
		indexes_theta[l,i] = possible_indexes_theta[l,my_list[i]]
		rfile.write ("lat = " + str(lat_theta[indexes_theta[l,i]]) + ", lon = " + str(lon_theta[indexes_theta[l,i]]) + "\n")
		i = i + 1
	rfile.write ( "\n" )

	#	Now, we repeat the selection for the u values.

	rfile.write(str(count_u[l]) + "\n")
	my_list = list(xrange(0,count_u[l]))
	random.shuffle(my_list)
	i = 0
	while i < data["observations"] :
		indexes_u[l,i] = possible_indexes_u[l,my_list[i]]
		rfile.write("l i = " + str(l)  + " " + str(i) + " " + "lat = " + "index = " + str(indexes_u[l,i]) + " " + str(lat_u[indexes_u[l,i]]) + ", lon = " + str(lon_u[indexes_u[l,i]]) + "\n")
		i = i + 1
	l = l + 1

print ("\nData to verify the region lat lons: region_lat_lon.txt\n")

#	Now we are generating data for the ANOVA test.

tfile = open("theta.txt", "w")
ufile = open("u.txt", "w")

#	How many factors are we processing

tfile.write(str(max_fac) + "\n")
ufile.write(str(max_fac) + "\n")

#	List those factors

for fac in range(0,max_fac):
	tfile.write(data['design'][fac]['factor'] + "\n")
	ufile.write(data['design'][fac]['factor'] + "\n")

#	How many levels per each factor

for fac in range(0,max_fac):
	tfile.write(str(len(data['design'][fac]['levels'])) + "\n")
	ufile.write(str(len(data['design'][fac]['levels'])) + "\n")

#	What are the names of those levels (for each factor)

for fac in range(0,max_fac):
	for lev in range(0,len(data['design'][fac]['levels'][:])):
		tfile.write(data['design'][fac]['levels'][lev] + "\n")
		ufile.write(data['design'][fac]['levels'][lev] + "\n")

#	How many samples per region, compiler, time

tfile.write(str(obs)+ "\n")
ufile.write(str(obs)+ "\n")

#	Only care about two fields: theta and u

importantVars = [ 'u', 'theta' ]

#	Loop over the variables of interest.

for v in importantVars:

	#	Loop over each of the primary factors, find the TIME

	for fac_t in range(0,max_fac):

		#	TIME factor

		if factor[fac_t] == "T" :

			#	Loop over each level of the TIME factor

			for lev_t in range(0,len(data['design'][fac_t]['levels'][:])):

				#	Keep this level string for TIME, it is part of the file name
				
				time = data['design'][fac_t]['levels'][lev_t]
	
				#	Loop over each of the primary factors, find the COMPILER

				for fac_c in range(0,max_fac):

					#	COMPILER factor

					if factor[fac_c] == "C" :

						#	Loop over each level of the COMPILER factor

						for lev_c in range(0,len(data['design'][fac_c]['levels'][:])):

							#	Keep this level string for COMPILER, also part of the file name.

							comp = data['design'][fac_c]['levels'][lev_c]
	
							#	Construct the filename with the TIME and COMPILER info
	
							fname = root + "." + time + "_" + comp + tail
							#print (" filename = " + fname )
	
							#	The above looping and if tests get us to where we can open a 
							#	particular MPAS netcdf file with the name. The files are 
							#	separated into distinct time periods and also have a naming
							#	convention that tells us which compiler was used to construct
							#	the data.

							#	Once we have the file, we can difference the two specific fields
							#	(theta and u), for each of the requested geophysical lat lon boxes, 
							#	for grid locations that were randomly**2 chosen.
							# 	

							f = Dataset(fname)
	
							#	For particular geophysical regions. The init files and the validation files
							#	have the same matching grid distribution. We have chosen the lat lons from the 
							#	init file. Using those randomly selected indices, we do some differencing. These
							#	differences we would expect to have mean zero.
	
							l=0
							while l <= len(min_lat)-1 :

								#	theta

								if v == 'theta' :
									i = 0
									while i < data["observations"] :
										#print f.variables[v][0,indexes_theta[l,i],0] - o.variables[v][0,indexes_theta[l,i],0]
										tfile.write(str(f.variables[v][0,indexes_theta[l,i],0] - o.variables[v][0,indexes_theta[l,i],0]) + "\n")
										i = i + 1
								
								#	u

								else :
									i = 0
									while i < data["observations"] :
										#print f.variables[v][0,indexes_u[l,i],0] - o.variables[v][0,indexes_u[l,i],0]
 										ufile.write(str(f.variables[v][0,indexes_u[l,i],0] - o.variables[v][0,indexes_u[l,i],0]) + "\n")
										i = i + 1
								l = l + 1
	

print ("Input for ANOVA for theta: theta.txt\n")
print ("Input for ANOVA for u:     u.txt\n")      
sys.exit(0)
