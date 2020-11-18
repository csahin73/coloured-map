ffmpeg -i images/anim.gif -y -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" anim.mp4
#ffmpeg -framerate 30 -pattern_type glob -i 'images/*.png' \
#  -c:v libx264 -pix_fmt yuv420p out.mp4

