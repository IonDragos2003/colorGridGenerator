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