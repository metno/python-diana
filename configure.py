import glob, os, sys
import sipconfig

diana_src_dir = sys.argv[1]

config = sipconfig.Configuration()

# The name of the SIP build file generated by SIP and used by the build
# system.
sip_files_dir = "sip"
modules = ["diana", "metlibs", "qt", "std"]

if not os.path.exists("modules"):
    os.mkdir("modules")

# Run SIP to generate the code.
output_dirs = []

for module in modules:

    output_dir = os.path.join("modules", module)
    build_file = module + ".sbf"
    build_path = os.path.join(output_dir, build_file)
    
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    
    sip_file = os.path.join("sip", module, module+".sip")
    
    command = " ".join(
        [config.sip_bin, "-c", output_dir, "-b", build_path,
         "-I"+config.sip_inc_dir, "-I"+diana_src_dir, "-I/usr/include",
         "-I/usr/include/metlibs",
         "-I/opt/qt4-qws/include",
         "-Isip", sip_file]
        )
    print command
    if os.system(command) != 0:
        sys.exit(1)
    
    # Create the Makefile (within the diana directory).
    makefile = sipconfig.SIPModuleMakefile(
        config, build_file, dir=output_dir,
        install_dir=".."
        )
    
    if module in ("diana", "metlibs"):
        makefile.extra_include_dirs.append(diana_src_dir)
        makefile.extra_include_dirs.append("/usr/include/metlibs")
        makefile.extra_lib_dirs.append(diana_src_dir)
        makefile.extra_libs.append("diana")
    
    if module in ("diana", "qt"):
        makefile.extra_include_dirs.append(os.path.join(diana_src_dir, "PaintGL"))
        makefile.extra_include_dirs.append("/opt/qt4-qws/include")
        makefile.extra_include_dirs.append("/opt/qt4-qws/include/QtCore")
        makefile.extra_include_dirs.append("/opt/qt4-qws/include/QtGui")
        makefile.extra_lflags.append("-Wl,-rpath=/opt/qt4-qws/lib")
        makefile.extra_lib_dirs.append("/opt/qt4-qws/lib")
        makefile.extra_libs.append("QtGui")
    
    makefile.generate()
    
    output_dirs.append(output_dir)

# Generate the top-level Makefile.
sipconfig.ParentMakefile(
    configuration = config,
    subdirs = output_dirs
    ).generate()
