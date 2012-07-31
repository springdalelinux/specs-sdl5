# Build switch:
#   --with mailtests         Enable mail tests

%define mailtests      0

%{?_with_mailtests:%define mailtests 1}


Name:           perl-Log-Dispatch
Version:        2.20
Release:        1%{?dist}
Summary:        Dispatches messages to one or more outputs

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Log-Dispatch/
Source0:        http://www.cpan.org/authors/id/D/DR/DROLSKY/Log-Dispatch-%{version}.tar.gz
Patch0:         Log-Dispatch-2.11-enable-mail-tests.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Params::Validate)
%if %{mailtests}
BuildRequires:  perl(Mail::Send), perl(Mail::Sender)
BuildRequires:  perl(Mail::Sendmail), perl(MIME::Lite)
%endif
BuildRequires:  perl(File::Find::Rule), perl(Test::Pod)
BuildRequires:  mod_perl
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Log::Dispatch is a suite of OO modules for logging messages to
multiple outputs, each of which can have a minimum and maximum log
level.  It is designed to be easily subclassed, both for creating a
new dispatcher object and particularly for creating new outputs.


%prep
%setup -q -n Log-Dispatch-%{version}
%if %{mailtests}
%patch0 -p1
%endif

# Requirements list: exclude mod_perl
cat <<__EOF__ > %{name}-perlreq
#!/bin/sh
/usr/lib/rpm/perl.req \$* | grep -v 'perl(Apache'
__EOF__
%define __perl_requires %{_builddir}/Log-Dispatch-%{version}/%{name}-perlreq
chmod +x %{__perl_requires}



%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*


%check
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/Log/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Dec 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.20-1
- bump to 2.20

* Sat Jun  9 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.18-1
- Update to 2.18.

* Wed Dec 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.16-1
- Update to 2.16.
- Removed perl(IO::String) from the BR list (no longer needed).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-2
- New build requirement: perl(IO::String).

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.15-1
- Update to 2.15.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-2
- Log-Dispatch-2.11-mod_perl2.patch no longer needed.

* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.14-1
- Update to 2.14.

* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.13-1
- Update to 2.13.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.12-1
- Update to 2.12.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-4
- Rebuild for FC5 (perl 5.8.8).

* Thu Sep 22 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-3
- Exclude mod_perl from the requirements list
  (overkill for most applications using Log::Dispatch).

* Mon Sep 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-2
- Better mod_perl handling.

* Fri Sep 09 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.11-1
- First build.
