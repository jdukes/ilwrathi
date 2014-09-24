from setuptools import setup

import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'ilwrath'))
import ilwrath

setup(name="ilwrath",
      version="0.3",
      description="A framework for building web pen test tools",
      url="https://github.com/jdukes/ilwrath",
      author="Josh Dukes",
      author_email="hex@neg9.org",
      license="GNU General Public License v3 (GPLv3)",
      keywords = "hacker, web, CTF, pen test",
      long_description=ilwrath.__doc__,
      packages=["ilwrath", "ilwrath._py2"])
