from PIL import Image, ImageDraw
import os
import sys
import random
import argparse
import webbrowser
import cv2

def make_animation(inpdir, output):
    
    img_files = sorted((fn for fn in os.listdir(inpdir) if fn.endswith('.png')))

    images = [Image.open(os.path.join(inpdir,fn)) for fn in  img_files]
    faster = int(len(images)*60/100)
    final = images[1:faster]
    for im in images[faster:]:
      final += [im, im, im]
    
    output = os.path.join(inpdir, output)
    final[0].save(output, format='GIF',
               append_images=final[1:],
               save_all=True,
               duration=500)

def make_video(inpdir, output):

    
    img_files = sorted((fn for fn in os.listdir(inpdir) if fn.endswith('.png')))

    images = [cv2.imread(os.path.join(inpdir,fn)) for fn in  img_files]
    height, width, layers = images[0].shape
    size = (width,height)
    
    faster = int(len(images)*60/100)
    final = images[0:faster]
    for im in images[faster:]:
      final += [im, im, im]

    output = os.path.join(inpdir, output)
    out = cv2.VideoWriter(output,cv2.VideoWriter_fourcc(*'DIVX'), 3, size)
   
    for i in range(len(final)):
        out.write(final[i])
    out.release()
    
if __name__ == "__main__":

    make_animation("images", "anim.gif")
