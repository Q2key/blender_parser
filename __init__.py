import sys
import os

if sys.platform == 'cli':
    from serialcli import *
else:
    import os
    # chose an implementation, depending on os
    if os.name == 'nt': #sys.platform == 'win32':
        from serialwin32 import *
    elif os.name == 'posix':
        from serialposix import *
    elif os.name == 'java':
        from serialjava import *
    else:
        raise Exception(
            "Sorry: no implementation for your platform ('%s') available" % os.name
        )