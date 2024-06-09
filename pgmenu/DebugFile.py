from pgmenu import * # Should import everything regardless of file or stuff

widget = globals()["pgmenu.widget.Widget"]()
print(widget)

window = projects.PgmenuWindow() # Would like it to be: window = PgmenuWindow()

window.loop()
