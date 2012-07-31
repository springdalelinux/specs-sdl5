Summary: 	Params-Validate Perl module
Name: 		perl-Params-Validate
Version: 	0.88
Release: 	3%{?dist}
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Params-Validate/
Source0: 	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Params-Validate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker)
# Required by the tests
BuildRequires: 	perl(Test::Taint)
BuildRequires:	perl(Readonly)
BuildRequires:	perl(Readonly::XS)

%description
The Params::Validate module allows you to validate method or function
call parameters to an arbitrary level of specificity. At the simplest
level, it is capable of validating the required parameters were given
and that no unspecified additional parameters were passed in. It is
also capable of determining that a parameter is of a specific type,
that it is an object of a certain class hierarchy, that it possesses
certain methods, or applying validation callbacks to arguments.

%prep
%setup -q -n Params-Validate-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%clean
rm -rf $RPM_BUILD_ROOT

%check
make test

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README TODO
%{perl_vendorarch}/Params
%{perl_vendorarch}/auto/Params
%{perl_vendorarch}/Attribute
%{_mandir}/man3/*

%changelog
* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-3
- Update license tag.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-2
- Mass rebuild.

* Mon Mar 12 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-1
- BR: perl(ExtUtils::MakeMaker).
- Upstream update.

* Sat Jan 20 2007 Ralf Corsépius <rc040203@freenet.de> - 0.87-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-2
- Mass rebuild.

* Sun Aug 13 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-1
- Upstream update.

* Mon Jun 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.85-1
- Upstream update.

* Mon Jun 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.84-1
- Upstream update.

* Sun May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.82-1
- Upstream update.

* Wed Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.81-1
- Upstream update.

* Wed Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-2
- Rebuild.

* Wed Feb 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-1
- Upstream update.

* Sat Jan 14 2006 Ralf Corsépius <rc040203@freenet.de> - 0.79-1
- Upstream update.
- BR perl(Readonly), perl(Readonly::XS).

* Sun Aug 14 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-2
- Spec file cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-1
- FE submission.
