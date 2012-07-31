%define netcdfversion 4.2
%define netcdfnumversion %(echo %{netcdfversion} | tr -d .)

%define netcdfversioncxx 4.2
%define netcdfversioncxx4 4.2
%define netcdfversionf 4.2

%{!?hdf5version: %define hdf5version 1.8.8}
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
# do nothing special for gcc for build prep
%define compilerbuildprep export F77=gfortran FC=gfortran
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

%define compilerruntime BuildRequires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-devel \
Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}
%define compilerruntimeopenmpi BuildRequires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-openmpi%{openmpinumversion}-devel openmpi-%{compilerrname}-devel = %{openmpiversion} \
Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-openmpi%{openmpinumversion}
%define compilerruntimempt BuildRequires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-mpt-devel \
Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-mpt
%define compilerruntimeimpi BuildRequires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-impi-devel \
Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-impi
%define compilerdevel Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-devel
%define compilerdevelopenmpi Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-openmpi%{openmpinumversion}-devel
%define compilerdevelmpt Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-mpt-devel
%define compilerdevelimpi Requires: netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-impi-devel

# where modules really go
%define modulefile_path %{modulefile_path_top}/%{compilerlong}/hdf5-%{hdf5version}

%ifarch %{ix86}
%define bits 32
%else
%define bits 64
%endif

Name:           netcdf%{netcdfnumversion}-%{compilerrname}-hdf5-%{hdf5numversion}-extra
Version:        %{netcdfversion}
Release:        6%{?dist}
Summary:        Extra Libraries for the Unidata network Common Data Form

Group:          Applications/Engineering
License:        NetCDF
URL:            http://www.unidata.ucar.edu/software/netcdf/
Source0:        ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-cxx-%{netcdfversioncxx}.tar.gz
Source1:	http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx4-%{netcdfversioncxx4}.tar.gz
Source2:        http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-%{netcdfversionf}.tar.gz
#Use pkgconfig in nc-config to avoid multi-lib issues
Patch0:         netcdf-pkgconfig.patch
#Strip FFLAGS from nc-config
Patch1:         netcdf-fflags.patch
# Fix issue parsing mpif90 output
Patch2:         netcdf-postdeps.patch

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
%global mpi_list %{?mpi_list} impi
%endif
%if %{with_serial}
%global mpi_list %{?mpi_list} serial
%endif

%description
NetCDF extra libraries.

%package devel
Summary:        Development files for netcdf extras
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
This package contains development files for netcdf
extra libraries.


%package static
Summary:        Static libs for netcdf
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description static
This package contains the netCDF extras static libs



%if %{with_mpich2}
%package mpich2
Summary: NetCDF extras mpich2 libraries
Group: Development/Libraries
Requires: mpich2
BuildRequires: mpich2-devel

%description mpich2
NetCDF extras parallel mpich2 libraries


%package mpich2-devel
Summary: NetCDF extras mpich2 development files
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
NetCDF extras parallel mpich2 development files


%package mpich2-static
Summary: NetCDF extras mpich2 static libraries
Group: Development/Libraries
Requires: %{name}-mpich2-devel = %{version}-%{release}

%description mpich2-static
NetCDF extras parallel mpich2 static libraries
%endif


%if %{with_openmpi}
%package openmpi%{openmpinumversion}
Summary: NetCDF extras openmpi libraries
Group: Development/Libraries
%{compilerruntimeopenmpi}

%description openmpi%{openmpinumversion}
NetCDF extras parallel openmpi libraries


%package openmpi%{openmpinumversion}-devel
Summary: NetCDF extras openmpi development files
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
NetCDF extras parallel openmpi development files


%package openmpi%{openmpinumversion}-static
Summary: NetCDF extras openmpi static libraries
Group: Development/Libraries
Requires: %{name}-openmpi%{openmpinumversion}-devel = %{version}-%{release}

%description openmpi%{openmpinumversion}-static
NetCDF extras parallel openmpi static libraries
%endif


%if %{with_mpt}
%package mpt
Summary: NetCDF extras mpt libraries
Group: Development/Libraries
%{compilerruntimempt}

%description mpt
NetCDF extras parallel mpt libraries

%package mpt-devel
Summary: NetCDF extras mpt development files
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
NetCDF extras parallel mpt development files

%package mpt-static
Summary: NetCDF extras mpt static libraries
Group: Development/Libraries
Requires: %{name}-mpt-devel = %{version}-%{release}

%description mpt-static
NetCDF extras parallel mpt static libraries
%endif

%if %{with_impi}
%package impi
Summary: NetCDF extras intel-mpi libraries
Group: Development/Libraries
%{compilerruntimeimpi}

%description impi
NetCDF extras parallel intel-mpi libraries

%package impi-devel
Summary: NetCDF extras intel-mpi development files
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
NetCDF extras parallel intel-mpi development files

%package impi-static
Summary: NetCDF extras intel-mpi static libraries
Group: Development/Libraries
Requires: %{name}-impi-devel = %{version}-%{release}

%description impi-static
NetCDF extras parallel intel-mpi static libraries
%endif


%prep
%setup -q -c -n netcdf-extras-%{version} -a 1 -a 2
cd netcdf-fortran-*
%patch0 -p1 -b .pkgconfig
%patch1 -p1 -b .fflags
%patch2 -p1 -b .postdeps
cd ..
sed -i -e '1i#!/bin/sh' netcdf-fortran*/examples/F90/run_f90_par_examples.sh

for i in %{mpi_list}; do
	mkdir $i
	cp -ar netcdf-* $i/
	# Fix line endings
	sed -i -e 's/\r//' $i/netcdf-cxx4-*/examples/*.cpp
done

%build
# setup modules here first, even if may not need them - will not hurt
. /etc/profile.d/modules.sh

build_one() {
pushd $1
%{compilerbuildprep}
module load $4 $5 $6
OPTS="--libdir=$2/%{_lib} \
           --bindir=$2/bin \
           --sbindir=$2/bin \
           --includedir=$2/include \
           --datarootdir=$2/share \
           --infodir=$2/share/info \
           --mandir=$2/share/man"
cd netcdf-cxx-%{netcdfversioncxx}
%configure $OPTS
make %{?_smp_mflags}
cd ..
cd netcdf-cxx4-%{netcdfversioncxx4}
if [ "$3" = "mpi" ]; then
	export CC=mpicc
	export CXX=mpicxx
fi
%configure $OPTS
make %{?_smp_mflags}
cd .. 
cd netcdf-fortran-*
export FCFLAGS="$RPM_OPT_FLAGS"
if [ "$3" = "mpi" ]; then
	export F77="mpif90"
	export FC="mpif90"
	export CC="mpicc"
	OPTSTWO="--enable-parallel --enable-parallel-tests"
%if "%{compiler}" == "gcc"
	export CPPFLAGS=-DpgiFortran
%endif
%if "%{compiler}" == "intel"
	export CPPFLAGS=-DpgiFortran
	perl -pi -e 's,ifort\*,ifort* | mpif90*,' m4/libtool.m4 configure
%endif
else
	OPTSTWO="--enable-extra-example-tests"
fi
%configure $OPTS $OPTSTWO
make %{?_smp_mflags}
cd ..
module purge
popd
}

%if %{with_serial}
build_one serial %{localdir} serial hdf5/%{compiler}/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/%{version}
%endif
%if %{with_openmpi}
build_one openmpi %{localdiropenmpi} mpi openmpi/%{compiler} hdf5/%{compilerlong}/openmpi-%{openmpiversion}/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/openmpi-%{openmpiversion}/%{version}
%endif
%if %{with_mpt}
build_one mpt %{localdirmpt} mpi %{modulempt} hdf5/%{compilerlong}/mpt/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/mpt/%{version}
%endif
%if %{with_impi}
build_one impi %{localdirimpi} mpi intel-mpi/%{compiler} hdf5/%{compilerlong}/intel-mpi/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/intel-mpi/%{version}
%endif

%install
. /etc/profile.d/modules.sh

install_one() {
%{compilerbuildprep}
pushd $1
module load $4 $5 $6
cd netcdf-cxx-%{netcdfversioncxx}
make install DESTDIR=${RPM_BUILD_ROOT}
/bin/rm ${RPM_BUILD_ROOT}$2/share/info/dir
mkdir -p ${RPM_BUILD_ROOT}$2/share/doc
cp -ar examples ${RPM_BUILD_ROOT}$2/share/doc/examples-cxx
cp -ar man4/netcdf-cxx.pdf ${RPM_BUILD_ROOT}$2/share/doc/
cd ..
cd netcdf-cxx4-%{netcdfversioncxx4}
if [ "$3" = "mpi" ]; then
	export CC=mpicc
	export CXX=mpicxx
fi
make install DESTDIR=${RPM_BUILD_ROOT}
cp -ar examples ${RPM_BUILD_ROOT}$2/share/doc/examples-cxx4
cd ..
cd netcdf-fortran-*
export FCFLAGS="$RPM_OPT_FLAGS"
if [ "$3" = "mpi" ]; then
	export F77="mpif90"
	export FC="mpif90"
	export CC="mpicc"
%if "%{compiler}" == "gcc"
	export CPPFLAGS=-DpgiFortran
%endif
fi
make install DESTDIR=${RPM_BUILD_ROOT}
#gzip $RPM_BUILD_ROOT/%{_libdir}/$mpi/share/man/man3/*.3
cd ..
/bin/rm ${RPM_BUILD_ROOT}$2/%{_lib}/*.la
find ${RPM_BUILD_ROOT}$2/share -name \*.3 -exec gzip '{}' \;
popd
}

%if %{with_serial}
install_one serial %{localdir} serial hdf5/%{compiler}/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/%{version}
%endif
%if %{with_openmpi}
install_one openmpi %{localdiropenmpi} mpi openmpi/%{compiler} hdf5/%{compilerlong}/openmpi-%{openmpiversion}/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/openmpi-%{openmpiversion}/%{version}
%endif
%if %{with_mpt}
install_one mpt %{localdirmpt} mpi %{modulempt} hdf5/%{compilerlong}/mpt/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/mpt/%{version}
%endif
%if %{with_impi}
install_one impi %{localdirimpi} mpi intel-mpi/%{compiler} hdf5/%{compilerlong}/intel-mpi/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/intel-mpi/%{version}
%endif

%check
. /etc/profile.d/modules.sh

check_one() {
%{compilerbuildprep}
pushd $1
module load $3 $4 $5
make -C netcdf-cxx-%{netcdfversioncxx} check
make -C netcdf-cxx4-%{netcdfversioncxx4} check
make -C netcdf-fortran-* check
cd ..
popd
}

%if %{with_serial}
check_one serial %{localdir} hdf5/%{compiler}/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/%{version}
%endif
%if %{with_openmpi}
check_one openmpi %{localdiropenmpi} openmpi/%{compiler} hdf5/%{compilerlong}/openmpi-%{openmpiversion}/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/openmpi-%{openmpiversion}/%{version}
%endif
%if %{with_mpt}
#check_one mpt %{localdirmpt} %{modulempt} hdf5/%{compilerlong}/mpt/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/mpt/%{version}
%endif
%if %{with_impi}
perl -pi -e 's|mpiexec|mpirun|' impi/netcdf-fortran-*/nf_test/run*test.sh 
check_one impi %{localdirimpi} intel-mpi/%{compiler} hdf5/%{compilerlong}/intel-mpi/%{hdf5version} netcdf/%{compilerlong}/hdf5-%{hdf5version}/intel-mpi/%{version}
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%if %{with_serial}
%files
%defattr(-,root,root,-)
%doc netcdf-cxx-%{netcdfversioncxx}/COPYRIGHT 
%doc netcdf-cxx-%{netcdfversioncxx}/cxx/README
%{localdir}/%{_lib}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc %{localdir}/share/doc/*
%doc %{localdir}/share/info/*
%doc %{localdir}/share/man/*/*
%{localdir}/bin/*
%{localdir}/include/*
%{localdir}/%{_lib}/*.so
%{localdir}/%{_lib}/pkgconfig/*

%files static
%defattr(-,root,root,-)
%{localdir}/%{_lib}/*.a
%endif

%if %{with_mpich2}
%files mpich2
%defattr(-,root,root,-)
%doc netcdf-cxx-%{netcdfversioncxx}/COPYRIGHT netcdf-cxx-%{netcdfversioncxx}/cxx/README
%{localdir}/%{_lib}/*.so.*

%files mpich2-devel
%defattr(-,root,root,-)
%doc %{localdir}/share/doc/*
%doc %{localdir}/share/info/*
%doc %{localdir}/share/man/*/*
%{localdir}/include/*
%{localdir}/%{_lib}/*.so
%{localdir}/%{_lib}/pkgconfig/*

%files mpich2-static
%defattr(-,root,root,-)
%{_libdir}/mpich2/lib/*.a
%endif

%if %{with_openmpi}
%files openmpi%{openmpinumversion}
%defattr(-,root,root,-)
%doc netcdf-cxx-%{netcdfversioncxx}/COPYRIGHT netcdf-cxx-%{netcdfversioncxx}/cxx/README
%{localdiropenmpi}/%{_lib}/*.so.*

%files openmpi%{openmpinumversion}-devel
%defattr(-,root,root,-)
%doc %{localdiropenmpi}/share/doc/* 
%doc %{localdiropenmpi}/share/info/*
%doc %{localdiropenmpi}/share/man/*/*
%{localdiropenmpi}/bin/*
%{localdiropenmpi}/include/*
%{localdiropenmpi}/%{_lib}/*.so
%{localdiropenmpi}/%{_lib}/pkgconfig/*

%files openmpi%{openmpinumversion}-static
%defattr(-,root,root,-)
%{localdiropenmpi}/%{_lib}/*.a
%endif

%if %{with_mpt}
%files mpt
%defattr(-,root,root,-)
%doc netcdf-cxx-%{netcdfversioncxx}/COPYRIGHT netcdf-cxx-%{netcdfversioncxx}/cxx/README
%{localdirmpt}/%{_lib}/*.so.*

%files mpt-devel
%defattr(-,root,root,-)
%doc %{localdirmpt}/share/doc/*
%doc %{localdirmpt}/share/info/*
%doc %{localdirmpt}/share/man/*/*
%{localdirmpt}/bin/*
%{localdirmpt}/include/*
%{localdirmpt}/%{_lib}/*.so
%{localdirmpt}/%{_lib}/pkgconfig/*

%files mpt-static
%defattr(-,root,root,-)
%{localdirmpt}/%{_lib}/*.a
%endif

%if %{with_impi}
%files impi
%defattr(-,root,root,-)
%doc netcdf-cxx-%{netcdfversioncxx}/COPYRIGHT
%doc netcdf-cxx-%{netcdfversioncxx}/cxx/README
%{localdirimpi}/%{_lib}/*.so.*

%files impi-devel
%defattr(-,root,root,-)
%doc %{localdirimpi}/share/doc/*
%doc %{localdirimpi}/share/info/*
%doc %{localdirimpi}/share/man/*/*
%{localdirimpi}/bin/*
%{localdirimpi}/include/*
%{localdirimpi}/%{_lib}/*.so
%{localdirimpi}/%{_lib}/pkgconfig/*

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
