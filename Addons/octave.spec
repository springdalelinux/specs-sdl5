# From src/version.h:#define OCTAVE_API_VERSION
%define octave_api api-v32

Name:           octave
Version:        3.0.5
Release:        1%{?dist}
Summary:        A high-level language for numerical computations
Epoch:          6

Group:          Applications/Engineering
License:        GPLv3+
Source:         ftp://ftp.octave.org/pub/octave/octave-%{version}.tar.bz2
#Patch1:         %{name}-sh-arch.patch
#Patch2:         %{name}-gcc44.patch
URL:            http://www.octave.org
Requires:       gnuplot less info texinfo 
Requires(post): /sbin/install-info
Requires(postun): /sbin/ldconfig
Requires(post): /sbin/ldconfig
Requires(preun): /sbin/install-info
BuildRequires:  bison flex less tetex gcc-gfortran lapack-devel blas-devel
BuildRequires:  ncurses-devel zlib-devel hdf5-devel texinfo qhull-devel
BuildRequires:  readline-devel glibc-devel fftw-devel gperf ghostscript
BuildRequires:  curl-devel pcre-devel
BuildRequires:  suitesparse-devel glpk-devel gnuplot desktop-file-utils
Provides:       octave(api) = %{octave_api}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
GNU Octave is a high-level language, primarily intended for numerical
computations. It provides a convenient command line interface for
solving linear and nonlinear problems numerically, and for performing
other numerical experiments using a language that is mostly compatible
with Matlab. It may also be used as a batch-oriented language. Octave
has extensive tools for solving common numerical linear algebra
problems, finding the roots of nonlinear equations, integrating
ordinary functions, manipulating polynomials, and integrating ordinary
differential and differential-algebraic equations. It is easily
extensible and customizable via user-defined functions written in
Octave's own language, or using dynamically loaded modules written in
C++, C, Fortran, or other languages.


%package devel
Summary:        Development headers and files for Octave
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       readline-devel fftw-devel hdf5-devel zlib-devel
Requires:       lapack-devel blas-devel gcc-c++ gcc-gfortran

%description devel
The octave-devel package contains files needed for developing
applications which use GNU Octave.


%prep
%setup -q
# Check that octave_api is set correctly
if ! grep -q '^#define OCTAVE_API_VERSION "%{octave_api}"' src/version.h
then
  echo "octave_api variable in spec does not match src/version.h"
  exit 1
fi

# patch for sh arch
#%patch1 -p1 -b .sh-arch
# patch for gcc 4.4
#%patch2 -p1 -b .gcc44

%build
%define enable64 no
export CPPFLAGS="-DH5_USE_16_API"
%configure --enable-shared --disable-static --enable-64=%enable64 --with-f77=gfortran
make %{?_smp_mflags} OCTAVE_RELEASE="Fedora %{version}-%{release}"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

# Make library links
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/octave-%{version}" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/octave-%{_arch}.conf

# Remove RPM_BUILD_ROOT from ls-R files
perl -pi -e "s,$RPM_BUILD_ROOT,," $RPM_BUILD_ROOT%{_libexecdir}/%{name}/ls-R
perl -pi -e "s,$RPM_BUILD_ROOT,," $RPM_BUILD_ROOT%{_datadir}/%{name}/ls-R

# Clean doc directory
pushd doc
  make distclean
  rm -f *.in */*.in */*.cc refcard/*.tex
popd

# Create desktop file
rm $RPM_BUILD_ROOT%{_datadir}/applications/www.octave.org-octave.desktop
desktop-file-install --vendor fedora --add-category X-Fedora --remove-category Development \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications examples/octave.desktop

# Create directories for add-on packages
HOST_TYPE=`$RPM_BUILD_ROOT%{_bindir}/octave-config -p CANONICAL_HOST_TYPE`
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}/site/oct/%{octave_api}/$HOST_TYPE
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}/site/oct/$HOST_TYPE
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/packages
touch $RPM_BUILD_ROOT%{_datadir}/%{name}/octave_packages


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/install-info --info-dir=%{_infodir} --section="Programming" \
	%{_infodir}/octave.info || :

%preun
if [ "$1" = "0" ]; then
   /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/octave.info || :
fi


%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING NEWS* PROJECTS README README.Linux README.kpathsea ROADMAP
%doc SENDING-PATCHES THANKS emacs examples doc/interpreter/octave.p*
%doc doc/faq doc/interpreter/HTML doc/refcard
%{_bindir}/octave*
%config(noreplace) /etc/ld.so.conf.d/*
%{_libdir}/octave*
%{_datadir}/octave
%ghost %{_datadir}/octave/octave_packages
%{_libexecdir}/octave
%{_mandir}/man*/octave*
%{_infodir}/octave.info*
%{_datadir}/applications/*

%files devel
%defattr(-,root,root)
%doc doc/liboctave
%{_bindir}/mkoctfile*
%{_includedir}/octave-%{version}
%{_mandir}/man*/mkoctfile*


%changelog
* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 6:3.0.5-1
- Updated to latest upstream (3.0.5)

* Mon Feb 23 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.3-2
- Add patches from upstream for compiling against GCC 4.4
  http://hg.savannah.gnu.org/hgweb/octave/rev/93cf10950334
  http://hg.tw-math.de/release-3-0-x/rev/712d9e045b1e

* Wed Dec 10 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.3-1
- Update to latest upstream (3.0.3)

* Thu Oct 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 6:3.0.2-2
- patch for sh arch: it adds '-little' flag

* Mon Sep 8 2008 Orion Poplawski <orion@cora.nwra.com> 6:3.0.2-1
- Update to 3.0.2

* Mon Apr 21 2008 Quentin Spencer <qspencer@users.sf.net> 6:3.0.1-1
- New release of octave. Remove gcc 4.3 patch.

* Mon Mar  3 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.0-6
- Re-enable patch, but change cstring -> string.h so it works for C as
  well as C++.  Hopefully this will #435600 for real.

* Sun Mar  2 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 6:3.0.0-5
- Backout GCC 4.3 patch temporarily, causes trouble for octave-forge and 
  may not be necessary (#435600)

* Fri Feb 29 2008 Orion Poplawski <orion@cora.nwra.com> 3.0.0-4
- Rebuild for hdf5 1.8.0 using compatability API define
- Add gcc43 patch

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6:3.0.0-3
- Autorebuild for GCC 4.3

* Wed Jan  9 2008 Quentin Spencer <qspencer@users.sf.net> 3.0.0-2
- Add curl-devel and pcre-devel as build dependencies. Closes bug 302231.

* Fri Dec 21 2007 Quentin Spencer <qspencer@users.sf.net> 3.0.0-1
- Update to 3.0.0.

* Wed Dec 12 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.19-1
- Update to 2.9.19 and update octave_api.

* Wed Dec  5 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.18-1
- Update to 2.9.18 and update octave_api.

* Wed Nov 28 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.17-1
- Update to 2.9.17 and update octave_api.

* Mon Nov  5 2007 Quentin Spencer <qspencer@users.sf.net> 2.9.16-1
- Update to 2.9.16, remove old patch.
- Update licencse from GPLv2+ to GPLv3+.
- Detection of glpk no longer needs special CPPFLAGS.

* Tue Oct 16 2007 Orion Poplawski <orion@ora.nwra.com> 2.9.15-2
- Updated pkg.m patch

* Mon Oct 15 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.15-1
- New release. Remove old patch.

* Tue Sep 25 2007 Orion Poplawski <orion@ora.nwra.com> 2.9.14-2
- Add /usr/share/octave/packages for add on packages and %%ghost 
  /usr/share/octave/octave_packages
- Add patch for octave package manager that will be going upstream

* Tue Sep 18 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.14-1
- New release.
- Remove redundant menu category in desktop file (bug 274431).
- Update license tag.
- Add qhull-devel as new build dependency.

* Thu Jul 26 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.13-1
- New release.
- Changed ufsparse-devel dependency to suitesparse-devel.
- Add configure flag to close bug 245562.
- Add directories for add-on packages (bug 234012).
- Since texinfo is now separate from tetex, it is a build requirement.

* Wed May 23 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.12-1
- New release.

* Tue Feb 20 2007 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.9-2
- Fix install-info bug (Bug 219404). 
- Add dependency on octave API so that breakages will be detected. (Bug 224050).
- Remove libtermcap-devel as build dependency (Bug 226768).

* Mon Oct  3 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.9-1
- New release. Remove old patch.

* Fri Sep 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.8-2
- Fix this bug:
  https://www.cae.wisc.edu/pipermail/bug-octave/2006-September/000687.html

* Fri Aug 25 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.8-1
- New release. Remove old patch. This fixes bug #203676.

* Tue Aug 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.7-3
- Add ghostscript as a build dependency.

* Tue Aug 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.7-2
- Update patch to fix several small bugs, including #201087.

* Fri Jul 28 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.7-1
- New release. Remove old patches and add one new one.

* Tue Jul 11 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.6-2
- Patch for some erroneous warnings and a file path bug.

* Mon Jul 10 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.6-1
- New release. Remove old patches.
- Disable 64-bit extensions (some libraries don't support 64-bit indexing yet).
- Add gcc-gfortran to -devel dependencies (mkoctfile fails without it).
- Move octave-bug and octave-config from devel to main package.
- Fix categorization of info files (bug 196760).

* Wed Apr 27 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-6
- Add patch for bug #190481
- Manual stripping of .oct files is no longer necessary.

* Wed Apr 19 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-5
- Add new patch to configure script (breaks octave-forge without it).

* Fri Mar 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-4
- Change patch again (suggested by the author on Octave mailing list).

* Fri Mar 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-3
- Fix broken patch.

* Fri Mar 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-2
- Add more changes to sparse patch.

* Thu Mar 23 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.5-1
- New upstream release; remove old patches; add sparse patch.
- Add gcc-c++ as dependency for devel package.
- Add more docs; cleanup extra files in docs.
- Simplify configure command.
- Install desktop file.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-8
- Rebuild for new hdf5.
- Remove obsolete configure options.
- Make sure /usr/libexec/octave is owned by octave.

* Wed Feb 15 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-7
- Rebuild for Fedora Extras 5.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-6
- Change dependency from fftw3 to fftw.

* Thu Jan 26 2006 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-5
- Rebuild for new release of hdf5.

* Mon Dec 19 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-4
- Rebuild for gcc 4.1.

* Thu Dec  1 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-3
- Make sure patch applies correctly before building!

* Thu Dec  1 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-2
- Patch to enable compilation on x86_64.

* Fri Nov 11 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.4-1
- New upstream release.
- Patch to make sure all headers are included in -devel.
- PKG_ADD file now needs $RPM_BUILD_ROOT stripped from it.
- Cleanup errors in dependencies.

* Tue Oct 25 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-6
- Add lapack-devel and blas-devel dependencies to devel package.

* Mon Oct 03 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-5
- Change umfpack-devel dependency to the new ufsparse-devel package.

* Thu Sep 22 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-5
- Change lapack and blas dependencies to lapack-devel and blas-devel

* Mon Aug 08 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-4
- Cleanup: remove redefinition of __libtoolize, ExcludeArch of two platforms,
  old s390 workarounds, and LC_ALL setting. None of these appear to be
  necessary any longer, even if the platforms were supported.
- Add --enable-64 to configure to enable 64-bit array indexing on x86_64.
- Add support for GLPK (new build dependency and CPPFLAGS for configure).

* Wed Jul 27 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-3
- Add fftw3-devel to dependencies for devel

* Tue Jul 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-2
- Add dependencies (hdf5-devel and zlib-devel) for devel

* Tue Jul 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.9.3-1
- Move to new 2.9.x development tree.
- Add umfpack-devel as new build dependency.

* Tue Jul 05 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-12
- Require hdf5-devel for build.

* Wed Jun 22 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-11
- Force octave-devel to require readline-devel.
- Add _libdir to configure command (fixes broken mkoctfile on x86_64).

* Tue Jun 21 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-10
- Add epoch to BuildRequires in octave-devel.

* Mon Jun 20 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-9
- Rebuild.

* Sat Jun 18 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-8
- Force octave-devel to require octave.

* Wed Jun  8 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-7
- Fix configure command again. The prefix isn't used for the install step
  but it is used to calculate internal variables in octave.

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 2.1.71-6
- disable explicit gcc-c++/libstdc++-devel BR and bump for another
  rebuild attempt

* Wed Jun  1 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-4
- Fix configure command. Remove irrelevant files from docs.

* Fri May 27 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-3
- Added patch for http://www.octave.org/mailing-lists/bug-octave/2005/617 

* Thu May 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-2
- Added dist tag.

* Fri May 20 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.71-1
- Imported 2.1.71 from upstream, removed 2.1.70 patches (in upstream).
- Begin cleanup of spec file, including the big configure command
  (some options are obsolete, others appear unneeded if rpm configure
  macro is used).

* Mon May  3 2005 Quentin Spencer <qspencer@users.sourceforge.net> 2.1.70-1
- Imported 2.1.70 from upstream, removed old patches (resolved in new version)
- Changed g77 dependency to gfortran.
- Added fftw3 to BuildRequires.
- Added patches (from maintainer) to fix build problems.

* Wed Feb 23 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-13
- fix typo in spec 149420

* Mon Feb 21 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-12
- Fix problem with symlinks using ldconfig (bug 147922)

* Wed Feb 16 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-11
- add $RPM_OPT_FLAGS

* Tue Feb 15 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-10
- Fix bug 142477 - problem with signbit definition (Patch2) 

* Wed Jan 19 2005 Ivana Varekova <varekova@redhat.com> 2.1.57-9
- Fix bug #142440 - change octave.spec: autoconf is BuildPrereq
- Fix bug #142631 - change octave.spec: mkoctfile.1.gz is part of octave-devel not octave

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.1.57-8
- Rebuilt for new readline.

* Mon Oct 18 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-7
- Don't forget default attributes for -devel package

* Mon Oct 18 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-6
- Remove old lib/lib64 badness.

* Wed Oct 13 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-5
- Split into octave and octave-devel

* Thu Jun 24 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-4
- Remove RPM_BUILD_ROOT from preun section (#119112)

* Thu Jun 24 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-3
- Er, typo in patch (thanks Nils)

* Thu Jun 24 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-2
- Fix for #113852 - signbit broken

* Wed Jun 15 2004 Lon Hohberger <lhh@redhat.com> 2.1.57-1
- Import 2.1.57 from upstream; this fixes #126074

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 30 2004 Karsten Hopp <karsten@redhat.de> 2.1.50-9 
- remove builddir references from file list (#119112)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-7
- Add requirement for texinfo. #101299, round 3!

* Tue Sep 09 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-6
- Disable s390x again

* Tue Sep 09 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-5
- Disable ppc64

* Tue Sep 09 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-4
- Rebuild for Taroon

* Wed Jul 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-3
- Fix for Bugzilla #101299, round 2.  Include a patch to
quell sterr from info; it gives us funny messages if $HOME/.info
does not exist.

* Wed Jul 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-2
- Fix for Bugzilla #101299

* Mon Jun 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.50-1
- Import 2.1.50 from upstream
- Fix for Bugzilla #100682; try ppc64 again

* Mon Jun 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.49-6
- Rebuild; disabling ppc64

* Mon Jun 30 2003 Lon Hohberger <lhh@redhat.com> 2.1.49-4
- Added link generation to /usr/lib so that munging
/etc/ld.so.conf isn't required to get octave to work.
(#98226)

* Thu Jun 05 2003 Lon Hohberger <lhh@redhat.com> 2.1.49-2
- Import from upstream; rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 16 2003 Lon Hohberger <lhh@redhat.com> 2.1.46-2
- Rebuilt

* Tue Apr 15 2003 Lon Hohberger <lhh@redhat.com> 2.1.46-1
- Import from upstream: 2.1.46.  Disabled s390x.

* Mon Mar 10 2003 Lon Hohberger <lhh@redhat.com> 2.1.40-5
- Enabled s390[x]

* Fri Feb 7 2003 Lon Hohberger <lhh@redhat.com> 2.1.40-4
- Disabled s390 and s390x builds for now.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 2 2003 Lon Hohberger <lhh@redhat.com> 2.1.40-2
- Fixed readline-devel build-rereq line. (#80673)

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 2.1.40-1
- update to 2.1.40, fix matrix plotting (#77906).

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 2.1.39-2
- build on x86_64.

* Sun Nov 10 2002 Jeff Johnson <jbj@redhat.com> 2.1.39-1
- update to 2.1.39.

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Aug  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-7
- Rebuild

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-6
- Rebuild

* Thu Jul 11 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Rebuild with new readline

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-3
- Get rid of 0 size doc files (#66116)

* Thu May 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-2
- Rebuild
- Patch C++ code gcc changed its opinion of the last 3 weeks

* Wed May  1 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.36-1
- 2.1.36
- Disable patch

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.1.35-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 27 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.1.35-2
- Add patch for kpathsea to avoid segfaults

* Tue Nov  6 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.1.35-1
- 2.1.35
- s/Copyright/License/

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Wed Jun 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add more dependencies in BuildPrereq (#45184)

* Fri Jun 08 2001 Trond Eivind Glomsrød <teg@redhat.com>
- No longer exclude ia64

* Mon Apr 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.34

* Tue Mar 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- set LC_ALL to POSIX before building, otherwise the generated paths.h is bad

* Wed Jan 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.33

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require compat-egcs-c++, but gcc-c++
- add some libtoolize calls to add newest versions

* Fri Dec 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.32, no longer use CVS as our needed fixes are in now
- add Prereq for info

* Thu Dec 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use a development version, as they have now been fixed
  to compile with the our current toolchain.

* Thu Aug 24 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.0.16, with compat C++ compiler and new C and f77 compilers
  The C++ code is too broken for our new toolchain (C++ reserved
  words used as enums and function names, arcane macros), but
  plotting works here and not in the beta (#16759)
- add epoch to upgrade the betas

* Tue Jul 25 2000 Jakub Jelinek <jakub@redhat.com>
- make sure #line commands are not output within macro arguments

* Wed Jul 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.31

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- no longer disable optimizations, sparc excepted

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Mon Jul  3 2000 Matt Wilson <msw@redhat.com>
- added missing %% before {_infodir} in the %%post 

* Sat Jun 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 2.1.30 - the old version contains invalid C++ code
  accepted by older compilers.

* Sat Jun 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable optimization for C++ code

* Fri Jun 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add "Excludearch: " for Alpha - it triggers compiler bugs

* Fri Jun 08 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%configure, %%makeinstall, %{_infodir}. %{_mandir}
- remove prefix

* Tue May 09 2000 Trond Eivind Glomsrød <teg@redhat.com>
- upgraded to 2.0.16
- removed "--enable-g77" from the configure flags - let autoconf find it

* Thu Jan 20 2000 Tim Powers <timp@redhat.com>
- bzipped source to conserve space.

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.0.15.

* Tue Jul 20 1999 Tim Powers <timp@redhat.com>
- rebuit for 6.1

* Wed Apr 28 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.0.14.

* Fri Oct 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.0.13.90

* Thu Jul  9 1998 Jeff Johnson <jbj@redhat.com>
- repackage in powertools.

* Thu Jun 11 1998 Andrew Veliath <andrewtv@usa.net>
- Add %attr, build as user.

* Mon Jun 1 1998 Andrew Veliath <andrewtv@usa.net>
- Add BuildRoot, installinfo, require gnuplot, description from
  Octave's web page, update to Octave 2.0.13.
- Adapt from existing spec file.

* Tue Dec  2 1997 Otto Hammersmith <otto@redhat.com>
- removed libreadline stuff from the file list

* Mon Nov 24 1997 Otto Hammersmith <otto@redhat.com>
- changed configure command to put things in $RPM_ARCH-rehat-linux, 
  rather than genereated one... was causing problems between building 
  on i686 build machine.

* Mon Nov 17 1997 Otto Hammersmith <otto@redhat.com>
- moved buildroot from /tmp to /var/tmp

* Mon Sep 22 1997 Mike Wangsmo <wanger@redhat.com>
- Upgraded to version 2.0.9 and built for glibc system

* Thu May 01 1997 Michael Fulbright <msf@redhat.com>
- Updated to version 2.0.5 and changed to build using a BuildRoot
