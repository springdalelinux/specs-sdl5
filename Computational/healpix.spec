# EPEL hack
%global _fmoddir %{_libdir}/gfortran/modules

Name:           healpix
Version:        2.13a
Release:        1%{?dist}
Summary:        Hierarchical Equal Area isoLatitude Pixelization of a sphere

Group:          Development/Libraries
License:        GPLv2+
URL:            http://healpix.jpl.nasa.gov/
Source0:        http://downloads.sourceforge.net/project/healpix/Healpix_%{version}/Healpix_%{version}_2009Nov27.tar.gz
Source1:        healpix-f90test.sh
Patch0:         healpix-2.12a-shlib.patch
Patch1:         healpix-2.11c-gcc44.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cfitsio-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran

%description
HEALPix is an acronym for Hierarchical Equal Area isoLatitude Pixelization
of a sphere. As suggested in the name, this pixelization produces a
subdivision of a spherical surface in which each pixel covers the same
surface area as every other pixel.

This package contains Fortran binaries and libraries.

NB. Due to some generic names, the binaries have been renamed to start with
hp_, e.g. anafast is now hp_anafast.


%package devel
Summary:        Healpix Fortran headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:	gcc-gfortran

%description devel
This package contains the Fortran module files needed to compile against
the HEALPix Fortran libraries.


%package c++
Summary:        Healpix C++ binaries and libraries
Group:          System Environment/Libraries

%description c++
HEALPix is an acronym for Hierarchical Equal Area isoLatitude Pixelization
of a sphere. As suggested in the name, this pixelization produces a
subdivision of a spherical surface in which each pixel covers the same
surface area as every other pixel.

This package contains HEALPix binaries and libraries that are written in C++.

NB. Due to some generic names, the binaries have been renamed to start with
hp_, e.g. anafast is now hp_anafast.


%package c++-devel
Summary:        Healpix C++ headers
Group:          System Environment/Libraries
Requires:       %{name}-c++ = %{version}-%{release}

%description c++-devel
HEALPix is an acronym for Hierarchical Equal Area isoLatitude Pixelization
of a sphere. As suggested in the name, this pixelization produces a
subdivision of a spherical surface in which each pixel covers the same
surface area as every other pixel.

This package contains development headers for the C++ part of HEALPix.


%package -n c%{name}
Summary:        HEALPix C Bindings Library
Group:          System Environment/Libraries

%description -n c%{name}
HEALPix is an acronym for Hierarchical Equal Area isoLatitude Pixelization
of a sphere. As suggested in the name, this pixelization produces a
subdivision of a spherical surface in which each pixel covers the same
surface area as every other pixel.

This package contains the library for tools that use HEALPix C bindings.


%package -n c%{name}-devel
Summary:        HEALPix C Bindings Library development files
Group:          Development/Libraries
Requires:       c%{name} = %{version}-%{release}

%description -n c%{name}-devel
HEALPix is an acronym for Hierarchical Equal Area isoLatitude Pixelization
of a sphere. As suggested in the name, this pixelization produces a
subdivision of a spherical surface in which each pixel covers the same
surface area as every other pixel.

This package contains the C include file for development with HEALPix.


%prep
%setup -q -n Healpix_%{version}
%patch0 -p1 -b .shlib
%patch1 -p1 -b .gcc44

# Fortran tests:
rm test/README
install -p -m 755 %{SOURCE1} runtest.sh

# Remove patch backup from doc
rm -f src/cxx/test/*.shlib

%build
# Generic stuff
export CC="gcc"
export CXX="g++"
export CXXL="g++"
export FC="gfortran"


### C bindings
export CFITSIO_LIBDIR="%{_libdir}"

make %{?_smp_mflags} -C src/C/subs PIC="-fPIC" OPT="%{optflags}" \
        CFITSIO_INCDIR=%{_includedir}/cfitsio shared

make %{?_smp_mflags} -C src/C/subs PIC="-fPIC" OPT="%{optflags} " \
        CFITSIO_INCDIR=%{_includedir}/cfitsio test_chealpix2

make %{?_smp_mflags} -C src/C/subs PIC="-fPIC" OPT="%{optflags}" \
        CFITSIO_INCDIR=%{_includedir}/cfitsio test_cio


### C++ bindings

# directories
export DESTBIN=$PWD/cxxbin
export DESTINC=$PWD/cxxinc
export DESTLIB=$PWD/cxxlib
export DESTDOC=$PWD/cxxdoc
mkdir -p $DESTBIN $DESTINC $DESTLIB $DESTDOC

export INCDIR="%{_includedir}/cfitsio"
export LIBDIR=$DESTLIB

# Make nonsense
export TEMP1="."
export PARAMFILE=$PWD/src/cxx/config/rules.common

# Compiler flags
export CCFLAGS_NO_C="%{optflags} -I%{_includedir}/cfitsio -I$PWD/src/cxx/cxxsupport -fPIC -I${DESTINC} -fopenmp" 
export CCFLAGS="$CCFLAGS_NO_C -c"
export CXXFLAGS="$CCFLAGS"
export CXXFLAGS_NO_C="$CCFLAGS_NO_C"
export CXXCFLAGS="$CCFLAGS"
export CXXLFLAGS="%{optflags} -L. -L$DESTLIB"
export CXX_EXTRALIBS="-lcfitsio -lhealpix_cxx -lhealpix_cxxsupport -lhealpix_fft --as-needed"

# SMP make doesn't work
for dir in cxxsupport libfftpack Healpix_cxx alice docsrc; do
        make -C src/cxx/$dir -f planck.make SRCROOT=$PWD/src/cxx/$dir
done


### F90 bindings

# Make nonsense
export MOD=mod
export OS=Linux

# Directories for the created include, library and binary files
export BINDIR=$PWD/f90bin
export INCDIR=$PWD/f90inc
export LIBDIR=$PWD/f90lib
mkdir -p $INCDIR $LIBDIR $BINDIR

# Compiler stuff
export CFLAGS="%{optflags} -fPIC"
export FFLAGS="%{optflags} -fPIC -DGFORTRAN -I$INCDIR -ffree-line-length-none"

# SMP make doesn't work
make -C src/f90/mod 
make -C src/f90/lib
for dir in anafast map2gif hotspot smoothing synfast ud_grade plmgen \
        alteralm median_filter ngsims_full_sky
do
        make -C src/f90/$dir
done

# Rename binaries
cd f90bin
for exec in *; do
        mv $exec hp_$exec
done
cd ..

cd cxxbin
mv median_filter median_filter_cxx # Binary with same name exists in Fortran
for exec in *; do
        mv $exec hp_$exec
done
cd ..

%install
rm -rf $RPM_BUILD_ROOT

# Directory structure
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}/healpix

# C bindings
make install -C src/C/subs LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
        INCDIR=$RPM_BUILD_ROOT%{_includedir}

# C test binaries
install -p -m 0755 src/C/subs/test_chealpix2 $RPM_BUILD_ROOT%{_bindir}
install -p -m 0755 src/C/subs/test_cio $RPM_BUILD_ROOT%{_bindir}

# C++ stuff
install -p cxxbin/* $RPM_BUILD_ROOT%{_bindir}
install -p cxxlib/* $RPM_BUILD_ROOT%{_libdir}
install -pm 0644 cxxinc/* $RPM_BUILD_ROOT%{_includedir}/healpix

# Fortran stuff
install -p f90bin/* $RPM_BUILD_ROOT%{_bindir}
install -p f90lib/* $RPM_BUILD_ROOT%{_libdir}
# Modules contain API/ABI and thus architecture dependent
mkdir -p $RPM_BUILD_ROOT%{_fmoddir}/healpix
install -pm 0644 f90inc/* $RPM_BUILD_ROOT%{_fmoddir}/healpix


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%post c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig


%post -n c%{name} -p /sbin/ldconfig
%postun -n c%{name} -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING READ_Copyrights_Licenses.txt test
%{_bindir}/hp_alteralm
%{_bindir}/hp_anafast
%{_bindir}/hp_hotspot
%{_bindir}/hp_map2gif
%{_bindir}/hp_median_filter
%{_bindir}/hp_plmgen
%{_bindir}/hp_sky_ng_sim
%{_bindir}/hp_sky_ng_sim_bin
%{_bindir}/hp_smoothing
%{_bindir}/hp_synfast
%{_bindir}/hp_ud_grade
%{_libdir}/libhealpix.so
%{_libdir}/libhpxgif.so


%files devel
%defattr(-,root,root,-)
%{_fmoddir}/healpix/


%files c++
%defattr(-,root,root,-)
%doc COPYING READ_Copyrights_Licenses.txt
%{_bindir}/hp_alice2
%{_bindir}/hp_alice_test
%{_bindir}/hp_alm2map_cxx
%{_bindir}/hp_anafast_cxx
%{_bindir}/hp_calc_powspec
%{_bindir}/hp_generateTexture
%{_bindir}/hp_hotspots_cxx
%{_bindir}/hp_hpxtest
%{_bindir}/hp_map2tga
%{_bindir}/hp_median_filter_cxx
%{_bindir}/hp_mult_alm
%{_bindir}/hp_rotalm_cxx
%{_bindir}/hp_smoothing_cxx
%{_bindir}/hp_syn_alm_cxx
%{_bindir}/hp_testMollweideSkyMap
%{_bindir}/hp_testOrthogonalSkyMap
%{_bindir}/hp_testSoSSkyMap
%{_bindir}/hp_udgrade_cxx
%{_libdir}/libhealpix_cxx.so
%{_libdir}/libhealpix_cxxsupport.so
%{_libdir}/libhealpix_fft.so


%files c++-devel
%defattr(-,root,root,-)
%doc src/cxx/test
%dir %{_includedir}/healpix
%{_includedir}/healpix/*.h


%files -n chealpix
%defattr(-,root,root,-)
%doc COPYING READ_Copyrights_Licenses.txt
%{_libdir}/libchealpix.so


%files -n chealpix-devel
%defattr(-,root,root,-)
%{_bindir}/test_chealpix2
%{_bindir}/test_cio
%{_includedir}/chealpix.h


%changelog
* Sun Dec 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.13a-1
- Update to upstream 2.13a.

* Tue Sep 22 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.12a-1
- Update to upstream 2.12a.

* Mon Jul 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.11c-7
- Move modules to %%{_fmoddir}.
- Add missing documentation to -c++ package.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11c-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 04 2009 Lubomir Rintel (Fedora Astronomy) <lkundrak@v3.sk> - 2.11c-5
- Minor style adjustments
- Don't override sane gcc flags
- Moved tests to -devel packages
- C++ -devel doesn't depend on fortran ones anymore
- mkdir with -p to allow short-circuit builds
- Fix build with GCC 4.4

* Sat Apr 04 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.11c-4
- Review fixes.
- Add C++ bindings, rename C++ and Fortran binaries (general names!).

* Fri Apr 03 2009 Lubomir Rintel (Fedora Astronomy) <lkundrak@v3.sk> - 2.11c-3
- Build Fortran library as DSO

* Thu Mar 26 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.11c-2
- Add Fortran bindings.

* Wed Mar 25 2009 Lubomir Rintel (Fedora Astronomy) <lkundrak@v3.sk> - 2.11c-1
- Initial packaging of the C bindings
