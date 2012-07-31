%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pyxdg
Version:        0.16
Release:        1%{?dist}
Summary:        Python library to access freedesktop.org standards
Group:          Development/Libraries
License:        LGPLv2
URL:            http://freedesktop.org/Software/pyxdg
Source0:        http://www.freedesktop.org/~lanius/%{name}-%{version}.tar.gz
Patch0:		pyxdg-0.16-indentfix-bz469229.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel

%description
PyXDG is a python library to access freedesktop.org standards 

%prep
%setup -q
%patch0 -p1 -b .indentfix

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT 
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT 

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%{python_sitelib}/xdg

%changelog
* Thu Oct 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-1
- update to 0.16
- fix indent bug in DesktopEntry.py (bz 469229)

* Sat Apr  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-6
- add egg-info (fixes FTBFS bz 440813)

* Wed Jan  3 2007 Patrice Dumas <pertusus@free.fr> - 0.15-5
- remove requires for python-abi (automatic now) and python directory
- remove package name from summary
- change tabs to spaces

* Thu Dec 21 2006 Patrice Dumas <pertusus@free.fr> - 0.15-4
- rebuild for python 2.5

* Sat Sep 23 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 0.15-3
- rebuild for fc6

* Wed Feb 15 2006 John Mahowald <jpmahowald@gmail.com> - 0.15.2
- Rebuild for Fedora Extras 5

* Fri Oct 14 2005 John Mahowald <jpmahowald@gmail.com> - 0.15-1
- Rebuilt for 0.15

* Sun Jul 03 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.14-2
- Added %%{?dist} tag to release
- BuildArch: noarch
- Removed unneccesary CLFAGS

* Sun Jun 05 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.14-1
- Rebuilt for 0.14

* Wed Jun 01 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.13-1
- Rebuilt for 0.13

* Tue May 31 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.12-1
- Rebuilt for 0.12

* Sat May 28 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.11-1
- Rebuilt for 0.11

* Mon May 23 2005 Sindre Pedersen Bjordal <foolish[AT]fedoraforum.org> - 0.10-1
- Adapt to Fedora Extras template, based on spec from NewRPMs

* Tue Dec 14 2004 Che
- initial rpm release


