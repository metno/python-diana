#!/usr/bin/env python

import popen2, sys

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <symbol> ...\n" % sys.argv[0])
        sys.exit(1)
    
    so, si = popen2.popen2("dpkg -l | grep metlibs")
    si.close()
    packages = map(lambda x: x.split()[1], filter(lambda y: y.startswith("ii"), so.readlines()))
    so.close()
    
    for package in packages:
    
        so, si = popen2.popen2("dpkg --listfiles " + package + " | grep '\\.a$'")
        si.close()
        libs = map(lambda x: x.strip(), so.readlines())
        so.close()
        
        for lib in libs:
            so, si = popen2.popen2("objdump -t " + lib)
            si.close()
            for line in so.readlines():
                for symbol in sys.argv[1:]:
                    if symbol in line:
                        print package, lib, line.strip()
            so.close()
    
    sys.exit()
