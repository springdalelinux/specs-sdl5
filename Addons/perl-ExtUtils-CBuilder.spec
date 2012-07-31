Name:           perl-ExtUtils-CBuilder
Version:        0.21
Release:        2%{?dist}
Summary:        Compile and link C code for Perl modules
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/ExtUtils-CBuilder/
Source0:        http://www.cpan.org/authors/id/K/KW/KWILLIAMS/ExtUtils-CBuilder-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module can build the C portions of Perl modules by invoking the
appropriate compilers and linkers in a cross-platform manner. It was
motivated by the Module::Build project, but may be useful for other
purposes as well.

%prep
%setup -q -n ExtUtils-CBuilder-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-2
- rebuild for new perl

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 0.21-1
- Update to 0.21.
- Use fixperms macro instead of our own chmod incantation.
- Reformat to more closely match cpanspec output (but don't use
  Module::Build, since that would create a dependency loop).
- Package README.

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.19-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu May 31 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- Update to 0.19.

* Thu Mar 30 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-1
- Update to 0.18.

* Sat Mar 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-1
- Update to 0.17.

* Tue Mar 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.16-1
- Update to 0.16.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-2
- Rebuild for FC5 (perl 5.8.8).

* Thu Oct  6 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.15-1
- Update 0.15.

* Thu Sep 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.14-1
- Update 0.14.

* Thu Aug 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.13-1
- Update 0.13.

* Fri Jun  3 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.12-1
- Update 0.12.
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.10-2
- rebuilt

* Wed Mar 16 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.10-1
- Update to 0.10.

* Tue Feb 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.09-1
- Update to 0.09.
- Patch no longer needed.

* Sat Jan 15 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.07-1
- Update to 0.07.

* Tue Dec 28 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.06-0.fdr.1
- Update to 0.06.

* Mon Nov 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.05-1
- Revert to building with ExtUtils::MakeMaker to eliminate a build
  dependency loop with Module::Build.

* Fri Oct 15 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.05-0.fdr.1
- Update to 0.05.
- Building procedure: Makefile.PL -> Build.PL.

* Mon Oct 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.04-0.fdr.1
- Update to 0.04.

* Sat May 15 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.03-0.fdr.1
- Uptade to 0.03.
- Avoid creation of the perllocal.pod file (make pure_install).

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.02-0.fdr.2
- Require perl(:MODULE_COMPAT_*).

* Sat Feb 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.02-0.fdr.1
- Update to 0.02.

* Mon Jan 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.01-0.fdr.1
- First build.
