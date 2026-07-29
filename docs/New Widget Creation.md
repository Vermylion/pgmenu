## For widgets using RectWidget super class
### Base Structure
```python
from pgmenu.animation import *
from pgmenu.widget import RectWidget


class Checkbox(RectWidget):
    
    def __init__(self,
                 **kwargs):
        
        # A defined widget type for easier widget comprehension in code
        # Each built-in widget has their own, un-impactful if they don't
        self.type = pgmenu.WIDGET
        
        # Declare other widget arguments
        # border_radius and co is defined in RectWidget __init__
        # Therefore needs to be passed, if used, as super().__init__(border_radius=border_radius, **kwargs)
        super().__init__(**kwargs)

        # Add widget to widget list
        pgmenu.widget.add(self)
        
    def __setattr__(self, key, value):
        # Return if called with same value
        if hasattr(self, key) and getattr(self, key) == value:
            return False

        # Call the original __setattr__ method to set the attribute
        super().__setattr__(key, value)

        # Base Arguments
        # Animation Arguments
        if not isinstance(getattr(self, key), Animate | AnimateTuple | AnimateColor | AnimateFill):
            ...
        
    def draw(self):
        super().draw()
        
        ...
    
    def update(self, event):
        # Update code using event ex: to detect mouse clicks
        ...
```