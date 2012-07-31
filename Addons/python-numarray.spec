%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_siteinc: %define python_siteinc %(%{__python} -c "from distutils.sysconfig import get_python_inc; print get_python_inc()")}

Name:           python-numarray
Version:        1.5.2
Release:        1%{?dist}
Summary:        Python array manipulation and computational library

Group:          Development/Languages
License:        Distributable
URL:            http://www.stsci.edu/resources/software_hardware/numarray
Source0:        http://dl.sf.net/numpy/numarray-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
Requires:   python-abi = %(%{__python} -c "import sys ; print sys.version[:3]")
Provides:   %{name}-devel = %{version}-%{release}

%description
Numarray provides array manipulation and computational capabilities
similar to those found in IDL, Matlab, or Octave. Using numarray, it is
possible to write many efficient numerical data processing applications
directly in Python without using any C, C++ or Fortran code (as well as
doing such analysis interactively within Python or PyRAF). For algorithms
that are not well suited for efficient computation using array facilities
it is possible to write C functions (and eventually Fortran) that can
read and write numarray arrays that can be called from Python.


%prep
%setup -q -n numarray-%{version}
find -name \*~ | xargs rm -f

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
chmod +x $RPM_BUILD_ROOT%{python_sitearch}/numarray/examples/convolve/benchmark.py

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt Doc/*
%{python_siteinc}/numarray/
%{python_sitearch}/numarray/


%changelog
* Wed Sep  6 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.5.2-1
- Update to 1.5.2
- No longer ghost .pyo files

* Tue Feb 14 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.5.1-1
- Update to 1.5.1

* Thu Dec 22 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.5.0-1
- Update to 1.5.0

* Thu Aug 11 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.3.3-4
- Use sitearch macro instead of sitelib

* Thu Aug 11 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.3.3-3
- Properly %ghost .pyo files

* Tue Aug 09 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.3.3-2
- Cleanup
- Added -devel provides

* Tue Aug 02 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.3.3-1
- Initial release for Fedora Extras
