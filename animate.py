from PIL import Image, ImageDraw
import os
import sys
import random
import argparse
import webbrowser

def make_animation(inpdir, output):
    path = inpdir
    os.chdir(path)
    img_files = sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))

    images = [Image.open(fn) for fn in img_files]
    faster = int(len(images)*60/100)
    final = images[1:faster]
    for im in images[faster:]:
      final += [im, im, im]
    
    final[0].save(output, format='GIF',
               append_images=final[1:],
               save_all=True,
               duration=500)
    
if __name__ == "__main__":

    make_animation("images", "anim.gif")
