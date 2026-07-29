import pygame
import pgmenu

import ctypes
from ctypes import wintypes


# Functions that allow for more extensive or easier manipulation of the window


# Small, built-in integration for fullscreen support.
# Unfortunately, it cannot be added as default in update loop
def fullscreen_controls(screen, event):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_F11:

            # Detect first call in a way
            if pgmenu.vars.fs_window_size is None:
                pgmenu.vars.fs_window_size = pygame.display.get_window_size()

                # Needs VIDEORESIZE on first call for some reason
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))

            if not pygame.display.is_fullscreen():
                # VIDEORESIZE is not needed here apparently
                pgmenu.vars.fs_window_size = pygame.display.get_window_size()
                screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[0],
                                                 screen.get_flags(),
                                                 screen.get_bitsize())
                pygame.display.toggle_fullscreen()
            else:
                # Add VIDEORESIZE to event queue
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE))

                pygame.display.toggle_fullscreen()
                screen = pygame.display.set_mode(pgmenu.vars.fs_window_size,
                                                 screen.get_flags(),
                                                 screen.get_bitsize())

    return screen


# Function allowing for a transparent window
def set_transparent_window(transparency):
    # Constants for Windows API
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x80000
    LWA_ALPHA = 0x2

    # Set window style to layered
    hwnd = pygame.display.get_wm_info()["window"]
    hwnd = wintypes.HWND(hwnd)

    current_exstyle = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    new_exstyle = current_exstyle | WS_EX_LAYERED
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_exstyle)

    # Set window transparency (alpha value)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, transparency, LWA_ALPHA)

    # Update the window
    ctypes.windll.user32.UpdateWindow(hwnd)


# Works the same as transparent_window, but instead makes a colorkey transparent
def set_transparent_colorkey(colorkey):
    # Constants for Windows API
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x80000
    LWA_COLORKEY = 0x1

    # Set window style to layered
    hwnd = pygame.display.get_wm_info()["window"]
    hwnd = wintypes.HWND(hwnd)

    current_exstyle = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    new_exstyle = current_exstyle | WS_EX_LAYERED
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_exstyle)

    # Set pixels with colorkey to transparency
    colorkey_value = colorkey[0] << 16 | colorkey[1] << 8 | colorkey[2]
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, ctypes.c_uint32(colorkey_value), 0, LWA_COLORKEY)

    # Update the window
    ctypes.windll.user32.UpdateWindow(hwnd)