from modules.util.path_util import SUPPORTED_VIDEO_EXTENSIONS
import pathlib
import cv2
import random
import os
import math
import scenedetect
import subprocess
import shlex
import concurrent

from modules.ui.models.SingletonConfigModel import SingletonConfigModel



class VideoModel(SingletonConfigModel):
    pass