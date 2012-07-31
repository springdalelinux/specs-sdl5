Name:           GMT-doc
Version:        4.3.1
Release:        3
Summary:        Documentation for Generic Mapping Tools

Group:          Documentation
License:        GPLv2
URL:            http://gmt.soest.hawaii.edu/
Source0:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_pdf.tar.bz2
Source1:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_tut.tar.bz2
Source2:        ftp://ftp.soest.hawaii.edu/gmt/GMT%{version}_web.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       GMT = %{version}
Provides:       gmt-doc = %{version}-%{release}


%description
This package provides the documentation for the GMT (Generic Mapping Tools)
package.


%prep
%setup -q -b1 -b2 -n GMT%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/GMT-%{version}
#Install www and pdf
cp -pr www/gmt/* $RPM_BUILD_ROOT/%{_docdir}/GMT-%{version}/
#Install tutorial
cp -pr tutorial $RPM_BUILD_ROOT/%{_docdir}/GMT-%{version}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_docdir}/GMT-%{version}/*


%changelog
* Thu May 29 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-3
- Bump release for EPEL

* Wed May 21 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-2
- Install the index files properly

* Wed May 21 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.1-1
- Update to 4.3.1

* Mon Apr 12 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.0-2
- Rename to GMT-doc
- Require only GMT-%%{version}, drop release

* Tue Apr 6 2008 Orion Poplawski <orion@cora.nwra.com> 4.3.0-1
- Update to 4.3.0
- Make single package

* Mon Mar 24 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.1-1
- Initial version
