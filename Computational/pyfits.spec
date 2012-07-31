%define __python /usr/bin/python26
%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')

Name: pyfits26
Version: 2.3.1
Release: 1%{?dist}
Summary: Python interface to FITS

Group: Development/Languages
License: BSD

URL: http://www.stsci.edu/resources/software_hardware/pyfits
Source0: http://www.stsci.edu/resources/software_hardware/pyfits/pyfits-%{version}.tar.gz
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: python26-devel python26-setuptools numpy26
Requires: numpy26

%description
PyFITS provides an interface to FITS formatted files under the Python 
scripting language. It is useful both for interactive data analysis and for 
writing analysis scripts in Python using FITS files as either input or output. 

%prep
%setup -q -n pyfits-%{version}
sed -i -e "1d" lib/core.py

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root  %{buildroot}
chmod 755 %{buildroot}%{python_sitearch}/pyfits/pyfitsComp.so

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root,-)
%doc lib/LICENSE.txt 
%{python_sitearch}/*

%changelog
* Wed Jun 23 2010 Sergio Pascual <sergiopr@fedoraproject.org> - 2.3.1-1
- New upstream source
- Added CFLAGS to the build line

* Tue Nov 17 2009 Sergio Pascual <sergiopr@fedoraproject.org> - 2.2.2-1
- New upstream source

* Fri Sep 25 2009 Sergio Pascual <sergiopr@fedoraproject.org> - 2.2-1
- New upstream source

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Sergio Pascual <sergiopr@fedoraproject.org> - 2.1.1-2
- Fixed strange permision of the .so file

* Tue May 19 2009 Sergio Pascual <sergiopr@fedoraproject.org> - 2.1.1-1
- New upstream source with support for "tile image compression".

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3-4
- Rebuild for Python 2.6

* Tue Apr 08 2008 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3-3
- Adding dist tag

* Sun Apr 06 2008 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3-2
- Fixing setup not quiet
- Shebang removed from non-script python files

* Wed Mar 26 2008 Sergio Pascual <sergio.pasra@gmail.com> - 1.3-1
- Initial specfile

