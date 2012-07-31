%define __python /usr/bin/python26

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define pyver %(%{__python} -c 'import sys ; print sys.version[:3]')

Summary: Python bindings for the cairo library
Name: pycairo26
Version: 1.2.0 
Release: 1.1 
License: LGPL
Group: Development/Languages
URL: http://cairographics.org/
Source0: pycairo-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python26
BuildRequires: cairo-devel 
BuildRequires: python26-devel
BuildRequires: pkgconfig
Requires: cairo >= 1.1.10
%description
Python bindings for the cairo library

%package devel
Summary: Libraries and headers for pycairo
Group: Development/Libraries
Requires: %name = %{version}-%{release}
Requires: cairo-devel python26-devel

%description devel

Headers for pycairo 

%prep
%setup -q -n pycairo-%{version}
export PYTHON=%{__python}
%configure

%build
export PYTHON=%{__python}
make

%install
rm -rf $RPM_BUILD_ROOT

export PYTHON=%{__python}
%makeinstall
find $RPM_BUILD_ROOT -name '*.la' |xargs rm 

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_libdir}/python%{pyver}/site-packages/cairo/

%files devel
%defattr(-,root,root,-)

%{_libdir}/pkgconfig/pycairo.pc
%dir %{_includedir}/pycairo
%{_includedir}/pycairo/pycairo.h

%changelog
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.1
- rebuild

* Wed Jul 05 2006 John (J5) Palmieri <johnp@redhat.com> - 1.2.0-1
- Update to upstream 1.2.0

* Mon Jul  3 2006 Jeremy Katz <katzj@redhat.com> - 1.0.2-3
- require new enough cairo (#197457)

* Mon Jun 05 2006 John (J5) Palmieri <johnp@redhat.com> - 1.0.2-2
- add pkgconfig BR

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct 26 2005 John (J5) Palmieri <johnp@redhat.com> - 1.0.2-1
- Updated to latest and push into rawhide

* Fri Dec 10 2004 Kristian Høgsberg <krh@redhat.com> - 0.1.3-1
- Add python-devel build requires.

* Wed Nov 24 2004  <jrb@redhat.com> - 
- Initial build.

