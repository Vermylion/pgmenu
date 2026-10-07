import pgmenu

window = core.simple.PgmenuWindow((625, 250))
window.fps = 1000
screen = window.screen

toggleswitch1 = pgmenu.toggleswitch.ToggleSwitch(screen, (50, 50), (60, 30), text="Horizontal Right", toggle_direction=pgmenu.RIGHT)
toggleswitch2 = pgmenu.toggleswitch.ToggleSwitch(screen, (50, 150), (60, 30), text="Horizontal Left", text_side_margin=16, toggle_direction=pgmenu.LEFT)

toggleswitch3 = pgmenu.toggleswitch.ToggleSwitch(screen, (400, 30), (30, 60), text="Vertical Right", text_margin=15, toggle_direction=pgmenu.RIGHT)
toggleswitch3 = pgmenu.toggleswitch.ToggleSwitch(screen, (400, 130), (30, 60), text="Vertical Left", text_margin=15, text_side_margin=16, toggle_direction=pgmenu.LEFT)

def loop():
    core.text.write(screen, (20, 20), str(round(window.clock.get_fps())))


window.loop(loop)