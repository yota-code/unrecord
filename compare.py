import sys, os

import pack
import black_white

black_white._method = 'glob'



def one_variable_two_datasets(data_one, data_two, variable_list) :
	p = pack.Pack()
	one = p.load_data(data_one)
	two = p.load_data(data_two)

	for variable in variable_list :

		out = p.dump_data(variable + '.svg')

		out[variable + 'one'] = one[variable]
		out[variable + 'two'] = two[variable]
		out.dump()

def compare(data_list, white_list=None) :
	
	p = pack.Pack()
	
	variable_set = None
	
	for data in data_list :
		print("loading: ", data)
		u = p.load_data(data)
		if variable_set == None :
			variable_set = set(u)
		else :
			variable_set &= set(u)
	
	v = black_white.select(list(variable_set), white=white_list)
	
	for variable in v :

		out = p.dump_data(variable + '.svg')

		for reader in p.reader :
			out[variable + ' - ' + reader] = p.reader[reader][variable]
			
		out.dump()


if __name__ == '__main__' :
	data_list = [
		r"D:\tmp\ftd225_1c2\enregSUNnoopt.res.B",
		r"D:\tmp\ftd225_1c2\enregSUNexp.res.B",
		r"D:\tmp\1c2_nopid\enreg_9b506001246a62e4e126fd2974931d42.res.B",
		r"D:\tmp\1c2_nopid\enreg_9b506001246a62e4e126fd2974931d42ancien.res.B",
		r"D:\tmp\1c2_nopid\enreg_6203aaea8c3c9a325209a90f78c57b96.res.B",
		r"D:\tmp\1c2_nopid\enreg_e0b10a8ae9e9da305544da360dd450fc.res.B",
	]
	
	white_list = ('S*', 'PM*', 'MDD*')
	
	u = compare(data_list, white_list)
