#!/usr/bin/env python3
"""
>>> from mns.types import ChoiceEnum

>>> class Color(ChoiceEnum):
...     RED = 'red'
...     GREEN = 'green'
...     BLUE = 'blue'
...     __labels__ = {
...         RED: 'ReD',
...    }

>>> Color.RED
<Color.RED: 'red'>

>>> Color.GREEN
<Color.GREEN: 'green'>

>>> Color('red')
<Color.RED: 'red'>

>>> Color.RED.name
'RED'

>>> Color.RED.label
'ReD'

>>> str(Color.RED)
'red'

>>> list(Color)
[<Color.RED: 'red'>, <Color.GREEN: 'green'>, <Color.BLUE: 'blue'>]

>>> Color.get_choices()
[(<Color.RED: 'red'>, 'ReD'), (<Color.GREEN: 'green'>, 'green'), (<Color.BLUE: 'blue'>, 'blue')]

"""

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# Local Variables:
# compile-command: "./choices.py"
# End:
