from flask import Flask
from flask import render_template
from time import sleep
#import gopro.camera
#from gopro.camera import (mode_video, CAPTURE_LIST, capture_start,
                          #capture_stop, get_captures)
import urllib2
app = Flask(__name__)


@app.route('/playback')
def base():
    return render_template('playback.html')


@app.route('/capture')
def capture():
    return render_template('capture.html')


def capture_drop():
    """Switch to video and record 1.5 seconds of video """
    # None of these will work right this sec, b/c I haven't setup the fabric
    # recipes above as an import.
    mode_video()
    capture_start()
    sleep(1.5)
    capture_stop()
    capture_files = get_captures()
    url = '%s%s' % (CAPTURE_LIST, capture_files[-1])
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    # Nothing too secret here. This should probably be part of a config script
    # at some point.
    f = open('/Library/WebServer/Documents/drop_tower/media/latest.mp4', 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,

    f.close()

if __name__ == '__main__':
    app.run(debug=True)
