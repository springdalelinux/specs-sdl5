# The following defines the version of compiler suite we are doing this
# that we can do this easily as new versions come out, directly when
# rebuilding this src.rpm
# should be 9.1, 9.0 and so on
%{!?intelversion:%define intelversion 9.1}

# is this for C or Fortran? - set to icc, icce, ifort or iforte
%{!?intelbits:%define intelbits 32}

# The rest should be figured out automatically just from the above two things
%{!?intelshortversion:%define intelshortversion %(echo %{intelversion} | cut -d. -f1-2)}
%if "%{intelshortversion}" == "9.1" || "%{intelshortversion}" == "10.0"
%define intelnumversion %(echo %{intelshortversion} | tr -d \.)
%endif
%if "%{intelshortversion}" == "9.0"
%define intelnumversion 9
%endif
%if "%{intelshortversion}" == "8.1"
%define intelnumversion 8
%endif

# in most cases it is a compiler, will override for iidb
%define inteltype compiler

# Now we set the install directory - depends on above
%if "%{intelbits}" == "32"
ExclusiveArch: i386
Requires: intel-icc%{intelnumversion}-modules 
Requires: intel-ifort%{intelnumversion}-modules
Requires: intel-iidb%{intelnumversion}-modules
%else
ExclusiveArch: x86_64
Requires: intel-icce%{intelnumversion}-modules 
Requires: intel-iforte%{intelnumversion}-modules
Requires: intel-iidbe%{intelnumversion}-modules
%endif
# In any case, require intel-license
Requires: intel-license

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles

Summary: Common/Default Modules configuration files for intel %{intelshortversion} compilers
Name: intel-compiler%{intelnumversion}-%{intelbits}-default-modules
Version: %{intelshortversion}
Release: 14.PU_IAS.5
License: Other
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Provides: intel-compiler-default-modules = %{intelshortversion}
Requires: environment-modules >= 3.2.3

%description
This rpm contains modules configuration files for the default setup
of intel %{intelshortversion} compilers.  It will try load C, Fortran and
Iidb for this version if you do not specify otherwise.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{compiler}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/default <<ENDDEFAULT
#%Module1.0#####################################################################
##
## default modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module gets loaded by default if you do"
        puts stderr "\t\tmodule load intel/%{intelshortversion}/%{intelbits}"
        puts stderr "\tand it attempts configure both intel C and Fortran compilers"
        puts stderr "\tas well as the Intel idb debugger for Intel Compilers version %{intelshortversion}"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

# We check to see if any incompatible intel compilers are loaded
if {[module-info mode load] && ![module-info mode remove]} {
  if {[info exists env(LOADEDMODULES)]} {
    set envloaded [split \$env(LOADEDMODULES) ":"]
    foreach mod [lsort -decreasing \$envloaded] {
      set mmod "\$mod/"
      # only consider intel modules
      if {[string first "intel/" \$mmod] == 0 && [string first "intel/%{intelshortversion}/" \$mmod] != 0 && [string first "intel/%{intelshortversion}/%{intelbits}/" \$mmod] != 0 } {
        puts stderr "Conflicting Intel module \$mod - removing before inserting requested module intel/%{intelshortversion}/%{intelbits}/default"
        module unload \$mod
      }
    }
  }
}

module-whatis   "Loads Intel C and Fortran Compilers and the debugger for %{intelshortversion} %{intelbits} bit"
module load intel/%{intelshortversion}/%{intelbits}/C
module load intel/%{intelshortversion}/%{intelbits}/Fortran
module load intel/%{intelshortversion}/%{intelbits}/Iidb
append-path LD_LIBRARY_PATH /usr/local/intel/%{_lib}
#append-path -d { } LOCAL_LDFLAGS "-L/usr/local/intel/%{_lib}"
#append-path -d { } LOCAL_CFLAGS "-I/usr/local/intel/include"
#append-path -d { } LOCAL_CXXFLAGS "-I/usr/local/intel/include"
#append-path -d { } LOCAL_FFLAGS "-I/usr/local/intel/include"

set     version      "3.2.3"
ENDDEFAULT

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{modulesdestination}/intel
%dir %{modulesdestination}/intel/%{intelshortversion}
%dir %{modulesdestination}/intel/%{intelshortversion}/%{intelbits}
%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/default
