#!/usr/bin/env python3


# take a res.B file as input, drop a pickle files

import pickle
import sys

from pathlib import Path

import unrecord.plugin.res_b


if __name__ == "__main__" :

	resb_pth = Path(sys.argv[1])
	u = unrecord.plugin.res_b.Reader(str(resb_pth))
	pickle_pth = resb_pth.with_suffix(".pickle")
	with pickle_pth.open('wb') as fid :
		pickle.dump(u._data, fid, protocol=pickle.HIGHEST_PROTOCOL)
