Name:           perl-YAML-Syck
Version:        0.98
Release:        1%{?dist}
Summary:        Fast, lightweight YAML loader and dumper
License:        MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-Syck/
Source0:        http://www.cpan.org/authors/id/A/AU/AUDREYT/YAML-Syck-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Devel::Leak)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides a Perl interface to the libsyck data serialization
library. It exports the Dump and Load functions for converting Perl data
structures to YAML strings, and the other way around.

%prep
%setup -q -n YAML-Syck-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes COMPATIBILITY COPYING README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/YAML*
%{perl_vendorarch}/JSON*
%{_mandir}/man3/*

%changelog
* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.98-1
- Update to 0.98.

* Tue Sep 18 2007 Steven Pritchard <steve@kspei.com> 0.97-1
- Update to 0.97.

* Sun Aug 12 2007 Steven Pritchard <steve@kspei.com> 0.96-1
- Update to 0.96.

* Fri Aug 03 2007 Steven Pritchard <steve@kspei.com> 0.95-1
- Update to 0.95.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 0.94-1
- Update to 0.94.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.91-1
- Update to 0.91.

* Sat May 19 2007 Steven Pritchard <steve@kspei.com> 0.85-1
- Update to 0.85.

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-3
- add perl split BR's

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-2
- bump

* Thu Feb 01 2007 Steven Pritchard <steve@kspei.com> 0.82-1
- Specfile autogenerated by cpanspec 1.69.1.
- Remove explicit build dependency on perl.
- Include JSON module.
- BR Devel::Leak (for tests).
