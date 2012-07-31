Name:           perl-Pod-Coverage
Version:        0.18
Release:        2%{?dist}
Summary:        Checks if the documentation of a module is comprehensive

Group:          Development/Libraries
License:        GPL or Artistic
URL:            http://search.cpan.org/dist/Pod-Coverage/
Source0:        http://www.cpan.org/authors/id/R/RC/RCLAMP/Pod-Coverage-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Devel::Symdump)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Developers hate writing documentation.  They'd hate it even more if their
computer tattled on them, but maybe they'll be even more thankful in the
long run.  Even if not, perlmodstyle tells you to, so you must obey.

This module provides a mechanism for determining if the pod for a given
module is comprehensive.


%prep
%setup -q -n Pod-Coverage-%{version}


%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README examples/
%{_bindir}/*
%{perl_vendorlib}/Pod/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-2
- Version 0.18 is now a noarch package.

* Wed Aug  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.18-1
- Update to 0.18.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-5
- Rebuild for FC5 (perl 5.8.8).

* Thu May 12 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-4
- Add dist tag.

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.17-3
- Avoid .packlist creation with Module::Build >= 0.2609.
- Trust that %%{perl_vendorlib} is defined.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Nov 27 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.17-1
- Update to 0.17.

* Wed Oct 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.16-0.fdr.1
- Update to 0.16.

* Thu May 20 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.14-0.fdr.1
- First build.
