#!/usr/bin/env python
import git
from setuptools import setup, find_packages
from datetime import datetime #for version string

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'ilwrathi'))
import ilwrathi

now = datetime.now()
repo = git.Repo('.')
commit = repo.log()[0]

setup(name="ilwrathi",
      version="%s%s.1a%s" % (now.year, now.month, commit.id[:8]), # PEP440 compliant
      # The first section lets users know how old a module is, the
      # second lets the user compare relative versions of the same age.
      description="A framework for building pen test tools",
      url="https://github.com/jdukes/ilwrathi",
      author="Josh Dukes",
      author_email="hex@neg9.org",
      license="GNU General Public License v3 (GPLv3)",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent', # Tested on Linux and OSX
          'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 3', #uncomment when tested on py3
          'Topic :: Security',
          'Topic :: Software Development :: Testing'],
      keywords="hacker web CTF pen test",
      long_description=ilwrathi.__doc__,
      packages=find_packages(exclude=['demo', 'tests*']),
      test_suite="tests.TestIdempotentAccessor")
