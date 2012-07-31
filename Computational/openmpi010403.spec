#
# Copyright (c) 2004-2005 The Trustees of Indiana University and Indiana
#                         University Research and Technology
#                         Corporation.  All rights reserved.
# Copyright (c) 2004-2005 The University of Tennessee and The University
#                         of Tennessee Research Foundation.  All rights
#                         reserved.
# Copyright (c) 2004-2005 High Performance Computing Center Stuttgart, 
#                         University of Stuttgart.  All rights reserved.
# Copyright (c) 2004-2005 The Regents of the University of California.
#                         All rights reserved.
# Copyright (c) 2006      Cisco Systems, Inc.  All rights reserved.
# $COPYRIGHT$
# 
# Additional copyrights may follow
# 
# $HEADER$
#
############################################################################
#
# Copyright (c) 2003, The Regents of the University of California, through
# Lawrence Berkeley National Laboratory (subject to receipt of any
# required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# Initially written by:
#       Greg Kurtzer, <gmkurtzer@lbl.gov>
#
############################################################################


#############################################################################
#
# Configuration Options
#
#############################################################################

# with pvfs2?
%if 0%{?suse_version}
%{!?pvfs2: %define pvfs2 0}
%else
%{!?pvfs2: %define pvfs2 1}
%endif

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# Define this if you want to make this SRPM build in /opt/NAME/VERSION-RELEASE
# instead of the default /usr/
# type: bool (0/1)
%{!?install_in_opt: %define install_in_opt 0}

# Define this if you want this RPM to install environment setup
# scripts in /etc/profile.d.  Only used if install_in_opt is true.
# type: bool (0/1)
%{!?install_profile_d_scripts: %define install_profile_d_scripts 0}

# Define this to 1 if you want this RPM to install a modulefile.  Only
# used if install_in_opt is true.
# type: bool (0/1)
%{!?install_modulefile: %define install_modulefile 1}
# type: string (root path to install modulefiles)
%{!?modulefile_path: %define modulefile_path /usr/local/share/Modules/modulefiles/}
# type: string (subdir to install modulefile)
%{!?modulefile_subdir: %define modulefile_subdir openmpi%{debug}}
# type: string (name of modulefile)
%{!?modulefile_name: %define modulefile_name %{version}}
# The name of the modules RPM.  Can vary from system to system.
# type: string (name of modules RPM)
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}
# 32 or 64?
%ifarch %{ix86}
%define modulebits 32
%else
%define modulebits 64
%endif

# Should we build a debuginfo RPM or not?
# type: bool (0/1)
# NO because we will not strip it anymore
%{!?build_debuginfo_rpm: %define build_debuginfo_rpm 0}
%define __os_install_post /usr/lib/rpm/brp-compress

# pvfs2 flags
%if %{pvfs2}
%define pvfs2_build_flags '--with-io-romio-flags=--with-file-system=pvfs2+nfs+ufs'
%define pvfs2_ld_flags -lpvfs2 -lpthread
%else
#define pvfs2_build_flags '--with-io-romio-flags="--with-file-system=lustre+nfs+ufs"'
%define pvfs2_build_flags '--with-io-romio-flags=--with-file-system=nfs+ufs'
%define pvfs2_ld_flags %{nil}
%endif

%{!?configure_options: %define configure_options %{nil}}

# compiler for which we are doing this
%define compiler intel111

# debug?
%define with_debug  %{?_with_debug:     1} %{?!_with_debug:     0}
%if %{with_debug}
%define debug -debug
%define debug_options --enable-debug --enable-memchecker --with-valgrind
%else
%define debug %{nil}
%define debug_options %{nil}
%endif

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilershort gcc
%if 0%{?suse_version}
# These days suse packages gfortran in gcc-fortran, just to make my life difficult
%define compilerruntimesection BuildRequires: gcc-fortran gcc-c++
%define compilerdevelsection Requires: gcc-fortran gcc-c++
%else
%if "%{?rhel}" == "4"
%define compilerruntimesection BuildRequires: gcc-g77 gcc-c++
%define compilerdevelsection Requires: gcc-g77 gcc-c++
%else
%define compilerruntimesection BuildRequires: gcc-gfortran gcc-c++
%define compilerdevelsection Requires: gcc-gfortran gcc-c++
%endif
%endif
%define compilerdocsection #nothing here
%define localdir /usr/local
# do nothing special for gcc for build prep
%define compilerbuildprep %{nil}
# we need a special ldflags
%define compilerldflags -Wl,-z,noexecstack
# this is for configuring modules
%define compilermodulename gcc
%define compilerloadmodule %{nil}
%define compilermodulefile %{nil}
%endif
#
# Intel 9.1 compiler
%if "%{compiler}" == "intel91"
%define compilershort intel
%define compilershortversion intel-9
%if "%{?rhel}" == "4"
%define compilerruntimesection BuildRequires: intel-compiler91-default-modules\
Requires: intel-compiler91-default-modules\
Provides: openmpi%{debug}-intel-runtime = %{version}-091.%{release}
%else
%define compilerruntimesection BuildRequires: intel-compiler91-%{modulebits}-default-modules\
Requires: intel-compiler91-%{modulebits}-default-modules\
Provides: openmpi%{debug}-intel-runtime = %{version}-091.%{release}
%endif
%define compilerdevelsection Provides: openmpi%{debug}-intel-devel = %{version}-091.%{release}
%define compilerdocsection Provides: openmpi%{debug}-intel-doc = %{version}-091.%{release}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort FC=ifort; . /etc/profile.d/modules.sh; module load intel
%if %{with_debug}
%define cflags -O2 -g -pipe -Wall
%else
%define cflags -O2 -pipe -Wall
%endif
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-9.1
%define compilerloadmodule module load intel/9.1/%{modulebits}
%if "%{?rhel}" == "4"
# for our older clusters we want 9.1 intel to be default, at least for now
%define compilermodulefile .modulerc-intel-%{modulebits}-991-%{version}
%else
# not so for newer ones
%define compilermodulefile .modulerc-intel-%{modulebits}-091-%{version}
%endif
%endif
#
# Intel 10.0 compiler
%if "%{compiler}" == "intel101" || "%{compiler}" == "intel111"
# we will extract versions we need out of above string
%define intelmajor %( echo %{compiler} | cut -b6-7 )
%define intelminor %( echo %{compiler} | cut -b8 )
%define intelversion %{intelmajor}.%{intelminor}
%define intelversionnum %{intelmajor}%{intelminor}
%if "%{compiler}" == "intel111"
%define intelminrelease 038
%define extradevel -devel
%else
%define intelminrelease 001
%define extradevel %{nil}
%endif
%define compilershort intel
%define compilershortversion intel-%{intelmajor}
%define compilerruntimesection BuildRequires: compat-libstdc++-33 intel-compiler%{intelmajor}-%{modulebits}-default-modules%{extradevel} >= %{intelversion}-%{intelminrelease}\
Requires: intel-compiler%{intelmajor}-%{modulebits}-default-modules >= %{intelversion}\
Provides: openmpi%{debug}-intel-runtime = %{version}-%{intelversionnum}.%{release}
%if "%{?rhel}" == "6"
%define compilerdevelsection Provides: openmpi%{debug}-intel-devel = %{version}-%{intelversionnum}.%{release}\
Requires: intel-compiler%{intelmajor}-%{modulebits}-default-modules%{extradevel} >= %{intelversion}-%{intelminrelease}, glibc-devel(x86-32)\
BuildRequires: glibc-devel(x86-32)
%else
%define compilerdevelsection Provides: openmpi%{debug}-intel-devel = %{version}-%{intelversionnum}.%{release}\
Requires: intel-compiler%{intelmajor}-%{modulebits}-default-modules%{extradevel} >= %{intelversion}-%{intelminrelease}
%endif
%define compilerdocsection Provides: openmpi%{debug}-intel-doc = %{version}-%{intelversionnum}.%{release}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort FC=ifort; . /etc/profile.d/modules.sh; module load intel
%if %{with_debug}
%define cflags -O2 -g -pipe -Wall
%else
%define cflags -O2 -pipe -Wall
%endif
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-%{intelversion}
%define compilerloadmodule module load intel/%{intelmajor}/%{modulebits}
%define compilermodulefile .modulerc-intel-%{modulebits}-%{intelversionnum}-%{version}
%endif
#
# PGI compiler
%if "%{compiler}" == "pgi71" || "%{compiler}" == "pgi80" || "%{compiler}" == "pgi90" || "%{compiler}" == "pgi103"
# we will extract versions we need out of above string but we have to treat differently 10.* and newer pgi versions
%if "%{compiler}" == "pgi71" || "%{compiler}" == "pgi80" || "%{compiler}" == "pgi90"
%define pgimajor %( echo %{compiler} | cut -b4 )
%define pgiminor %( echo %{compiler} | cut -b5 )
%define pgiversionnum 0%{pgimajor}%{pgiminor}
%else
%define pgimajor %( echo %{compiler} | cut -b4-5 )
%define pgiminor %( echo %{compiler} | cut -b6 )
%define pgiversionnum %{pgimajor}%{pgiminor}
%endif
%define pgiversion %{pgimajor}.%{pgiminor}
%define compilershort pgi
%define compilershortversion pgi-%{pgimajor}
%define compilerruntimesection BuildRequires: pgi-workstation >= %{pgiversion}\
Requires: pgi-workstation-libs >= %{pgiversion}\
Provides: openmpi%{debug}-pgi-runtime = %{version}-%{pgiversionnum}.%{release}
%define compilerdevelsection Requires: pgi-workstation >= %{pgiversion}\
Provides: openmpi%{debug}-pgi-devel = %{version}-%{pgiversionnum}.%{release}
%define compilerdocsection Provides: openmpi%{debug}-pgi-doc = %{version}-%{pgiversionnum}.%{release}
%define localdir /usr/local/pgi
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pgcc CXX=pgCC F77=pgf77 FC=pgf90; . /etc/profile.d/modules.sh; module load pgi
%define cflags -fast
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pgi-%{pgiversion}
%define compilerloadmodule module load pgi/%{pgimajor}/%{modulebits}
%define compilermodulefile .modulerc-pgi-%{modulebits}-%{pgiversionnum}-%{version}
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
%define compilerruntimesection BuildRequires: pathscale-compilers >= %{pathscaleversion}\
Requires: pathscale-compilers-libs >= %{pathscaleversion}\
Provides: openmpi%{debug}-pathscale-runtime = %{version}-%{pathscaleversionnum}.%{release}
%define compilerdevelsection Requires: pathscale-compilers >= %{pathscaleversion}\
Provides: openmpi%{debug}-pathscale-devel = %{version}-%{pathscaleversionnum}.%{release}
%define compilerdocsection Provides: openmpi%{debug}-pathscale-doc = %{version}-%{pathscaleversionnum}.%{release}
%define localdir /usr/local/pathscale
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pathcc CXX=pathCC F77=pathf90 FC=pathf90; . /etc/profile.d/modules.sh; module load pathscale
%define cflags -O3
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pathscale-%{pathscaleversion}
%define compilerloadmodule module load pathscale/%{pathscaleversion}/%{modulebits}
%define compilermodulefile .modulerc-pathscale-%{modulebits}-%{pathscaleversionnum}-%{version}
%endif

# we need this for backwards compatibility
# before RHEL5 we had /usr/local/intel/openmpi-intel and now we have /usr/local/intel/openmpi
# i.e. the duplicate -intel has been dropped.  Act accordingly to distro:
%if "%{?rhel}" == "4"
# now, here it gets stupidly complex, as we used to have intel-ib and gcc-ib and
# these builds all use ib we have to add -ib in those cases...
%if "%{compilershort}" == "intel" || "%{compilershort}" == "gcc"
%define localdirlib %{localdir}/%{_lib}/openmpi-%{compilershort}-ib
%else
%define localdirlib %{localdir}/%{_lib}/openmpi-%{compilershort}
%endif
%else
%define localdirlib %{localdir}/%{_lib}/openmpi
%endif

#############################################################################
#
# Configuration Logic
#
#############################################################################

%if %{install_in_opt}
%define _prefix /opt/openmpi%{debug}/%{version}/%{compiler}
%define _sysconfdir %{_prefix}/etc
%define _libdir %{_prefix}/lib
%define _includedir %{_prefix}/include
%define _mandir %{_prefix}/man
%define _datadir %{_prefix}/share/openmpi%{debug}
%else
%define _prefix /usr/local/openmpi%{debug}/%{version}/%{compiler}/%{_target_cpu}
%define _prefixtop /usr/local/openmpi%{debug}
%define _mandir %{_prefix}/man
%define _docdir %{_datadir}/doc
%define _infodir %{_datadir}/info
%global _sysconfdir /etc
%endif

%if !%{build_debuginfo_rpm}
%define debug_package %{nil}
%endif

# These are the cluster-specific options
#if "%{?rhel}" < "6"
#######################efine cluster_options --disable-heterogeneous --enable-static --enable-shared --without-slurm --disable-dlopen --with-tm=/usr --with-sge --with-libnuma=/usr}
#else
%{!?cluster_options: %define cluster_options --enable-mpi-threads --disable-static --enable-shared --without-slurm --with-tm=/usr --with-sge --with-libnuma=/usr}
#endif

# These are the default CSES IB values
%if 0%{?suse_version} || "%{?rhel}" > "4"
%define _with_openib    --with-openib=/usr
%else
%define _with_openib    --with-openib=/usr/ofed
%endif
%define _ib_name        -ib

# The following options is supported and used on 32-bit platforms to turn on IB support.
# It can also be used on 64-bit platforms to specify a different IB directory:
#   --with ib[=<dir>]
#
%if %{?_with_ib:1}%{!?_with_ib:0}
# Set default dir is none specified
%define _ib_dir %(set -- %{_with_ib}; echo $1 | grep -v with | sed 's/=//')
%if %(test "%{_ib_dir}" = "" && echo 1 || echo 0)
%define _with_openib    --with-openib=/usr/ofed
%else
%define _with_openib    --with-openib=%{_ib_dir}
%endif
%define _ib_name -ib
%endif

# The following option is supported and is used on 64-bit platforms to turn off IB support:
#   --without ib
#
%if %{?_without_ib:1}%{!?_without_ib:0}
%define _with_openib    %{nil}
%define _ib_name        %{nil}
%endif

# compile with blcr? comment out if not
#define _with_blcr 1
%if %{?_with_blcr:1}%{!?_with_blcr:0}
%define blcrcompileopts --with-ft --with-blcr=/usr --with-blcr-libdir=/usr/%{_lib}
%else
%define blcrcompileopts %{nil}
%endif

#############################################################################
#
# Preamble Section
#
#############################################################################

Summary: A powerful implementation of MPI
Name: %{?_name:%{_name}}%{!?_name:openmpi}010403%{debug}-%{compiler}
Version: 1.4.3
Release: 32.cses.5%{?dist}
License: BSD
Group: Development/Libraries
Source: openmpi-%{version}.tar.bz2
Patch1: pvfs2.diff
Patch2: romio-1-5-0-fixups-2.patch
Patch3: romio-nfs.patch
Patch4: lustre-romio.diff
Packager: %{?_packager:%{_packager}}%{!?_packager:%{_vendor}}
Vendor: %{?_vendorinfo:%{_vendorinfo}}%{!?_vendorinfo:%{_vendor}}
Distribution: %{?_distribution:%{_distribution}}%{!?_distribution:%{_vendor}}
Provides: mpi
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
%if %{install_modulefile}
Requires: %{modules_rpm_name}
%endif
BuildRequires: rsync flex zlib-devel
%if "%{?rhel}" <= "5"
BuildRequires: torque-devel >= 2.3.6
%else
BuildRequires: libtorque-devel >= 2.4.8
%endif
%if %{?_with_blcr:1}%{!?_with_blcr:0}
BuildRequires: blcr-devel
%endif
%if %{pvfs2}
BuildRequires: pvfs2-devel
%endif
Obsoletes: %{?_name:%{_name}}%{!?_name:openmpi}010203-%{compiler}


%description
Open MPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This RPM contains all the tools necessary to compile, link, and run
Open MPI jobs.

#############################################################################
#
# Preamble Section (runtime)
#
#############################################################################

%package runtime
Summary: Tools and plugin modules for running Open MPI jobs with %{compiler} compiler
Group: Development/Libraries
Provides: mpi
Provides: openmpi%{debug}-%{compiler}-runtime = %{version}
%if %{install_modulefile}
BuildRequires: %{modules_rpm_name}
%endif
%{compilerruntimesection}
BuildRequires: libtool
%if 0%{?suse_version} || "%{?rhel}" < "5"
BuildRequires: numactl
Requires: numactl
%else
BuildRequires: numactl-devel
Requires: librdmacm, python
%endif
%if %{?_with_openib:1}%{!?_with_openib:0}
%if 0%{?suse_version}
BuildRequires: sysfsutils, libibverbs-devel
%else
BuildRequires: libibverbs-devel >= 1.1.3, opensm-devel > 3.3.0, librdmacm-devel
BuildRequires: libibcm, libibcm-devel
%if %{with_debug}
BuildRequires: valgrind-devel
%endif
# not yet needed - only if we remove the included ones
#BuildRequires: libtool-ltdl-devel plpa-devel
%ifarch x86_64
%if "%{?rhel}" > "5"
BuildRequires:          infinipath-psm-devel
%endif
%endif
%if "%{?rhel}" < "5"
BuildRequires: sysfsutils-devel
%else
BuildRequires: libsysfs-devel
%endif
%endif
%endif
%if %{install_modulefile}
Requires: %{modules_rpm_name}
%endif
Obsoletes: %{?_name:%{_name}}%{!?_name:openmpi}010203-%{compiler}-runtime

%description runtime
Open MPI is a project combining technologies and resources from several other
projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in order to build the best
MPI library available.

This subpackage provides general tools (mpirun, mpiexec, etc.) and the
Module Component Architecture (MCA) base and plugins necessary for
running Open MPI jobs with the %{compiler} compiler.

#############################################################################
#
# Preamble Section (devel)
#
#############################################################################

%package devel
Summary: Development tools and header files for Open MPI with %{compiler} compiler
Group: Development/Libraries
Requires: %{name}-runtime
BuildRequires: libibverbs-devel >= 1.1.3, librdmacm-devel, libibcm, libibcm-devel
%ifarch x86_64
%if "%{?rhel}" > "5"
Requires:          infinipath-psm-devel
%endif
%endif
%if "%{?rhel}" <= "5"
Requires: torque-devel >= 2.3.6
%else
Requires: libtorque-devel >= 2.4.8
%endif
%{compilerdevelsection}
Provides: openmpi%{debug}-%{compiler}-devel = %{version}
Provides: openmpi%{debug}-%{compiler} = %{version}
%if %{pvfs2}
Requires: pvfs2-devel
%endif
Requires: numactl-devel libtool
Obsoletes: %{?_name:%{_name}}%{!?_name:openmpi}010203-%{compiler}-devel

%description devel
Open MPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This subpackage provides the development files for Open MPI, such as
wrapper compilers and header files for MPI development with %{compiler} compiler.

#############################################################################
#
# Preamble Section (docs)
#
#############################################################################

%package docs
Summary: Documentation for Open MPI %{compiler} compiler
Group: Development/Documentation
Requires: %{name}-runtime
%{compilerdocsection}
Provides: openmpi%{debug}-%{compiler}-docs = %{version}
Obsoletes: %{?_name:%{_name}}%{!?_name:openmpi}010203-%{compiler}-docs

%description docs
Open MPI is a project combining technologies and resources from several other
projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in order to build the best
MPI library available.

This subpackage provides the documentation for Open MPI with %{compiler} compiler.

#############################################################################
#
# Preparatory Section
#
#############################################################################
%prep
rm -rf $RPM_BUILD_ROOT
#setup -q -n openmpi-%{version}
%setup -q -n openmpi-%{version}
# as 1.3 branch has resynced with romio tree
# these three should not be required anymore 
#pushd ompi/mca/io/romio
#patch1 -p0
#patch2 -p0
#popd
#patch3 -p1
# old old patch
#patch4 -p1

#############################################################################
#
# Build Section
#
#############################################################################

%build
# Kill the stack protection and fortify source stuff...it slows things down
# and openmpi hasn't been audited for it yet
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
%if !%{with_debug}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-g//'`
%endif

CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS}"
CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS}"
F77FLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FFLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FCFLAGS="%{?fcflags:%{fcflags}}%{!?fcflags:$RPM_OPT_FLAGS}"

%{compilerbuildprep}

%if "%{?rhel}" > "5"
# fix location of torque include files
export CFLAGS="$CFLAGS -I/usr/include/torque"
perl -pi -e 's|include/tm.h|include/torque/tm.h|' configure
%endif

export CFLAGS CXXFLAGS F77FLAGS FCFLAGS FFLAGS

# Build in the library search path to any binaries produced, so
# if the runtime package is installed without the modules package
# it will still be able to find openmpi libraries (like libopal)
%configure %{cluster_options} %{_with_openib} %{configure_options} %{pvfs2_build_flags} %{blcrcompileopts} %{debug_options} \
		--sysconfdir=%{_sysconfdir}/openmpi/%{version}/%{compiler}/%{_target_cpu} \
		--with-wrapper-cflags="-I%{localdir}/include" --with-wrapper-cxxflags="-I%{localdir}/include" \
		--with-wrapper-fflags="-I%{localdir}/include" --with-wrapper-fcflags="-I%{localdir}/include" \
		--with-wrapper-ldflags="-L%{localdir}/%{_lib} -L%{localdirlib} %{pvfs2_ld_flags}" \
		LDFLAGS="-Wl,-rpath,%{_prefix}/%{_lib} %{pvfs2_ld_flags} %{compilerldflags}"

%{__make} %{?mflags}

# special non standard fixes
#case %{compiler} in
#	intel*)
#		echo "Fixing up torque/intel problems, hold on"
#		for i in orte/mca/ras/tm orte/mca/pls/tm; do
#			pushd $i
#			rm -f *.o *.lo *.la
#			make CC=gcc
#			popd
#		done
#		%{__make} %{?mflags}
#		;;
#esac

#############################################################################
#
# Install Section
#
#############################################################################
%install

# we might need to setup modules before installation
%{compilerbuildprep}

%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}

# An attempt to make enviornment happier when installed into non /usr path

%if %{install_modulefile}
%{__mkdir_p} $RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}

# we use this in libs compiled with openmpi
mkdir -p %dir $RPM_BUILD_ROOT/%{localdirlib}
mkdir -p %dir $RPM_BUILD_ROOT/%{localdir}/include

cat <<EOF >$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}/%{modulebits}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds Open MPI%{debug} %{compilermodulename} %{version} to various paths"
}

module-whatis   "Sets up Open MPI%{debug} %{compilermodulename} %{version} in your environment"

%{compilerloadmodule}
prepend-path PATH "%{_prefix}/bin"
prepend-path LD_LIBRARY_PATH "%{_libdir}:%{localdirlib}"
prepend-path MANPATH "%{_mandir}"
append-path -d { } LOCAL_LDFLAGS "-L%{_libdir} -L%{localdirlib}"
append-path -d { } LOCAL_INCLUDE "-I%{localdir}/include"
append-path -d { } LOCAL_CFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{localdir}/include"
EOF
%endif
# End of modulefile if

%if "%{compilermodulefile}" != ""
cat <<ENDMODULEFILETRICK >$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
#%Module
module-alias %{modulefile_subdir}/%{compilershort} %{modulefile_subdir}/%{compilermodulename}
module-alias %{modulefile_subdir}/%{compilershortversion} %{modulefile_subdir}/%{compilermodulename}
ENDMODULEFILETRICK
%if "%{?rhel}" == "4"
# and in case of rhel4 we have to take care of -ib variants...
cat <<ENDMODULERHEL4FILETRICK >>$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
module-alias %{modulefile_subdir}/%{compilershort}-ib %{modulefile_subdir}/%{compilermodulename}
ENDMODULERHEL4FILETRICK
%if "%{compiler}" == "intel91"
# one more tweak
cat <<ENDMODULERHEL4INTEL91 >>$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
module-alias %{modulefile_subdir} %{modulefile_subdir}/%{compilermodulename}
ENDMODULERHEL4INTEL91
%endif
%endif

%endif

# Next, the [optional] profile.d scripts

%if %{install_profile_d_scripts}
%{__mkdir_p} $RPM_BUILD_ROOT/etc/profile.d/
cat <<EOF > $RPM_BUILD_ROOT/etc/profile.d/%{name}-%{version}.sh
# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

CHANGED=0
if test -z "`echo $PATH | grep %{_prefix}/bin`"; then
    PATH=\${PATH}:%{_prefix}/bin/
    CHANGED=1
fi
if test -z "`echo $LD_LIBRARY_PATH | grep %{_libdir}`"; then
    LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:%{_libdir}
    CHANGED=1
fi
if test -z "`echo $MANPATH | grep %{_mandir}`"; then
    MANPATH=\${MANPATH}:%{_mandir}
    CHANGED=1
fi
if test "$CHANGED" = "1"; then
    export PATH LD_LIBRARY_PATH MANPATH
fi
EOF
cat <<EOF > $RPM_BUILD_ROOT/etc/profile.d/%{name}-%{version}.csh
# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

if ("`echo $PATH | grep %{_prefix}/bin`") then
    setenv PATH \${PATH}:%{_prefix}/bin/
endif
if ("$?LD_LIBRARY_PATH") then
    if ("`echo $LD_LIBRARY_PATH | grep %{_libdir}`") then
        setenv LD_LIBRARY_PATH \${LD_LIBRARY_PATH}:%{_libdir}
    endif
endif
if ("$?MANPATH") then
    if ("`echo $MANPATH | grep %{_mandir}`") then
        setenv MANPATH \${MANPATH}:%{_mandir}
    endif
endif
EOF
%endif
# end install_profile_d_scripts


# Build lists of files that are specific to each package that are not
# easily identifiable by a single directory (e.g., the different
# libraries).  In a somewhat lame move, we can't just pipe everything
# together because if the user, for example, did --disable-shared
# --enable-static, the "grep" for .so files will not find anything and
# therefore return a non-zero exit status.  This will cause RPM to
# barf.  So be super lame and dump the egrep through /bin/true -- this
# always gives a 0 exit status.

# Runtime files
find $RPM_BUILD_ROOT%{_prefix} -type f -o -type l | \
   sed -e "s@$RPM_BUILD_ROOT@@" | \
   egrep "lib.*.so|mca.*so" > %{compiler}-runtime.files | /bin/true

# Devel files
find $RPM_BUILD_ROOT%{_prefix} -type f -o -type l | \
   sed -e "s@$RPM_BUILD_ROOT@@" | \
   egrep "lib.*\.a|lib.*\.la|.*\.mod" > %{compiler}-devel.files | /bin/true

mkdir -p $RPM_BUILD_ROOT/%{_docdir}
install -m 644 README INSTALL LICENSE $RPM_BUILD_ROOT/%{_docdir}

# remove any references to -ltorque in various mpi commands
for i in `find $RPM_BUILD_ROOT/%{_datadir}/openmpi%{debug} -type f -exec grep -q ltorque {} \; -print`; do
	echo "Removing torque refs in $i"
	sed -i -e 's|-ltorque||g' $i
done

# configs go here
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/openmpi/%{version}/%{compiler}/%{_target_cpu}

#############################################################################
#
# Clean Section
#
#############################################################################
%clean
# Remove installed driver after rpm build finished
rm -rf $RPM_BUILD_DIR/%{_name}-%{_version} 

test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT

#############################################################################
#
# Files Section
#
#############################################################################

#
# Sub-package RPMs
#
# Harder than all-in-one.  We list the directories specifically so
# that if the RPM creates directories when it is installed, we will
# remove them when the RPM is uninstalled.  We also have to use
# specific file lists.
#

%files runtime -f %{compiler}-runtime.files
%defattr(-, root, root, -)
%dir %{_prefixtop}
%dir %{_prefixtop}/%{version}
%dir %{_prefixtop}/%{version}/%{compiler}
%dir %{_prefix}
%dir %{_sysconfdir}/openmpi
%dir %{_sysconfdir}/openmpi/%{version}
%dir %{_sysconfdir}/openmpi/%{version}/%{compiler}
%dir %{_sysconfdir}/openmpi/%{version}/%{compiler}/%{_target_cpu}
%{_sysconfdir}/openmpi/%{version}/%{compiler}/%{_target_cpu}/*
# If we're not installing in /opt, then the prefix is /usr, but the
# sysconfdir is /etc -- so list them both.  Otherwise, we install in
# /opt/openmpi/<version>, so be sure to list /opt/openmpi as well (so
# that it can be removed).
%if %{install_in_opt}
%dir /opt/%{name}
%dir /opt/%{name}/%{version}/share
%endif
# If we're installing the profile.d scripts, get those, too
%if %{install_profile_d_scripts}
/etc/profile.d/%{name}-%{version}.sh
/etc/profile.d/%{name}-%{version}.csh
%endif
%dir %{_prefix}/bin
%dir %{_prefix}/%{_lib}
%dir %{_prefix}/%{_lib}/openmpi
#%doc README INSTALL LICENSE
#%{_prefix}/etc
%dir %{_prefix}/share
%{_prefix}/share/openmpi
%{_prefix}/share/*SPEC
%{_prefix}/bin/mpirun
%{_prefix}/bin/mpiexec
%{_prefix}/bin/ompi_info
%{_prefix}/bin/ompi-server
%{_prefix}/bin/orterun
%{_prefix}/bin/orted
%{_prefix}/bin/orte-clean
%{_prefix}/bin/orte-iof
%{_prefix}/bin/orte-ps
%{_prefix}/bin/*otfinfo
%{_prefix}/bin/*compress
%if %{?_with_blcr:1}%{!?_with_blcr:0}
%{_prefix}/bin/opal-checkpoint
%{_prefix}/bin/opal-restart
%{_prefix}/bin/orte-checkpoint
%{_prefix}/bin/orte-restart
%endif
%if 0%{?suse_version} || "%{?rhel}" > "4"
%{_prefix}/bin/ompi-clean
%{_prefix}/bin/ompi-ps
%{_prefix}/bin/ompi-iof
%if %{?_with_blcr:1}%{!?_with_blcr:0}
%{_prefix}/bin/ompi-checkpoint
%{_prefix}/bin/ompi-restart
%endif
%endif
# for the following four I am not sure where they belong, here or
# the -devel so for now it goes here, just in case
%{_prefix}/bin/*otfaux
%{_prefix}/bin/*otfconfig
%{_prefix}/bin/*otfdump
%{_prefix}/bin/*otfmerge
%if %{install_modulefile}
%dir %{modulefile_path}/%{modulefile_subdir}
%dir %{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}
%dir %{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}
%{modulefile_path}/%{modulefile_subdir}/%{compilermodulename}/%{version}/%{modulebits}
%if "%{compilermodulefile}" != ""
%{modulefile_path}/%{modulefile_subdir}/%{compilermodulefile}
%endif
%endif
%dir %{localdir}/include
%dir %{localdir}/%{_lib}
%dir %{localdirlib}

%files devel -f %{compiler}-devel.files
%defattr(-, root, root, -)
%{_prefix}/include
%{_prefix}/bin/mpicc
%{_prefix}/bin/mpiCC
%{_prefix}/bin/mpic++
%{_prefix}/bin/mpicxx
%{_prefix}/bin/mpif77
%{_prefix}/bin/mpif90
%{_prefix}/bin/opal_wrapper
# the following are part of vampiretrace
%{_prefix}/bin/vtcc
%{_prefix}/bin/vtcxx
%{_prefix}/bin/vtf77
%{_prefix}/bin/vtf90
%{_prefix}/bin/vtfilter
%{_prefix}/bin/vtunify
%{_prefix}/bin/opari
%{_prefix}/share/vt*txt
%if 0%{?suse_version} || "%{?rhel}" > "4"
%{_prefix}/bin/mpi*vt
%endif


# Note that we list the mandir specifically here, because we want all
# files found in that tree, because rpmbuild may have compressed them
# (e.g., foo.1.gz or foo.1.bz2) -- and we therefore don't know the
# exact filenames.
%files docs
%defattr(-, root, root, -)
%{_prefix}/man
%{_prefix}/share/doc
%dir %{_prefix}/share/vampirtrace
%{_prefix}/share/vampirtrace/doc
#%doc README INSTALL LICENSE

#############################################################################
#
# Changelog
#
#############################################################################
%changelog
* Mon Mar 08 2010 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 1.4.1

* Tue Dec 01 2009 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 1.3.4

* Wed Aug 12 2009 Josko Plazonic <plazonic@math.princeton.edu>
- stop disabling memory managers - turns out now we need them for pinning
  which helps with IB performance

* Wed Jul 15 2009 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 1.3.3

* Fri May 01 2009 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild once more for new torque

* Thu Apr 23 2009 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 1.3.2

* Wed Feb 18 2009 Josko Plazonic <plazonic@math.princeton.edu>
- add pathscale

* Tue Feb 17 2009 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 1.3

* Fri Jan 09 2009 Josko Plazonic <plazonic@math.princeton.edu>
- tweak modules for 2cluster so that intel 9.1 is preferred over
  both pgi and intel-11.0

* Tue Dec 23 2008 Josko Plazonic <plazonic@math.princeton.edu>
- various fixes to allow all to build on rhel4

* Fri Dec 19 2008 Josko Plazonic <plazonic@math.princeton.edu>
- 1.2.8 plus gfortran fixes for suse

* Fri Feb 22 2008 Josko Plazonic <plazonic@math.princeton.edu>
- adapt to Suse 10.1 and try to add lustre support

* Mon Oct 01 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild but only for pgi to solve pthreads issues

* Fri Sep 15 2007 Josko Plazonic <plazonic@math.princeton.edu>
- lots of fixes plus special kludge to enable us to use openmpi/intel91
  and yet make it so that openmpi/intel resolves to the newest compiler
  compiled openmpi

* Thu Sep 14 2007 Josko Plazonic <plazonic@math.princeton.edu>
- drastically revise the build - now we use one generic spec file
  for all compilers with a define to build for a specific compiler
  NOTE: TAKE CARE TO KEEP ONE SPEC FILE!

* Mon Jun 25 2007 Josko Plazonic <plazonic@math.princeton.edu>
- 1.2.3 version

* Thu Jun 14 2007 Josko Plazonic <plazonic@math.princeton.edu>
- 1.2.2 version

* Wed Mar 21 2007 Josko Plazonic <plazonic@math.princeton.edu>
- 1.1.5 version

* Mon Feb 19 2007 Josko Plazonic <plazonic@math.princeton.edu>
- add support for pvfs2

* Fri Feb 2 2007 Josko Plazonic <plazonic@math.princeton.edu>
- 1.1.4 version

* Mon Jan 8 2007 Dennis McRitchie <dmcr@princeton.edu>
- Added command-line option "--with ib[=<dir>]" and "--without ib".
- Defaults to "with ib" on x86_64 systems, and to "without ib" on 32-bit systems.
- If "with ib", rpm and install directory name reflects that fact.
- Supports runtime, devel, and doc sub-packages.
- Use lib64 directory (instead of lib) on x86_64 systems.
- Install directories are nested by version, compiler, and arch.

* Mon Dec 18 2006 Dennis McRitchie <dmcr@princeton.edu>
- Uses modules to set up the Intel enviroment.

* Wed Dec 13 2006 Dennis McRitchie <dmcr@princeton.edu>
- Upgraded to openmpi v1.1.2
- No longer requires Intel compiler environment to be setup in advance.

* Fri Oct 06 2006 Dennis McRitchie <dmcr@princeton.edu>
- Changed it so additional configure options could be added with '--define "configure_options <configure-options>"', e.g., '--define "configure_options --without-memory-manager"'.
- Changed Intel compiler build code to only define the compilers (i.e., CC, CXX, F77, FC), and not the PATHs and FLAGS. So the assumption is that the Intel compiler environment would have been set up in advance of the build.
- Added --without-libnuma to the configure line.
- Commented out the two %doc lines in the files section that were causing duplicate file warnings.

* Fri Oct  6 2006 Jeff Squyes <jsquyres@cisco.com>
- Remove LANL section; they don't want it
- Add some help for OFED building
- Remove some outdated "rm -f" lines for executables that we no longer ship

* Wed Apr 26 2006 Jeff Squyres <jsquyres@cisco.com>
- Revamp files listings to ensure that rpm -e will remove directories
  if rpm -i created them.
- Simplify options for making modulefiles and profile.d scripts.
- Add oscar define.
- Ensure to remove the previous installation root during prep.
- Cleanup the modulefile specification and installation; also ensure
  that the profile.d scripts get installed if selected.
- Ensure to list sysconfdir in the files list if it's outside of the
  prefix.

* Wed Mar 30 2006 Jeff Squyres <jsquyres@cisco.com>
- Lots of bit rot updates
- Reorganize and rename the subpackages
- Add / formalize a variety of rpmbuild --define options
- Comment out the docs subpackage for the moment (until we have some
  documentation -- coming in v1.1!)

* Wed May 03 2005 Jeff Squyres <jsquyres@open-mpi.org>
- Added some defines for LANL defaults
- Added more defines for granulatirty of installation location for
  modulefile
- Differentiate between installing in /opt and whether we want to
  install environment script files
- Filled in files for man and mca-general subpackages

* Thu Apr 07 2005 Greg Kurtzer <GMKurtzer@lbl.gov>
- Added opt building
- Added profile.d/modulefile logic and creation
- Minor cleanups

* Fri Apr 01 2005 Greg Kurtzer <GMKurtzer@lbl.gov>
- Added comments
- Split package into subpackages
- Cleaned things up a bit
- Sold the code to Microsoft, and now I am retiring. Thanks guys!

* Wed Mar 23 2005 Mezzanine <mezzanine@kainx.org>
- Specfile auto-generated by Mezzanine

