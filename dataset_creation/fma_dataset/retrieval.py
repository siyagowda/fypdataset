import os
import IPython.display as ipd
import utils

fma = utils.FreeMusicArchive(os.environ.get('FMA_KEY'))

track_file = fma.get_track(3, 'track_file')
fma.download_track(track_file, path='track.mp3')