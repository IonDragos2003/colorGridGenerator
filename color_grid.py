import sys
import os
from vlc_player_final import Player
from PyQt5 import QtGui, QtCore, QtWidgets

# Global variables
framesTaken = 0
framesTakenList = []
framesSpecified = 0
clusters = 5
margin = 5
borderSize = 40
offset = 2

class Custom_VLC_Player(Player):
    def __init__(self):
        # inherit from the original class
        super(Custom_VLC_Player, self).__init__()
    # We want the width and height to be fixed, so the layout dimensions
        # don't change in a weird way
        self.videoframe.setFixedWidth(640)
        self.videoframe.setFixedHeight(360)

        # We create a new layout, where we will place our custom buttons
        self.snapbox = QtWidgets.QHBoxLayout()

        # We create a button, that will execute our snapshot taking function
        self.snapbutton = QtWidgets.QPushButton("Take Snapshot")

        # We will set it disabled for the start of the program
        self.snapbutton.setEnabled(0)

        # Let's add the button to our layout
        self.snapbox.addWidget(self.snapbutton)

        # We will connect a snapshot taking function to the button later.
        # Let's leave this command commented out for now
        #self.connect(self.snapbutton, QtCore.SIGNAL("clicked()"),self.take_snapshot)
        #self.connect(origin, SIGNAL('completed'), self._show_results)
        self.snapbutton.clicked.connect(self.take_snapshot)


        # We place a label for specifing the frame count to use
        self.l1 = QtWidgets.QLabel("Number of frames:")

        # We add it to the layout
        self.snapbox.addWidget(self.l1)

        # We create a spin box, where we can choose
        # how many frames we want to take
        self.sp = QtWidgets.QSpinBox()

        # We will limit the number to 10 frames in this program
        self.sp.setMaximum(10)
        self.sp.setMinimum(0)

        # We add it to the layout
        self.snapbox.addWidget(self.sp)
        # Connect a value change function to the spinbox.
        # Let's leave this command commented out for now
        self.sp.valueChanged.connect(self.valuechange)

        # We add an empty space that streches to the right side
        # that way the next added element will be aligned to the right
        self.snapbox.addStretch(1)

        # This label will hold information,
        # how many frames have been taken so far
        self.l2 = QtWidgets.QLabel("Frames taken: "+str(framesTaken))

        # This is needed for the layout not to break
        self.l2.setFixedHeight(24)
        self.snapbox.addWidget(self.l2)

        # While the process hasn't started yet, we can hide the label
        self.l2.setVisible(0)

        # We add it to the layout
        self.vboxlayout.addLayout(self.snapbox)

        # This is a layout which will consist of 10 labels, each label
        # will hold a thumbnail of the frame taken
        self.imageareaWidget = QtWidgets.QWidget(self)
        self.imageareaWidget.setFixedHeight(80)

        # This is a wrapper around our image label widget
        self.imagearea = QtWidgets.QHBoxLayout(self.imageareaWidget)

        # Let's create an array of 10 label objects and add them
        # to the widget we just created
        self.imageBoxes = []
        for i in range(0, 10):
            self.imageBoxes.append(QtWidgets.QLabel(str(i)))
            self.imageBoxes[len(self.imageBoxes)-1]
            self.imagearea.addWidget(self.imageBoxes[len(self.imageBoxes)-1])

        # We will add this area to our layout, but initially we will set it
        # invisible, while the snapshot capture process hasn't started yet
        self.vboxlayout.addWidget(self.imageareaWidget)
        self.imageareaWidget.setVisible(0)

    def valuechange(self):
        # We access our global variables within the function
        global framesTaken
        global framesSpecified

        # We set the framesSpecified value to
        # whatever is specified on the spinbox
        framesSpecified = self.sp.value()

        # We modify our label to give us info, how many
        # frames have been captured so far
        self.l2.setText(
            "Frames taken: "+str(framesTaken)+" from "+str(framesSpecified))

        # Once the snapshot taking process has begun,
        # we need to disable the spinbox
        self.sp.setEnabled(0) if (framesTaken > 0) else self.sp.setEnabled(1)

        # We enable our snapshot trigger button, if frames have been specified
        # and the process is ongoing.
        # If the process ends, we disable the button again
        if (self.sp.value() > 0
            and framesTaken < 10
                and framesTaken < framesSpecified):
            self.snapbutton.setEnabled(1)
        else:
            self.snapbutton.setEnabled(0)

        if (self.sp.value() > 0):
            self.l2.setVisible(1)
        else:
            self.l2.setVisible(0)

    def take_snapshot(self):
        # Import the global variables we'll be using
        global framesTaken, clusters, borderSize, offset
        # This will be needed to check if the player was playing at the
        # time of the button press
        wasPlaying = None
        # We need to get the width and height of the video file
        videoSize = self.mediaplayer.video_get_size()
        # This is the VLC function, that let's us
        # take a snap shot of the video frame and save it in the directory
        self.mediaplayer.video_take_snapshot(
            0, "./img_"+str(framesTaken)+".png",
            videoSize[0],
            videoSize[1])

        # While we do the image processing, let's pause the video
        if self.mediaplayer.is_playing():
            self.PlayPause()
            wasPlaying = True
# Initializing the QtWidgets Application instance
app = QtWidgets.QApplication(sys.argv)

# Initiliazing our custom VLC Player instance
vlc = Custom_VLC_Player()
vlc.show()
# Resizing the VLC player. Will use 660px by 530px for now
vlc.resize(660, 530)

if sys.argv[1:]:
    player.OpenFile(sys.argv[1])
sys.exit(app.exec_())