Summary:        Various mail-related perl modules
Name:           perl-MailTools
Version:        1.77
Release:        1%{?dist}
License:        GPL or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MailTools/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MARKOV/MailTools-%{version}.tar.gz
Patch0:         perl-MailTools-1.74-CPAN-20726.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  perl(Net::Domain), perl(Net::SMTP), perl(ExtUtils::MakeMaker)

%description
MailTools is a set of Perl modules related to mail applications.

%prep
%setup -q -n MailTools-%{version}

# This patch addresses CPAN RT#20726 (http://rt.cpan.org/Public/Bug/Display.html?id=20726)
# which is about handling filenames with trailing spaces. This patch has been rejected
# upstream because it raises the minimum perl version required to 5.6.1, which upstream
# considers to be "too recent". However, given that all distributions supported by this
# package have at least perl 5.8.0, it's not a problem for us.
%patch0 -p0

# Set up example scripts
cd examples
for file in *.PL
do
    %{__perl} $file
done
%{__chmod} -x *_demo
# Remove example-generation scripts, no longer needed
# It causes warnings from MakeMaker, but we don't care
%{__rm} *.PL
cd -

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

%check
%{__make} test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog README* examples/
%{perl_vendorlib}/auto/Mail/
%{perl_vendorlib}/Mail/
%{_mandir}/man3/Mail::*.3pm*

%changelog
* Fri May 11 2007 Paul Howarth <paul@city-fan.org> 1.77-1
- Update to 1.77

* Tue Apr 10 2007 Paul Howarth <paul@city-fan.org> 1.76-1
- Update to 1.76
- Add comment text about the patch for fixing CPAN RT#20726
- BuildRequire perl(ExtUtils::MakeMaker) rather than perl-devel

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 1.74-4
- Buildrequire perl-devel for Fedora 7 onwards
- Fix argument order for find with -depth

* Wed Aug 30 2006 Paul Howarth <paul@city-fan.org> 1.74-3
- FE6 mass rebuild

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.74-2
- cosmetic spec file changes
- fix CPAN RT#20726 (RH #200450), allowing Mail::Util::read_mbox() to open
  files with weird names

* Wed Mar  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.74-1
- 1.74.

* Sun Jan 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.73-1
- 1.73.

* Wed Jan 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.72-1
- 1.72.

* Fri Jan  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.71-1
- 1.71.

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.67-2
- Fix demo scripts.
- Sync with fedora-rpmdevtools' perl spec template.

* Fri Jul  1 2005 Paul Howarth <paul@city-fan.org> - 1.67-1
- update to 1.67 (#161830)
- assume perl_vendorlib is set
- license is same as perl (GPL or Artistic) according to README
- don't include module name in summary
- use macros consistently
- add dist tag

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.66-2
- rebuilt

* Sat Jan 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.66-1
- Update to 1.66.

* Wed Aug 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.64-0.fdr.1
- Update to 1.64, patch applied upstream.
- Bring up to date with current fedora.us Perl spec template.

* Sat Mar 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.61-0.fdr.2
- Add patch to complete test.pm -> testfile.pm change introduced in 1.61.

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.61-0.fdr.1
- Update to 1.61.
- Reduce directory ownership bloat.
- Run tests in the %%check section.

* Thu Sep 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.60-0.fdr.1
- Update to 1.60.
- Install into vendor dirs.
- Spec cleanups.

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.5
- Package is now noarch

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.4
- Changed group tag
- Making test in build section

* Tue Jul  1 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.3
- Modified files section

* Tue Jun 17 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.2
- Added forgotten description
- Modified Summary according to Michael Schwendt suggestion
- Modified tarball permissions to 0644

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
