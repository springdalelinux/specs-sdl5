Name:           perl-DBD-CSV
Version:        0.22
Release:        5%{?dist}
Summary:        DBI driver for CSV files

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-CSV/
Source0:        http://www.cpan.org/authors/id/J/JZ/JZUCKER/DBD-CSV-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(DBI) >= 1.00
BuildRequires:  perl(DBD::File) >= 0.30
BuildRequires:  perl(SQL::Statement) >= 0.1011
BuildRequires:  perl(Text::CSV_XS) >= 0.16
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(SQL::Statement) >= 0.1011

%description
The DBD::CSV module is yet another driver for the DBI (Database
independent interface for Perl). This one is based on the SQL
"engine" SQL::Statement and the abstract DBI driver DBD::File
and implements access to so-called CSV files (Comma separated
values). Such files are mostly used for exporting MS Access and
MS Excel data.


%prep
%setup -q -n DBD-CSV-%{version}
chmod -c a-x ChangeLog README lib/DBD/*.pm lib/Bundle/DBD/*.pm


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
%doc ChangeLog README
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/DBD/
%{_mandir}/man3/*.3pm*


%changelog
* Tue Sep 26 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-5
- Added perl(SQL::Statement) to requirements list (#208012).

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-4
- Rebuild for FC6.

* Fri Feb 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-3
- Rebuild for FC5 (perl 5.8.8).

* Sat Dec 17 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-2
- Missing build requirement: DBD::File >= 0.30.

* Sun Sep 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- First build.
