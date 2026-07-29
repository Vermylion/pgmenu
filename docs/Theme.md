## Theme

### Overview
Theme is dynamic and can be changed at any point during runtime.

Default value for any attribute is defined in `DEFAULT.json` under the following structure:
```json
{
  "[THEME]": {
    "[file name]_[attr]": [value],
    ...
  }
}
```
_**Exception**: As of current development, an exception is made for `pgmenu.draw.aarect` attributes which use the prefix `aarect_`._

### Comments
To organize the file, comments can be added through: 
```json
"#": "comment"
```

### Special Types
To be able to add normal python variable types into json, a json object can be used to define more variable types:
```json
"[attr]": {"type": "[type]", [args...]}
```
Here are the following types that can be referenced:
+ **method:** sets the attribute to a method
````json
"[attr]": {"type": "method", "module": "pgmenu.widget", "object": "Widget", "method": "m_on_standby"}
````
+ **function:** sets the attribute to a function
````json
"[attr]": {"type": "function", "module": "pgmenu.animation", "function": "circ"}
````
+ **attribute:** sets the attribute to a previous attribute already defined in the theme
````json
"[attr]": {"type": "attribute", "attribute": "border_radius"}
````
+ **variable:** sets the attribute to a variable defined inside of a module
````json
"[attr]": {"type": "variable", "module": "pgmenu", "variable": "NORMAL"}
````
+ **image:** sets the attribute to a `pygame.Surface` object by loading the precised path with `pygame.image.load()`
````json
"[attr]": {"type": "image", "path": "../dir1/dir2/image.png"}
````
+ **exec:** sets the attribute to executed code formulated in the `.json`. The given code will be automatically (and forcibly) preceded by `[attr] = ...`
````json
"[attr]": {"type": "exec", "code": "round(min(self.aarect_rect[2:]) / 3)"}
````

### Conventional
To have an attribute not be defined inside of a default theme and therefore set to another value unless the user defines said attribute in a theme of their own, the `null` operator will be used.

Json theme side:
```json
"aarect_border_top_left_radius": null,
```

Code side:
```python
border_top_left_radius = pgmenu.Theme.aarect_border_top_left_radius if pgmenu.Theme.aarect_border_top_left_radius is not None else border_radius
```

### Global attributes
To simplify the process of setting attributes inside of a theme, special attribute prefixes can be used to set multiple attributes to a same value.

#### Widget attributes
The global attribute `widgets_...` can be used in a theme to set all corresponding widgets' attributes to this attribute's value.

However, the `widgets_...` attribute still follows attribution priority. For example, if `button_border_radius` is defined in the theme file after `widgets_border_radius`, then the Button widget's attribute has `button_border_radius`'s value. 
