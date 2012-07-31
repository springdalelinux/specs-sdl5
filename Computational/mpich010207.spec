%define	 mp_name	mpich
%define	 mp_mversion	1.2.7
%define	 mp_release	p1
%define  mp_version	%{mp_mversion}%{mp_release}

%define me_name		mpiexec
%define me_version	0.81

# 32 or 64?
%ifarch %{ix86}
%define modulebits 32
%else
%define modulebits 64
%endif
# The name of the modules RPM
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}

# compiler for which we are doing this
%define compiler pgi90

# whether this is a debug version or not? comment out for debug version
#define mpich_debug 1

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilershort gcc
# rhel4 does not have f90, for simplicity pretent it is g77
%if "%{?rhel}" == "4"
%define gfortran g77
%else
%define gfortran gfortran
%endif
%define compilerruntimesection BuildRequires: gcc-%{gfortran} gcc-c++
%define compilerdevelsection Requires: gcc-%{gfortran} gcc-c++
%define compilermpiexecsection %{nil}
%define localdir /usr/local
# do nothing special for gcc for build prep
%define compilerbuildprep export CC=gcc CXX=g++ F77=%{gfortran} FC=%{gfortran} F90=%{gfortran} F77_GETARGDECL=" "
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define fflags %{cflags}
# we need a special ldflags
%define ldflags -Wl,-z,noexecstack
# this is for configuring modules
%define compilermodulename gcc
%define compilerloadmodule %{nil}
# and this is a list of conflicting modules
%define compilerconflictmodule openmpi/ mpich2/ lam/ intel/ pgi/
%define compilermodulefile %{nil}
%endif
#
# Intel 9.1 compiler
%if "%{compiler}" == "intel91"
%define compilershort intel
%define compilershortversion intel-9
%if "%{?rhel}" == "4"
%define intelmodule intel-compiler91-default-modules
%else
%define intelmodule intel-compiler91-%{modulebits}-default-modules
%endif
%define compilerruntimesection BuildRequires: %{intelmodule}\
Requires: %{intelmodule}\
Provides: mpich%{debug}-intel = %{version}-091.%{release}
%define compilerdevelsection Provides: mpich%{debug}-intel-devel = %{version}-091.%{release}
%define compilermpiexecsection %{nil}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort FC=ifort F90=ifort; . /etc/profile.d/modules.sh; module load intel
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define fflags %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-9.1
%define compilerloadmodule module load intel/9.1/%{modulebits}
%define compilerconflictmodule openmpi/ mpich2/ lam/ pgi/
%define compilermodulefile .modulerc-intel-%{modulebits}-091
%endif
#
# Intel 10.1 compiler
%if "%{compiler}" == "intel101" || "%{compiler}" == "intel110"
# we will extract versions we need out of above string
%define intelmajor %( echo %{compiler} | cut -b6-7 )
%define intelminor %( echo %{compiler} | cut -b8 ) 
%define intelversion %{intelmajor}.%{intelminor} 
%define intelversionnum %{intelmajor}%{intelminor}
%define compilershort intel
%define compilershortversion intel-%{intelmajor}
%define compilerruntimesection BuildRequires: intel-compiler-%{modulebits}-default-modules >= %{intelversion}\
Requires: intel-compiler-%{modulebits}-default-modules >= %{intelversion}\
Provides: mpich%{debug}-intel = %{version}-%{intelversionnum}.%{release}\
Obsoletes: mpich010207%{debug}-intel100-runtime
%define compilerdevelsection Provides: mpich%{debug}-intel-devel = %{version}-%{intelversionnum}.%{release} \
Obsoletes: mpich010207%{debug}-intel100-devel
%define compilermpiexecsection Obsoletes: mpich010207%{debug}-intel100-mpiexec
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort FC=ifort F90=ifort; . /etc/profile.d/modules.sh; module load intel
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define fflags %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-%{intelversion}
%define compilerloadmodule module load intel/%{intelmajor}/%{modulebits}
%define compilerconflictmodule openmpi/ mpich2/ lam/ pgi/
%define compilermodulefile .modulerc-intel-%{modulebits}-%{intelversionnum}
%endif
#
# PGI compiler
%if "%{compiler}" == "pgi71" || "%{compiler}" == "pgi80" || "%{compiler}" == "pgi90"
# we will extract versions we need out of above string
%define pgimajor %( echo %{compiler} | cut -b4 )
%define pgiminor %( echo %{compiler} | cut -b5 )
%define pgiversion %{pgimajor}.%{pgiminor}
%define pgiversionnum 0%{pgimajor}%{pgiminor}
%define compilershort pgi
%define compilershortversion pgi-%{pgimajor}
%define compilerruntimesection BuildRequires: pgi-workstation >= %{pgiversion} \
Requires: pgi-workstation-libs >= %{pgiversion}\
Provides: mpich%{debug}-pgi = %{version}-%{pgiversionnum}.%{release}
%define compilerdevelsection Requires: pgi-workstation >= %{pgiversion} \
Provides: mpich%{debug}-pgi-devel = %{version}-%{pgiversionnum}.%{release}
%define compilermpiexecsection %{nil}
%define localdir /usr/local/pgi
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pgcc CXX=pgCC F77=pgf77 FC=pgf77 F90=pgf90; . /etc/profile.d/modules.sh; module load pgi
%define cflags -fast
%define cxxflags %{cflags}
%define fflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pgi-%{pgiversion}
%define compilerloadmodule module load pgi/%{pgimajor}/%{modulebits}
%define compilerconflictmodule openmpi/ mpich2/ lam/ intel/
%define compilermodulefile .modulerc-pgi-%{modulebits}-%{pgiversionnum}
%endif
#
# Pathscale compiler
%if "%{compiler}" == "pathscale32"
# we will extract versions we need out of above string
%define pathscalemajor %( echo %{compiler} | cut -b10 )
%define pathscaleminor %( echo %{compiler} | cut -b11 )
%define pathscaleversion %{pathscalemajor}.%{pathscaleminor}
%define pathscaleversionnum 0%{pathscalemajor}%{pathscaleminor}
%define compilershort pathscale
%define compilershortversion pathscale-%{pathscalemajor}
%define compilerruntimesection BuildRequires: pathscale-compilers >= %{pathscaleversion} \
Requires: pathscale-compilers-libs >= %{pathscaleversion}\
Provides: mpich%{debug}-pathscale = %{version}-%{pathscaleversionnum}.%{release}
%define compilerdevelsection Requires: pathscale-compilers >= %{pathscaleversion} \
Provides: mpich%{debug}-pathscale-devel = %{version}-%{pathscaleversionnum}.%{release}
%define compilermpiexecsection %{nil}
%define localdir /usr/local/pathscale
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pathcc CXX=pathCC F77=pathf90 FC=pathf90; . /etc/profile.d/modules.sh; module load pathscale
%define cflags -O3
%define cxxflags %{cflags}
%define fflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pathscale-%{pathscaleversion}
%define compilerloadmodule module load pathscale/%{pathscalemajor}/%{modulebits}
%define compilerconflictmodule openmpi/ mpich2/ lam/ intel/
%define compilermodulefile .modulerc-pathscale-%{modulebits}-%{pathscaleversionnum}
%endif


# debug macro name
%{?mpich_debug: %define debug -debug}
%{!?mpich_debug: %define debug %{nil}}
# root path to install modulefiles
%{!?modulefile_path: %define modulefile_path /usr/local/share/Modules/modulefiles/mpich%{debug}}

%define debug_package %{nil}
%{?mpich_debug: %define __os_install_post /usr/lib/rpm/brp-compress}

# Pick the device.  The ch_p4mpd device is recommended for clusters of
# uniprocessors; the ch_p4 device with comm=shared is appropriate for
# clusters of SMPs.  
#define device ch_p4
#define other_device_opts %{nil}
# (warning: you cannot comment out a macro definition because they
# are apparently evaluated *before* comment processing (!!!)
# for ch_p4:
%define device ch_p4
%define other_device_opts %{nil}
#define other_device_opts --with-comm=shared
# You may also want to set
# define rshcommand /usr/bin/ssh
# define rcpcommand /usr/bin/rcp
# for ch_p4 with bproc (see mpich-scyld.spec instead, but the following is
# a start:)
# define device ch_p4
# define other_device_opts --with-comm=bproc
# for ch_shmem:
# define device ch_shmem
# define other_device_opts %{nil}

#
# Define this to +pvfs if pvfs is available.
%define other_file_systems %{nil}

#
# Define any other options for configure.  For example, 
# Turn off mpe
# define other_config_opts --without-mpe
# Turn off building the logfile viewers
# define other_config_opts -mpe-opts=--disable-viewers
%define other_config_opts %{nil}

#
# Allow overriding the default PBS directory
#   --define 'torquedir <dir>'
%{!?torquedir: %define torquedir /usr}

# we need this for backwards compatibility
# before RHEL5 we had /usr/local/intel/openmpi-intel and now we have /usr/local/intel/openmpi
# i.e. the duplicate -intel has been dropped.  Act accordingly to distro:
%if "%{?rhel}" == "4"
%define localdirlib %{localdir}/%{_lib}/mpich-%{compilershort}
%else
%define localdirlib %{localdir}/%{_lib}/mpich
%endif

Summary: 	Argonne National Laboratory MPI implementation for %{compiler} compiler
Name: 		%{mp_name}010207%{debug}-%{compiler}
Version: 	%{mp_version}
Release: 	10.%{mp_release}.6%{?dist}
Vendor: 	Argonne National Laboratory
Packager: 	William Gropp <gropp@mcs.anl.gov>
License: 	BSD-like
Group: 		System Environment/Libraries 
URL:		http://www.mcs.anl.gov/mpi/mpich/
Source0: ftp://ftp.mcs.anl.gov/pub/mpi/%{mp_name}-%{mp_version}.tar.gz
Source1: %{me_name}-%{me_version}.tgz
Patch0: %{me_name}-%{me_version}-configure.patch
Patch1: mpich-rshfixes.patch
Buildroot: %{_tmppath}/%{mp_name}-root
Provides: libmpich.so.1
BuildRequires:  openssh-clients 

%description
MPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.  
MPICH includes all of the routines in MPI 1.2, along with the I/O routines
from MPI-2 and some additional routines from MPI-2, including those supporting
MPI Info and some of the additional datatype constructors.  MPICH  was
developed by Argonne National Laboratory. See www.mcs.anl.gov/mpi/mpich for
more information.

This RPM contains all the tools necessary to compile, link, and run
MPI jobs with %{compiler} compiler.

%ifarch noarch
%package -n %{mp_name}010207-doc
Summary:        Argonne National Laboratory MPI implementation documentation
Group: 		System Environment/Libraries
%description -n %{mp_name}010207-doc
MPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.
MPICH includes all of the routines in MPI 1.2, along with the I/O routines
from MPI-2 and some additional routines from MPI-2, including those supporting
MPI Info and some of the additional datatype constructors.  MPICH  was
developed by Argonne National Laboratory. See www.mcs.anl.gov/mpi/mpich for
more information.

This RPM contains all the documentation shared between different architectures
and compilers.

%else

%package runtime
Summary: 	Runtime tools of Argonne National Laboratory MPI implementation for %{compiler} compiler
Group:         Applications/Engineering and Scientific
Provides: mpi
Provides: mpich%{debug}-%{compiler}-runtime = %{version}
%{compilerruntimesection}
BuildRequires: libtool
Requires: openssh-clients
Requires: %{modules_rpm_name}

%description runtime
MPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.  
MPICH includes all of the routines in MPI 1.2, along with the I/O routines
from MPI-2 and some additional routines from MPI-2, including those supporting
MPI Info and some of the additional datatype constructors.  MPICH  was
developed by Argonne National Laboratory. See www.mcs.anl.gov/mpi/mpich for
more information.

This RPM contains all the tools necessary to run
MPI jobs with %{compiler} compiler.

%package devel
Summary: 	Development tools of Argonne National Laboratory MPI implementation for %{compiler} compiler
Group:         Applications/Engineering and Scientific
Requires: %{name}-runtime = %{mp_version}
%{compilerdevelsection}
Provides: mpich%{debug}-%{compiler}-devel = %{version}
Provides: mpich%{debug}-%{compiler} = %{version}
%{compilerruntimesection}
BuildRequires: libtool
Requires: %{modules_rpm_name}

%description devel
MPICH is an open-source and portable implementation of the Message-Passing
Interface (MPI, www.mpi-forum.org).  MPI is a library for parallel programming,
and is available on a wide range of parallel machines, from single laptops to
massively parallel vector parallel processors.  
MPICH includes all of the routines in MPI 1.2, along with the I/O routines
from MPI-2 and some additional routines from MPI-2, including those supporting
MPI Info and some of the additional datatype constructors.  MPICH  was
developed by Argonne National Laboratory. See www.mcs.anl.gov/mpi/mpich for
more information.

This RPM contains all the tools necessary to compile and link
MPI jobs with %{compiler} compiler.


%package %{me_name}
Version:       %{me_version}
License:       GPL
Summary:       MPI job launcher built with %{compilre} that uses the PBS task interface directly
Vendor:        Pete Wyckoff <pw@osc.edu>
URL:           http://www.osc.edu/~pw/mpiexec/
Group:         Applications/Engineering and Scientific
BuildRequires: torque-devel >= 2.1.6
Requires: %{name}-runtime = %{mp_version}
%{compilermpiexecsection}

%description %{me_name}
Mpiexec gathers node settings from PBS, prepares for the MPI library run
environment, and starts tasks through the PBS task manager interface.
Attempts to duplicate mpirun as much as possible, while getting everything
correct, and being faster than rsh.  As a side effect, PBS maintains
proper accounting of all tasks of a parallel job, and can terminate
everything on job abort. Built with %{compiler} compiler.

%endif

# Define root directory for installation here.
%define _prefix /usr/local/%{mp_name}/%{mp_version}/%{compiler}%{debug}/%{_target_cpu}
%define _prefix_noarch /usr/local/%{mp_name}/%{mp_version}/noarch
%define _mandir %{_prefix}/man
%define _docdir %{_prefix}/doc

# For the directories that are defined by their installation dir, make sure 
# that they use the appropriate dire
%define sharedir %{?buildroot:%{buildroot}}%{_datadir}
%define libdir   %{?buildroot:%{buildroot}}%{_libdir}

# These directories are the same for either choice
%define prefixdir   %{?buildroot:%{buildroot}}%{_prefix}
%define bindir %{?buildroot:%{buildroot}}%{_bindir}
%define sbindir %{?buildroot:%{buildroot}}%{_sbindir}

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{mp_name}-%{mp_version} -c
%setup -q -n %{mp_name}-%{mp_version} -T -D -a 1
%patch -p0
%patch1 -p0 -b .rshfixes

#
# The MPICH configure is based on Autoconf version 1, and cannot be rebuilt
# with %%configure.
# These options do the following:
#   Pass the various installation directories into configure
#   Select the MPICH "device"
#   Build the shared libraries, and install them into the same directory
#   as the regular (.a) libraries
#   Build MPI-IO (ROMIO) with the specified file systems, including
#   PVFS if specified by setting other_file_systems to +pvfs.
%build

%ifarch noarch
echo Nothing to do for noarch build
%else

# first mpich
pushd %{mp_name}-%{mp_version}

# Kill the stack protection and fortify source stuff...it slows things down
# and mpich hasn't been audited for it yet
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`

USER_CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS} -I%{localdir}/include"
USER_CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS} -I%{localdir}/include"
USER_FFLAGS="%{?fflags:%{fflags}}%{!?fflags:$RPM_OPT_FLAGS} -I%{localdir}/include"
LDFLAGS="%{?ldflags:%{ldflags}} -L%{localdir}/%{_lib} -L%{localdirlib}"

%{compilerbuildprep}
export CXXFLAGS="$USER_CFLAGS"
export FFLAGS="$USER_FFLAGS"
export LDFLAGS LDFLAGS USER_FFLAGS USER_CXXFLAGS USER_CFLAGS

./configure --prefix=%{prefixdir} \
	--libdir=%{libdir} \
        --with-device=%{device} \
	--enable-sharedlib=%{libdir} \
        %{other_device_opts} %{other_config_opts} \
        --with-romio=--with-file-system=nfs+ufs%{other_file_systems} \
	-rsh=ssh %{?mpich_debug:--enable-debug}

# remove $RPM_BUILD_ROOT in msgqdllloc.o
perl -pi -e "s|$RPM_BUILD_ROOT(.*)libtvmpich.so|\$1libtvmpich.so|" src/env/Makefile
# remove $RPM_BUILD_ROOT in initutil.o 
perl -pi -e "s|$RPM_BUILD_ROOT||g" mpichconf.h include/mpichconf.h
make

popd

pushd %{me_name}-%{me_version}

./configure --prefix=%{prefixdir} --with-pbs --with-default-comm=mpich-p4 --disable-p4-shmem %{?mpich_debug:--enable-debug}

# remove $RPM_BUILD_ROOT in mpiexec
perl -pi -e "s|$RPM_BUILD_ROOT||g" config.h

make

popd
%endif

%install
%ifarch noarch
mkdir -p $RPM_BUILD_ROOT/%{_prefix_noarch}
pushd %{mp_name}-%{mp_version}
cp -ar doc www $RPM_BUILD_ROOT/%{_prefix_noarch}
install -m 644 README COPYRIGHT $RPM_BUILD_ROOT/%{_prefix_noarch}/doc/
popd
%else

# we might need to setup modules before installation
%{compilerbuildprep}

# change dirs to our compiler build tree
pushd %{mp_name}-%{mp_version}

make install

# Examples are installed in the wrong location 
mkdir -p %{sharedir}/examples
mv %{prefixdir}/examples/* %{sharedir}/examples
mv %{prefixdir}/etc/* %{sharedir}/examples

# Remove invalid symlinks
rm -f %{sharedir}/examples/MPI-2-C++/mpirun
rm -f %{sharedir}/examples/mpirun

# Fix the paths in the shell scripts (and ONLY the shell scripts)
# Note that this moves paths into /usr from builddir/fullname
for i in `find %{sharedir} %{prefixdir}/bin %{prefixdir}/sbin -type f -exec grep -q $RPM_BUILD_ROOT {} \; -print`; do
    echo "script = $i"
    if (file -b $i | grep ELF >/dev/null) ; then 
        # Ignore binary files.  They must use a search path
        # to allow multiple paths
        :
    else 
	echo "Fixing up $i"
	perl -pi -e "s,$RPM_BUILD_ROOT%{_prefix},%{_prefix},g" $i
    fi
done

mkdir -p $RPM_BUILD_ROOT/%{_docdir}
install -m 644 README COPYRIGHT $RPM_BUILD_ROOT/%{_docdir}

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.jar
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_prefix}/logfiles

popd

pushd %{me_name}-%{me_version}

make install

popd

find $RPM_BUILD_ROOT/%{_prefix}/man -type f -name \*.[1-9] -exec gzip -9 "{}" \; -print

pushd $RPM_BUILD_ROOT/%{_prefix}
rm -rf www
ln -sf %{_prefix_noarch}/www .
cd doc
LISTOFDOCS=`ls *pdf *ps *ps.gz`
rm -f *pdf *ps *ps.gz
for i in $LISTOFDOCS; do
	ln -sf %{_prefix_noarch}/doc/$i .
done
cd ..
popd

# Finally, create the module file
%{__mkdir_p} $RPM_BUILD_ROOT/%{modulefile_path}/%{compilermodulename}/%{mp_version}
cat <<EOFMODULES >$RPM_BUILD_ROOT/%{modulefile_path}/%{compilermodulename}/%{mp_version}/%{modulebits}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds mpich%{debug} %{mp_version} compiled with %{compiler} to various paths"
}

module-whatis   "Sets up mpich%{debug} %{mp_version} compiled with %{compiler} in your environment"

# We check to see if any incompatible intel compilers are loaded
if {[module-info mode load] && ![module-info mode remove]} {
  if {[info exists env(LOADEDMODULES)]} {
    set envloaded [split \$env(LOADEDMODULES) ":"]
    foreach mod [lsort -decreasing \$envloaded] {
      set mmod "\$mod/"
      # if an mpich module and it is different from us - then it conflicts, easy
      if {[string first "mpich%{debug}/" \$mmod] == 0 && [string first "mpich%{debug}/%{compiler}/%{mp_version}/%{modulebits}" \$mmod] != 0 } {
        puts stderr "Conflicting module \$mod - removing before inserting requested module mpich%{debug}/%{compiler}/%{mp_version}/%{modulebits}"
        module unload \$mod
      }
    }
    foreach conflicts [ split "%{compilerconflictmodule} mpich%{!?mpich_debug:-debug}" " " ] {
      set envloaded [split \$env(LOADEDMODULES) ":"]
      foreach mod [lsort -decreasing \$envloaded] {
        set mmod "\$mod/"
        if {[string first \$conflicts \$mmod] == 0} {
          puts stderr "Conflicting module \$mmod - removing before inserting requested module mpich%{debug}/%{compiler}/%{mp_version}/%{modulebits}"
          module unload \$mod
          }
      }
    }
  }
}

%{compilerloadmodule}
prepend-path PATH "%{_bindir}"
prepend-path LD_LIBRARY_PATH "%{_libdir}:%{localdirlib}"
prepend-path MANPATH "%{_mandir}"
append-path -delim { } LOCAL_LDFLAGS "-L%{_libdir} -L%{localdirlib}"
prepend-path C_INCLUDE_PATH "%{_prefix}/include:%{localdir}/include "
prepend-path CPLUS_INCLUDE_PATH "%{_prefix}/include:%{localdir}/include"
prepend-path FPATH "%{_prefix}/include:%{localdir}/include"
prepend-path LIBRARY_PATH "%{_libdir}:%{localdir}/%{_lib}:%{localdirlib}"
EOFMODULES

%if "%{compilermodulefile}" != ""
cat <<ENDMODULEFILETRICK >$RPM_BUILD_ROOT/%{modulefile_path}/%{compilermodulefile}
#%Module
module-alias mpich%{debug}/%{compilershort} mpich%{debug}/%{compilermodulename}
module-alias mpich%{debug}/%{compilershortversion} mpich%{debug}/%{compilermodulename}
ENDMODULEFILETRICK
%endif

mkdir -p $RPM_BUILD_ROOT/%{localdirlib}
mkdir -p $RPM_BUILD_ROOT/%{localdir}/include
%endif

rm -f $RPM_BUILD_ROOT/%{_prefix}/share/machines.LINUX

%clean
rm -rf $RPM_BUILD_ROOT

%ifarch noarch
%files -n %{mp_name}010207-doc
%defattr(-,root,root)
%{_prefix_noarch}
%dir %{_prefix_noarch}/..
%dir %{_prefix_noarch}/../..

%else
%files runtime
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_prefix}/..
%dir %{_prefix}/../..
%dir %{_prefix}/../../..
%dir %{_prefix}/bin
%{_prefix}/bin/clog*
%{_prefix}/bin/mpichversion
%{_prefix}/bin/mpiman
%{_prefix}/bin/mpirun*
%{_prefix}/bin/serv_p4
%{_prefix}/bin/t*
%exclude %{_prefix}/bin/mpiexec
%dir %{_prefix}/sbin
%exclude %{_prefix}/sbin/mpiuninstall
%{_prefix}/sbin
%{_prefix}/www
%{_prefix}/doc
%dir %{_prefix}/man
%dir %{_prefix}/man/man1
%{_prefix}/man/man1/c*
%{_prefix}/man/man1/mpiman*
%{_prefix}/man/man1/mpirun*
%{_prefix}/man/man1/tst*
%{_prefix}/man/mandesc
%dir %{_prefix}/%{_lib}
%{_prefix}/%{_lib}/*.so.*
%dir %{_prefix}/share
%{_prefix}/share/machines*
%dir %{modulefile_path}
%dir %{modulefile_path}/%{compilermodulename}
%dir %{modulefile_path}/%{compilermodulename}/%{mp_version}
%{modulefile_path}/%{compilermodulename}/%{mp_version}/%{modulebits}
%if "%{compilermodulefile}" != ""
%{modulefile_path}/%{compilermodulefile}
%endif
%dir %{localdir}/%{_lib}
%dir %{localdirlib}

%files devel
%defattr(-,root,root)
%dir %{localdir}/include
%{_prefix}/bin/mpiCC
%{_prefix}/bin/mpicc
%{_prefix}/bin/mpicxx
%{_prefix}/bin/mpif*
%{_prefix}/bin/mpireconfig*
%{_prefix}/include
%{_prefix}/%{_lib}/mpe_prof.o
%{_prefix}/%{_lib}/*.a
%{_prefix}/%{_lib}/*.so
%{_prefix}/sbin/mpiuninstall
%{_prefix}/share/Makefile*
%{_prefix}/share/examples
%{_prefix}/man/man1/J*
%{_prefix}/man/man1/MPI*
%{_prefix}/man/man1/mpiCC*
%{_prefix}/man/man1/mpicc*
%{_prefix}/man/man1/mpif*
%{_prefix}/man/man1/mpireconfig*
%{_prefix}/man/man[34]

%files %{me_name}
%defattr(-, root, root)
%{_prefix}/bin/mpiexec
%{_prefix}/man/man1/mpiexec*
%endif

%changelog
* Wed Dec 10 2008 Josko Plazonic <plazonic@math.princeton.edu>
- teach the src.rpm how to build for pgi80 and intel110

* Mon Oct 13 2008 Josko Plazonic <plazonic@math.princeton.edu>
- turn off shared memory use for mpiexec too...

* Mon Dec 03 2007 Josko Plazonic <plazonic@math.princeton.edu>
- turn off shared memory use

* Wed Nov 28 2007 Josko Plazonic <plazonic@math.princeton.edu>
- fix the wrong F90 for intel91/intel100

* Tue Sep 25 2007 Josko Plazonic <plazonic@math.princeton.edu>
- convert to new way of doing things, fix rsh param to mpirun
  processing and add intel10

* Thu Feb 01 2007 Josko Plazonic <plazonic@math.princeton.edu>
- fixed up code that was removing references to /var/tmp/

* Thu Feb 1 2007 Dennis McRitchie <dmcr@Princeton.EDU>
- Patched stdio.c to fix bug that caused premature failure of mpiexec. Reported to author.

* Mon Jan 15 2007 Josko Plazonic <plazonic@math.princeton.edu>
- simplified some things, complicated others - split up docs into
  separate rpms, change version to 1.2.7p1

* Tue Jan 9 2007 Dennis McRitchie <dmcr@Princeton.EDU>
- Modified spec file to build both gcc and Intel versions of binary rpm
- Used Josko's preference for installation path
- Used Intel module to set up Intel compiler environment

* Wed Nov 8 2006 Dennis McRitchie <dmcr@Princeton.EDU>
- Turned on --with-comm=shared configure option. Needed with p4 device on SMP cluster.
- Specified different Intel compiler for x86_64 arch.
- Modified it so it used the original name for Source0.
- General cleanup.
* Wed Aug 2 2006 Robert Knight <knight@princeton.edu>
- Change to Princeton naming
- Update Intel compiler version
* Wed Jul 28 2004 William Gropp <gropp@mcs.anl.gov>
- Update version number for next release
* Mon Jan 20 2003 William Gropp <gropp@mcs.anl.gov>
- Integrate suggestions; clean up the code for changing the installation dirs
* Fri Jan 10 2003 William Gropp <gropp@mcs.anl.gov>
- Update to MPICH 1.2.5 and fixed buildroot
* Thu Apr 25 2002 William Gropp <gropp@mcs.anl.gov>
- Initial version
