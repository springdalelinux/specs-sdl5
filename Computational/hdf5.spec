
# The name of the modules RPM.  Can vary from system to system.
# type: string (name of modules RPM)
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}
# 32 or 64?
%ifarch %{ix86}
%define modulebits 32
%else
%define modulebits 64
%endif

# compiler for which we are doing this
%define compiler intel101

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
# and this is a list of conflicting modules
%define compilerconflictmodule mpich/ mpich2/ lam/ intel/ pgi/
%define compilermodulefile %{nil}
%endif
#
# Intel 9.1 compiler
%if "%{compiler}" == "intel91"
%define compilershort intel
%define compilershortversion intel-9
%if "%{?rhel}" == "4"
%define compilerruntimesection BuildRequires: intel-compiler91-default-modules\
Requires: intel-compiler91-default-modules
%else
%define compilerruntimesection BuildRequires: intel-compiler91-%{modulebits}-default-modules\
Requires: intel-compiler91-%{modulebits}-default-modules
%endif
%define compilerdevelsection %{nil}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort F9X=ifort; . /etc/profile.d/modules.sh; module load intel
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-9.1
%define compilerloadmodule module load intel/9.1/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ pgi/
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
Requires: intel-compiler%{intelmajor}-%{modulebits}-default-modules >= %{intelversion}
%define compilerdevelsection %{nil}
%define localdir /usr/local/intel
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=icc CXX=icpc F77=ifort F9X=ifort; . /etc/profile.d/modules.sh; module load intel
%define cflags -O2 -g -pipe -Wall
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename intel-%{intelversion}
%define compilerloadmodule module load intel/%{intelmajor}/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ pgi/
%define compilermodulefile .modulerc-intel-%{modulebits}-%{intelversionnum}-%{version}
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
%define compilerruntimesection BuildRequires: pgi-workstation >= %{pgiversion}\
Requires: pgi-workstation-libs >= %{pgiversion}
%define compilerdevelsection Requires: pgi-workstation >= %{pgiversion}
%define localdir /usr/local/pgi
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pgcc CXX=pgCC F77=pgf77 F9X=pgf90; . /etc/profile.d/modules.sh; module load pgi
%define cflags -fast
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pgi-%{pgiversion}
%define compilerloadmodule module load pgi/%{pgimajor}/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ intel/
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
Requires: pathscale-compilers-libs >= %{pathscaleversion}
%define compilerdevelsection Requires: pathscale-compilers >= %{pathscaleversion}
%define localdir /usr/local/pathscale
# for intel we need to just specify our compilers
%define compilerbuildprep export CC=pathcc CXX=pathCC F77=pathf90 F9X=pathf90; . /etc/profile.d/modules.sh; module load pathscale
%define cflags -O3
%define cxxflags %{cflags}
%define f77flags %{cflags}
%define fcflags  %{cflags}
# no special ldflags here
%define compilerldflags %{nil}
# this is for configuring modules
%define compilermodulename pathscale-%{pathscaleversion}
%define compilerloadmodule module load pathscale/%{pathscaleversion}/%{modulebits}
%define compilerconflictmodule mpich/ mpich2/ lam/ intel/
%define compilermodulefile .modulerc-pathscale-%{modulebits}-%{pathscaleversionnum}-%{version}
%endif

%define _prefix %{localdir}
%define _mandir %{localdir}/share/man
%define _docdir %{localdir}/share/doc

Name: hdf5-%{compilershort}
Version: 1.6.9
Release: 2%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD
Group: System Environment/Libraries
URL: http://www.hdfgroup.org/HDF5/
Source0: ftp://ftp.hdfgroup.org/HDF5/current16/src/hdf5-%{version}.tar.gz
Patch1: hdf5-1.6.9-destdir.patch
Patch2: hdf5-1.6.9-norpath.patch
Patch5: hdf5-1.6.4-ppc.patch
Patch7: hdf5-1.6.5-x86_64.patch
Patch8: hdf5-1.6.5-sort.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: krb5-devel, openssl-devel, zlib-devel, time
%{compilerruntimesection}

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is 
essentially a multidimensional array of data elements, and a group is a 
structure for organizing objects in an HDF5 file. Using these two basic 
objects, one can create and store almost any kind of scientific data 
structure, such as images, arrays of vectors, and structured and unstructured 
grids. You can also mix and match them in HDF5 files according to your needs.

%package devel
Summary: HDF5 development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
%{compilerdevelsection}

%description devel
HDF5 development headers and libraries.

%prep
%setup -q -n hdf5-%{version}
%patch1 -p1 -b .destdir
%patch2 -p1 -b .norpath
%patch5 -p1 -b .ppc
%patch7 -p1 -b .x86_64
%patch8 -p1 -b .sort


%build
#export CC=gcc
#export CXX=g++
#export F9X=gfortran
%{compilerbuildprep}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS}"
CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS}"
F77FLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FFLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FCFLAGS="%{?fcflags:%{fcflags}}%{!?fcflags:$RPM_OPT_FLAGS}"
%configure --with-ssl --enable-cxx --enable-fortran \
           --enable-threadsafe --with-pthread
make


%install
rm -rf $RPM_BUILD_ROOT
find doc/html -type f | xargs chmod -x
%makeinstall docdir=${RPM_BUILD_ROOT}%{_docdir}
find doc/html -name Dependencies -o -name Makefile\* | xargs rm
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/*.settings
rm $RPM_BUILD_ROOT%{_bindir}/h5perf


%check
%{compilerbuildprep}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS}"
CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS}"
F77FLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FFLAGS="%{?f77flags:%{f77flags}}%{!?f77flags:$RPM_OPT_FLAGS}"
FCFLAGS="%{?fcflags:%{fcflags}}%{!?fcflags:$RPM_OPT_FLAGS}"
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING MANIFEST README.txt release_docs/RELEASE.txt
%doc release_docs/HISTORY.txt doc/html
%{_bindir}/gif2h5
%{_bindir}/h52gif
%{_bindir}/h5debug
%{_bindir}/h5diff
%{_bindir}/h5dump
%{_bindir}/h5import
%{_bindir}/h5jam
%{_bindir}/h5ls
%{_bindir}/h5repack
%{_bindir}/h5repart
%{_bindir}/h5unjam
%attr(0755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/h5c++
%{_bindir}/h5cc
%{_bindir}/h5fc
%{_bindir}/h5redeploy
%{_docdir}/hdf5/
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.mod


%changelog
* Wed Jun 3 2009 Orion Poplawski <orion@cora.nwra.com> 1.6.9-2
- No, don't ship h5perf

* Tue Jun 2 2009 Orion Poplawski <orion@cora.nwra.com> 1.6.9-1
- Update to 1.6.9
- Update destdir and norpath patches
- Drop open patch fixed upstream
- Ship h5perf

* Sat Nov 15 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.8-1
- Update to 1.6.8

* Wed May 28 2008 Orion Poplawski <orion@cora.nwra.com> 1.6.7-1
- Update to 1.6.7

* Wed Oct 17 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.6-1
- Update to 1.6.6, drop upstreamed patches
- Explicitly set compilers

* Fri Aug 24 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-9
- Update license tag to BSD
- Rebuild for BuildID

* Wed Aug  8 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-8
- Fix memset typo
- Pass mode to open with O_CREAT

* Mon Feb 12 2007 Orion Poplawski <orion@cora.nwra.com> 1.6.5-7
- New project URL
- Add patch to use POSIX sort key option
- Remove useless and multilib conflicting Makefiles from html docs
  (bug #228365)
- Make hdf5-devel own %{_docdir}/%{name}

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-6
- Rebuild for FC6

* Wed Mar 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-5
- Change rpath patch to not need autoconf
- Add patch for libtool on x86_64
- Fix shared lib permissions

* Mon Mar 13 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-4
- Add patch to avoid HDF setting the compiler flags

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 1.6.5-3
- Rebuild for gcc/glibc changes

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.5-2
- Don't ship h5perf with missing library

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.5-1
- Update to 1.6.5

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-9
- Rebuild

* Wed Nov 30 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-8
- Package fortran files properly
- Move compiler wrappers to devel

* Fri Nov 18 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-7
- Add patch for fortran compilation on ppc

* Wed Nov 16 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-6
- Bump for new openssl

* Tue Sep 20 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-5
- Enable fortran since the gcc bug is now fixed

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-4
- Make example scripts executable

* Wed Jul 01 2005 Orion Poplawski <orion@cora.nwra.com> 1.6.4-3
- Add --enable-threads --with-pthreads to configure
- Add %check
- Add some %docs
- Use %makeinstall
- Add patch to fix test for h5repack
- Add patch to fix h5diff_attr.c

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-2
- remove szip from spec, since szip license doesn't meet Fedora standards

* Sun Apr 3 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.4-1
- inital package for Fedora Extras
