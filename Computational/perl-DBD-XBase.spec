Name:           perl-DBD-XBase
Version:        0.241
Release:        5%{?dist}
Summary:        Perl module for reading and writing the dbf files

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DBD-XBase/
Source0:        http://www.cpan.org/authors/id/J/JA/JANPAZ/DBD-XBase-%{version}.tar.gz
Patch0:         DBD-XBase-0.241-indexdump.PL.patch
Patch1:         DBD-XBase-0.241-dbfdump-rename.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(DBI)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module can read and write XBase database files, known as dbf in
dBase and FoxPro world. It also transparently reads memo fields from
the dbt, fpt and smt files and works with index files (ndx, ntx, mdx, idx,
cdx and SDBM). This module XBase.pm provides simple native interface
to XBase files. For DBI compliant database access, see DBD::XBase and
DBI modules and their man pages.


%prep
%setup -q -n DBD-XBase-%{version}
%patch0 -p1
%patch1 -p1
chmod a-x eg/*table

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
%doc Changes README ToDo driver_characteristics new-XBase
%doc eg/
%{_bindir}/*
%{perl_vendorlib}/DBD/
%{perl_vendorlib}/XBase*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-5
- Rebuild due to repodata corruption (#195611).

* Thu Mar 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-4
- dbfdump renamed to dbfdump.pl to avoid file conflict with shapelib (#181999).

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Dec 16 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-2
- Patch to remove the duplicate shebang line in bin/indexdump (#175895).

* Sat Nov 05 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.241-1
- First build.
