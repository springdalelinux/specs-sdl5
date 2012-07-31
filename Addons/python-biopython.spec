%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:             python-biopython
Version:          1.51
Release:          1%{?dist}
Summary:          Python tools for computational molecular biology
Source0:          http://biopython.org/DIST/biopython-%{version}.tar.gz
Patch0:           python-biopython-1.51-enable-flex.patch
License:          MIT
Url:              http://www.biopython.org/
Group:            Development/Libraries
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    python-devel
BuildRequires:    flex
BuildRequires:    python-reportlab
BuildRequires:    numpy
BuildRequires:    MySQL-python
BuildRequires:    python-psycopg2
Requires:         python-reportlab
Requires:         numpy
Requires:         MySQL-python
Requires:         python-psycopg2
Requires:         wise2

%description
A set of freely available Python tools for computational molecular
biology.

%prep
%setup -q -n biopython-%{version}
# enable build of Bio.PDB.mmCIF.MMCIFlex (requires flex)
%patch0 -p0

# remove all execute bits from documentation and fix line endings
find Scripts -type f -exec chmod -x {} 2>/dev/null ';'
find Doc -type f -exec chmod -x {} 2>/dev/null ';'
find Doc -type f -exec sed -i 's/\r//' {} 2>/dev/null ';'

# remove execute bits from Python modules
find Bio -type f -exec chmod -x {} 2>/dev/null ';'
# remove she-bang lines in .py files to keep rpmlint happy
find Bio -type f -name "*.py" -exec sed -i '/^#![ ]*\/usr\/bin\/.*$/ d' {} 2>/dev/null ';'

%build
env CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT --install-data=%{_datadir}/python-biopython

## disable tests for the moment
%check
%{?_with_check:%{__python} setup.py test --no-gui || :}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Doc Scripts
%doc CONTRIB DEPRECATED LICENSE NEWS README
%if 0%{?fedora} >= 9
%{python_sitearch}/*egg-info
%endif
%dir %{python_sitearch}/Bio
%{python_sitearch}/Bio/*
%dir %{python_sitearch}/BioSQL
%{python_sitearch}/BioSQL/*

%changelog
* Tue Aug 18 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.51-1
- Update to upstream 1.51
- Drop mx {Build}Requires, no longer used upstream
- Remove Martel modules, no longer distributed upstream
- Add flex to BuildRequires, patch setup to build
  Bio.PDB.mmCIF.MMCIFlex as per upstream:
  http://bugzilla.open-bio.org/show_bug.cgi?id=2619

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  1 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.49-1
- Update to latest upstream (1.49) uses numpy and new API for psycopg2
- [Build]Requires python-numeric -> numpy 
- [Build]Requires python-psycopg -> python-psycopg2
- Remove interactive question hack, no longer needed

* Sun Nov 30 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.48-3
- Temporarily disable python-psycopg dependency until it is rebuilt
  for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.48-2
- Rebuild for Python 2.6

* Mon Sep 29 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.48-1
- Update to latest upstream (1.48)

* Fri Jul  4 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.47-1
- Update to latest upstream (1.47)

* Sun Mar 23 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.45-1
- Update to latest upstream (1.45)

* Sat Feb  9 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.44-4
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Thu Dec 13 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.44-3
- Include eggs in file list for F9+

* Sun Oct 28 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.44-2
- Drop patch to setup.py, applied upstream

* Sun Oct 28 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.44-1
- Update to latest upstream (1.44).

* Mon Aug 27 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.43-5
- Used "MIT" as short license name as the "Biopython License
  Agreement" is the same as the CMU MIT variant.

* Mon Apr 25 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.43-4
- Add wise2 Requires since the Wise biopython module uses the
  command-line behind-the-scenes.

* Mon Apr 17 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.43-3
- Use python_sitearch macro to enable x86_64 builds work.

* Mon Apr 16 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.43-2
- Fix Source0 URL as per suggestion from Parag AN on #235989.

* Mon Apr 02 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> 1.43-1
- Initial Fedora package.


