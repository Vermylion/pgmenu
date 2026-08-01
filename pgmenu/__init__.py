# FIXME -> Has to be a better way to maintain structure without having to use 'as draw' -> Doesn't work properly when using 'from pgmenu import *'

from pgmenu.constants import *

from pgmenu.lib import *

import pgmenu.system as system

import pgmenu.cache as cache

import pgmenu.vars as vars

from pgmenu.vars import Theme

import pgmenu.animation as animation

import pgmenu.text as text

import pgmenu.draw as draw

import pgmenu.theme as theme

import pgmenu.position as position

import pgmenu.projects as projects

import pgmenu.display as display

import pgmenu.rect as rect

import pgmenu.resize as resize

import pgmenu.simple as simple

import pgmenu.menu as menu

# Widgets
import pgmenu.label as label

import pgmenu.surface as surface

import pgmenu.frame as frame

import pgmenu.button as button

import pgmenu.checkbox as checkbox

# Initialize library
lib.init()
