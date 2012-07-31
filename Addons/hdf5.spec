Name: hdf5
Version: 1.6.10
Release: 1%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD
Group: System Environment/Libraries
URL: http://www.hdfgroup.org/HDF5/
Source0: ftp://ftp.hdfgroup.org/HDF5/current16/src/%{name}-%{version}.tar.gz
Patch2: hdf5-1.6.9-norpath.patch
Patch5: hdf5-1.6.4-ppc.patch
Patch7: hdf5-1.6.5-x86_64.patch
Patch8: hdf5-1.6.5-sort.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: krb5-devel, openssl-devel, zlib-devel, gcc-gfortran, time

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

%description devel
HDF5 development headers and libraries.

%prep
%setup -q
%patch2 -p1 -b .norpath
%patch5 -p1 -b .ppc
%patch7 -p1 -b .x86_64
%patch8 -p1 -b .sort


%build
export CC=gcc
export CXX=g++
export F9X=gfortran
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
%{_docdir}/%{name}/
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.mod


%changelog
* Mon Nov 30 2009 Orion Poplawski <orion@cora.nwra.com> 1.6.10-1
- Update to 1.6.10
- Drop destdir patch fixed upstream

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
