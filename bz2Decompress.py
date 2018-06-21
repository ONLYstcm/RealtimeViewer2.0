import os
import sys
import bz2
from bz2 import decompress

def decomp(path):
	filename = path.split('/')[-1]
	folder = '/'.join(path.split('/')[:-1])
	#print(filename[:-4], folder)
	newfilepath = path + '.decompressed'
	with open(newfilepath, 'wb') as new_file, bz2.BZ2File(path, 'rb') as file:
		for data in iter(lambda: file.read(100 * 1024), b''):
			new_file.write(data)
	os.rename(newfilepath, folder + '/' + filename[:-4])

decomp('C:/Users/William Cen/Documents/pol0.scio.bz2')