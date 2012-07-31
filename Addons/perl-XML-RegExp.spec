Name:           perl-XML-RegExp
Version:        0.03
Release:        2%{?dist}
Summary:        Regular expressions for XML tokens

Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/XML-RegExp/
Source0:        http://www.cpan.org/authors/id/T/TJ/TJMATHER/XML-RegExp-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This package contains an utility module containing regular expressions
for the following XML tokens: BaseChar, Ideographic, Letter, Digit,
Extender, CombiningChar, NameChar, EntityRef, CharRef, Reference,
Name, NmToken, and AttValue.


%prep
%setup -q -n XML-RegExp-%{version}


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
%doc Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/XML::RegExp.3*


%changelog
* Thu Jun 29 2006 Orion Poplawski <orion@cora.nwra.com> - 0.03-2
- Bump for new perl version (#196668)

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.03-1
- First Fedora Extras release (#172330).

* Thu Oct 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.03-0.1
- First build (#128879).
