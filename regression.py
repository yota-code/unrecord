#!/usr/bin/env python3



def larger_axlim( axlim ):
    """ argument axlim expects 2-tuple 
        returns slightly larger 2-tuple """
    axmin, axmax = axlim
    axrng = axmax - axmin
    new_min = axmin - 0.1 * axrng
    new_max = axmax + 0.1 * axrng
    return new_min,new_max

def regression(ref, tst, sync=None, only_diff=True) :
	
	reader = ref, tst
	
	if sync != None :
		ref_mark, tst_mark = upfront(ref[sync]), upfront(tst[sync])
	else :
		ref_mark, tst_mark = 0, 0

	ref_from, ref_to = ref_mark - min(ref_mark, tst_mark), ref_mark + min(len(ref) - ref_mark, len(tst) - tst_mark) - 1
	tst_from, tst_to = tst_mark - min(ref_mark, tst_mark), tst_mark + min(len(ref) - ref_mark, len(tst) - tst_mark) - 1

	print(ref_mark, ref_from, ref_to)
	print(tst_mark, tst_from, tst_to)
	
	ref_title = os.path.basename(ref.name).split('.')[0]
	tst_title = os.path.basename(tst.name).split('.')[0]

	regression_dir = "{} vs {}".format(ref_title, tst_title)
	try :
		os.makedirs(regression_dir)
	except :
		pass
	
	variable_list = ref.data.keys() & ref.data.keys()
	t = ref.time()[ref_from:ref_to] - ref.time()[ref_mark]
	for name in variable_list :
		x_ref = ref[name][ref_from:ref_to]
		x_tst = tst[name][tst_from:tst_to]
		if (x_ref != x_tst).any() or not only_diff :
			plot_diff(regression_dir, name, t, x_ref, x_tst)
	x_ref = ref[sync][ref_from:ref_to]
	x_tst = tst[sync][tst_from:tst_to]
	plot_diff(regression_dir, sync, t, x_ref, x_tst)
	
def plot_diff(directory, title, t, x_ref, x_tst) :

	fig, axe = plt.subplots(nrows=1, ncols=1)
	axe.grid(True)
	axe.set_title(title)
	plt.plot(t, x_ref, color='green')
	plt.plot(t, x_tst, color='red')
	axe.set_ylim(larger_axlim(axe.get_ylim()))
	fig.set_size_inches(15.0, 6.0)
	fig.tight_layout()
	plt.savefig(os.path.join(directory, title + '.png'), bbox_inches='tight', pad_inches=0.25)

