import cv2
import sys, ast
import math
from PIL import Image, ImageDraw
from timeit import default_timer as timer

start = timer()

if '-h' in sys.argv:
  print('\nThis python script takes a video file and creates a movie barcode out of it. By default it will take every 24th frame, average the color of every pixel and put fill in a pixel in a png image with that color. The result is a "barcode" so you can see the average colors throughout the movie.')
  print('\nusage: python frames.py -i <input> -o <output>')
  print('arguments:\n-i: path to input file\n-o: path to output file (it gets created in the script)')
  print('-l: list of input files\n\texample:\n\t"/path/to/movie/1.mkv movie.1.png /path/to/movie/2.mkv movie.2.png"')
  print('-f: change the amount of frames skipped for each sample (default=24)')
  exit()

names_list = []

i = 1
while i < len(sys.argv):
  if sys.argv[i] == '-i':
    i += 1
    if ".mkv" in sys.argv[i]:
      names_list.append(sys.argv[i])
    else:
      print("Not a valid input file. Must be .mkv video file")
      exit()
  elif sys.argv[i] == '-o':
    i += 1
    if ".png" in sys.argv[i]:
      names_list.append(sys.argv[i])
    else:
      print("Not a valid output file. Must be .png file")
      exit()
  elif sys.argv[i] == '-l':
    i += 1
    names_list.append(sys.argv[i].split())
  elif sys.argv[i] == '-f':
    i += 1
    if int(sys.argv[i]) is not int:
      print("-f value must be an integer")
      exit()
    frame_skip = int(sys.argv[i])
  i += 1
names_list = names_list[0]
names_count = 0
while names_count < len(names_list):
  outpic = []

  frame_skip = 24
  vidcap = cv2.VideoCapture(names_list[names_count])
  frames_tot = math.floor(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)/24)
  success,image = vidcap.read()
  framesize = math.floor(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)*vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  count = 0
  print(count,'/', frames_tot, ' (', sep='', end='')
  interval = timer() - start
  hours, remain = divmod(interval,3600)
  minutes,seconds = divmod(remain,60)
  print('{:0>2}:{:0>2}:{:05.2f})'.format(int(hours),int(minutes),seconds))
  count += 1
  r = 0
  g = 0
  b = 0

  while count < frames_tot-1:
    for i in image:
      for j in i:
        r += j[2]
        g += j[1]
        b += j[0]
    outpic.append([int(r/framesize) ,int(g/framesize) ,int(b/framesize)])
    #print('Frame',count)
    for i in range(frame_skip):
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
  print(count,'/', frames_tot, ' (', sep='', end='')
  interval = timer() - start
  hours, remain = divmod(interval,3600)
  minutes,seconds = divmod(remain,60)
  print('{:0>2}:{:0>2}:{:05.2f})'.format(int(hours),int(minutes),seconds))

  print('Finished processing frames')

  im = Image.new('RGB',(len(outpic),1),color='white')

  draw = ImageDraw.Draw(im)
  for i in range(len(outpic)):
    draw.line((i,0,i,0), fill=(outpic[i][0],outpic[i][1],outpic[i][2]))

  im.save(names_list[names_count + 1])
  print('Barcode done')
  names_count += 2
