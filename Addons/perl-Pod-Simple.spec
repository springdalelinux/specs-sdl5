Name:           perl-Pod-Simple
Version:        3.05
Release:        2.2%{?dist}
Summary:        Framework for parsing POD documentation

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Pod-Simple/
Source0:        http://www.cpan.org/authors/id/A/AR/ARANDAL/Pod-Simple-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl >= 2:5.8.0
BuildRequires:  perl(Pod::Escapes)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Pod::Simple is a Perl library for parsing text in the Pod ("plain old
documentation") markup language that is typically used for writing
documentation for Perl and for Perl modules.


%prep
%setup -q -n Pod-Simple-%{version}


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
%exclude %{perl_vendorlib}/perlpod*.pod
%exclude %{_mandir}/man3/perlpod*.3*


%changelog
* Thu Mar 20 2008 Robert Rati <rrati@redhat> - 3.05-2.2
- Rebuild to support condor

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.05-2.1
Rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 3.05-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed May 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.05-1
- Update to 3.05.

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.04-3
- Rebuild for FC6.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.04-2
- Rebuild for FC5 (perl 5.8.8).

* Thu Jan 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.04-1
- Update to 3.04.

* Tue Nov 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 3.03-1
- Update to 3.03.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.02-2
- rebuilt

* Tue May 25 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:3.02-0.fdr.1
- Update to 3.02.

* Sun May  9 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.06-0.fdr.1
- Update to 2.06.
- Avoid creation of the perllocal.pod file (make pure_install).

* Sun May  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.05-0.fdr.3
- Use canonical source URL (bug 1541).
- Exclude duplicate POD manpages too (bug 1541).
- Requires perl 5.8 or newer (bug 1541).

* Fri Apr 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.05-0.fdr.2
- Require perl(:MODULE_COMPAT_*).
- Reduce directory ownership bloat.
- Exclude POD docs that are part of perl itself.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.05-0.fdr.1
- First build.
