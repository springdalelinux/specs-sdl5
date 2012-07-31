Name:           perl-Mail-Sendmail
Version:        0.79
Release:        9%{?dist}.1
Summary:        Simple platform independent mailer for Perl

License:        Copyright only
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Mail-Sendmail/
Source0:        http://www.cpan.org/authors/id/M/MI/MIVKOVIC/Mail-Sendmail-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Not picked up automatically.
Requires:       perl(MIME::QuotedPrint)

%description
Mail::Sendmail is a simple platform independent library for sending
e-mail from your perl script.  It only requires Perl 5 and a network
connection.  Mail::Sendmail contains mainly &sendmail, which takes a
hash with the message to send and sends it. It is intended to be very
easy to setup and use.


%prep
%setup -q -n Mail-Sendmail-%{version}


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
# We don't want to send the test mail -> no make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README Sendmail.html Todo
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3pm*


%changelog
* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.79-9.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.79-9
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.79-8
- Rebuild for FC5 (perl 5.8.8).
- Dist tag and specfile cleanup.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.79-7
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-6
- Sync with fedora-rpmdevtools' Perl spec template to fix x86_64 build.

* Tue Jan 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.5
- Fix License and %%description (#65).

* Wed Oct 29 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.4
- Specfile cleanup.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.3
- Install into vendor dirs.

* Sun May  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.2
- Own more dirs.
- Save .spec in UTF-8.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.1
- Update to current Fedora guidelines.

* Sun Feb  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.79-1.fedora.1
- First Fedora release.
