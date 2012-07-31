Name:           perl-Readonly-XS
Version:        1.04
Release:        7%{?dist}.1
Summary:        Companion module for Readonly

Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/Readonly-XS/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RO/ROODE/Readonly-XS-%{version}.tar.gz
Patch0:         makefile.pl.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:  perl(Readonly) >= 1.02


%description
Readonly::XS is a companion module for Readonly, to speed up read-only
scalar variables.


%prep
%setup -q -n Readonly-XS-%{version}
%patch0


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*


%check
make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README Changes
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Readonly/
%{_mandir}/man3/*.3*


%changelog
* Sun May 06 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- rebuilt for RHEL5 final

* Fri Oct 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.04-7
- bump for missing patch...

* Fri Oct 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.04-6
- drop br on perl(Readonly), patch Makefile.PL as well
- rework spec to use macros

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.04-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.04-4
- bump for mass rebuild

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.04-3
- proper version on perl(Readonly) BuildRequires & Requires

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.04-1
- New Version
- BuildRequires perl(Readonly), remove explicit requires on
- perl-Readonly version

* Thu Dec 08 2005 Michael A. Peters <mpeters@mac.com> - 1.03-2
- Fix license and BuildRequires

* Sat Nov 12 2005 Michael A. Peters <mpeters@mac.com> - 1.03-1
- created spec file
