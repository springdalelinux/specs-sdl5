Name:           perl-Log-Dispatch-FileRotate
Version:        1.16
Release:        1%{?dist}
Summary:        Log to files that archive/rotate themselves

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Log-Dispatch-FileRotate/
Source0:        http://www.cpan.org/authors/id/M/MA/MARKPF/Log-Dispatch-FileRotate-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Date::Manip)
BuildRequires:  perl(Log::Dispatch)
# See comment in the %%check section
# BuildRequires:  perl(Log::Log4perl) >= 0.23
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module provides a simple object for logging to files under the
Log::Dispatch::* system, and automatically rotating them according to
different constraints. This is basically a Log::Dispatch::File wrapper
with additions.


%prep
%setup -q -n Log-Dispatch-FileRotate-%{version}


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
# Test suite disabled: circular dependencies with Log::Log4perl
# make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Log/Dispatch/
%{_mandir}/man3/*.3pm*


%changelog
* Sat Nov 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- Update to 1.16.

* Wed Apr 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.15-1
- Update to 1.15.
- The author corrected the licensing terms (License: GPL+ or Artistic).

* Mon Apr 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.
- License: Artistic.

* Mon Apr 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-2
- The license is: GPL+ or Artistic.
  License information: http://rt.cpan.org/Public/Bug/Display.html?id=14563.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-1
- First build.
