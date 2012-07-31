%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-dateutil
Version:        1.2
Release:        1%{?dist}
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        Python Software Foundation License
URL:            http://labix.org/python-dateutil
Source0:        http://labix.org/download/python-dateutil/python-dateutil-%{version}.tar.bz2
Patch0:         python-dateutil-1.1-x86_64.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

%prep
%setup -q
%patch -p1


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc example.py LICENSE NEWS README
%{python_sitelib}/dateutil/

%changelog
* Thu Jun 28 2007 Orion Poplawski <orion@cora.nwra.com> 1.2-1
- Update to 1.2

* Wed Jul 26 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-3
- Add patch to fix building on x86_64

* Wed Feb 15 2006 Orion Poplawski <orion@cora.nwra.com> 1.1-2
- Rebuild for gcc/glibc changes

* Thu Dec 22 2005 Orion Poplawski <orion@cora.nwra.com> 1.1-1
- Update to 1.1

* Thu Jul 28 2005 Orion Poplawski <orion@cora.nwra.com> 1.0-1
- Update to 1.0

* Tue Jul 05 2005 Orion Poplawski <orion@cora.nwra.com> 0.9-1
- Initial Fedora Extras package
