
==Building and installing modules==

*From source:*

Install the dependencies:

        python-lxml
        python-bsddb3

Untar the source distribution and run:

{{{
  $ python setup.py build
  $ python setup.py install
}}}


==using the module==

import crawler.crawler


== examples==

== compile==
python setup.py sdist
#python setup.py bdist
python setup.py bdist_wininst
python setup.py bdist_rpm
##need pkg stded
python setup.py --command-packages=stdeb.command bdist_deb
