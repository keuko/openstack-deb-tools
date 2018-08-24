

import requirements

import requirements
import subprocess
import os
import re

reqs = []
with open('test/requirements.txt', 'r') as fd:
    for req in requirements.parse(fd):
        reqs.append(req.name)
        #print(req.name, req.specs)

for package in reqs:

    package = re.sub(r"-", '_', package)
    deb_package2_found = os.system("grep '^{}\ ' /usr/share/dh-python/dist/cpython2_fallback > /dev/null".format(package))
    if deb_package2_found == 0:
        deb_package2 = subprocess.check_output(
            "grep '^{}\ ' /usr/share/dh-python/dist/cpython2_fallback | cut -d' ' -f2 | head -n 1".format(package),
            shell=True).decode('utf8').strip()
    else:
        deb_package2 = "!!! NOT_FOUND !!!"

    deb_package3_found = os.system("grep '^{}\ ' /usr/share/dh-python/dist/cpython3_fallback 2>/dev/null".format(package))
    if deb_package3_found == 0:
        deb_package3 = subprocess.check_output(
            "grep '^{}\ ' /usr/share/dh-python/dist/cpython3_fallback | cut -d' ' -f2 | head -n 1".format(package),
            shell=True).decode('utf8').strip()
    else:
        deb_package3 = "!!! NOT_FOUND !!!"

    print("{}|{}|{}".format(package, deb_package2, deb_package3))

    stdout = subprocess.PIPE