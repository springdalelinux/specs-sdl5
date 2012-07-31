%define with_python %{?_without_python: `} %{?!_without_python: 1}
%define with_php %{?_without_php: 0} %{?!_without_php: 1}
%define with_tcl %{?_without_tcl: 0} %{?!_without_tcl: 1}
%define php_rrd_svn 839
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

%define with_python 1
%define with_php 1
%define with_tcl 1

Summary: Round Robin Database Tool to store and display time-series data
Name: rrdtool
Version: 1.2.23
Release: 3%{?dist}
License: GPL
Group: Applications/Databases
URL: http://people.ee.ethz.ch/~oetiker/webtools/%{name}/
Source0: http://people.ee.ethz.ch/~oetiker/webtools/%{name}/pub/%{name}-%{version}.tar.gz
Source1: php4-svn%{php_rrd_svn}.tar.gz
Patch0: rrdtool-1.2.13-php.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gcc-c++, openssl-devel, freetype-devel
BuildRequires: libpng-devel, zlib-devel, libart_lgpl-devel >= 2.0
%if "%{?fedora}" >= "7"
BuildRequires: perl-devel
%endif

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). It stores the data in a very compact way that will not
expand over time, and it presents useful graphs by processing the data to
enforce a certain data density. It can be used either via simple wrapper
scripts (from shell or Perl) or via frontends that poll network devices and
put a friendly user interface on it.

%package devel
Summary: RRDtool libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package allow you to use directly this library.

%package doc
Summary: RRDtool documentation
Group: Documentation

%description doc
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data (i.e. network bandwidth, machine-room temperature,
server load average). This package contains documentation on using RRD.

%package perl
Summary: Perl RRDtool bindings
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes: perl-%{name} < %{version}-%{release}
Provides: perl-%{name} = %{version}-%{release}

%description perl
The Perl RRDtool bindings

%if %{with_python}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')}
# eval to 2.3 if python isn't yet present, workaround for no python in fc4 minimal buildroot
%{!?python_version: %define python_version %(%{__python} -c 'import sys; print sys.version.split(" ")[0]' || echo "2.3")}

%package python
Summary: Python RRDtool bindings
Group: Development/Languages
BuildRequires: python-devel >= 2.3
Requires: python >= %{python_version}
Requires: %{name} = %{version}-%{release}
Obsoletes: python-%{name} < %{version}-%{release}
Provides: python-%{name} = %{version}-%{release}

%description python
Python RRDtool bindings.
%endif

%ifarch ppc64
# php bits busted on ppc64 at the moment
%define with_php 0
%endif

%if %{with_php}
%package php
Summary: PHP RRDtool bindings
Group: Development/Languages
BuildRequires: php-devel >= 4.0
Requires: php >= 4.0
Requires: %{name} = %{version}-%{release}
Obsoletes: php-%{name} < %{version}-%{release}
Provides: php-%{name} = %{version}-%{release}

%description php
The %{name}-php package includes a dynamic shared object (DSO) that adds
RRDtool bindings to the PHP HTML-embedded scripting language.
%endif

%if %{with_tcl}
%package tcl
Summary: Tcl RRDtool bindings
Group: Development/Languages
BuildRequires: tcl-devel >= 8.0
Requires: tcl >= 8.0
Requires: %{name} = %{version}-%{release}
Obsoletes: tcl-%{name} < %{version}-%{release}
Provides: tcl-%{name} = %{version}-%{release}

%description tcl
The %{name}-tcl package includes RRDtool bindings for Tcl.
%endif

%prep
%setup -q
%setup -q -T -D -a 1
# Patch based on http://oss.oetiker.ch/rrdtool/pub/contrib/php_rrdtool.tgz
%if %{with_php}
%patch0 -p0 -b .php
%{__perl} -pi -e 's|../config.h|../rrd_config.h|g' php4/rrdtool.c
%endif

# Fix to find correct python dir on lib64
%{__perl} -pi -e 's|get_python_lib\(0,0,prefix|get_python_lib\(1,0,prefix|g' \
    configure

# Most edits shouldn't be necessary when using --libdir, but
# w/o, some introduce hardcoded rpaths where they shouldn't,
%{__perl} -pi.orig -e 's|/lib\b|/%{_lib}|g' \
    configure Makefile.in php4/configure php4/ltconfig*

%build
%configure \
    --with-perl-options='INSTALLDIRS="vendor"' \
%if %{with_tcl}
    --enable-tcl-site \
    --with-tcllib=%{_libdir} \
%else
    --disable-tcl \
%endif
%if %{with_python}
    --enable-python \
%else
    --disable-python \
%endif
    --disable-static \
    --with-pic

# Fix another rpath issue
%{__perl} -pi.orig -e 's|-Wl,--rpath -Wl,\$rp||g' \
    bindings/perl-shared/Makefile.PL

# Force RRDp bits where we want 'em, not sure yet why the
# --with-perl-options and --libdir don't take
pushd bindings/perl-piped/
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__perl} -pi.orig -e 's|/lib/perl|/%{_lib}/perl|g' Makefile
popd

%{__make} %{?_smp_mflags}

# Build the php module, the tmp install is required
%if %{with_php}
%define rrdtmp %{_tmppath}/%{name}-%{version}-tmpinstall
%{__make} install DESTDIR="%{rrdtmp}"
pushd php4/
%configure \
    --with-rrdtool="%{rrdtmp}%{_prefix}" \
    --disable-static
%{__make} %{?_smp_mflags}
popd
%{__rm} -rf %{rrdtmp}
%endif

# Fix @perl@ and @PERL@
find examples/ -type f \
    -exec %{__perl} -pi -e 's|^#! \@perl\@|#!%{__perl}|gi' {} \;
find examples/ -name "*.pl" \
    -exec %{__perl} -pi -e 's|\015||gi' {} \;

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

# Install the php module
%if %{with_php}
%{__install} -D -m0755 php4/modules/rrdtool.so \
    %{buildroot}%{php_extdir}/rrdtool.so
# Clean up the examples for inclusion as docs
%{__rm} -rf php4/examples/.svn
# Put the php config bit into place
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/rrdtool.ini
; Enable rrdtool extension module
extension=rrdtool.so
__EOF__
%endif

# Pesky RRDp.pm...
%{__mv} $RPM_BUILD_ROOT%{perl_vendorarch}/../RRDp.pm $RPM_BUILD_ROOT%{perl_vendorarch}/

# We only want .txt and .html files for the main documentation
%{__mkdir_p} doc2/html doc2/txt
%{__cp} -a doc/*.txt doc2/txt/
%{__cp} -a doc/*.html doc2/html/

# Put perl docs in perl package
%{__mkdir_p} doc3/html
%{__mv} doc2/html/RRD*.html doc3/html/

# Clean up the examples
%{__rm} -f examples/Makefile* examples/*.in

# This is so rpm doesn't pick up perl module dependencies automatically
find examples/ -type f -exec chmod 0644 {} \;

# Clean up the buildroot
%{__rm} -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}/{txt,html}/ \
	$RPM_BUILD_ROOT%{perl_vendorarch}/ntmake.pl \
	$RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod \
        $RPM_BUILD_ROOT%{_datadir}/%{name}/examples \
        $RPM_BUILD_ROOT%{perl_vendorarch}/auto/*/{.packlist,*.bs}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/%{name}
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%exclude %{_libdir}/*.la
%{_libdir}/*.so

%files doc
%defattr(-,root,root,-)
%doc CHANGES CONTRIBUTORS COPYING COPYRIGHT README TODO NEWS THREADS
%doc examples doc2/html doc2/txt

%files perl
%defattr(-,root,root,-)
%doc doc3/html
%{_mandir}/man3/*
%{perl_vendorarch}/*.pm
%attr(0755,root,root) %{perl_vendorarch}/auto/RRDs/

%if %{with_python}
%files python
%defattr(-,root,root,-)
%doc bindings/python/AUTHORS bindings/python/COPYING bindings/python/README
%{python_sitearch}/rrdtoolmodule.so
%endif

%if %{with_php}
%files php
%defattr(-,root,root,0755)
%doc php4/examples php4/README
%config(noreplace) %{_sysconfdir}/php.d/rrdtool.ini
%{php_extdir}/rrdtool.so
%endif

%if %{with_tcl}
%files tcl
%defattr(-,root,root,-)
%doc bindings/tcl/README
%{_libdir}/tclrrd*.so
%{_libdir}/rrdtool/*.tcl
%endif

%changelog
* Thu May 03 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-3
- Disable php bits on ppc64 for now, they fail to build

* Thu May 03 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-2
- Add BR: perl-devel for Fedora 7 and later

* Tue May 01 2007 Jarod Wilson <jwilson@redhat.com> 1.2.23-1
- New upstream release

* Tue May 01 2007 Jarod Wilson <jwilson@redhat.com> 1.2.21-1
- New upstream release

* Wed Apr 25 2007 Jarod Wilson <jwilson@redhat.com> 1.2.19-2
- Define %%python_version *before* its needed (#237826)

* Mon Apr 09 2007 Jarod Wilson <jwilson@redhat.com> 1.2.19-1
- New upstream release

* Tue Jan 23 2007 Jarod Wilson <jwilson@redhat.com> 1.2.18-1
- New upstream release

* Mon Jan 22 2007 Jarod Wilson <jwilson@redhat.com> 1.2.17-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 1.2.15-9
- Fix crash with long error strings (upstream
  changesets 929 and 935)

* Thu Dec 14 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-8
- Fix for log grid memory leak (#201241)

* Tue Dec 12 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-7
- Rebuild for python 2.5

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-6
- Conditionalize python, php and tcl bits (Resolves #203275)

* Wed Oct 25 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-5
- Add tcl sub-package (#203275)

* Tue Sep 05 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-4
- Rebuild for new glibc

* Wed Aug 02 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-3
- One more addition to initrrdtool patch, to fully revert
  and correct upstream changeset 839
- Fix for no python in minimal fc4 buildroots

* Tue Aug  1 2006 Mihai Ibanescu <misa@redhat.com> 1.2.15-2
- Fixed rrdtool-python to import the module properly (patch
  rrdtool-1.2.15-initrrdtool.patch)

* Mon Jul 17 2006 Jarod Wilson <jwilson@redhat.com> 1.2.15-1
- Update to 1.2.15
- Minor spec cleanups

* Sat Jun 24 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-7
- Fix up Obsoletes

* Mon Jun 19 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-6
- Flip perl, php and python sub-package names around to 
  conform with general practices

* Sat Jun 10 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-5
- Minor fixes to make package own created directories

* Wed Jun 07 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-4
- Add php bits back into the mix

* Mon Jun 05 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-3
- Merge spec fixes from bz 185909

* Sun Jun 04 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-2
- Remove explicit perl dep, version grabbing using rpm during
  rpmbuild not guaranteed to work (fails on ppc in plague),
  and auto-gen perl deps are sufficient

* Sat Jun 03 2006 Jarod Wilson <jwilson@redhat.com> 1.2.13-1
- Update to release 1.2.13
- Merge spec changes from dag, atrpms and mdk builds
- Additional hacktastic contortions for lib64 & rpath messiness
- Add missing post/postun ldconfig
- Fix a bunch of rpmlint errors
- Disable static libs, per FE guidelines
- Split off docs

* Wed Apr 19 2006 Chris Ricker <kaboom@oobleck.net> 1.2.12-1
- Rev to 1.2

* Fri May 20 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-5
- Include patch from Michael to fix perl module compilation on FC4 (#156242).

* Fri May 20 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-4
- Fix for the php module patch (Joe Pruett, Dag Wieers), #156716.
- Update source URL to new location since 1.2 is now the default stable.
- Don't (yet) update to 1.0.50, as it introduces some changes in the perl
  modules install.

* Mon Jan 31 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-3
- Put perl modules in vendor_perl and not site_perl. #146513

* Thu Jan 13 2005 Matthias Saou <http://freshrpms.net/> 1.0.49-2
- Minor cleanups.

* Thu Aug 25 2004 Dag Wieers <dag@wieers.com> - 1.0.49-1
- Updated to release 1.0.49.

* Wed Aug 25 2004 Dag Wieers <dag@wieers.com> - 1.0.48-3
- Fixes for x86_64. (Garrick Staples)

* Fri Jul  2 2004 Matthias Saou <http://freshrpms.net/> 1.0.48-3
- Actually apply the patch for fixing the php module, doh!

* Thu May 27 2004 Matthias Saou <http://freshrpms.net/> 1.0.48-2
- Added php.d config entry to load the module once installed.

* Thu May 13 2004 Dag Wieers <dag@wieers.com> - 1.0.48-1
- Updated to release 1.0.48.

* Tue Apr 06 2004 Dag Wieers <dag@wieers.com> - 1.0.47-1
- Updated to release 1.0.47.

* Thu Mar  4 2004 Matthias Saou <http://freshrpms.net/> 1.0.46-2
- Change the strict dependency on perl to fix problem with the recent
  update.

* Mon Jan  5 2004 Matthias Saou <http://freshrpms.net/> 1.0.46-1
- Update to 1.0.46.
- Use system libpng and zlib instead of bundled ones.
- Added php-rrdtool sub-package for the php4 module.

* Fri Dec  5 2003 Matthias Saou <http://freshrpms.net/> 1.0.45-4
- Added epoch to the perl dependency to work with rpm > 4.2.
- Fixed the %% escaping in the perl dep.

* Mon Nov 17 2003 Matthias Saou <http://freshrpms.net/> 1.0.45-2
- Rebuild for Fedora Core 1.

* Sun Aug  3 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.45.

* Wed Apr 16 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.42.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Wed Mar  5 2003 Matthias Saou <http://freshrpms.net/>
- Added explicit perl version dependency.

* Sun Feb 23 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.41.

* Fri Jan 31 2003 Matthias Saou <http://freshrpms.net/>
- Update to 1.0.40.
- Spec file cleanup.

* Fri Jul 05 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.39

* Mon Jun 03 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.38

* Fri Apr 19 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.37

* Tue Mar 12 2002 Henri Gomez <hgomez@users.sourceforge.net>
- 1.0.34
- rrdtools include zlib 1.1.4 which fix vulnerabilities in 1.1.3

