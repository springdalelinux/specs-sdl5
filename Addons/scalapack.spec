Summary: A subset of LAPACK routines redesigned for heterogenous computing
Name: scalapack
Version: 1.7.5
Release: 1%{?dist}
# This is freely distributable without any restrictions.
License: Public Domain
Group: Development/Libraries
URL: http://www.netlib.org/lapack-dev/
Source0: http://www.netlib.org/scalapack/scalapack-%{version}.tgz
BuildRequires: lapack-devel, blas-devel, lam-devel, blacs-devel
BuildRequires: gcc-gfortran, glibc-devel
Requires: lapack, blas-devel, lam, blacs-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: scalapack-1.7-fedora.patch
Patch1: scalapack-1.7-64bitlibs.patch

%description
The ScaLAPACK (or Scalable LAPACK) library includes a subset 
of LAPACK routines redesigned for distributed memory MIMD 
parallel computers. It is currently written in a 
Single-Program-Multiple-Data style using explicit message 
passing for interprocessor communication. It assumes 
matrices are laid out in a two-dimensional block cyclic 
decomposition.

ScaLAPACK is designed for heterogeneous computing and is 
portable on any computer that supports MPI or PVM.

Like LAPACK, the ScaLAPACK routines are based on 
block-partitioned algorithms in order to minimize the frequency 
of data movement between different levels of the memory hierarchy. 
(For such machines, the memory hierarchy includes the off-processor 
memory of other processors, in addition to the hierarchy of registers, 
cache, and local memory on each processor.) The fundamental building 
blocks of the ScaLAPACK library are distributed memory versions (PBLAS) 
of the Level 1, 2 and 3 BLAS, and a set of Basic Linear Algebra 
Communication Subprograms (BLACS) for communication tasks that arise 
frequently in parallel linear algebra computations. In the ScaLAPACK 
routines, all interprocessor communication occurs within the PBLAS and the 
BLACS. One of the design goals of ScaLAPACK was to have the ScaLAPACK 
routines resemble their LAPACK equivalents as much as possible. 

%package devel
Summary: Development libraries for scalapack
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development libraries for scalapack.

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1
%ifarch x86_64 ppc64 sparc64 ia64
%patch1 -p1 -b .64
%endif

%build
cd %{name}-%{version}
make lib
make exe

%install
rm -fr ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

cd %{name}-%{version}
cp -f INSTALL/scalapack_install.ps ../
cp -f README ../
cp -f libscalapack.a ${RPM_BUILD_ROOT}%{_libdir}
cp -f libscalapack.so* ${RPM_BUILD_ROOT}%{_libdir}
cp -f TESTING/x* ${RPM_BUILD_ROOT}%{_bindir}

cd ${RPM_BUILD_ROOT}%{_libdir}
ln -fs libscalapack.so.1.0.0 libscalapack.so.1
ln -s libscalapack.so.1.0.0 libscalapack.so
cd ..

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -fr ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc scalapack_install.ps README
%{_bindir}/x*
%{_libdir}/libscalapack.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libscalapack.a
%{_libdir}/libscalapack.so

%changelog
* Thu Jan 18 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.5-1
- bump to 1.7.5

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-4
- I said "BR" not "R". Stupid packager.

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-3
- fix BR: lam-devel

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-2
- fix 64bit patch

* Fri Sep 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7.4-1
- bump to 1.7.4

* Wed Mar  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-13
- lam moved into _libdir/lam... need to fix patches

* Wed Mar  8 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-12
- set -fPIC as NOOPT

* Sun Feb 26 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-11
- fix 64 bit builds
- enable shared libraries
- split package into base and devel

* Tue Feb 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-10
- Incorporate Andrew Gormanly's fixes

* Mon Jan  9 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-9
- fix BR

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-8
- rebuild for gcc4.1

* Sun May 15 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-7
- 64 bit library fix

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-6
- remove hardcoded dist tags

* Sun May  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-4
- fix broken patch for fc-3 branch

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-3
- use dist tag
- fix fc3 BuildRequires

* Tue Apr 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-2
- fix buildroot
- add gcc-gfortran to BuildRequires (gcc-g77 for fc3)

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.7-1
- initial package creation
