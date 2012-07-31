# The following defines the version of compiler we are doing this for so 
# that we can do this easily as new versions come out, directly when
# rebuilding this src.rpm
%{!?intelversion:%define intelversion 9.1.053}

# is this for C or Fortran? - set to icc, icce, ifort or iforte
%{!?intelcompiler:%define intelcompiler iidbe}

# does it obsolete anything, not by default
%define intelobsoletes %{nil}

# The rest should be figured out automatically just from the above two things
%{!?intelshortversion:%define intelshortversion %(echo %{intelversion} | cut -d. -f1-2)}
%if "%{intelshortversion}" == "9.1" || "%{intelshortversion}" == "10.1"
%define intelnumversion %(echo %{intelversion} | tr -d \.)
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
%if "%{intelcompiler}" == "icc"
%if "%{intelnumversion}" == "8"
%define intelinstalldir /opt/intel_cc_80
%else
%define intelinstalldir /opt/intel/cc/%{intelversion}
%endif
ExclusiveArch: i386
%define intelbits 32
%define compiler C
%endif

%if "%{intelcompiler}" == "icce"
%if "%{intelnumversion}" == "8"
%define intelinstalldir /opt/intel_cce_80
%else
%define intelinstalldir /opt/intel/cce/%{intelversion}
%endif
ExclusiveArch: x86_64
%define intelbits 64
%define compiler C
%endif

%if "%{intelcompiler}" == "ifort"
%if "%{intelnumversion}" == "8"
%define intelinstalldir /opt/intel_fc_80
%else
%define intelinstalldir /opt/intel/fc/%{intelversion}
%endif
ExclusiveArch: i386
%define intelbits 32
%define compiler Fortran
%endif

%if "%{intelcompiler}" == "iforte"
%if "%{intelnumversion}" == "8"
%define intelinstalldir /opt/intel_fce_80
%else
%define intelinstalldir /opt/intel/fce/%{intelversion}
%endif
ExclusiveArch: x86_64
%define intelbits 64
%define compiler Fortran
%endif

%if "%{intelcompiler}" == "iidb"
%if "%{intelnumversion}" == "8"
%define intelinstalldir /opt/intel_idb_80
%else
%define intelinstalldir /opt/intel/idb/%{intelversion}
%endif
ExclusiveArch: i386
%define intelbits 32
%define compiler Iidb
%define inteltype debugger
%endif

%if "%{intelcompiler}" == "iidbe"
%if "%{intelnumversion}" == "8"
%define intelinstalldir /opt/intel_idbe_80
%else
%define intelinstalldir /opt/intel/idbe/%{intelversion}
%endif
ExclusiveArch: x86_64
%define intelbits 64
%define compiler Iidb
%define inteltype debugger
%endif

#if "%{intelshortversion}" == "10.1"
#define intelobsoletes Obsoletes: intel-%{intelcompiler}100026-modules \
#Obsoletes: intel-%{intelcompiler}10-modules < %{intelversion} \
#Obsoletes: intel-%{intelcompiler}100026
#endif

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles

# all the scripts that might need fixing
%define scriptstofix ifortvars.sh ifortvars.csh iccvars.sh iccvars.csh ifort ifc icc icpc ifc.cfg ifort.cfg idbvars.csh idbvars.sh

Summary: Modules configuration files for intel-%{intelcompiler}%{intelnumversion}-%{intelversion} compiler
Name: intel-%{intelcompiler}%{intelnumversion}-modules
Version: %{intelversion}
Release: 17.PU_IAS.5
License: Other
Group: Development/Languages
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: intel-%{intelcompiler}%{intelnumversion} = %{intelversion}
Requires: environment-modules >= 3.2.3
%if "%{intelshortversion}" == "9.1"
Provides: intel-%{intelcompiler}91-modules = %{intelversion}
%endif
%if "%{intelshortversion}" == "10.1"
Provides: intel-%{intelcompiler}101-modules = %{intelversion}
Provides: intel-%{intelcompiler}10-modules = %{intelversion}
%endif
Provides: intel-%{intelcompiler}-modules = %{intelversion}
%{intelobsoletes}

%description
This rpm contains modules configuration files for the Intel
intel-%{intelcompiler}%{intelnumversion}-%{intelversion} compiler

It also fixes up various scripts like icc, ifc, icvars and other Intel 
scripts where they reference INSTALLDIR (in original Intel's RPM).

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{compiler}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{compiler}/%{intelversion} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{compiler} %{intelversion} %{inteltype} %{intelbits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Intel %{compiler} %{intelversion} %{inteltype} %{intelbits} bit"
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
        puts stderr "Conflicting Intel module \$mod - removing before inserting requested module intel/%{intelshortversion}/%{intelbits}/%{compiler}/%{intelversion}"
        module unload \$mod
      } else {
        # if we are here it means we are under the same intel compiler version and architecture
        # now check if same compiler type but different version, if so remove it
        if {[string first "intel/%{intelshortversion}/%{intelbits}/%{compiler}" \$mmod] == 0 && [string compare "intel/%{intelshortversion}/%{intelbits}/%{compiler}/%{intelversion}/" \$mmod] != 0} {
          puts stderr "Conflicting Intel module \$mod - removing before inserting requested module intel/%{intelshortversion}/%{intelbits}/%{compiler}/%{intelversion}"
          module unload \$mod
        }
      }
    }
  }
}

# and now treat special removals
if {[module-info mode remove] && ![module-info mode load]} {
  set modtoremove "[module-info specified]/"
  set ourname     "[module-info name]/"
  if {[string compare \$modtoremove \$ourname] != 0} {
    set envloaded [split \$env(LOADEDMODULES) ":"]
    foreach mod [lsort -decreasing \$envloaded] {
      set mmod "\$mod/"
      if {[info exists env(LOADEDMODULES)] && [string first \$modtoremove \$mmod] == 0 && [string compare \$mmod \$ourname] != 0} {
        module unload \$mod
      }
    }
  }
}

module-whatis   "Loads settings for the Intel %{compiler} %{inteltype} %{intelversion} %{intelbits} bit"
prepend-path	PATH		%{intelinstalldir}/bin
prepend-path	MANPATH		%{intelinstalldir}/man
%if "%{inteltype}" != "debugger"
prepend-path	LD_LIBRARY_PATH	%{intelinstalldir}/lib
#append-path -d { } LOCAL_LDFLAGS	"-L%{intelinstalldir}/lib"
%endif
set     version      "3.2.3"
ENDDEFAULT

%post
for i in %{scriptstofix}; do
%if "%{intelnumversion}" == "8"
	# for this version we also have to fix up INTEL_LICENSE_FILE better
	[ -e %{intelinstalldir}/bin/$i ] && perl -pi -e "s|<INSTALLDIR>/licenses|%{intelinstalldir}/licenses:/opt/intel/licenses:\${HOME}/intel/licenses|g" %{intelinstalldir}/bin/$i || :
%endif
%if "%{intelnumversion}" == "9"
	# for this version we also have to fix up INTEL_LICENSE_FILE better
	[ -e %{intelinstalldir}/bin/$i ] && perl -pi -e "s|<INSTALLDIR>/licenses:/opt/intel/licenses|%{intelinstalldir}/licenses:/opt/intel/licenses:\${HOME}/intel/licenses|g" %{intelinstalldir}/bin/$i || :
%endif
	[ -e %{intelinstalldir}/bin/$i ] && perl -pi -e "s|<INSTALLDIR>|%{intelinstalldir}|g" %{intelinstalldir}/bin/$i || :
done

# this is just in case we get a revision of the compiler - i.e.
# same version but different release so it installs in the same
# location so we might need to fix up files again
%triggerin -- intel-%{intelcompiler}%{intelnumversion}
for i in %{scriptstofix}; do
%if "%{intelnumversion}" == "8"
	# for this version we also have to fix up INTEL_LICENSE_FILE better
	[ -e %{intelinstalldir}/bin/$i ] && perl -pi -e "s|<INSTALLDIR>/licenses|%{intelinstalldir}/licenses:/opt/intel/licenses:\${HOME}/intel/licenses|g" %{intelinstalldir}/bin/$i || :
%endif
%if "%{intelnumversion}" == "9"
	# for this version we also have to fix up INTEL_LICENSE_FILE better
	[ -e %{intelinstalldir}/bin/$i ] && perl -pi -e "s|<INSTALLDIR>/licenses:/opt/intel/licenses|%{intelinstalldir}/licenses:/opt/intel/licenses:\${HOME}/intel/licenses|g" %{intelinstalldir}/bin/$i || :
%endif
	[ -e %{intelinstalldir}/bin/$i ] && perl -pi -e "s|<INSTALLDIR>|%{intelinstalldir}|g" %{intelinstalldir}/bin/$i || :
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{modulesdestination}/intel
%dir %{modulesdestination}/intel/%{intelshortversion}
%dir %{modulesdestination}/intel/%{intelshortversion}/%{intelbits}
%dir %{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{compiler}
%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{compiler}/*
