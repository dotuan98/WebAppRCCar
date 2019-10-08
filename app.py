#!/usr/bin/env python
# from importlib import import_module
# import os
# from importlib import import_module
from flask import Flask, render_template, Response, request, redirect, url_for, make_response
import motor

# import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_opencv import Camera


app = Flask(__name__)

LEFT, RIGHT, FORWARD, BACKWARD, STOP = "left", "right", "forward", "backward", "stop"
AVAILABLE_COMMANDS = {
    'Left': LEFT,
    'Forward': FORWARD,
    'Right' : RIGHT,
    'Backward': BACKWARD,
    'Stop': STOP
}

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', commands=AVAILABLE_COMMANDS)


def gen(camera):
    while True:
        """This function generates the frame for displaying the video. The 'yield' increments the iteration by the 
        next, therefore, the image overlaps. The frame variable is used later in the function video_feed() """
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """This function streams the images on the frame, with the next one overlapping and replacing the former. This is
    achieved by setting mimetype to 'multipart/x-mixed-replace'. The idea is that by replacing the image with another
    so quickly, it'd look like a video."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

"""@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")
"""

@app.route('/<cmd>')
def command(cmd=None):
	if cmd == STOP:
		motor.stop()
	elif cmd == FORWARD:
		motor.forward()
	elif cmd == BACKWARD:
		motor.backward()
	elif cmd == LEFT:
		motor.left()
	else:
		motor.right()
	response = "Moving {}".format(cmd.capitalize())
	return response, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

