Name:           perl-Test-Pod
Version:        1.26
Release:        4%{?dist}
Summary:        Perl module for checking for POD errors in files

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Pod/
Source0:        http://www.cpan.org/authors/id/P/PE/PETDANCE/Test-Pod-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Pod::Simple) >= 2.04
BuildRequires:  perl(Test::Builder::Tester) >= 1.02
BuildRequires:  perl(Test::More) >= 0.62
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.


%prep
%setup -q -n Test-Pod-%{version}


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
%doc Changes
%{perl_vendorlib}/Test/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-4
- Rebuild for perl 5.10 (again)

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-3
- rebuild for new perl

* Thu Dec 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.26-2
- license tag fix

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.26-1
- Update to 1.26.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-2
- Rebuild for FC5 (perl 5.8.8).

* Fri Feb  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.24-1
- Update to 1.24.

* Thu Dec 29 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.22-1
- Update to 1.22.

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-3
- Add dist tag.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.20-2
- rebuilt

* Thu Jun 24 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.20-0.fdr.1
- Update to 1.20.

* Wed May 12 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.16-0.fdr.2
- Avoid creation of the perllocal.pod file (make pure_install).

* Mon May  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.16-0.fdr.1
- Update to 1.16, dir handling patch applied upstream.

* Fri Apr 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.14-0.fdr.1
- Update to 1.14.
- Require perl(:MODULE_COMPAT_*).
- Add patch to avoid warnings from all_pod_files().

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.12-0.fdr.1
- Update to 1.12.

* Thu Jan 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.08-0.fdr.1
- Update to 1.08.
- Use %%{perl_vendorlib}.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.96-0.fdr.1
- First build.
