%{!?intelmpiversion:%define intelmpiversion 4.0.3}
%{!?intelmpirelease:%define intelmpirelease 008}

%define intelversion %{intelmpiversion}.%{intelmpirelease}
# Our root dir is now always:
%define intelinstalldir /opt/intel/impi/%{intelversion}

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
%define modulesdestination /opt/share/Modules/modulefiles/intel-mpi

Summary: Modules configuration files for Intel MPI
Name: intel-mpi-modules
Version: %{intelmpiversion}p
Release: %{intelmpirelease}.3%{?dist}
License: Other
Group: Development/Languages
ExclusiveArch: i486 x86_64 ia64 i686
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: environment-modules >= 3.2.3
Requires: intel-license
Requires: compat-libstdc++-33
Requires: intel-mpi-rt-%{archdir} = %{intelmpiversion}p-%{intelmpirelease}
%ifarch x86_64
Provides: libjmi_slurm.so.1()(64bit) libmpi.so.4()(64bit) libmpi_ilp64.so.4()(64bit) libmpi_lustre.so.4.0()(64bit)
Provides: libmpi_mt.so.4()(64bit) libmpi_panfs.so.4.0()(64bit) libmpi_pvfs2.so.4.0()(64bit) libmpigc3.so.4()(64bit)
Provides: libmpigc4.so.4()(64bit) libmpigf.so.4()(64bit) libtmi.so.1.0()(64bit) libtmip_mx.so.1.0()(64bit) libtmip_psm.so.1.0()(64bit)
%endif

%description
This rpm contains modules configuration files for the Intel MPI

%package gcc
Group: Development/Languages
Summary: Modules configuration files for Intel MPI with gcc
Requires: %{name} = %{version}-%{release}

%description gcc
This rpm contains modules configuration files for the Intel MPI for gcc
compiler.

%package intel
Group: Development/Languages
Summary: Modules configuration files for Intel MPI with intel compilers
Requires: %{name} = %{version}-%{release}

%description intel
This rpm contains modules configuration files for the Intel MPI for intel
compilers.


%package devel
Group: Development/Languages
Summary: Configuration files for Intel MPI development
Requires: %{name} = %{version}-%{release}
Requires: intel-mpi-%{archdir} = %{intelmpiversion}p-%{intelmpirelease}
Requires: intel-mpi-rt = %{intelmpiversion}p-%{intelmpirelease}
Requires: intel-mpi = %{intelmpiversion}p-%{intelmpirelease}
%ifarch x86_64
Provides: libmpi_dbg.so.4()(64bit) libmpi_dbg_mt.so.4()(64bit) libmpi_log.so.4()(64bit) libmpi_log_mt.so.4()(64bit) libtvmpi.so.4()(64bit)
%endif

%description devel
This rpm just contains relevant development requirements for
all compilers

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/{gcc,intel}/%{intelversion}
for i in gcc intel; do
if [ "$i" = "gcc" ]; then
	EXTRA="setenv MPICH_CC gcc
setenv MPICH_CXX g++
setenv MPICH_F77 gfortran
setenv MPICH_F90 gfortran
"
	L=/usr/local/%{_lib}/intel-mpi
	I=/usr/local/include
fi
if [ "$i" = "intel" ]; then
	EXTRA="setenv MPICH_CC icc
setenv MPICH_CXX icpc
setenv MPICH_F77 ifort
setenv MPICH_F90 ifort
"
	L=/usr/local/intel/%{_lib}/intel-mpi
	I=/usr/local/intel/include
fi
mkdir -p $RPM_BUILD_ROOT/$L
mkdir -p $RPM_BUILD_ROOT/$I
cat > $RPM_BUILD_ROOT%{modulesdestination}/$i/%{intelversion}/%{intelbits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{intelversion} %{intelbits} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets paths for Intel MPI %{intelmpiversion}p-%{intelmpirelease} %{intelbits}bit with compiler $i"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for Intel %{intelmpiversion}p-%{intelmpirelease} %{intelbits} bit with compiler $i"
prepend-path	PATH		%{intelinstalldir}/%{archdir}/bin
prepend-path	LD_LIBRARY_PATH	%{intelinstalldir}/%{archdir}/lib:$L
prepend-path	MANPATH		%{intelinstalldir}/man
prepend-path	INCLUDE		%{intelinstalldir}/%{archdir}/include:$I
prepend-path	CPATH		%{intelinstalldir}/%{archdir}/include:$I
prepend-path	FPATH		%{intelinstalldir}/%{archdir}/include:$I
prepend-path	LIBRARY_PATH	%{intelinstalldir}/%{archdir}/lib:$L
prepend-path	INTEL_LICENSE_FILE	/opt/intel/licenses:${HOME}/intel/licenses
$EXTRA
append-path -delim { } LOCAL_LDFLAGS "-L%{intelinstalldir}/%{archdir}/lib -L$L"
append-path -delim { } LOCAL_CFLAGS "-I%{intelinstalldir}/%{archdir}/include -I$L"
append-path -delim { } LOCAL_CXXFLAGS "-I%{intelinstalldir}/%{archdir}/include -I$L"
append-path -delim { } LOCAL_FFLAGS "-I%{intelinstalldir}/%{archdir}/include -I$L"
set     version      "3.2.3"
ENDDEFAULT
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{modulesdestination}

%files gcc
%defattr(-,root,root)
%dir %{modulesdestination}/gcc
%dir %{modulesdestination}/gcc/%{intelversion}
%{modulesdestination}/gcc/%{intelversion}/*
%dir /usr/local/%{_lib}/intel-mpi

%files intel
%defattr(-,root,root)
%dir %{modulesdestination}/intel
%dir %{modulesdestination}/intel/%{intelversion}
%{modulesdestination}/intel/%{intelversion}/*
%dir /usr/local/intel/%{_lib}/intel-mpi

%files devel
%defattr(-,root,root)

%changelog
* Sun Apr 08 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
