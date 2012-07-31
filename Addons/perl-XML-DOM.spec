Name:           perl-XML-DOM
Version:        1.44
Release:        2%{?dist}
Summary:        DOM extension to XML::Parser

Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/XML-DOM/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJMATHER/XML-DOM-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(XML::Parser::PerlSAX)
BuildRequires:  perl(XML::RegExp)
Requires:       perl(XML::Parser)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes:      perl-libxml-enno <= 1.02

%description
This is a Perl extension to XML::Parser. It adds a new 'Style' to
XML::Parser, called 'Dom', that allows XML::Parser to build an Object
Oriented datastructure with a DOM Level 1 compliant interface.  For a
description of the DOM (Document Object Model), see
http://www.w3.org/DOM/


%prep
%setup -q -n XML-DOM-%{version}

cat <<EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} \$* | grep -v 'perl(XML::XQL::Node)'
EOF
%define __perl_provides %{_builddir}/XML-DOM-%{version}/%{name}-prov
chmod +x %{__perl_provides}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc BUGS Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::*.3*


%changelog
* Thu Jun 29 2006 Orion Poplawski <orion@cora.nwra.com> - 1.44-2
- Bump for new perl version (#196667)

* Sat Nov  5 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.44-1
- First Fedora Extras release (#172331).

* Thu Oct 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.44-0.1
- First build (#128879).
