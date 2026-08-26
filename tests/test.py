import winreg
from ctypes import (POINTER, Structure, byref, c_int, pointer, sizeof,
                    windll, c_buffer, WINFUNCTYPE, c_uint64)
from ctypes.wintypes import DWORD, ULONG
import platform

import pygame
import pgmenu
from pywinstyles import py_win_style
import pywinstyles


pygame.init()

screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
pygame.display.set_caption("Window")
clock = pygame.time.Clock()
fps = 1000

win = pygame.display.get_wm_info()["window"]
hwnd = py_win_style.detect(win)

# py_win_style.paint(win)
# windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(c_int(1)), sizeof(c_int))
# py_win_style.ChangeDWMAttrib(hwnd, 20, c_int(1))
# py_win_style.ChangeDWMAccent(hwnd, 30, 3, color=0x292929)
# py_win_style.ExtendFrameIntoClientArea(hwnd)

pywinstyles.apply_style(win, "acrylic")

running = True
while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    pgmenu.draw_all()
    pgmenu.update(events)
    pygame.display.flip()
    clock.tick(fps)