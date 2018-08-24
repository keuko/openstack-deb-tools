

import requirements
import re
import os

pwd = os.getcwd()

class Package:

    def __init__(self, name):
        self.name = re.sub(r"-", '_', name)
        self.py2_deb_pkg = None
        self.py3_deb_pkg = None

    def getPy2DebPkgName(self):
        py2_file = '/usr/share/dh-python/dist/cpython2_fallback'
        with open(py2_file) as f:
            for line in f:
                res = re.match("^{}\ .*".format(self.name), line)
                if res:
                    self.py2_deb_pkg = res.string.strip().split()[1]
        if self.py2_deb_pkg:
            return self.py2_deb_pkg
        else:
            return "!!! Python2 Deb Package for {} not available".format(self.name)

    def getPy3DebPkgName(self):
        py3_file = '/usr/share/dh-python/dist/cpython3_fallback'
        with open(py3_file) as f:
            for line in f:
                res = re.match("^{}\ .*".format(self.name), line)
                if res:
                    self.py3_deb_pkg = res.string.strip().split()[1]
        if self.py3_deb_pkg:
            return self.py3_deb_pkg
        else:
            return "!!! Python3 Deb Package for {} not available".format(self.name)



from deb_pkg_tools import control
control_file = "{}/debian/control".format(pwd)
a = control.load_control_file(control_file)
print(control.parse_depends())
print(a)





# req_file = "{}/requirements.txt".format(pwd)
# test_req_file = "{}/test-requirements".format(pwd)
#
# reqs = []
# with open(req_file, 'r') as fd:
#     for req in requirements.parse(fd):
#         reqs.append(req.name)
#         #print(req.name, req.specs)
#
# py2_file = '/usr/share/dh-python/dist/cpython2_fallback'
# py3_file = '/usr/share/dh-python/dist/cpython3_fallback'
#
# for package in reqs:
#     p = Package(package)
#     print(p.getPy2DebPkgName())
#     print(p.getPy3DebPkgName())



# for package in reqs:
#
#     package = re.sub(r"-", '_', package)
#     deb_package2_found = os.system("grep '^{}\ ' /usr/share/dh-python/dist/cpython2_fallback > /dev/null".format(package))
#     if deb_package2_found == 0:
#         deb_package2 = subprocess.check_output(
#             "grep '^{}\ ' /usr/share/dh-python/dist/cpython2_fallback | cut -d' ' -f2 | head -n 1".format(package),
#             shell=True).decode('utf8').strip()
#     else:
#         deb_package2 = "!!! NOT_FOUND !!!"
#
#     deb_package3_found = os.system("grep '^{}\ ' /usr/share/dh-python/dist/cpython3_fallback 2>/dev/null".format(package))
#     if deb_package3_found == 0:
#         deb_package3 = subprocess.check_output(
#             "grep '^{}\ ' /usr/share/dh-python/dist/cpython3_fallback | cut -d' ' -f2 | head -n 1".format(package),
#             shell=True).decode('utf8').strip()
#     else:
#         deb_package3 = "!!! NOT_FOUND !!!"
#
#     print("{}|{}|{}".format(package, deb_package2, deb_package3))