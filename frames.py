import cv2
import sys
import math
from PIL import Image, ImageDraw
from timeit import default_timer as timer

start = timer()

if len(sys.argv) == 3:
  vid_name = sys.argv[1]
  out_name = sys.argv[2]
else:
  print('Give input name and output name as arguments\npython frames.py in.mkv out.png')
  exit()

outpic = []

vidcap = cv2.VideoCapture(vid_name)
frames_tot = math.floor(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)/24)
success,image = vidcap.read()
framesize = math.floor(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)*vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
count = 1
r = 0
g = 0
b = 0

while count < frames_tot:
  for i in image:
    for j in i:
      r += j[2]
      g += j[1]
      b += j[0]
  outpic.append([int(r/framesize) ,int(g/framesize) ,int(b/framesize)])
  #print('Frame',count)
  for i in range(24):
    success,image = vidcap.read()
    if not(success):
      exit()
  r = 0
  g = 0
  b = 0
  if count % 100 == 0:
    print(count,'/', frames_tot, ' (', sep='', end='')
    interval = timer() - start
    hours, remain = divmod(interval,3600)
    minutes,seconds = divmod(remain,60)
    print('{:0>2}:{:0>2}:{:05.2f})'.format(int(hours),int(minutes),seconds))
  count += 1

print('Finished processing frames')

im = Image.new('RGB',(len(outpic),1),color='white')

draw = ImageDraw.Draw(im)
for i in range(len(outpic)):
  draw.line((i,0,i,0), fill=(outpic[i][0],outpic[i][1],outpic[i][2]))

im.save(out_name)
print('Barcode done')
