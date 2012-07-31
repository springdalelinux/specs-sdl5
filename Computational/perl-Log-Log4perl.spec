Name:           perl-Log-Log4perl
Version:        1.13
Release:        2%{?dist}
Summary:        Log4j implementation for Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
# CPAN URL:     http://search.cpan.org/dist/Log-Log4perl/
URL:            http://log4perl.sourceforge.net/
Source0:        http://log4perl.sourceforge.net/releases/Log-Log4perl-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(IPC::Shareable)
BuildRequires:  perl(Log::Dispatch)
BuildRequires:  perl(Log::Dispatch::FileRotate) >= 1.10
BuildRequires:  perl(SQL::Statement)
BuildRequires:  perl(DBD::CSV)
BuildRequires:  perl(XML::DOM)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
# perl(RRDs) is provided by rrdtool-perl (a rrdtool subpackage)
BuildRequires:  perl(RRDs)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Log::Log4perl lets you remote-control and fine-tune the logging
behaviour of your system from the outside. It implements the widely
popular (Java-based) Log4j logging package in pure Perl.


%prep
%setup -q -n Log-Log4perl-%{version}
find lib -name "*.pm" -exec chmod -c a-x {} ';'
%{__perl} -pi -e 's|^#!/usr/local/bin/perl|#!%{__perl}|' eg/newsyslog-test
chmod -c a-x eg/* 


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# These tests fail in the Fedora buildsystem. 
# No clue as to why. They work fine in local testing.
# make test L4P_ALL_TESTS=1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README eg/ ldap/
%{perl_vendorlib}/Log/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-2
- rebuild for new perl

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1.1
- disable tests

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.13-1
- bump to 1.13

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.2
- add BR: perl(Test::More)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.12-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jun 29 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-1
- Update to 1.12.

* Thu Jun  7 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.11-1
- Update to 1.11.

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.10-1
- Update to 1.10.

* Sun Feb 11 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.09-1
- Update to 1.09.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.08-1
- Update to 1.08.

* Sat Oct 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- Update to 1.07.

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.06-1
- Update to 1.06.

* Sun Jun 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.05-1
- Update to 1.05.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-2
- Log::Dispatch::FileRotate is no longer excluded due to licensing
  problems (the package now includes copyright information).

* Mon Mar  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.04-1
- Update to 1.04.

* Mon Feb 27 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-3
- Rebuild for FC5 (perl 5.8.8).

* Thu Feb  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-2
- Added a couple of comments as suggested by Paul Howarth (#176137).

* Tue Feb  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- Update to 1.03.
- Disabled the Log::Dispatch::FileRotate requirement (see #171640).

* Mon Dec 19 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.02-1
- Update to 1.02.

* Sat Oct 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.01-1
- Update to 1.01.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.00-1
- First build.
