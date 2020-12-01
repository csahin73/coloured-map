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
    final = [] #images[1:faster]
    for  im in images[0:faster]:
      final += [im, im]
    for im in images[faster:]:
      final += [im, im, im]
    final = images
    output = os.path.join(inpdir, output)
    final[0].save(output, format='GIF',
               append_images=final[1:],
               save_all=True,
               duration=1000)
    return output
def make_mp4(avi, output):
    
    cmd = []
    cmd.append("ffmpeg -y -i {}".format(avi)) 
    cmd.append("-movflags faststart -pix_fmt yuv420p -vf") 
    cmd.append("'scale=trunc(iw/2)*2:trunc(ih/2)*2'")
    cmd.append(output)

    cmd = " ".join(cmd)
    os.system(cmd)
    return output

def make_video(inpdir, output):

    img_files = sorted((fn for fn in os.listdir(inpdir) if fn.endswith('.png')))
    images = [cv2.imread(os.path.join(inpdir,fn)) for fn in  img_files]
    height, width, layers = images[0].shape
    size = (width,height)
    
    faster = int(len(images)*60/100)
    final = [] #images[0:faster]
    """for  im in images[0:faster]:
      final += [im, im]
    for im in images[faster:]:
      final += [im, im, im]
    """
    final = images
    output = os.path.join(inpdir, output)
    out = cv2.VideoWriter(output,cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
   
    for i in range(len(final)):
        out.write(final[i])
    out.release()
    return output
    
if __name__ == "__main__":

    make_animation("images", "anim.gif")
