from setuptools import setup
from datetime import datetime #for version string

import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'ilwrathi'))
import ilwrathi

now = datetime.now()

setup(name="ilwrathi",
      version="%s%s.1a3" % (now.year, now.month), # PEP440 compliant
      # The first section lets users know how old a module is, the
      # second lets the user compare relative versions of the same age.
      description="A framework for building pen test tools",
      url="https://github.com/jdukes/ilwrathi",
      author="Josh Dukes",
      author_email="hex@neg9.org",
      license="GNU General Public License v3 (GPLv3)",
      keywords = "hacker, web, CTF, pen test",
      long_description=ilwrathi.__doc__,
      packages=["ilwrathi", "ilwrathi._py2"])
