%{?el5: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

# For EPEL5 make a python26 package.
%if 0%{?rhel} == 5
%global __python26 %{_bindir}/python2.6
# Disable byte compiling. Do ourselves later.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g') 
%{!?pydir26: %global pydir26 %{_builddir}/python26-%{name}-%{version}-%{release}}
%{!?python26_sitearch: %global python26_sitearch %(%{__python26} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:		Cython26
Version:	0.14.1
#Release:	1.beta2%{?dist}
Release:	3%{?dist}
Summary:	A language for writing Python extension modules

#%define upstreamversion %{version}.beta2
%define upstreamversion %{version}

Group:		Development/Tools
License:	Python
URL:		http://www.cython.org
Source:		http://www.cython.org/Cython-%{upstreamversion}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python-devel python-setuptools
%if 0%{?rhel} == 5
BuildRequires:  python26-devel
BuildRequires:  python26-distribute
%endif 

%if 0%{?rhel} ==  5
Requires:       python(abi) = 2.4
%endif

%description
This is a development version of Pyrex, a language
for writing Python extension modules.

For more info, see:

    Doc/About.html for a description of the language
    INSTALL.txt	   for installation instructions
    USAGE.txt	   for usage instructions
    Demos	   for usage examples


%if 0%{?rhel} == 5
%package -n python26-Cython
Summary:        A language for writing Python extension modules
Group:          Development/Libraries
Requires:       python(abi) = 2.6

%description -n python26-Cython
This is a development version of Pyrex, a language
for writing Python extension modules.

For more info, see:

    Doc/About.html for a description of the language
    INSTALL.txt	   for installation instructions
    USAGE.txt	   for usage instructions
    Demos	   for usage examples
%endif

%prep
%setup -q -n Cython-%{upstreamversion}

%if 0%{?rhel} == 5
rm -rf   %{pydir26}
mkdir -p %{pydir26}
cp -a *  %{pydir26}
%endif


%build
%{__python} setup.py build

%if 0%{?rhel} == 5
pushd %{pydir26}
%{__python26} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?rhel} == 5
pushd %{pydir26}
%{__python26} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
pushd $RPM_BUILD_ROOT%{_bindir}
mv cython cython-python26
mv cygdb  cygdb-python26
popd
%endif

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#On rhel5 we do our own byte compiling that we disabled earlier.
%if 0%{?rhel} == 5 
%{__python} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitearch}", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT"'", 10, "%{python_sitearch}", 1)' > /dev/null
%{__python26}    -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python26_sitearch}"'", 10, "%{python26_sitearch}", 1)' > /dev/null
%{__python26} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python26_sitearch}"'", 10, "%{python26_sitearch}", 1)' > /dev/null
%endif


%clean
rm -rf $RPM_BUILD_ROOT

##%%check
##%%{__python} runtests.py -x numpy

%files
%defattr(-,root,root,-)
%{_bindir}/cython
#cygdb is not built with python 2.4 or 2.3.
%if 0%{?fedora} || 0%{?rhel} >= 6
%{_bindir}/cygdb
%endif
%{python_sitearch}/Cython
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%{python_sitearch}/Cython*egg-info
%endif
%doc *.txt Demos Doc Tools

%if 0%{?rhel} == 5
%files -n python26-Cython
%defattr(-,root,root,-)
%{_bindir}/cython-python26
%{_bindir}/cygdb-python26
%{python26_sitearch}/Cython
%{python26_sitearch}/cython.py*
%{python26_sitearch}/pyximport
%{python26_sitearch}/Cython*egg-info
%doc *.txt Demos Doc Tools
%endif

%changelog
* Sun Apr 03 2012 Steve Traylen <steve.traylen@cern.ch> - 0.14.1-3
- Adapt SPEC file for python3 and python26 on EPEL5.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb  5 2011 Neal Becker <ndbecker2@gmail.com> - 0.14.1-1
- Update to 0.14.1

* Wed Dec 15 2010 Neal Becker <ndbecker2@gmail.com> - 0.14-2
- Add cygdb

* Wed Dec 15 2010 Neal Becker <ndbecker2@gmail.com> - 0.14-1
- Update to 0.14

* Wed Aug 25 2010 Neal Becker <ndbecker2@gmail.com> - 0.13-1
- Update to 0.13

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Feb  5 2010 Neal Becker <ndbecker2@gmail.com> - 0.12.1-4
- Disable check for now as it fails on PPC

* Tue Feb  2 2010 Neal Becker <ndbecker2@gmail.com> - 0.12.1-2
- typo
- stupid rpm comments

* Mon Nov 23 2009 Neal Becker <ndbecker2@gmail.com> - 0.12-1.rc1
- Make that 0.12

* Mon Nov 23 2009 Neal Becker <ndbecker2@gmail.com> - 0.12.1-1.rc1
- Update to 0.12.1

* Sun Sep 27 2009 Neal Becker <ndbecker2@gmail.com> - 0.11.3-1.rc1
- Update to 0.11.3rc1
- Update to 0.11.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Neal Becker <ndbecker2@gmail.com> - 0.11.2-1
- Update to 0.11.2

* Thu Apr 16 2009 Neal Becker <ndbecker2@gmail.com> - 0.11.1-1
- Update to 0.11.1

* Sat Mar 14 2009 Neal Becker <ndbecker2@gmail.com> - 0.11-2
- Missed cython.py*

* Sat Mar 14 2009 Neal Becker <ndbecker2@gmail.com> - 0.11-1
- Update to 0.11
- Exclude numpy from tests so we don't have to BR it

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Neal Becker <ndbecker2@gmail.com> - 0.10.3-1
- Update to 0.10.3

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10.2-2
- Rebuild for Python 2.6

* Mon Dec  1 2008 Neal Becker <ndbecker2@gmail.com> - 0.10.2-1
- Update to 0.10.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10.1-2
- Rebuild for Python 2.6

* Wed Nov 19 2008 Neal Becker <ndbecker2@gmail.com> - 0.10.1-1
- Update to 0.10.1

* Sun Nov  9 2008 Neal Becker <ndbecker2@gmail.com> - 0.10-3
- Fix typo

* Sun Nov  9 2008 Neal Becker <ndbecker2@gmail.com> - 0.10-1
- Update to 0.10

* Fri Jun 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.8-2
- Install into python_sitearch
- Add %%check

* Fri Jun 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Mon Apr 14 2008 José Matos <jamatos[AT]fc.up.pt> - 0.9.6.13.1-3
- Remove remaining --record.
- Add more documentation (Doc and Tools).
- Add correct entry for egg-info (F9+).

* Mon Apr 14 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.6.13.1-2
- Change License to Python
- Install About.html
- Fix mixed spaces/tabs
- Don't use --record

* Tue Apr  8 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.6.13.1-1
- Update to 0.9.6.13.1

* Mon Apr  7 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.6.13-1
- Update to 0.9.6.13
- Add docs

* Tue Feb 26 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.6.12-1
- Initial version

