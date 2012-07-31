# The following defines the version of compiler we are doing this for so 
# that we can do this easily as new versions come out, directly when
# rebuilding this src.rpm
%{!?intelversion:%define intelversion 12.1.9.293}
%{!?intelyear:%define intelyear 2011}
%{!?intelmklversion:%define intelmklversion 10.3}
# the mpi version is from /opt/intel/composerxe-2011.4.191/mpirt/bin/intel64/mpi-rtsupport.txt
%{!?intelmpirtversion:%define intelmpirtversion 4.0.2.003}
%define intelextrad -sp1
%define intelextra_ _sp1

# The rest should be figured out automatically just from the above two things
%define intelshortversion %(echo %{intelversion} | cut -d. -f1-2)
%define intelshortshortversion %(echo %{intelversion} | cut -d. -f1)
%define intelupdate %(echo %{intelversion} | cut -d. -f3)
%define intelrelease %(echo %{intelversion} | cut -d. -f4)
%define intelnumversion %(echo %{intelversion} | tr -d \.)
%define intelmpirtshortversion %(echo %{intelmpirtversion} | cut -d. -f1-2)
%define intelmpirtrelease %(echo %{intelmpirtversion} | cut -d. -f3-4)

# Our root dir is now always:
%define intelinstalldir /opt/intel/composer_xe_%{intelyear}%{intelextra_}.%{intelupdate}.%{intelrelease}

# here for different bits
%ifarch i486 i686
%define intelbits 32
%define archdir ia32
%else
%ifarch ia64
%define intelbits 64
%define archdir ia64
%else
%define intelbits 64
%define archdir intel64
%endif
%endif

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles

Summary: Modules configuration files for Intel CompilerPro XE %{intelyear} %{intelshortversion} Update %{intelupdate}
Name: intel-compilerpro%{intelnumversion}-modules
Version: %{intelversion}
Release: 18%{?dist}
License: Other
Group: Development/Languages
ExclusiveArch: i486 x86_64 ia64 i686
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Provides: intel-compilerpro%(echo %{intelshortversion} | tr -d \.)-modules = %{intelversion}
Provides: intel-compilerpro%(echo %{intelshortversion} | tr -d \.)-modules = %{intelshortversion}-%{intelupdate}
Provides: intel-compilerpro%(echo %{intelshortshortversion} | tr -d \.)-modules = %{intelversion}
Provides: intel-compilerpro%(echo %{intelshortshortversion} | tr -d \.)-modules = %{intelshortversion}-%{intelupdate}
Provides: intel-compilerpro-modules = %{intelversion}
Provides: intel-compilerpro-modules = %{intelshortversion}-%{intelupdate}
Provides: intel-compiler-default-modules = %{intelshortversion}-%{intelupdate}
Provides: intel-compiler%{intelshortshortversion}-%{intelbits}-default-modules = %{intelshortversion}-%{intelupdate}
Provides: intel-compiler-%{intelbits}-default-modules = %{intelshortversion}-%{intelupdate}
Requires: environment-modules >= 3.2.3
Requires: intel-license
Requires: hardlink
Requires: compat-libstdc++-33
Requires: intel-mkl%{intelextrad}-%{intelrelease} = %{intelmklversion}-%{intelupdate}
Requires: intel-compilerpro-common-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-compilerpro-vars-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-compilerproc-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-compilerprof-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-openmp-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-idb-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-idb-common-%{intelrelease} = %{intelshortversion}-%{intelupdate}
%ifarch x86_64
Provides: libcilkrts.so.5()(64bit)
%else
Provides: libcilkrts.so.5
%endif

%description
This rpm contains modules configuration files for the Intel CompilerPro XE
version %{intelyear} %{intelshortversion} Update %{intelupdate}

It also fixes up various scripts like icc, ifc, icvars and other Intel 
scripts where they reference INSTALLDIR (in original Intel's RPM).

%package devel
Group: Development/Languages
Summary: Configuration files for Intel compilerpro XE %{intelyear} %{intelshortversion} Update %{intelupdate}
Requires: intel-compilerpro%{intelnumversion}-modules = %{version}-%{release}
Requires: intel-compilerpro-devel-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-compilerproc-devel-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-compilerprof-devel-%{intelrelease} = %{intelshortversion}-%{intelupdate}
Requires: intel-mkl%{intelextrad}-devel-%{intelrelease} = %{intelmklversion}-%{intelupdate}
Provides: intel-compilerpro%(echo %{intelshortversion} | tr -d \.)-modules-devel = %{intelversion}
Provides: intel-compilerpro%(echo %{intelshortversion} | tr -d \.)-modules-devel = %{intelshortversion}-%{intelupdate}
Provides: intel-compilerpro%(echo %{intelshortshortversion} | tr -d \.)-modules-devel = %{intelversion}
Provides: intel-compilerpro%(echo %{intelshortshortversion} | tr -d \.)-modules-devel = %{intelshortversion}-%{intelupdate}
Provides: intel-compilerpro-modules-devel = %{intelversion}
Provides: intel-compilerpro-modules-devel = %{intelshortversion}-%{intelupdate}
Provides: intel-compiler-default-modules-devel = %{intelshortversion}-%{intelupdate}
Provides: intel-compiler%{intelshortshortversion}-%{intelbits}-default-modules-devel = %{intelshortversion}-%{intelupdate}
Provides: intel-compiler-%{intelbits}-default-modules-devel = %{intelshortversion}-%{intelupdate}

%description devel
This rpm just contains relevant development requirements.

%package mpirt
Group: Development/Languages
Summary: Configuration files for Intel MPI runtime included in compilerpro XE %{intelyear} %{intelshortversion} Update %{intelupdate}
Requires: intel-compilerpro%{intelnumversion}-modules = %{version}-%{release}
Provides: intel-mpirt = %{intelmpirtrelease}-%{intelmpirtshortversion}

%description mpirt
This rpm just contains the MPI RT environment module.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}
mkdir -p $RPM_BUILD_ROOT/usr/local/intel/{bin,include,%{_lib}}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/%{intelversion} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{intelversion} %{intelbits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Intel CompilerPro XE %{intelyear} %{intelshortversion} Update %{intelupdate} %{intelbits}bit"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for the Intel %{intelversion} %{intelbits} bit"
prepend-path	PATH		%{intelinstalldir}/bin/%{archdir}:/usr/local/intel/bin
prepend-path	LD_LIBRARY_PATH	%{intelinstalldir}/compiler/lib/%{archdir}:%{intelinstalldir}/debugger/lib/%{archdir}:/usr/local/intel/%{_lib}
prepend-path	NLSPATH		%{intelinstalldir}/compiler/lib/%{archdir}/locale/%l_%t/%N:%{intelinstalldir}/debugger/%{archdir}/locale/%l_%t/%N
setenv		LANGUAGE_TERRITORY	en_US
prepend-path	MANPATH		%{intelinstalldir}/man/en_US
prepend-path	INCLUDE		/usr/local/intel/include
prepend-path	CPATH		/usr/local/intel/include
prepend-path	FPATH		/usr/local/intel/include
prepend-path	LIBRARY_PATH	%{intelinstalldir}/compiler/lib/%{archdir}:/usr/local/intel/%{_lib}
prepend-path	INTEL_LICENSE_FILE	/opt/intel/licenses:${HOME}/intel/licenses
append-path -delim { } LOCAL_LDFLAGS "-L%{intelinstalldir}/compiler/lib/%{archdir} -L/usr/local/intel/%{_lib}"
append-path -delim { } LOCAL_CFLAGS -I/usr/local/intel/include
append-path -delim { } LOCAL_CXXFLAGS -I/usr/local/intel/include
append-path -delim { } LOCAL_FFLAGS -I/usr/local/intel/include
# load exactly the right mkl module
module load intel-mkl/%{intelmklversion}/%{intelupdate}/%{intelbits}
set     version      "3.2.3"
ENDDEFAULT

mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel-mkl/%{intelmklversion}/%{intelupdate}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel-mkl/%{intelmklversion}/%{intelupdate}/%{intelbits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{intelmklversion} %{intelupdate} %{intelbits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Intel MKL Libraries %{intelmklversion} Update %{intelupdate} %{intelbits}bit"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for the Intel MKL Libraries %{intelmklversion}-%{intelupdate} %{intelbits} bit"
prepend-path	LD_LIBRARY_PATH	%{intelinstalldir}/compiler/lib/%{archdir}:%{intelinstalldir}/mkl/lib/%{archdir}
prepend-path	LIBRARY_PATH	%{intelinstalldir}/compiler/lib/%{archdir}:%{intelinstalldir}/mkl/lib/%{archdir}
prepend-path	MANPATH		%{intelinstalldir}/man/en_US
prepend-path	NLSPATH		%{intelinstalldir}/mkl/lib/%{archdir}/locale/%l_%t/%N
setenv		LANGUAGE_TERRITORY	en_US
setenv		OMP_NUM_THREADS		1
prepend-path	INCLUDE		%{intelinstalldir}/mkl/include
prepend-path	CPATH		%{intelinstalldir}/mkl/include
prepend-path	FPATH		%{intelinstalldir}/mkl/include
prepend-path	INTEL_LICENSE_FILE	/opt/intel/licenses
append-path -delim { } LOCAL_LDFLAGS "-L%{intelinstalldir}/compiler/lib/%{archdir} -L%{intelinstalldir}/mkl/lib/%{archdir}"
append-path -delim { } LOCAL_CFLAGS "-I%{intelinstalldir}/mkl/include"
append-path -delim { } LOCAL_CXXFLAGS "-I%{intelinstalldir}/mkl/include"
append-path -delim { } LOCAL_FFLAGS "-I%{intelinstalldir}/mkl/include"
set     version      "3.2.3"
ENDDEFAULT

mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel-mpirt/%{intelmpirtshortversion}/%{intelmpirtrelease}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel-mpirt/%{intelmpirtshortversion}/%{intelmpirtrelease}/%{intelbits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{intelmpirtshortversion} %{intelmpirtrelease} %{intelbits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Intel MPI Runtime Libraries %{intelmpirtshortversion} Update %{intelmpirtrelease} %{intelbits}bit"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for the Intel MPI Runtime Libraries %{intelmpirtshortversion}.%{intelmpirtrelease} %{intelbits} bit"
prepend-path	PATH		%{intelinstalldir}/mpirt/bin/%{archdir}
prepend-path	LD_LIBRARY_PATH	%{intelinstalldir}/mpirt/lib/%{archdir}
prepend-path	LIBRARY_PATH	%{intelinstalldir}/mpirt/lib/%{archdir}
prepend-path	INTEL_LICENSE_FILE	/opt/intel/licenses
append-path -delim { } LOCAL_LDFLAGS "-L%{intelinstalldir}/mpirt/lib/%{archdir}"
append-path -delim { } LOCAL_LDFLAGS "-L%{intelinstalldir}/mpirt/lib/%{archdir}"
set     version      "3.2.3"
ENDDEFAULT

cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/.modulerc-intel-%{intelnumversion}-%{intelbits} <<ENDGENERIC
#%Module
module-alias intel/%{intelshortshortversion} intel/%{intelshortversion}
ENDGENERIC
mkdir $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortshortversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel/%{intelshortshortversion}/.modulerc-intel-%{intelnumversion}-%{intelbits} <<ENDMOREGENERIC
#%Module
module-alias intel/%{intelshortshortversion}/%{intelbits} intel/%{intelshortversion}/%{intelbits}
ENDMOREGENERIC

%post
/usr/sbin/hardlink -c %{intelinstalldir} /opt/intel >/dev/null 2>&1 || :

%post devel
/usr/sbin/hardlink -c %{intelinstalldir} /opt/intel >/dev/null 2>&1 || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{modulesdestination}/intel
%dir %{modulesdestination}/intel/%{intelshortversion}
%dir %{modulesdestination}/intel/%{intelshortversion}/%{intelbits}
%{modulesdestination}/intel/%{intelshortversion}/%{intelbits}/*
%{modulesdestination}/intel/.modulerc-intel-%{intelnumversion}-%{intelbits}
%dir %{modulesdestination}/intel/%{intelshortshortversion}
%{modulesdestination}/intel/%{intelshortshortversion}/.modulerc-intel-%{intelnumversion}-%{intelbits}
%dir %{modulesdestination}/intel-mkl/
%dir %{modulesdestination}/intel-mkl/%{intelmklversion}
%dir %{modulesdestination}/intel-mkl/%{intelmklversion}/%{intelupdate}
%{modulesdestination}/intel-mkl/%{intelmklversion}/%{intelupdate}/%{intelbits}
%dir /usr/local/intel/bin
%dir /usr/local/intel/%{_lib}

%files devel
%defattr(-,root,root)
%dir /usr/local/intel/include

%files mpirt
%defattr(-,root,root)
%dir %{modulesdestination}/intel-mpirt
%dir %{modulesdestination}/intel-mpirt/%{intelmpirtshortversion}
%dir %{modulesdestination}/intel-mpirt/%{intelmpirtshortversion}/%{intelmpirtrelease}
%{modulesdestination}/intel-mpirt/%{intelmpirtshortversion}/%{intelmpirtrelease}/%{intelbits}

%changelog
* Fri Oct 07 2011 Josko Plazonic <plazonic@math.princeton.edu>
- upgraded to 12.1.06.233, split up mpirt into separate package

* Thu Jun 16 2011 Josko Plazonic <plazonic@math.princeton.edu>
- intel compiler suite 12.0 aka Composer XE update, also split 
  up mkl and mpi bits into separate module

* Thu Dec 03 2009 Josko Plazonic <plazonic@math.princeton.edu>
- added /usr/local/intel/bin to the path and the appropriate dirs to rpm 
  ownership (to ensure existence)
- updated to 11.1.059
