Name:           cfitsio
Version:        3.040
Release:        3%{?dist}
Summary:        Library for manipulating FITS data files

Group:          Development/Libraries
License:        GPLv2+
URL:            http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
Source0:        ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3040.tar.gz
Patch:          cfitsio.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     gcc-gfortran
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing 
data files in FITS (Flexible Image Transport System) data format. CFITSIO 
simplifies the task of writing software that deals with FITS files by 
providing an easy to use set of high-level routines that insulate the 
programmer from the internal complexities of the FITS file format. At the 
same time, CFITSIO provides many advanced features that have made it the 
most widely used FITS file programming interface in the astronomical 
community.

%package devel
Group:  Development/Libraries
Summary: Headers required when building programs against cfitsio
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Headers required when building a program against the cfitsio library.

%prep
%setup -q -n cfitsio
%patch -p1

%build
FC=f95
export FC
export CC=gcc # fixes -O*, -g
%configure
make shared %{?_smp_mflags}
unset FC

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/%{name}
make LIBDIR=%{_lib} INCLUDEDIR=include/%{name} CFITSIO_LIB=%{buildroot}%{_libdir} \
     CFITSIO_INCLUDE=%{buildroot}%{_includedir}/%{name} install
pushd %{buildroot}%{_libdir}
ln -s libcfitsio.so.0 libcfitsio.so
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README License.txt changes.txt fitsio.doc fitsio.ps cfitsio.doc cfitsio.ps
%{_libdir}/libcfitsio.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/libcfitsio.a
%{_libdir}/libcfitsio.so
%{_libdir}/pkgconfig/cfitsio.pc

%changelog
* Tue Aug 21 2007 Matthew Truch <matt at truch.net> - 3.040-3
- Bump release for rebuild (build-id etc.)

* Thu Aug 2 2007 Matthew Truch <matt at truch.net> - 3.040-2
- Update License tag

* Mon Jul 9 2007 Matthew Truch <matt at truch.net> - 3.040-1
- Upgrade to version 3.040 of cfitsio.

* Fri Feb 16 2007 Matthew Truch <matt at truch.net> - 3.030-2
- Require pkgconfig for -devel.
- export CC=gcc so we don't clobber $RPM_OPT_FLAGS, thereby 
  ruining any -debuginfo packages.  
  See RedHat Bugzilla 229041.

* Fri Jan 5 2007 Matthew Truch <matt at truch.net> - 3.030-1
- Upgrade to version 3.020 of cfitsio.

* Fri Dec 8 2006 Matthew Truch <matt at truch.net> - 3.020-3
- Commit correct patch to configure and Makefiles.

* Fri Dec 8 2006 Matthew Truch <matt at truch.net> - 3.020-2
- Modify spec file to install to correct directories.
- Package cfitsio.pc file in -devel package.

* Wed Dec 6 2006 Matthew Truch <matt at truch.net> - 3.020-1
- Upgrade to revision 3.020 of cfitsio.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 3.006-6
- Bump release for rebuild in prep. for FC6.

* Thu Mar 30 2006 Matthew Truch <matt at truch.net> - 3.006-5
- Include defattr() for devel package as well - bug 187366

* Sun Mar 19 2006 Matthew Truch <matt at truch.net> - 3.006-4
- Don't use macro {buildroot} in build, only in install as per 
  appended comments to Bugzilla bug 172042
  
* Fri Mar 10 2006 Matthew Truch <matt at truch.net> - 3.006-3
- Point to f95 instead of g95 as per bugzilla bug 185107

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.006-2
- Fix spelling typo in name of License.txt file.

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.006-1
- Use new 3.006 fully official stable (non-beta) upstream package.

* Tue Feb 28 2006 Matthew Truch <matt at truch.net> - 3.005-0.2.beta
- Bump release for FC5 extras rebuild.

* Fri Dec 23 2005 Matthew Truch <matt at truch.net> - 3.005-0.1.beta
- Update to 3.005beta release.

* Mon Nov 14 2005 Matthew Truch <matt at truch.net> - 3.004-0.12.b
- Put in proper URL and Source addresses.
- Sync up spec files.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.11.b
- Clean up unused code in spec file.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.10.b
- Set environment variables correctly.
- Include patch so Makefile will put things where they belong.

* Sun Nov 13 2005 Matthew Truch <matt at truch.net> - 3.004-0.9.b
- Set libdir and includedir correctly for build process.

* Sat Nov 12 2005 Matthew Truch <matt at truch.net> - 3.004-0.8.b
- unset FC once we are done with the build

* Sat Nov 12 2005 Ed Hill <ed@eh3.com> - 3.004-0.7.b
- shared libs and small cleanups

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.6.b
- Own include directory created by the devel package.

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.5.b
- Shorten summary.
- Improve specfile post and postun syntax.
- Install headers in cfitsio include subdir.
- Include more documentation provided in tarball.

* Sun Nov 06 2005 Matthew Truch <matt at truch.net> - 3.004-0.4.b
- Require cfitsio for cfitsio-devel

* Sat Nov 05 2005 Matthew Truch <matt at truch.net> - 3.004-0.3.b
- Use proper virgin tarball from upstream.

* Sun Oct 30 2005 Matthew Truch <matt at truch.net> - 3.004-0.2.b
- Include gcc-gfortran build requirment and make sure it gets used.
- Use macros instead of hard coded paths.
- Include home page in description

* Sat Oct 29 2005 Matthew Truch <matt at truch.net> - 3.004-0.1.b
- Initial spec file for Fedora Extras.

