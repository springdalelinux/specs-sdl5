%define module_version 0.2808

Name:           perl-Module-Build
# When the module version is x.yz, set Version to x.yz00.
Version:        0.2808
Release:        1.1%{?dist}
Summary:        Perl module for building and installing Perl modules
License:        GPL or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Build/
Source0:        http://www.cpan.org/authors/id/K/KW/KWILLIAMS/Module-Build-%{module_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Archive::Tar) >= 1.08
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.15
BuildRequires:  perl(ExtUtils::ParseXS) >= 1.02
BuildRequires:  perl(PAR::Dist) >= 0.17
BuildRequires:  perl(YAML)
# Avoid a circular build dependency (#215558).
#BuildRequires:  perl(Pod::Readme) >= 0.04
#BuildRequires:  perl(version) >= 0.661
Requires:       perl(Archive::Tar) >= 1.08
Requires:       perl(ExtUtils::CBuilder) >= 0.15
Requires:       perl(ExtUtils::ParseXS) >= 1.02
#Requires:       perl(Pod::Readme) >= 0.04
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.
Developers may alter the behavior of the module through subclassing in a
much more straightforward way than with MakeMaker. It also does not require
a make on your system - most of the Module::Build code is pure-perl and
written in a very cross-platform way. In fact, you don't even need a shell,
so even platforms like MacOS (traditional) can use it fairly easily. Its
only prerequisites are modules that are included with perl 5.6.0, and it
works fine on perl 5.005 if you can install a few additional modules.

%prep
%setup -q -n Module-Build-%{module_version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/config_data
%{perl_vendorlib}/Module
%{_mandir}/man1/config_data.1*
%{_mandir}/man3/Module::Build*.3*

%changelog
* Thu Mar 20 2008 Robert Rati <rrat@redhat> 0.2808-1.1
- Rebuild to support condor

* Fri May 18 2007 Steven Pritchard <steve@kspei.com> 0.2808-1
- Update to 0.2808.
- Drop explicit dependency on Pod::Readme.
- BR PAR::Dist and Archive::Zip for better test coverage.

* Mon Apr 02 2007 Steven Pritchard <steve@kspei.com> 0.2807-1
- Update to 0.2807.

* Sat Dec 16 2006 Steven Pritchard <steve@kspei.com> 0.2806-1
- Update to 0.2806.
- Use fixperms macro instead of our own chmod incantation.

* Wed Nov 15 2006 Steven Pritchard <steve@kspei.com> 0.2805-3
- Don't BR Pod::Readme.  (#215558)

* Sun Sep 17 2006 Steven Pritchard <steve@kspei.com> 0.2805-2
- Rebuild.

* Sat Aug 05 2006 Steven Pritchard <steve@kspei.com> 0.2805-1
- Update to 0.2805.
- Use the bundled version.pm code for now.

* Fri Jul 28 2006 Steven Pritchard <steve@kspei.com> 0.2804-1
- Update to 0.2804.
- BR perl(version).
- Fix find option order.

* Mon May 22 2006 Steven Pritchard <steve@kspei.com> 0.2801-1
- Update to 0.2801.
- Drop the /dev/zero hack.  (Upstream fixed this problem.)

* Thu May 18 2006 Steven Pritchard <steve@kspei.com> 0.2800-2
- Take input from /dev/zero during "Build test" to avoid test failure.

* Wed May 17 2006 Steven Pritchard <steve@kspei.com> 0.2800-1
- Update to 0.28, but call it 0.2800 to avoid an epoch bump.
- Various spec cleanups to closer match cpanspec output.

* Wed Mar 15 2006 Steven Pritchard <steve@kspei.com> - 0.2612-2
- Add versioned deps for Archive::Tar, ExtUtils::CBuilder, and
  ExtUtils::ParseXS.

* Sat Mar 11 2006 Steven Pritchard <steve@kspei.com> - 0.2612-1
- Update to 0.2612.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> - 0.2611-2
- Minor spec cleanup.
- Add COPYING and Artistic.

* Wed Jul 06 2005 Steven Pritchard <steve@kspei.com> - 0.2611-1
- Update to 0.2611.

* Sat May  7 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2610-3
- Rebuild.

* Sat Apr 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.2610-2
- 0.2610.
- Trust that %%{perl_vendorlib} is defined.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Jan 27 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2608-1
- Update to 0.2608, Test::Harness kludge no longer needed.

* Sun Dec 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2606-1
- Update to 0.2606.

* Wed Dec  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2605-1
- Update to 0.2605.
- Disable some tests if Test::Harness::Straps is < 0.20 to avoid failing
  when the default @INC is longish, such as in FC3 Perl.
  http://sourceforge.net/mailarchive/forum.php?thread_id=6056820&forum_id=10905
  http://rt.cpan.org/NoAuth/Bug.html?id=5649

* Sun Oct 10 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.26-0.fdr.1
- Update to 0.26.

* Sat May 22 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.25-0.fdr.3
- Require perl(YAML) and perl(ExtUtils::ParseXS) (bug 1348).

* Tue Apr 27 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.25-0.fdr.2
- Do not require Archive::Tar, it is not used on Unix platforms anyway.
  Instead, gzip and tar are used, but even they are optional and used only
  in the 'dist' and 'ppmdist' actions.

* Mon Apr 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.25-0.fdr.1
- Update to 0.25.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.24-0.fdr.2
- Require perl(:MODULE_COMPAT_*).

* Thu Feb 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.24-0.fdr.1
- Update to 0.24.

* Mon Jan 26 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.22-0.fdr.1
- Update to 0.22.

* Thu Sep  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.20-0.fdr.1
- First build.
