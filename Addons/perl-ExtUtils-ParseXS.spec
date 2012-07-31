Name:           perl-ExtUtils-ParseXS
Version:        2.18
Release:        1%{?dist}.1
Summary:        Module and a script for converting Perl XS code into C code

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/ExtUtils-ParseXS/
Source0:        http://www.cpan.org/authors/id/K/KW/KWILLIAMS/ExtUtils-ParseXS-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
ExtUtils::ParseXS will compile XS code into C code by embedding the
constructs necessary to let C functions manipulate Perl values and
creates the glue necessary to let Perl access those functions.


%prep
%setup -q -n ExtUtils-ParseXS-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/ExtUtils/
%{_mandir}/man3/*.3pm*


%changelog
* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.18-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Jan 30 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.18-1
- Update to 2.18.

* Wed Nov 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.17-1
- Update to 2.17.

* Sat Sep 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.16-1
- Update to 2.16.

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-3
- Rebuild for FC6.

* Wed Feb 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-2
- Rebuild for FC5 (perl 5.8.8).

* Tue Oct 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-1
- Update to 2.15.

* Fri Oct  7 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.13-1
- Update to 2.13.

* Thu Aug 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.12-1
- Update to 2.12.

* Tue Jun 14 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-1
- Update to 2.11.

* Tue Jun  7 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.10-1
- Update to 2.10.
- Add dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.09-2
- rebuilt

* Tue Mar 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-1
- Update to 2.09.

* Sat May 15 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:2.08-0.fdr.2
- Avoid creation of the perllocal.pod file (make pure_install).

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.08-0.fdr.1
- Update to 2.08.
- Require perl(:MODULE_COMPAT_*).

* Mon Jan 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.07-0.fdr.1
- Update to 2.07.

* Sat Dec 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.06-0.fdr.1
- Update to 2.06.

* Tue Sep 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.05-0.fdr.1
- Update to 2.05.

* Thu Sep  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.04-0.fdr.1
- Update to 2.04.

* Thu Sep  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.03-0.fdr.1
- First build.
