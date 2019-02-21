from netCDF4 import Dataset
import os.path
import sys
import json
import numpy as np
import math
import random

	
def check_args():

	#	Executable (first arg) and input file name (second arg)

	if len(sys.argv) != 2:
		print " "
	 	print 'Usage: ' + sys.argv[0] + ' <JSON_info_file> '
	 	print " "
	 	sys.exit(1)
	 	
	#	Does the input file actually exist?

	for file in range(1,len(sys.argv)):
		if os.path.exists(sys.argv[file]):
	 		print 'Found ' + sys.argv[file]
			print ' '
	 	else:
	 		print " "
	 		print 'File does not exist: ' + sys.argv[file]
	 		print " "
	 		sys.exit(file)



def read_input_json():

	#	Pull in the JSON info file
	
	for file in range(1,len(sys.argv)):
		print 'File ' + str(file) + ': ' + sys.argv[file]
	 	print " "
	
		#	Get the setup for the ANOVA from the JSON input file
	
		fp = sys.argv[file]
		print 'FP: File = ' + fp
		with open(fp, "r") as read_file:
			data = json.load(read_file)
	
	#	Raw dump of the input JSON file, mostly for debugging
	
	if data["debug"]:
		print json.dumps(data, sort_keys=True, indent=4)

	#	Return the JSON file information

	return data



def init_names_and_numbers(data):

	#	Print the initial comment, so we know what is going on
	
	print data["_comment_"]
	print ( " " )
	
	#	Assignment of filenames from the input JSON file
	
	root = data["mpas_root"]
	tail = data["mpas_tail"]
	obs = data["num_points_per_region"]
	
	#	Clear out some strings for the factor names
	
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
	print ("Initialization file: " + data["init_file"] )
	if os.path.exists(data["init_file"]):
 		print 'Found ' + data["init_file"]
		print ' '
 	else:
 		print " "
 		print 'File does not exist: ' + data["init_file"]
 		print " "
 		sys.exit(data["init_file"])

	print ("MPAS root:           " + root )
	print ("MPAS tail:           " + tail )
	
	print ("Number of sampled measurements per geographical region = " + str(data["num_points_per_region"]) + "\n" )
	
	#	Get the local names for the regions we will be testing.
	
	regions = len(data['design'][0]['levels'])
	names = np.empty((regions,100), dtype=str)
	str_len = np.empty(regions, dtype=int)
	r=0
	while r < regions :
		str_len[r] = len(data['design'][0]['levels'][r])
		s=0
		while s < str_len[r] :
			names[r][s] = data['design'][0]['levels'][r][s]
			s = s + 1
		r = r + 1
	
	#	Get the local region lat lon box limits.
	
	min_lat = data["min_lat_box_degrees"]
	max_lat = data["max_lat_box_degrees"]
	min_lon = data["min_lon_box_degrees"]
	max_lon = data["max_lon_box_degrees"]
	
	#	How many fields are we processing? The fields are separate. For example,
	#	a theta field's results would not be used in any of the statistics for
	#	a u field's results.
	
	num_fields = len(data['compare'])
	
	#	We initialize our count of how many of the points in each
	#	field match our random criteria. Also, same size, initialize
	#	the count of values within each region for each field.
	
	count            = np.zeros([num_fields,regions],dtype=int)
	contains_in_each = np.zeros([num_fields,regions],dtype=int)
	
	#	We eventually want data[observation] number of measurements 
	#	within each box. We first randomly thin down to "want_in_each".
	
	want_in_each = 50.
	
	#	Allocate space and initialize the field horizontal and vertical 
	#	dimensions, and the vertical level for comparison for each
	#	field.
	
	fields_hdim = np.empty(num_fields,dtype=int)
	fields_vdim = np.empty(num_fields,dtype=int)
	v_lev = np.empty(num_fields,dtype=int)
	
	#	Make a list for the field names. If the field names are longer than 32 characters,
	#	then we'd bump up that 32 thing.
	
	fields = [[' '] * 32 for i in range(num_fields)]
	
	#	How many locations are there
	
	l=0
	while l < len(data['design']) :
		if data['design'][l]['factor'] == "LOCATIONS" :
			locations = len(data['design'][l]['levels'])
			break
		l = l + 1
	
	#	Allocate space for indexes. This is the location in the MPAS file. We are
	#	partitioning this into an array that has a fixed number of grid cells
	#	that are selected per region, the number of regions, and the total number
	#	of fields that are being tested. We HUGELY over allocate the possible index
	#	array as we end up doing a couple of random things (literally) to finally
	#	get down to our requested index set.
	
	indexes          = np.empty((num_fields, locations,   obs),dtype=np.int)
	possible_indexes = np.empty((num_fields, locations, 5*obs),dtype=np.int)
	
	#	Repeatable random sequences, PLEASE!
	
	random.seed(data["random_seed"])
	
	#	Open up the text-based output file that has the per-region 
	#	info explicitly detailed.
	
	rfile = open("region_lat_lon.txt", "w")
	
	return root, tail , obs, factor, lev, max_fac, max_lev, levels, lenny, regions, names, str_len, min_lat, max_lat, min_lon, max_lon, num_fields, count, contains_in_each, want_in_each, fields_hdim, fields_vdim, v_lev, fields, indexes, possible_indexes, rfile




def get_lat_lon_box_info(data, root, tail , obs, factor, lev, max_fac, max_lev, levels, lenny, regions, names, str_len, min_lat, max_lat, min_lon, max_lon, num_fields, count, contains_in_each, want_in_each, fields_hdim, fields_vdim, v_lev, fields, indexes, possible_indexes, rfile):

	#	We difference with this IC file
	
	o = Dataset(data["init_file"])
	
	#	Fill in the field names and dimensions, and the vertical level that is
	#	selected for the 3d field comparison.
	
	for f in range(num_fields):
		fields[f] = list(data['compare'][f]['field'])
		fields_hdim[f] = o.variables[data['compare'][f]['field']].shape[1]
		fields_vdim[f] = o.variables[data['compare'][f]['field']].shape[2]
		v_lev[f] = data['compare'][f]['v_lev_0_based']
	
	lat_cell_dim_size = o.variables['latCell'].shape[0]
	lat_edge_dim_size = o.variables['latEdge'].shape[0]
	
	#	Loop over all of the requested fields
	
	n=0
	while n < num_fields :
	
		#	The IC has the lat lon fields, which we use to select boxes.
		#	Get the correct lat/lon for this variable, and convert to degrees.
		#	The longitude is modifed to be: -180 < lon <= 180
	
		if   fields_hdim[n] == lat_cell_dim_size :
			print ("doing cell_size lat lon")
			lat = o.variables["latCell"][:] * 180. / math.pi
			lon = o.variables["lonCell"][:] * 180. / math.pi
			for i in range(len(lon)):
				if lon[i] > 180:
					lon[i] = lon[i] - 360.
		elif fields_hdim[n] == lat_edge_dim_size :
			print ("doing edge_size lat lon")
			lat = o.variables["latEdge"][:] * 180. / math.pi
			lon = o.variables["lonEdge"][:] * 180. / math.pi
			for i in range(len(lon)):
				if lon[i] > 180:
					lon[i] = lon[i] - 360.
	
		#	Loop over the total horizontal dimension (places) for this field.
	
		p=0
		while p < fields_hdim[n] :
		
			#	Loop over the number of locations (regions that we requested)
		
			l=0
			while l < regions :
		
				#	For this data value, check to see if we are inside of the 
				#	lat lon box for this region / location
		
				if ( lat[p] >= min_lat[l] ) and ( lat[p] < max_lat[l] ) and \
				   ( lon[p] >= min_lon[l] ) and ( lon[p] < max_lon[l] ) :
					contains_in_each[n,l] = contains_in_each[n,l] + 1
	
				l = l + 1
			p = p + 1
	
		#	Loop over the total horizontal dimension (places) for this field.
	
		p=0
		while p < fields_hdim[n] :
		
			#	Loop over the number of locations (regions that we requested)
		
			l=0
			while l < regions :
		
				#	For this data value, check to see if we are inside of the 
				#	lat lon box for this region / location
		
				joe_count = 0
				if ( lat[p] >= min_lat[l] ) and ( lat[p] < max_lat[l] ) and \
				   ( lon[p] >= min_lon[l] ) and ( lon[p] < max_lon[l] ) :
			
					#	Randomly decide: do we take this location based on 
					#	whether the random number is <= the ratio of values
					#	that we want to the number of values we have in this 
					#	lat lon box for this specific location. We have made the
					#	possible dimension twice what we want, to allow some 
					#	random slop.
		
					rr = random.uniform(0.,1.)
					if rr <= want_in_each / contains_in_each[n,l] :
						possible_indexes[n,l,count[n,l]] = p
						count[n,l] = count[n,l] + 1
				l = l + 1
			p = p + 1
	
		#	We now have sufficient points that were randomly chosen, dimensioned to 5* # obs requested,
		#	but we have approximately half that number by design, so we did not over run
		#	our allocated space. From these "approximately half a hundred" points, we 
		#	apply our second randomizer.
	
		#	Loop over each region
	
		l=0
		while l < regions :

			#	Which field and which region

			rfile.write( "CHECK " + "".join(fields[n]) + " field for domain " + "".join(names[l][0:str_len[l]]) + "\n")
		
			#	Choosing requested number from initial count
		
			rfile.write("Choosing " + str(obs) + " out of " + str(count[n,l]) + " values\n")
			my_list = list(xrange(0,count[n,l]))
			random.shuffle(my_list)
		
			#	From these super-duper random points, choose the first set that is
			#	the size of the sample of measurements per geophysical grid box location.
		
			i = 0
			while i < data["num_points_per_region"] :
				indexes[n,l,i] = possible_indexes[n,l,my_list[i]]
				rfile.write ("lat = " + str(lat[indexes[n,l,i]]) + ", lon = " + str(lon[indexes[n,l,i]]) + "\n")
				i = i + 1
			rfile.write ( "\n" )
			l = l + 1
		n = n + 1
	
	print ("\nData to verify the regions by lat lon locations is output to region_lat_lon.txt\n")
	return o, lat, lon, indexes



def diffs_for_anova(data,num_fields,fields,max_fac,obs,factor,root,tail,regions,indexes,v_lev,o):

	#	Loop over all of the requested fields
	
	n=0
	while n < num_fields :
	
		#	Now we are generating data for the ANOVA test, for a specific variable.
		
		file = open("".join(fields[n]) + ".txt", "w")
		
		#	How many factors are we processing
		
		file.write(str(max_fac) + "\n")
		
		#	List those factors
		
		for fac in range(0,max_fac):
			file.write(data['design'][fac]['factor'] + "\n")
		
		#	How many levels per each factor
		
		for fac in range(0,max_fac):
			file.write(str(len(data['design'][fac]['levels'])) + "\n")
		
		#	What are the names of those levels (for each factor)
		
		for fac in range(0,max_fac):
			for lev in range(0,len(data['design'][fac]['levels'][:])):
				file.write(data['design'][fac]['levels'][lev] + "\n")
		
		#	How many samples for each of the bins (for example, in this compiler x region x time sample)
		
		file.write(str(obs)+ "\n")
		
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
		
								#	The above looping and if tests get us to where we can open a 
								#	particular MPAS netcdf file with the name. The files are 
								#	separated into distinct time periods and also have a naming
								#	convention that tells us which compiler was used to construct
								#	the data.
	
								#	Once we have the file (a function of the compiler test and the time), 
								#	we can difference the specific fields,
								#	for each of the requested geophysical lat lon boxes, 
								#	for value locations that were randomly**2 chosen.
	
								print ("File name to open = " + fname )
								f = Dataset(fname)
		
								#	For particular geophysical regions. The init files and the validation files
								#	have the same matching grid distribution. We have chosen the lat lons from the 
								#	init file. Using those randomly selected indices, we do some differencing. These
								#	differences we would expect to have mean zero.
		
								l=0
								while l < regions :
	
									i = 0
									while i < data["num_points_per_region"] :
										file.write(str( \
										              '{:.16e}'.format( \
										               f.variables["".join(fields[n])][0,indexes[n,l,i],v_lev[n]] - \
									                       o.variables["".join(fields[n])][0,indexes[n,l,i],v_lev[n]] \
										              ) \
										              ) + "\n")
										i = i + 1
									l = l + 1
		
		print ('\nInput for ANOVA for field ' + "".join(fields[n]) + ': ' + "".join(fields[n]) + '.txt\n')
		n = n + 1
	

def main():

	check_args()
	data = read_input_json()
	root, tail , obs, factor, lev, max_fac, max_lev, levels, lenny, regions, names, str_len, min_lat, max_lat, min_lon, max_lon, num_fields, count, contains_in_each, want_in_each, fields_hdim, fields_vdim, v_lev, fields, indexes, possible_indexes, rfile = init_names_and_numbers(data)
	o, lat, lon, indexes = get_lat_lon_box_info(data, root, tail , obs, factor, lev, max_fac, max_lev, levels, lenny, regions, names, str_len, min_lat, max_lat, min_lon, max_lon, num_fields, count, contains_in_each, want_in_each, fields_hdim, fields_vdim, v_lev, fields, indexes, possible_indexes, rfile)
	diffs_for_anova(data,num_fields,fields,max_fac,obs,factor,root,tail,regions,indexes,v_lev,o)
	#sys.exit(1)
	#os.system('ls')
	sys.exit(0)


if __name__ == "__main__":
	main()
