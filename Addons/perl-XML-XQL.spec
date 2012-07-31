Name:           perl-XML-XQL
Version:        0.68
Release:        3%{?dist}
Summary:        Perl module for querying XML tree structures with XQL

Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/XML-XQL/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJMATHER/XML-XQL-%{version}.tar.gz
Patch0:         %{name}-tput-147465.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(XML::DOM) >= 1.29
BuildRequires:  perl(Date::Manip)
BuildRequires:  perl(Parse::Yapp)
Requires:       perl(XML::DOM)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is a Perl extension that allows you to perform XQL queries on XML
object trees. Currently only the XML::DOM module is supported, but
other implementations, like XML::Grove, may soon follow.


%prep
%setup -q -n XML-XQL-%{version}
%patch0 -p0

cat <<EOF > %{name}-prov
#!/bin/sh
# Filter versionless XML::XQL, we expect perl.prov to emit the versioned one.
%{__perl_provides} \$* | grep -v 'perl(XML::\(DOM::\|XQL)$\)'
EOF
%define __perl_provides %{_builddir}/XML-XQL-%{version}/%{name}-prov
chmod +x %{__perl_provides}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*


%check
make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/xql.pl
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::XQL*.3*


%changelog
* Mon Aug 27 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.68-3
- Rebuild for FC6

* Thu Jun 08 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.68-2
- rebuilt and spec clean.
 
* Sun Nov  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-1
- First Fedora Extras release.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-0.3
- Add minimum version to XML::DOM build dependency, filter out
  versionless perl(XML::DOM) provision (#172332, Ralf Corsepius).

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-0.2
- Fix insecure $PATH error in taint mode (#147465).
- Avoid warnings with empty (but defined) $TERM (#147465).

* Thu Oct 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.68-0.1
- First build (#128879).
