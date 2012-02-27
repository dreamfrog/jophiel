python setup.py sdist
#python setup.py bdist
sleep 2
python setup.py bdist_wininst
sleep 2
python setup.py bdist_rpm
##need pkg stded
sleep 2
python setup.py --command-packages=stdeb.command bdist_deb
