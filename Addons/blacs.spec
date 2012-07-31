Summary: Basic Linear Algebra Communication Subprograms
Name: blacs
Version: 1.1
Release: 24%{?dist}.1
License: Freely distributable
Group: Development/Libraries
URL: http://www.netlib.org/blacs
Source0: http://www.netlib.org/blacs/mpiblacs.tgz
Source1: http://www.netlib.org/blacs/blacstester.tgz
Source2: Bmake.inc
Source3: http://www.netlib.org/blacs/mpi_prop.ps
Source4: http://www.netlib.org/blacs/blacs_install.ps
Source5: http://www.netlib.org/blacs/mpiblacs_issues.ps
Source6: http://www.netlib.org/blacs/f77blacsqref.ps
Source7: http://www.netlib.org/blacs/cblacsqref.ps
Source8: http://www.netlib.org/blacs/lawn94.ps
Source9: Bmake.inc.64bit
BuildRequires: gcc-gfortran
# Lam before 7.1.1-5 is missing:
# -shared library support
# -fPIC compilation flag
BuildRequires: lapack, blas, lam-devel >= 2:7.1.1-5
Requires: lapack, blas, lam >= 2:7.1.1-5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: blacs-shared.patch

%description
The BLACS (Basic Linear Algebra Communication Subprograms) project is 
an ongoing investigation whose purpose is to create a linear algebra 
oriented message passing interface that may be implemented efficiently 
and uniformly across a large range of distributed memory platforms.

The length of time required to implement efficient distributed memory 
algorithms makes it impractical to rewrite programs for every new 
parallel machine. The BLACS exist in order to make linear algebra 
applications both easier to program and more portable. 

%package devel
Summary: Development libraries for blacs
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains development libraries for blacs.

%prep
%setup -q -c -n %{name}
%setup -q -D -T -a 1 -n %{name}
%patch0 -p1
cd BLACS/
%ifarch ppc64 sparc64 x86_64 ia64
cp -f %{SOURCE9} ./Bmake.inc
%else
cp -f %{SOURCE2} .
%endif

%build
cd BLACS/
CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fstack-protector//g'`
RPM_OPT_FLAGS=`echo $CFLAGS`
make mpi

cd TESTING/
make
cd ../..

cp %{SOURCE3} mpi_prop.ps
cp %{SOURCE4} blacs_install.ps
cp %{SOURCE5} mpiblacs_issues.ps
cp %{SOURCE6} f77blacsqref.ps
cp %{SOURCE7} cblacsqref.ps
cp %{SOURCE8} lawn94.ps

%install
rm -fr ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

cd BLACS/LIB
for f in *.a *.so*; do
  cp -f $f ${RPM_BUILD_ROOT}%{_libdir}/$f
done
cd ../TESTING/EXE
cp -f x*test_MPI-LINUX-0 ${RPM_BUILD_ROOT}%{_bindir}

cd ${RPM_BUILD_ROOT}%{_libdir}
for i in libmpiblacs libmpiblacsF77init libmpiblacsCinit; do
  ln -fs $i.so.1.0.0 $i.so.1
  ln -s $i.so.1.0.0 $i.so
done
cd ..

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -fr ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,0755)
%doc mpi_prop.ps blacs_install.ps mpiblacs_issues.ps f77blacsqref.ps cblacsqref.ps lawn94.ps
%{_bindir}/x*test_MPI-LINUX-0
%{_libdir}/libmpiblacs*.so.*

%files devel
%defattr(-,root,root,0755)
%{_libdir}/libmpiblacs*.a
%{_libdir}/libmpiblacs*.so

%changelog
* Wed Dec 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-24.1
- updated bmake files to include new lam-devel header path

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-24
- FC-5+ needs lam-devel as a BR

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-23
- bump for FC-6

* Fri Apr  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-22
- FC-5+ also needs -L libdir/lam

* Fri Apr  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-21
- FC-5+ needs includedir/lam

* Fri Apr  7 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-20
- fix lam BR

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-19
- fix broken bits in shared lib (no -fstack-protector for us)

* Mon Dec 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-18
- rebuild for gcc4.1

* Sun Jul 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-17
- fix g77 for FC-3 spec

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-16
- remove ppc hack

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-15
- Fix typo in fix. :/

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-12
- fix INTFACE for FC-4+

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-11
- bump for new tag

* Mon Jun 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-10
- split static lib and .so into -devel package
- fix Bmake files for shared library support
- build shared libraries

* Tue May 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-8
- g77 needs some special compile flags, edited Bmake.inc*

* Mon May  9 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-7
- remove hardcoded dist tags

* Thu May  5 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-6
- fix 64bit issues

* Sun Apr 24 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-5
- use dist tag
- fix fc3 package sources and dependencies

* Tue Apr 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-4
- fix buildroot
- add gcc-gfortran as a BuildRequires (gcc-g77)

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-3
- backout shared patch

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-2
- rename libs to what scalapack thinks they should be called

* Mon Apr 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.1-1
- initial package creation
