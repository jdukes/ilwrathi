Dir Structure:

ilwrathi/
    __init__.py 
    _common/
        __init__.py
	meta.py
    _py2.py
    _py3.py
    iac.py
demo/
    client.py
    demo.py
    simple_demo.py
tests/
    __init__.py
    test_ilwrathi_iac.py
todo.org
LICENSE
README.md
setup.py

--------------------

All version dependant syntax should go in _py?.py. Version independant code required to make things version independant should go in _common. 