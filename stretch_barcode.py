from PIL import Image
import sys

if len(sys.argv) != 2:
  print('There needs to be 1 argument.\n  This has', len(sys.argv)-1, 'arguments')
  exit()

img = Image.open(sys.argv[1])

if img.size[1] != 1:
  print(sys.argv[1], 'must have height of 1\n  It has a height of', img.size[1])
  exit()

result = Image.new('RGB', (img.size[0],800))

for i in range(result.size[1]):
  result.paste(img, (0, i))

result.save(sys.argv[1][:-4] + '_stretched' + sys.argv[1][-4:])
