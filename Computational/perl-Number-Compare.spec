Name: 		perl-Number-Compare
Version: 	0.01
Release: 	8%{?dist}
Summary: 	Perl module for numeric comparisons
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Number-Compare/
Source0: 	http://www.cpan.org/modules/by-module/Number/Number-Compare-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: 	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
Requires:  	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Number::Compare compiles a simple comparison to an anonymous subroutine,
which you can call with a value to be tested again.

%prep
%setup -q -n Number-Compare-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%clean
rm -rf $RPM_BUILD_ROOT


%check
make test

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/Number
%{_mandir}/man3/*

%changelog
* Fri Aug 17 2007 Ralf Corsépius <rc040203@freenet.de> - 0.01-8
- Update license tag.

* Thu Apr 19 2007 Ralf Corsépius <rc040203@freenet.de> - 0.01-7
- Reflect perl package split.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.01-6
- Mass rebuild.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.01-5
- Rebuild for perl-5.8.8.

* Tue Aug 16 2005 Paul Howarth <paul@city-fan.org> - 0.01-4
- BR: perl redundant for Extras.

* Sat Aug 13 2005 Ralf Corsepius <ralf@links2linux.de> - 0.01-3
- Spec cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.01-2
- FE re-submission.

* Fri Jul 01 2005 Ralf Corsepius <ralf@links2linux.de> - 0.01-1
- FE submission.
