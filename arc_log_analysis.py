import sys
import re
from fractions import Fraction

def main():
	if len(sys.argv)!=2:
		print "Usage:python %s <file>" % sys.argv[0]
		sys.exit(0)
	else:
		inputFile=open(sys.argv[1],'r').readlines()
		out_name=str(sys.argv[1]) + ".values"
		data=read_log(inputFile)
		outFile=open(out_name, 'w')
		outFile.write(read_log(inputFile))
		outFile.close()
		outVal=ext_vals(out_name)
		calc_vals(outVal[0],outVal[1],outVal[2],outVal[3],data)

def read_log(input):
	raw_data=''
	for line in input:
		if 'HT=' in line:
			xl_line=line.split('{')
			raw_data+=xl_line[1].strip('}\n') + '\n'
	
	return raw_data

def ext_vals(input):
	raw_data=open(input,'r').readlines()
	n_line=0
	cache_vals=[]
	tput_vals=[]
	for line in raw_data:
		n_line+=1
		vals=line.split(',')
		cache=int(vals[0].strip('C='))
		tput=float(vals[5].strip(' T='))
		tput_vals.append(tput)
		cache_vals.append(cache)
	return n_line, cache_vals.count(0), max(cache_vals), max(tput_vals)


def calc_vals(n_lines,zero_cache,max_cache,max_tput,input):
		max_cache_patt=re.compile('(?:.*' + str(max_cache) + '.*)')
		max_tput_patt=re.compile('(?:.*' + str(int(max_tput)) + '.*)')
		c_maxt=re.findall(max_tput_patt, input)
		t_maxc=re.findall(max_cache_patt, input)
		c_maxt_val=0
		t_maxx_val=0
		for item in c_maxt:
			c_maxt_val=int((item.split(',')[0]).strip('C='))
		for item in t_maxc:
			t_maxc_val=float((item.split(',')[5]).strip(' T=\n'))
		
		if zero_cache > 0:
	                print "Ratio of Zero-Cache values to total input: %s" % Fraction(zero_cache,n_lines).limit_denominator()
		else:
			print "No zero Zero-Caching events recoded"

		print "Maximum cache value is %d recorded while throughput at %f" % (max_cache, t_maxc_val)
		print "Maximum througput value is %f recoded while cache at %d" %(max_tput, c_maxt_val)
		

		


if __name__=='__main__':
	main()
