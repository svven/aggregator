"""
Loads lua script from current folder.
Current script list: mark, unmark, set_fellows, set_edition.
"""
import jinja2
import os.path as path

from .. import r, keys

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(searchpath=path.dirname(__file__)))
def _load(template):
    "Load script from specified jinja2 template."
    temp = _env.get_template(template)
    return temp.render(**keys.DICT)

# def _load(script):
#     "Load script from specified file name."
#     with open(path.join(path.dirname(__file__), script), 'r') as file:
#         return file.read()

mark = r.register_script(_load('mark.lua'))
unmark = r.register_script(_load('unmark.lua'))
rem_marks = r.register_script(_load('rem_marks.lua'))
set_fellows = r.register_script(_load('set_fellows.lua'))
set_edition = r.register_script(_load('set_edition.lua'))
