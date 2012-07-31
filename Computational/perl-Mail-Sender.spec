Name:           perl-Mail-Sender
Version:        0.8.13
Release:        2%{?dist}.1
Summary:        Module for sending mails with attachments through an SMTP server

Group:          Development/Libraries
# There is also a clause which says that it may not be used for SPAM.
# However, since spamming is illegal in the US, this isn't really a use restriction.
# Instead, its a friendly reminder of the law, so we won't list it here.
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Mail-Sender/
Source0:        http://www.cpan.org/authors/id/J/JE/JENDA/Mail-Sender-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.


%prep
%setup -q -n Mail-Sender-%{version}
%{__perl} -pi -e 's/\r\n/\n/' README


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} < /dev/null


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Remove the Win32 module in order to avoid requiring perl(Win32API::Registry)
find $RPM_BUILD_ROOT -type f -name Win32.pm -exec rm -f {} ';'


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
# License: perl + spam exception.
# See the main POD page for the copyright information.
# For the Artistic and GPL license text(s), see the perl package.
%doc Changes README
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3pm*


%changelog
* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.13-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 14 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.13-2
- Update to 0.8.13.

* Wed Mar 15 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.13-1
- Update to 0.8.13.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-3
- Rebuild for FC5 (perl 5.8.8).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-2
- License clarification.

* Sat Sep 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.8.10-1
- First build.
