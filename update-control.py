

import requirements
import re
import os
import shutil
import tempfile
import gzip
import urllib.request
import shutil

pwd = os.getcwd()
req_file = "{}/test/requirements.txt".format(pwd)
test_req_file = "{}/test-requirements".format(pwd)


def sed_inplace(filename, pattern, repl):
    '''
    Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
    `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
    '''
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            for line in src_file:
                tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)



class Package:

    def __init__(self, name, pip_version_list):
        self.name = re.sub(r"-", '_', name)
        self.py2_deb_pkg = None
        self.py3_deb_pkg = None
        self.pip_version_list = pip_version_list

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

    def getPy2DebPkgVersionStable(self):
        stable_url = "http://deb.debian.org/debian/dists/stable/main/binary-all/Packages.gz"
        file = "/tmp/stable_Packages.gz"
        with urllib.request.urlopen(stable_url) as response, open(file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        with gzip.open(file, mode="rt") as f:
            for line in f:
                res = re.match("^Package:\ {}.*".format(self.py2_deb_pkg), line)
                if res:
                    for i in range(10):
                        line_to_search = f.__next__()
                        res_ver = re.match("^Version: .*$", line_to_search)
                        if res_ver:
                            self.py2_deb_pkg_stable_ver = res_ver.string.strip().split()[1]
                            return self.py2_deb_pkg_stable_ver.split("-")[0]

    def getPy3DebPkgVersionStable(self):
        stable_url = "http://deb.debian.org/debian/dists/stable/main/binary-all/Packages.gz"
        file = "/tmp/stable_Packages.gz"
        with urllib.request.urlopen(stable_url) as response, open(file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        with gzip.open(file, mode="rt") as f:
            for line in f:
                res = re.match("^Package:\ {}$".format(self.py3_deb_pkg), line)
                if res:
                    for i in range(10):
                        line_to_search = f.__next__()
                        res_ver = re.match("^Version: .*$", line_to_search)
                        if res_ver:
                            self.py3_deb_pkg_stable_ver = res_ver.string.strip().split()[1]
                            return self.py3_deb_pkg_stable_ver.split("-")[0]







package = 'tenacity'
version = []
p = Package(package, version)
print(p.getPy2DebPkgName())
print(p.getPy3DebPkgName())
print(p.getPy2DebPkgVersionStable())
print(p.getPy3DebPkgVersionStable())


    #print(p.getPy2DebPkgName())
    #print(p.getPy3DebPkgName())


























# Do it for Johnny.
#sed_inplace("{}/ahoj".format(pwd), r'^kokot', 'pica')

# reqs = {}
# with open(req_file, 'r') as fd:
#     for req in requirements.parse(fd):
#         reqs.update({req.name:req.specs})
#         # print(req.name)
#         # print(req.specs)
#         # print(req)
#
# py2_file = '/usr/share/dh-python/dist/cpython2_fallback'
# py3_file = '/usr/share/dh-python/dist/cpython3_fallback'
#
#
# for package, version in reqs.items():
#     p = Package(package, version)
#     #print(p.getPy2DebPkgName())
#     #print(p.getPy3DebPkgName())