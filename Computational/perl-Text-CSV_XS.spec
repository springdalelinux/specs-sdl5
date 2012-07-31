Name:		perl-Text-CSV_XS
Version:	0.85
Release:	1%{?dist}
Summary:	Comma-separated values manipulation routines
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Text-CSV_XS/
Source0:	http://search.cpan.org/CPAN/authors/id/H/HM/HMBRAND/Text-CSV_XS-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(Test::Harness)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Tie::Scalar)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private perl objects
%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values. An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

%prep
%setup -q -n Text-CSV_XS-%{version}

# Fix perl location in example scripts
perl -pi -e 's|^#!/pro/bin/perl|#!/usr/bin/perl|' \
	examples/{csv-check,parser-xs.pl,csvdiff,csv2xls}

# Turn off exec bits in examples to avoid a multitude of docfile dependencies
chmod -c a-x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
chmod -R u+w %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog README examples/
%{perl_vendorarch}/Text/
%{perl_vendorarch}/auto/Text/
%{_mandir}/man3/Text::CSV_XS.3pm*

%changelog
* Mon Sep 19 2011 Paul Howarth <paul@city-fan.org> - 0.85-1
- Update to 0.85
  - Improve date conversion in examples/csv2xls
    - New option -D allows column selection for date conversions
  - Added a note about EBCDIC data files
  - Test suite is now safe for parallel test (prove --shuffle -j6)
  - Spelling fixes
  - Real eol support for parsing streams (beyond \n, \r and \r\n)
  - Clarify doc for always_quote to not quote undef fields
  - Clarify UTF8 process for print () and combine ()
  - Fixed undefinedness of $\ in print (CPAN RT#61880)
  - Windows doesn't support STDERR redirection as used in t/80_diag
  - Internals now use warn() instead of (void)fprintf (stderr, ...)
  - The test in t/80_diag now passes on Windows
  - Better parsing for eol = \r and set as such (CPAN RT#61525)
  - Workaround for AIX cpp bug (CPAN RT#62388)
  - Version 0.77 broke MacOS exported CSV files with only \r
  - Use correct type for STRLEN (HP-UX/PA-RISC/32)
  - More code coverage
  - EOF unreliable when line-end missing at EOF
  - Implement getline_all() and getaline_hr_all()
  - Fixed another parsing issue with eol = \r (CPAN RT#61525)
  - Add is_missing ()
  - Doc overhaul
  - Fix build on OpenVMS (CPAN RT#65654)
  - Fix SetDiag () leak (CPAN RT#66453)
  - Documentation fix (CPAN RT#66905)
  - Documentation overhaul (pod links)
  - Fix spurious auto_diag warning (CPAN RT#69673)
  - Tested with 50 versions of perl, including 1.15.1
  - NAME / DISTNAME in Makefile.PL
  - More cross-checks for META data
- Fix shellbangs in example scripts
- Comment fixes done in %%prep
- Use macros in a consistent and approved manner

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.72-1
- PERL_INSTALL_ROOT => DESTDIR, add perl_default_filter (XS module)
- auto-update to 0.72 (by cpan-spec-update 0.01) (DBIx::Class needed a newer
  Text::CSV, which in turn can only leverage Text::CSV_XS >= 0.70)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- added a new br on perl(IO::Handle) (version 0)
- added a new br on perl(Test::Harness) (version 0)
- added a new br on perl(Test::More) (version 0)
- added a new br on perl(Tie::Scalar) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.69-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 0.69
- new upstream release

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.68-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.58-1
- Update to latest upstream
- SvUPGRADE patch upstreamed

* Tue Jul 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.52-2
- Actually solving the issue mentioned in previous change

* Tue Jul 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.52-1
- Updated to 0.52 to solve an issue with perl 5.10

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-5
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.30-4
- Autorebuild for GCC 4.3

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-3
- rebuild for new perl

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.30-2
- Rebuild for selinux ppc32 issue.

* Sat Jun 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.30-1
- Update to 0.30.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.29-1
- Update to 0.29.

* Sat Jun 16 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.27-1
- Update to 0.27.
- New upstream maintainer.

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-5
- Rebuild for FC6.

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-4
- Rebuild for FC5 (perl 5.8.8).

* Wed Feb 22 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-3
- The wonders of CVS problems (released skipped).

* Thu Jan  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-2
- Build section: simplified RPM_OPT_FLAGS handling (#175898).

* Sat Nov 05 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- First build.
