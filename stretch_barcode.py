import os
import sys
from PIL import Image

def stretchfiles(path, png):
	img = Image.open(os.path.join(path,png))

	if img.size[1] != 1:
	  print(sys.argv[1], 'must have height of 1\n  It has a height of', img.size[1])
	  exit()

	result = Image.new('RGB', (img.size[0],800))

	for i in range(result.size[1]):
	  result.paste(img, (0, i))

	result.save(os.path.join(path,png[:-4] + '_stretched' + png[-4:]))


def main():
	if len(sys.argv) != 3:
		print('usage: python stretch_barcode.py <path to files> <-u/-s>')

	folder = sys.argv[1]

	path = os.path.join(os.getcwd(),folder)

	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]

	stretched = []
	unstretched = []

	for f in files:
		if '_stretched.png' in f:
			stretched.append(f)
		else:
			unstretched.append(f)

	if '-u' in sys.argv:
		for f in stretched:
			os.remove(os.path.join(path,f))

	elif '-s' in sys.argv:
		for num, f in enumerate(stretched):
			del stretched[num]
			stretched.insert(num,f.replace('_stretched',''))

		for num,f in enumerate(unstretched):
			if f not in stretched:
				stretchfiles(path,f)

	else:
		print('-u to remove stretched files\n-s to make stretched files')


if __name__ == '__main__':
	main()
