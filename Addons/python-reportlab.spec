%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		python-reportlab
Version:	2.0
Release:	2%{?dist}
Summary:	Python PDF generation library

Group:		Development/Libraries
License:	BSD
URL:		http://www.reportlab.org/
Source0:	http://www.reportlab.org/ftp/ReportLab_2_0.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	python-devel


%description
Python PDF generation library.


%package docs
Summary:	Documentation files for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}


%description docs
The %{name}-docs package contains the documentation for ReportLab in PDF format.


%prep
%setup -q -n reportlab_2_0


%build
cd ./reportlab
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
cd ./reportlab
%{__python} setup.py install --root $RPM_BUILD_ROOT

# Remove test, doc, and demo files.
rm -Rf ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/demos
rm -Rf ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/tools/pythonpoint/demos
rm -Rf ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/docs
rm -Rf ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/test/

rm ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/README
rm ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/changes
rm ${RPM_BUILD_ROOT}%{python_sitelib}/reportlab/license.txt


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc reportlab/README reportlab/changes reportlab/license.txt
%dir %{python_sitelib}/reportlab
%{python_sitelib}/reportlab/*.py*
%{python_sitelib}/reportlab/extensions/
%{python_sitelib}/reportlab/fonts/
%{python_sitelib}/reportlab/graphics/
%{python_sitelib}/reportlab/lib/
%{python_sitelib}/reportlab/pdfbase/
%{python_sitelib}/reportlab/pdfgen/
%{python_sitelib}/reportlab/platypus/
%{python_sitelib}/reportlab/tools/


%files docs
%defattr(-,root,root,-)
%doc reportlab/docs/*.pdf reportlab/demos

%changelog
* Wed Apr  4 2007 Josko Plazonic <plazonic@math.princeton.edu>
- fixup demos bug

* Wed Dec 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0-2
- Make docs subpackage.

* Wed Dec 27 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0-1
- Update to 2.0.

* Fri Dec  8 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.21.1-2
- Rebuild against new python.

* Thu Sep  7 2006 Brian Pepple <bpepple@fedoraproject.org> - 1.21.1-1
- Update to 1.20.1.

* Tue Feb 14 2006 Brian Pepple <bdpepple@ameritech.net> - 1.20-5
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 26 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-4
- Add dist tag. (#176479)

* Mon May  9 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-3.fc4
- Switchback to sitelib patch.
- Make package noarch.

* Thu Apr  7 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-2.fc4
- Use python_sitearch to fix x86_64 build.

* Wed Mar 30 2005 Brian Pepple <bdpepple@ameritech.net> - 1.20-1.fc4
- Rebuild for Python 2.4.
- Update to 1.20.
- Switch to the new python macros for python-abi
- Add dist tag.

* Sat Apr 24 2004 Brian Pepple <bdpepple@ameritech.net> 0:1.19-0.fdr.2
- Removed %ghosts.

* Sat Mar 20 2004 Brian Pepple <bdpepple@ameritech.net> 0:1.19-0.fdr.1
- Initial Fedora RPM build.

