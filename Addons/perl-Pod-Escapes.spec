Name:           perl-Pod-Escapes
Version:        1.04
Release:        7%{?dist}
Summary:        Perl module for resolving POD escape sequences

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Pod-Escapes/
Source0:        http://www.cpan.org/authors/id/S/SB/SBURKE/Pod-Escapes-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides things that are useful in decoding Pod E<...>
sequences. Presumably, it should be used only by Pod parsers and/or
formatters.


%prep
%setup -q -n Pod-Escapes-%{version}


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
%doc ChangeLog README
%{perl_vendorlib}/Pod/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-7
- Rebuild for perl 5.10 (again)

* Sun Jan 13 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-6
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-5
- Rebuild for FC6.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-3
- Dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.04-2
- rebuilt

* Sun May  9 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.04-0.fdr.1
- Update to 1.04.
- Avoid creation of the perllocal.pod file (make pure_install).

* Fri Apr 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.03-0.fdr.2
- Require perl(:MODULE_COMPAT_*).
- Reduce directory ownership bloat.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.03-0.fdr.1
- First build.
