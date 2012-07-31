%define netcdfversion 4.2
%define netcdfnumversion %(echo %{netcdfversion} | tr -d .)

%define hdf5version 1.8.8
%define hdf5numversion %(echo %{hdf5version} | tr -d .)

# compiler for which we are doing this
%{!?compiler: %define compiler gcc}
%{!?compilermajor: %define compilermajor 12}
%{!?compilerminor: %define compilerminor 1}
%{!?openmpiversion: %define openmpiversion 1.4.5}
%define openmpinumversion %( printf "%02d%02d%02d" `echo %{openmpiversion} | cut -d. -f1,2,3 --output-delimiter=" "` )
%define compilerrname %{compiler}%{compilerversionnum}

# modules defaults
%define modulefile_path_top /usr/local/share/Modules/modulefiles/netcdf

# deployment plan:
# top dir /usr/local/netcdf/
#                        /gcc/hdf-1.8.8/4.2
#                        /gcc/hdf-1.8.8/openmpi-1.5.4/4.2
#                        /intel-12.1/hdf-1.8.8/4.2
#                        /intel-12.1/hdf-1.8.8/openmpi-1.5.4/4.2
%define localdir /usr/local/netcdf/%{compilerlong}/hdf5-%{hdf5version}/%{version}
%define localdiropenmpi /usr/local/netcdf/%{compilerlong}/hdf5-%{hdf5version}/openmpi-%{openmpiversion}/%{version}
%define localdirmpt /usr/local/netcdf/%{compilerlong}/hdf5-%{hdf5version}/mpt/%{version}
%define localdirimpi /usr/local/netcdf/%{compilerlong}/hdf5-%{hdf5version}/intel-mpi/%{version}

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilerruntime BuildRequires: gcc-gfortran hdf5-%{hdf5numversion}-gcc-devel \
Requires: hdf5-%{hdf5numversion}-gcc
%define compilerruntimeopenmpi BuildRequires: openmpi-gcc-devel = %{openmpiversion} hdf5-%{hdf5numversion}-gcc-openmpi%{openmpinumversion}-devel \
Requires: openmpi-gcc-runtime >= %{openmpiversion} hdf5-%{hdf5numversion}-gcc-openmpi%{openmpinumversion}
%define compilerruntimempt BuildRequires: gcc-gfortran hdf5-%{hdf5numversion}-gcc-mpt-devel sgi-mpt >= 2.05 \
Requires: sgi-mpt >= 2.05 hdf5-%{hdf5numversion}-gcc-mpt
%define compilerruntimeimpi BuildRequires: intel-mpi-modules-devel intel-mpi-modules-gcc hdf5-%{hdf5numversion}-gcc-impi-devel \
Requires: intel-mpi-modules-gcc hdf5-%{hdf5numversion}-gcc-impi
%define compilerdevel Requires: gcc-gfortran hdf5-%{hdf5numversion}-gcc-devel
%define compilerdevelopenmpi Requires: gcc-gfortran openmpi-gcc-devel >= %{openmpiversion} hdf5-%{hdf5numversion}-gcc-openmpi%{openmpinumversion}-devel
%define compilerdevelmpt Requires: gcc-gfortran sgi-mpt >= 2.05 hdf5-%{hdf5numversion}-gcc-mpt-devel
%define compilerdevelimpi Requires: gcc-gfortran intel-mpi-modules-devel intel-mpi-modules-gcc hdf5-%{hdf5numversion}-gcc-impi-devel
# do nothing special for gcc for build prep
%define compilerbuildprep echo Nothing to do for gcc prep
# no alias
%define modulefile_compiler_alias %{nil}
%define compilershort gcc
%define compilerlong gcc
%define compilerversionnum 446
%define compilerrname gcc
%define modulempt mpt
%endif
#
# Intel compiler
%if "%{compiler}" == "intel"
# these two are used to decide which version of intel we will be using to build it all
# and which version we will be providing
%define intelminrelease 6
%define compilerversion %{compilermajor}.%{compilerminor}
%define compilerversionnum %{compilermajor}%{compilerminor}
%define compilerruntime BuildRequires: hdf5-%{hdf5numversion}-intel%{compilerversionnum}-devel intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease} \
Requires: hdf5-%{hdf5numversion}-intel%{compilerversionnum} intel-compiler%{compilermajor}-%{bits}-default-modules >= %{compilerversion}-%{intelminrelease}
%define compilerruntimeopenmpi BuildRequires: openmpi-intel%{compilerversionnum}-devel = %{openmpiversion} hdf5-%{hdf5numversion}-intel%{compilerversionnum}-openmpi%{openmpinumversion}-devel intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease} \
Requires: openmpi-intel%{compilerversionnum}-runtime >= %{openmpiversion} hdf5-%{hdf5numversion}-intel%{compilerversionnum}-openmpi%{openmpinumversion} intel-compiler%{compilermajor}-%{bits}-default-modules >= %{compilerversion}-%{intelminrelease}
%define compilerruntimempt BuildRequires: sgi-mpt-intel%{compilerversionnum}-devel >= 2.05 hdf5-%{hdf5numversion}-intel%{compilerversionnum}-mpt-devel intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease} \
Requires: sgi-mpt-intel%{compilerversionnum} >= 2.05 hdf5-%{hdf5numversion}-intel%{compilerversionnum}-mpt intel-compiler%{compilermajor}-%{bits}-default-modules >= %{compilerversion}-%{intelminrelease}
%define compilerruntimeimpi BuildRequires: intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease}, intel-mpi-modules-devel, intel-mpi-modules-intel hdf5-%{hdf5numversion}-intel%{compilerversionnum}-impi-devel \
Requires: intel-mpi-modules-intel intel-compiler%{compilermajor}-%{bits}-default-modules >= %{compilerversion}-%{intelminrelease} hdf5-%{hdf5numversion}-intel%{compilerversionnum}-impi
%define compilerdevel Requires: intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease} hdf5-%{hdf5numversion}-intel%{compilerversionnum}-devel
%define compilerdevelopenmpi Requires: openmpi-intel%{compilerversionnum}-devel >= %{openmpiversion} hdf5-%{hdf5numversion}-intel%{compilerversionnum}-openmpi%{openmpinumversion}-devel
%define compilerdevelmpt Requires: sgi-mpt-intel%{compilerversionnum}-devel >= 2.05 hdf5-%{hdf5numversion}-intel%{compilerversionnum}-mpt-devel intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease}
%define compilerdevelimpi Requires: intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease}, intel-mpi-modules-devel, intel-mpi-modules-intel hdf5-%{hdf5numversion}-intel%{compilerversionnum}-impi-devel
# for intel we need to just specify our compilers
%if 0%{?rhel} > 5
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort FC=ifort F90=ifort CPP="icc -E" CXXCPP="icpc -E" LDFLAGS="-Wl,--build-id"; module load intel
%else
%define compilerbuildprep export CC=icc CXX=icpc F9X=ifort FC=ifort F90=ifort CPP="icc -E" CXXCPP="icpc -E"; module load intel
%endif
%define optflags -O3 -ip -no-prec-div
# the following is used in above
%define compilershort intel-%{compilermajor}
%define compilerlong intel-%{compilerversion}
%define modulempt mpt/intel-%{compilerversion}
%endif

# where modules really go
%define modulefile_path %{modulefile_path_top}/%{compilerlong}/hdf5-%{hdf5version}

%ifarch %{ix86}
%define bits 32
%else
%define bits 64
%endif

Name:           netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}
Version:        %{netcdfversion}
Release:        3%{?dist}
Summary:        Libraries for the Unidata network Common Data Form

Group:          Applications/Engineering
License:        NetCDF
URL:            http://www.unidata.ucar.edu/software/netcdf/
Source0:        http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-%{version}.tar.gz
#Source0:        http://www.unidata.ucar.edu/downloads/netcdf/ftp/snapshot/netcdf-4-daily.tar.gz
#Use pkgconfig in nc-config to avoid multi-lib issues
Patch0:         netcdf-pkgconfig.patch
#Strip FFLAGS from nc-config
Patch1:         netcdf-fflags.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  chrpath
BuildRequires:  gawk
%if 0%{?rhel} > 5
BuildRequires:  libcurl-devel
BuildRequires:  doxygen
%else
BuildRequires:  curl-devel
BuildRequires:  doxygen16
%endif
BuildRequires:  zlib-devel
%ifnarch s390 s390x %{arm}
BuildRequires:  valgrind
%endif
#mpiexec segfaults if ssh is not present
#https://trac.mcs.anl.gov/projects/mpich2/ticket/1576
BuildRequires:  openssh-clients
%{compilerruntime}

%define with_serial %{?_without_serial: 0}%{?!_without_serial: 1}
%global with_mpich2 0
%define with_openmpi %{?_without_openmpi: 0}%{?!_without_openmpi: 1}
%define with_impi %{?_without_impi: 0}%{?!_without_impi: 1}
%if 0%{?rhel} == 5
%define with_mpt  %{?_with_mpt: 1}%{?!_with_mpt: 0}
%else
%define with_mpt  %{?_without_mpt: 0}%{?!_without_mpt: 1}
%endif

%if %{with_mpich2}
%global mpi_list mpich2
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif
%if %{with_mpt}
%global mpi_list %{?mpi_list} mpt
%endif
%if %{with_impi}
%global mpi_list %{?mpi_list} intel-mpi
%endif

%description
NetCDF (network Common Data Form) is an interface for array-oriented 
data access and a freely-distributed collection of software libraries 
for C, Fortran, C++, and perl that provides an implementation of the 
interface.  The NetCDF library also defines a machine-independent 
format for representing scientific data.  Together, the interface, 
library, and format support the creation, access, and sharing of 
scientific data. The NetCDF software was developed at the Unidata 
Program Center in Boulder, Colorado.

NetCDF data is: 

   o Self-Describing: A NetCDF file includes information about the
     data it contains.

   o Network-transparent:  A NetCDF file is represented in a form that
     can be accessed by computers with different ways of storing
     integers, characters, and floating-point numbers.

   o Direct-access:  A small subset of a large dataset may be accessed
     efficiently, without first reading through all the preceding
     data.

   o Appendable:  Data can be appended to a NetCDF dataset along one
     dimension without copying the dataset or redefining its
     structure. The structure of a NetCDF dataset can be changed,
     though this sometimes causes the dataset to be copied.

   o Sharable:  One writer and multiple readers may simultaneously
     access the same NetCDF file.


%package devel
Summary:        Development files for netcdf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
%if 0%{?rhel} > 5
Requires:       libcurl-devel
%else
Requires:       curl-devel
%endif
%{compilerdevel}

%description devel
This package contains the netCDF C header files, shared devel libs, and 
man pages.


%package static
Summary:        Static libs for netcdf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description static
This package contains the netCDF C static libs.


%if %{with_mpich2}
%package mpich2
Summary: NetCDF mpich2 libraries
Group: Development/Libraries
Requires: mpich2
BuildRequires: mpich2-devel

%description mpich2
NetCDF parallel mpich2 libraries


%package mpich2-devel
Summary: NetCDF mpich2 development files
Group: Development/Libraries
Requires: %{name}-mpich2 = %{version}-%{release}
Requires: mpich2
Requires: pkgconfig
%if 0%{?rhel} > 5
Requires: libcurl-devel
%else
Requires: curl-devel
%endif

%description mpich2-devel
NetCDF parallel mpich2 development files


%package mpich2-static
Summary: NetCDF mpich2 static libraries
Group: Development/Libraries
Requires: %{name}-mpich2-devel = %{version}-%{release}

%description mpich2-static
NetCDF parallel mpich2 static libraries
%endif


%if %{with_openmpi}
%package openmpi%{openmpinumversion}
Summary: NetCDF openmpi libraries
Group: Development/Libraries
%{compilerruntimeopenmpi}

%description openmpi%{openmpinumversion}
NetCDF parallel openmpi libraries


%package openmpi%{openmpinumversion}-devel
Summary: NetCDF openmpi development files
Group: Development/Libraries
Requires: %{name}-openmpi%{openmpinumversion} = %{version}-%{release}
Requires: pkgconfig
%if 0%{?rhel} > 5
Requires: libcurl-devel
%else
Requires: curl-devel
%endif
%{compilerdevelopenmpi}

%description openmpi%{openmpinumversion}-devel
NetCDF parallel openmpi development files


%package openmpi%{openmpinumversion}-static
Summary: NetCDF openmpi static libraries
Group: Development/Libraries
Requires: %{name}-openmpi%{openmpinumversion}-devel = %{version}-%{release}

%description openmpi%{openmpinumversion}-static
NetCDF parallel openmpi static libraries
%endif


%if %{with_mpt}
%package mpt
Summary: NetCDF mpt libraries
Group: Development/Libraries
%{compilerruntimempt}

%description mpt
NetCDF parallel mpt libraries

%package mpt-devel
Summary: NetCDF mpt development files
Group: Development/Libraries
Requires: %{name}-mpt = %{version}-%{release}
Requires: pkgconfig
%if 0%{?rhel} > 5
Requires: libcurl-devel
%else
Requires: curl-devel
%endif
%{compilerdevelmpt}

%description mpt-devel
NetCDF parallel mpt development files

%package mpt-static
Summary: NetCDF mpt static libraries
Group: Development/Libraries
Requires: %{name}-mpt-devel = %{version}-%{release}

%description mpt-static
NetCDF parallel mpt static libraries
%endif

%if %{with_impi}
%package impi
Summary: NetCDF intel-mpi libraries
Group: Development/Libraries
%{compilerruntimeimpi}

%description impi
NetCDF parallel intel-mpi libraries

%package impi-devel
Summary: NetCDF intel-mpi development files
Group: Development/Libraries
Requires: %{name}-impi = %{version}-%{release}
Requires: pkgconfig
%if 0%{?rhel} > 5
Requires: libcurl-devel
%else
Requires: curl-devel
%endif
%{compilerdevelimpi}

%description impi-devel
NetCDF parallel intel-mpi development files

%package impi-static
Summary: NetCDF intel-mpi static libraries
Group: Development/Libraries
Requires: %{name}-impi-devel = %{version}-%{release}

%description impi-static
NetCDF parallel intel-mpi static libraries
%endif


%prep
%setup -q -n netcdf-%{version}
%patch0 -p1 -b .pkgconfig
%patch1 -p1 -b .fflags


%build
# setup modules here first, even if may not need them - will not hurt
. /etc/profile.d/modules.sh
%{compilerbuildprep}
module load hdf5/%{compiler}/%{hdf5version}
#Do out of tree builds
%global _configure ../configure
#Common configure options
%global configure_opts \\\
           --enable-shared \\\
           --enable-netcdf-4 \\\
           --enable-dap \\\
           --enable-extra-example-tests \\\
           --disable-dap-remote-tests \\\
%{nil}

%if %{with_serial}
# Serial build
mkdir build
pushd build
ln -s ../configure .
%configure %{configure_opts} \
    --libdir=%{localdir}/%{_lib} \
    --bindir=%{localdir}/bin \
    --sbindir=%{localdir}/sbin \
    --includedir=%{localdir}/include \
    --datarootdir=%{localdir}/share \
    --mandir=%{localdir}/share/man \
	
make %{?_smp_mflags}
popd
%endif
module purge

build_onempi() {
  mkdir $1
  pushd $1
  %{compilerbuildprep}
  export CC=mpicc
  module load $3 
  module load $4
  ln -s ../configure .
  %configure %{configure_opts} \
    --libdir=$2/%{_lib} \
    --bindir=$2/bin \
    --sbindir=$2/sbin \
    --includedir=$2/include \
    --datarootdir=$2/share \
    --mandir=$2/share/man \
    --enable-parallel-tests
  make %{?_smp_mflags}
  module purge
  popd
}

%if %{with_openmpi}
build_onempi openmpi %{localdiropenmpi} openmpi/%{compiler} hdf5/%{compilerlong}/openmpi-%{openmpiversion}/%{hdf5version}
%endif
%if %{with_mpt}
build_onempi mpt %{localdirmpt} %{modulempt} hdf5/%{compilerlong}/mpt/%{hdf5version}
%endif
%if %{with_impi}
build_onempi impi %{localdirimpi} intel-mpi/%{compiler} hdf5/%{compilerlong}/intel-mpi/%{hdf5version}
%endif

%install
. /etc/profile.d/modules.sh
%{compilerbuildprep}
%if %{with_serial}
module load hdf5/%{compiler}/%{hdf5version}
make -C build install DESTDIR=${RPM_BUILD_ROOT}
module purge
/bin/rm -f ${RPM_BUILD_ROOT}/%{localdir}/%{_lib}/*.la
chrpath --delete ${RPM_BUILD_ROOT}/%{localdir}/bin/nc{copy,dump,gen,gen3}
/bin/rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
mkdir -p ${RPM_BUILD_ROOT}/%{localdir}/share/doc
cp -ar COPYRIGHT README examples ${RPM_BUILD_ROOT}/%{localdir}/share/doc/
mkdir -p ${RPM_BUILD_ROOT}/%{modulefile_path}
cat > ${RPM_BUILD_ROOT}/%{modulefile_path}/%{version} <<ENDSERIAL
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# netcdf rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds netcdf %{version} for %{compilerlong} compiled with hdf5-%{hdf5version} to various paths"
}

module-whatis   "Sets up netcdf %{version} for %{compilerlong} compiled with hdf5-%{hdf5version} in your environment"

prepend-path PATH "%{localdir}/bin"
prepend-path LD_LIBRARY_PATH "%{localdir}/%{_lib}"
prepend-path LIBRARY_PATH "%{localdir}/%{_lib}"
prepend-path MANPATH "%{localdir}/share/man"
setenv NETCDFDIR "%{localdir}"
append-path -d { } LDFLAGS "-L%{localdir}/%{_lib}"
append-path -d { } INCLUDE "-I%{localdir}/include"
append-path CPATH "%{localdir}/include"
append-path -d { } FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_LDFLAGS "-L%{localdir}/%{_lib}"
append-path -d { } LOCAL_INCLUDE "-I%{localdir}/include"
append-path -d { } LOCAL_CFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{localdir}/include"
ENDSERIAL
%endif
module purge

# params:
# 1 - name
# 2 - long name
# 3 - destination dir
# 4 - what module to load
# 5 - other module
install_one() {
  module load $4
  module load $5
  make -C $1 install DESTDIR=${RPM_BUILD_ROOT}
  rm $RPM_BUILD_ROOT/$3/%{_lib}/*.la
  chrpath --delete ${RPM_BUILD_ROOT}/$3/bin/nc{copy,dump,gen,gen3}
  mkdir -p ${RPM_BUILD_ROOT}/$3/share/doc
  cp -ar COPYRIGHT README ${RPM_BUILD_ROOT}/$3/share/doc/
  mkdir -p ${RPM_BUILD_ROOT}/%{modulefile_path}/$2
  cat > ${RPM_BUILD_ROOT}/%{modulefile_path}/$2/%{version} <<ENDMPI
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# netcdf rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds netcdf %{version} for %{compilerlong} compiled with hdf5-%{hdf5version} and $2 various paths"
}

module-whatis   "Sets up netcdf %{version} for %{compilerlong} compiled with hdf5-%{hdf5version} and $2 in your environment"

prepend-path PATH "$3/bin"
prepend-path LD_LIBRARY_PATH "$3/%{_lib}"
prepend-path LIBRARY_PATH "$3/%{_lib}"
prepend-path MANPATH "$3/share/man"
setenv NETCDFDIR "$3"
append-path -d { } LDFLAGS "-L$3/%{_lib}"
append-path -d { } INCLUDE "-I$3/include"
append-path CPATH "$3/include"
append-path -d { } FFLAGS "-I$3/include"
append-path -d { } LOCAL_LDFLAGS "-L$3/%{_lib}"
append-path -d { } LOCAL_INCLUDE "-I$3/include"
append-path -d { } LOCAL_CFLAGS "-I$3/include"
append-path -d { } LOCAL_FFLAGS "-I$3/include"
append-path -d { } LOCAL_CXXFLAGS "-I$3/include"
ENDMPI
  module purge
}

%if %{with_openmpi}
install_one openmpi openmpi-%{openmpiversion} %{localdiropenmpi} openmpi/%{compiler} hdf5/%{compilerlong}/openmpi-%{openmpiversion}/%{hdf5version}
%endif
%if %{with_mpt}
install_one mpt mpt %{localdirmpt} %{modulempt} hdf5/%{compilerlong}/mpt/%{hdf5version}
%endif
%if %{with_impi}
install_one impi intel-mpi %{localdirimpi} intel-mpi/%{compiler} hdf5/%{compilerlong}/intel-mpi/%{hdf5version}
%endif

%check
. /etc/profile.d/modules.sh
%{compilerbuildprep}
%if %{with_serial}
module load hdf5/%{compiler}/%{hdf5version}
make -C build check
%endif
module purge

check_onempi() {
  %{compilerbuildprep}
  export CC=mpicc
  module load $3
  module load $4
  make -C $1 check
  module purge
}

%if %{with_openmpi}
check_onempi openmpi %{localdiropenmpi} openmpi/%{compiler} hdf5/%{compilerlong}/openmpi-%{openmpiversion}/%{hdf5version}
%endif
%if %{with_mpt}
echo Skipping mpt check - to review at a later time to see if we can get it to run
#check_onempi mpt %{localdirmpt} %{modulempt} hdf5/%{compilerlong}/mpt/%{hdf5version}
%endif
%if %{with_impi}
# this will work with mpirun
perl -pi -e 's|mpiexec|mpirun|g' *test*/run*sh
check_onempi impi %{localdirimpi} intel-mpi/%{compiler} hdf5/%{compilerlong}/intel-mpi/%{hdf5version}
perl -pi -e 's|mpirun|mpiexec|g' *test*/run*sh
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if %{with_serial}
%files
%defattr(-,root,root,-)
%dir %{localdir}/bin
%{localdir}/bin/nccopy
%{localdir}/bin/ncdump
%{localdir}/bin/ncgen
%{localdir}/bin/ncgen3
%dir %{localdir}/%{_lib}
%{localdir}/%{_lib}/*.so.*
%dir %{localdir}/share
%dir %{localdir}/share/doc
%doc %{localdir}/share/doc/COPYRIGHT
%doc %{localdir}/share/doc/README
%dir %{localdir}/share/man
%dir %{localdir}/share/man/man*
%doc %{localdir}/share/man/man1/*
%dir %{modulefile_path_top}
%dir %{modulefile_path_top}/*
%dir %{modulefile_path}
%{modulefile_path}/%{version}

%files devel
%defattr(-,root,root,-)
%{localdir}/bin/nc-config
%dir %{localdir}/include
%{localdir}/include/netcdf.h
%{localdir}/%{_lib}/*.so
%{localdir}/%{_lib}/pkgconfig/netcdf.pc
%doc %{localdir}/share/man/man3/*
%doc %{localdir}/share/doc/examples

%files static
%defattr(-,root,root,-)
%{localdir}/%{_lib}/*.a
%endif

%if %{with_mpich2}
%files mpich2
%defattr(-,root,root,-)
%doc COPYRIGHT README
%{_libdir}/mpich2/bin/nccopy
%{_libdir}/mpich2/bin/ncdump
%{_libdir}/mpich2/bin/ncgen
%{_libdir}/mpich2/bin/ncgen3
%{_libdir}/mpich2/lib/*.so.*
%doc %{_libdir}/mpich2/share/man/man1/*.1*

%files mpich2-devel
%defattr(-,root,root,-)
%{_libdir}/mpich2/bin/nc-config
%{_includedir}/mpich2-%{_arch}
%{_libdir}/mpich2/lib/*.so
%{_libdir}/mpich2/lib/pkgconfig
%doc %{_libdir}/mpich2/share/man/man3/*.3*

%files mpich2-static
%defattr(-,root,root,-)
%{_libdir}/mpich2/lib/*.a
%endif

%if %{with_openmpi}
%defattr(-,root,root,-)
%files openmpi%{openmpinumversion}
%dir %{localdiropenmpi}/bin
%{localdiropenmpi}/bin/nccopy
%{localdiropenmpi}/bin/ncdump
%{localdiropenmpi}/bin/ncgen
%{localdiropenmpi}/bin/ncgen3
%dir %{localdiropenmpi}/%{_lib}
%{localdiropenmpi}/%{_lib}/*.so.*
%dir %{localdiropenmpi}/share
%dir %{localdiropenmpi}/share/doc
%doc %{localdiropenmpi}/share/doc/COPYRIGHT
%doc %{localdiropenmpi}/share/doc/README
%dir %{localdiropenmpi}/share/man
%dir %{localdiropenmpi}/share/man/man*
%doc %{localdiropenmpi}/share/man/man1/*.1*
%dir %{modulefile_path_top}
%dir %{modulefile_path_top}/*
%dir %{modulefile_path}
%dir %{modulefile_path}/openmpi-%{openmpiversion}
%{modulefile_path}/openmpi-%{openmpiversion}/%{version}

%files openmpi%{openmpinumversion}-devel
%defattr(-,root,root,-)
%{localdiropenmpi}/bin/nc-config
%dir %{localdiropenmpi}/include
%{localdiropenmpi}/include/*
%{localdiropenmpi}/%{_lib}/*.so
%{localdiropenmpi}/%{_lib}/pkgconfig
%doc %{localdiropenmpi}/share/man/man3/*.3*

%files openmpi%{openmpinumversion}-static
%defattr(-,root,root,-)
%{localdiropenmpi}/%{_lib}/*.a
%endif

%if %{with_mpt}
%defattr(-,root,root,-)
%files mpt
%dir %{localdirmpt}/bin
%{localdirmpt}/bin/nccopy
%{localdirmpt}/bin/ncdump
%{localdirmpt}/bin/ncgen
%{localdirmpt}/bin/ncgen3
%dir %{localdirmpt}/%{_lib}
%{localdirmpt}/%{_lib}/*.so.*
%dir %{localdirmpt}/share
%dir %{localdirmpt}/share/doc
%doc %{localdirmpt}/share/doc/COPYRIGHT
%doc %{localdirmpt}/share/doc/README
%dir %{localdirmpt}/share/man
%dir %{localdirmpt}/share/man/man*
%doc %{localdirmpt}/share/man/man1/*.1*
%dir %{modulefile_path_top}
%dir %{modulefile_path_top}/*
%dir %{modulefile_path}
%dir %{modulefile_path}/mpt
%{modulefile_path}/mpt/%{version}

%files mpt-devel
%defattr(-,root,root,-)
%{localdirmpt}/bin/nc-config
%dir %{localdirmpt}/include
%{localdirmpt}/include/*
%{localdirmpt}/%{_lib}/*.so
%{localdirmpt}/%{_lib}/pkgconfig
%doc %{localdirmpt}/share/man/man3/*.3*

%files mpt-static
%defattr(-,root,root,-)
%{localdirmpt}/%{_lib}/*.a
%endif

%if %{with_impi}
%defattr(-,root,root,-)
%files impi
%dir %{localdirimpi}/bin
%{localdirimpi}/bin/nccopy
%{localdirimpi}/bin/ncdump
%{localdirimpi}/bin/ncgen
%{localdirimpi}/bin/ncgen3
%dir %{localdirimpi}/%{_lib}
%{localdirimpi}/%{_lib}/*.so.*
%dir %{localdirimpi}/share
%dir %{localdirimpi}/share/doc
%doc %{localdirimpi}/share/doc/COPYRIGHT
%doc %{localdirimpi}/share/doc/README
%dir %{localdirimpi}/share/man
%dir %{localdirimpi}/share/man/man*
%doc %{localdirimpi}/share/man/man1/*.1*
%dir %{modulefile_path_top}
%dir %{modulefile_path_top}/*
%dir %{modulefile_path}
%dir %{modulefile_path}/intel-mpi
%{modulefile_path}/intel-mpi/%{version}

%files impi-devel
%defattr(-,root,root,-)
%{localdirimpi}/bin/nc-config
%dir %{localdirimpi}/include
%{localdirimpi}/include/*
%{localdirimpi}/%{_lib}/*.so
%{localdirimpi}/%{_lib}/pkgconfig
%doc %{localdirimpi}/share/man/man3/*.3*

%files impi-static
%defattr(-,root,root,-)
%{localdirimpi}/%{_lib}/*.a
%endif

%changelog
* Wed Mar 21 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-3
- Update to real 4.2 final

* Tue Mar 20 2012 Dan Horák <dan[at]danny.cz> - 4.2-2
- use %%{mpi_list} also in %%check

* Fri Mar 16 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-1
- Update to 4.2 final

* Wed Mar 7 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.4.rc2
- Ship examples with -devel

* Wed Mar 7 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.3.rc2
- Enable MPI builds

* Tue Mar 6 2012 Orion Poplawski <orion@cora.nwra.com> - 4.2-0.2.rc2
- Update to 4.2-rc2
- Fortran and C++ APIs are now in separate packages

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.3-3
- Rebuild for hdf5 1.8.8, add explicit requires

* Thu Aug 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 4.1.3-2
- Add ARM to valgrind excludes

* Tue Jun 21 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.3-1
- Update to 4.1.3
- Update pkgconfig and fflags patches
- Drop libm patch fixed upstream

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.2-2
- Rebuild for hdf5 1.8.7

* Thu Mar 31 2011 Orion Poplawski <orion@cora.nwra.com> - 4.1.2-1
- Update to 4.1.2 (soname bump)
- Add patch to add -lm to libnetcdf4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 19 2010 Dan Horák <dan[at]danny.cz> - 4.1.1-4
- no valgrind on s390(x)

* Mon Apr 19 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-3
- Explicitly link libnetcdf.so against -lhdf5_hl -lhdf5

* Fri Apr 9 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-2
- Add patch to cleanup nc-config --fflags

* Thu Apr 8 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.1-1
- Update to 4.1.1

* Fri Feb 5 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-1
- Update to 4.1.0 final

* Mon Feb 1 2010 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.8.2010020100
- Update snapshot, pkgconfig patch
- Re-enable make check

* Sat Dec 5 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.7.2009120100
- Leave include files in /usr/include

* Tue Dec 1 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.6.2009120100
- Update snapshot, removes SZIP defines from header

* Fri Nov 13 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.5.2009111309
- Update snapshot
- Docs are installed now

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.5.2009111008
- Explicitly link libnetcdf to the hdf libraries, don't link with -lcurl

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.4.2009111008
- Add Requires: libcurl-devel to devel package

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.3.2009111008
- Drop hdf4 support - too problematic with linking all required libraries

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.2.2009111008
- Add patch to use proper hdf4 libraries
- Add Requires: hdf-devel, hdf5-devel to devel package
- Move nc-config to devel package

* Wed Nov 11 2009 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.1.2009111008
- Update to 4.1.0 beta 2 snapshot
- Enable: netcdf-4, dap, hdf4, ncgen4, a lot more tests

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Orion Poplawski <orion@cora.nwra.com> - 4.0.1-1
- Update to 4.0.1
- Add pkgconfig file

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Orion Poplawski <orion@cora.nwra.com> - 4.0.0-1
- Update to 4.0 final
- Drop netcdf-3 symlink (bug #447158)
- Update cstring patch, partially upstreamed

* Thu May 29 2008 Balint Cristian <rezso@rdsor.ro> - 4.0.0-0.6.beta2
- fix symlink to netcdf-3

* Sun May 18 2008 Patrice Dumas <pertusus@free.fr> - 4.0.0-0.5.beta2
- use %%{_fmoddir}
- don't use %%makeinstall

* Thu May 15 2008 Balint Cristian <rezso@rdsor.ro> - 4.0.0-0.4.beta2
- re-enable ppc64 since hdf5 is now present for ppc64

* Thu May  8 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.3.beta2
- make package compliant with bz # 373861

* Thu May  8 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.2.beta2
- ExcludeArch: ppc64 since it doesn't (for now) have hdf5

* Wed May  7 2008 Ed Hill <ed@eh3.com> - 4.0.0-0.1.beta2
- try out upstream 4.0.0-beta2

* Wed Apr  2 2008 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-7
- Change patch to include <cstring>
- Remove %%{?_smp_mflags} - not parallel build safe (fortran modules)

* Wed Feb 20 2008 Ed Hill <ed@eh3.com> - 3.6.2-6
- add patch that (hopefully?) allows the GCC 4.3 build to proceed

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6.2-5
- Autorebuild for GCC 4.3

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 3.6.2-4
- add BR: gawk

* Sat Aug 25 2007 Ed Hill <ed@eh3.com> - 3.6.2-3
- rebuild for BuildID

* Mon May 21 2007 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-2
- Run checks

* Sat Mar 17 2007 Ed Hill <ed@eh3.com> - 3.6.2-1
- 3.6.2 has a new build system supporting shared libs

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.6.1-4
- switch to compat-gcc-34-g77 instead of compat-gcc-32-g77

* Sat Sep  2 2006 Ed Hill <ed@eh3.com> - 3.6.1-3
- rebuild for imminent FC-6 release

* Thu May 11 2006 Ed Hill <ed@eh3.com> - 3.6.1-2
- add missing BuildRequires for the g77 interface

* Fri Apr 21 2006 Ed Hill <ed@eh3.com> - 3.6.1-1
- update to upstream 3.6.1

* Thu Feb 16 2006 Ed Hill <ed@eh3.com> - 3.6.0-10.p1
- rebuild for new GCC

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> - 3.6.0-9.p1
- rebuild for gcc4.1

* Sun Oct 16 2005 Ed Hill <ed@eh3.com> - 3.6.0-8.p1
- building the library twice (once each for g77 and gfortran) 
  fixes an annoying problem for people who need both compilers

* Fri Sep 29 2005 Ed Hill <ed@eh3.com> - 3.6.0-7.p1
- add FFLAGS="-fPIC"

* Fri Jun 13 2005 Ed Hill <ed@eh3.com> - 3.6.0-6.p1
- rebuild

* Fri Jun  3 2005 Ed Hill <ed@eh3.com> - 3.6.0-5.p1
- bump for the build system

* Mon May  9 2005 Ed Hill <ed@eh3.com> - 3.6.0-4.p1
- remove hard-coded dist/fedora macros

* Wed May  5 2005 Ed Hill <ed@eh3.com> - 3.6.0-3.p1
- make netcdf-devel require netcdf (bug #156748)
- cleanup environment and paths

* Tue Apr  5 2005 Ed Hill <ed@eh3.com> - 0:3.6.0-2.p1
- update for gcc-gfortran
- fix file permissions

* Sat Mar  5 2005 Ed Hill <ed@eh3.com> - 0:3.6.0-1.p1
- update for 3.6.0-p1 large-files-bug fix and remove the Epoch

* Sun Dec 12 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0-0.2.beta6
- fix naming scheme for pre-releases (per Michael Schwendt)

* Sat Dec 11 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.2
- For Fortran, use only g77 (ignore gfortran, even if its installed)

* Tue Dec  7 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.1
- remove "BuildRequires: gcc4-gfortran"

* Sat Dec  4 2004 Ed Hill <eh3@mit.edu> - 0:3.6.0beta6-0.fdr.0
- upgrade to 3.6.0beta6
- create separate devel package that does *not* depend upon 
  the non-devel package and put the headers/libs in "netcdf-3" 
  subdirs for easy co-existance with upcoming netcdf-4

* Thu Dec  2 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.12
- remove unneeded %%configure flags

* Wed Dec  1 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.11
- headers in /usr/include/netcdf, libs in /usr/lib/netcdf

* Mon Oct  4 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.10
- Put headers in their own directory but leave the libraries in the 
  %%{_libdir} -- there are only two libs and the majority of other
  "*-devel" packages follow this pattern

* Sun Oct  3 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:3.5.1-0.fdr.9
- add patch to install lib and headers into own tree

* Sun Aug  1 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.8
- added -fPIC so x86_64 build works with nco package

* Fri Jul 30 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.7
- fix typo in the x86_64 build and now works on x86_64

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.6
- fix license

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.5
- fix (hopefully?) x86_64 /usr/lib64 handling

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.4
- replace paths with macros

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.3
- fix spelling

* Thu Jul 15 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.2
- removed "--prefix=/usr" from %%configure

* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.1
- Remove unnecessary parts and cleanup for submission

* Wed Jul 14 2004 Ed Hill <eh3@mit.edu> - 0:3.5.1-0.fdr.0
- Initial RPM release.
