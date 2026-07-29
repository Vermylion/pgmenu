# Surface Widget

Responsive resize by default resizes the surface with `pygame.transform.smoothscale`. For cleaner resize, it is recommended to do:

```python
import pgmenu


def on_resize():
    surface_widget.surface = ...

    
surface_widget = pgmenu.surface.Surface(..., on_resize=on_resize)
```

On resize, the `surface` attribute gets reassigned and loses its `AnimateSurface` object. To keep animations on the surface:
```python
def on_resize():
    surface_widget.surface = AnimateSurface(...)
```