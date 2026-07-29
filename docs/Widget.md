## Widget
A widget has different states in which it can be:
+ **pgmenu.NORMAL:** a widget's default state
+ **pgmenu.HOVERED:** the widget's state when the cursor hovers over it
+ **pgmenu.ACTIVE:** a state that can be set by the widget's update function; is generally the widget's state when it's selected by the cursor
+ **pgmenu.DISABLED:** a widget set to this state will not be updated in the update loop
+ **pgmenu.HIDDEN:** a widget set to this state will not be updated in the update loop nor will it be drawn

### Widget Object
Base widget structure all widgets should inherit.

### Attribute Definition
The Widget object handles core functionality for widgets by default, removing the need to define animation attributes for each widget in the default theme file (due to fallback to widget_animation_...).

It handles:
+ animation attribution (setattr) (Widget has its own pgmenu.Theme.animation_scale, pgmenu.Theme.animation_duration, pgmenu.Theme.animation_curve)
+ animation and action functions assignment through attributes (animation_on_... (which default to m_animation_on_...) and on_... (default to m_on_...))

#### modify()
This method allows the user to be able to change the value of multiple attributes at once.