
%define ver 1.4.0
%define beta a

Name:	 OpenEXR
Version: %{ver}%{?beta} 
Release: 3%{?dist}
Summary: A high dynamic-range (HDR) image file format

Group:	 System Environment/Libraries
License: BSD
URL:	 http://www.openexr.com/
Source0: http://download.savannah.nongnu.org/releases/openexr/openexr-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# FIXME: IlmThread contains undefined references to stuff in -lpthread
Patch1: openexr-1.4.0-no_undefined.patch
# Use Libs.private
Patch2: openexr-1.4.0-pkgconfig.patch

BuildRequires:  fltk-devel >= 1.1
BuildRequires:  zlib-devel
BuildRequires:  automake libtool

%description
OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial
Light & Magic for use in computer imaging applications. This package contains
libraries and sample applications for handling the format.

%package devel
Summary: Headers and libraries for building apps that use OpenEXR
Group:	 Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel
This package contains headers and libraries required to build applications that
use the OpenEXR format.


%prep
%setup -q -n openexr-%{ver}

%patch1 -p1 -b .no_undefined
%patch2 -p1 -b .pkgconfig

# for patch1
./bootstrap


%build
%configure --disable-static

make %{?_smp_mflags}


%check
# Not enabled, by default, takes a *very* long time. -- Rex
%{?_with_check:make check}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{ver}
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la

# prepare docs
mkdir -p rpmdocs
cp -a IlmImfExamples rpmdocs/examples
rm -rf rpmdocs/examples/.deps

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE NEWS README
%{_bindir}/*
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%doc rpmdocs/examples 
%{_datadir}/aclocal/*
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*


%changelog
* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-3
- pkgconfig patch to use Libs.private

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-2
- -devel: +Requires: pkgconfig

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.4.0a-1
- openexr-1.4.0a

* Sat Feb 18 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-7
- Further zlib fixes (#165729)

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-6
- Rebuild for Fedora Extras 5

* Wed Aug 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-5
- Remove *.a from %%files devel

* Tue Aug 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-4
- Removed -devel dep on zlib-devel (#165729)
- Added --disable-static to %%configure
- Fixed build with GCC 4.0.1
- Added .so links to -devel

* Wed May 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-3
- Add zlib-devel to BR
- Delete all .la files (#157652)

* Mon May  9 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Add disttag

* Sun May  8 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-2
- Fix BuildRequires
- Fix Requires on -devel
- Add %%post[un] scriptlets
- Fix ownership in -devel
- Don't have .deps files in %%doc

* Wed Mar 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.2-1
- Initial RPM release
