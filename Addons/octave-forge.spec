%{!?octave_api: %define octave_api %(octave-config -p API_VERSION || echo 0)}

Name:           octave-forge
Version:        20071212
Release:        6.1%{?dist}
Summary:        Contributed functions for octave

Group:          Applications/Engineering
License:        GPLv2+ and Public Domain
URL:            http://octave.sourceforge.net
## Source0:        http://downloads.sourceforge.net/sourceforge/octave/%{name}-bundle-%{version}.tar.gz
## The original sources contain a non-free tree of functions that are
## GPL incompatible. A patched version with the non-free sources removed
## is created as follows:
## tar xzf octave-forge-bundle-%{version}.tar.gz
## rm -Rf octave-forge-bundle-%{version}/nonfree/
## tar czf octave-forge-bundle-%{version}.patched.tar.gz octave-forge-bundle-%{version}
## rm -Rf octave-forge-bundle-%{version}
Source0:        %{name}-bundle-%{version}.patched.tar.gz
buIldRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	octave(api) = %{octave_api} ImageMagick
BuildRequires:  octave-devel >= 6:3.0.0-1
BuildRequires:  tetex gcc-gfortran ginac-devel qhull-devel
BuildRequires:  ImageMagick-c++-devel libnc-dap-devel pcre-devel gsl-devel
BuildRequires:  libjpeg-devel libpng-devel ncurses-devel
BuildRequires:  openssl-devel java-devel-gcj dos2unix
Provides: octave-audio = 1.0.2
Provides: octave-combinatorics = 1.0.3
Provides: octave-communications = 1.0.3
Provides: octave-control = 1.0.2
Provides: octave-econometrics = 1.0.3
Provides: octave-fixed = 0.7.3
Provides: octave-general = 1.0.3
Provides: octave-gsl = 1.0.2
Provides: octave-ident = 1.0.2
Provides: octave-image = 1.0.3
Provides: octave-informationtheory = 0.1.2
Provides: octave-io = 1.0.3
Provides: octave-irsa = 1.0.2
Provides: octave-linear-algebra = 1.0.2
Provides: octave-miscellaneous = 1.0.3
Provides: octave-nnet = 0.1.4
Provides: octave-octcdf = 1.0.6
Provides: octave-odebvp = 1.0.1
Provides: octave-odepkg = 0.3.3
Provides: octave-optim = 1.0.0
Provides: octave-optiminterp = 0.2.4
Provides: octave-outliers = 0.13.4
%ifnarch x86_64 ppc64
Provides: octave-parallel = 1.0.3
%endif
Provides: octave-physicalconstants = 0.1.2
Provides: octave-plot = 1.0.2
Provides: octave-signal = 1.0.4
Provides: octave-sockets = 1.0.2
Provides: octave-specfun = 1.0.3
Provides: octave-special-matrix = 1.0.2
Provides: octave-splines = 1.0.2
Provides: octave-statistics = 1.0.3
Provides: octave-strings = 1.0.2
Provides: octave-struct = 1.0.2
Provides: octave-symbolic = 1.0.3
Provides: octave-time = 1.0.2
Provides: octave-vrml = 1.0.3
Provides: octave-zenity = 0.5.2
Provides: octave-bim = 0.0.2
Provides: octave-civil-engineering = 1.0.2
Provides: octave-fpl = 0.0.2
Provides: octave-graceplot = 1.0.2
Provides: octave-integration = 1.0.2
Provides: octave-java = 1.2.1
Provides: octave-mapping = 1.0.2
Provides: octave-msh = 0.0.2
Provides: octave-nan = 1.0.2
Provides: octave-pdb = 1.0.2
Provides: octave-secs1d = 0.0.3
Provides: octave-secs2d = 0.0.3
Provides: octave-symband = 1.0.3
Provides: octave-tcl-octave = 0.1.3
Provides: octave-triangular = 1.0.1
Provides: octave-tsa = 3.10.3
Provides: octave-xraylib = 1.0.3
Provides: octave-language-pt_br = 1.0.3

%description
Octave-forge is a community project for collaborative development of
Octave extensions. The extensions in this package include additional
data types, and functions for a variety of different applications
including signal and image processing, communications, control,
optimization, statistics, and symbolic math.


%prep
%setup -q -n octave-forge-bundle-%{version}
#Not 64-bit safe
%ifarch x86_64 ppc64
rm main/parallel-*.tar.gz
%endif
#Don't install engine - not a real octave package
rm extra/engine-*.tar.gz
#Can't handle jhandles yet
rm extra/jhandles-*.tar.gz
#Not MacOSX
rm extra/macosx-*.tar.gz
#Not Windows
rm extra/windows-*.tar.gz

#Unpack everything
for pkg in main extra language
do
   cd $pkg
   for tgz in *.tar.gz
   do
      tar xzf $tgz

      #Collect provides
      echo $tgz | sed 's/\(.*\)-\([0-9]*\.[0-9]*\.[0-9]*\)\.tar\.gz/Provides: octave-\1 = \2/' >> ../octave-forge-provides
   done
   cd ..
done

# edit.m is now in octave
rm main/miscellaneous-1.0.4/inst/edit.m

#Cleanup some CVS directories
find -name CVS | xargs rm -rf

#Install with -nodeps
sed -i -e "s/pkg('install',/pkg('install','-nodeps',/" */*/Makefile

#Fix permissions
find -name COPYING -o -name INDEX -o -name DESCRIPTION -o -name \*.m | xargs chmod -x

#Fix line endings
find -name \*.m | xargs dos2unix


%build
#Prevents escape sequence from being inserted into octave version string
export TERM=""
for pkg in main extra language
do
   cd $pkg
   for dir in *.[0-9]
   do
      cd $dir
      if [ -f configure ]
      then
         %configure
      elif [ -f src/configure ]
      then
         cd src
         %configure
         cd ..
      fi
      if [ -f Makefile ]
      then
         make TMPDIR=%{_tmppath}
      elif [ -f src/Makefile ]
      then
         cd src
         make TMPDIR=%{_tmppath}
         cd ..
      fi
      cd ..
   done
   cd ..
done
   

%install
rm -rf $RPM_BUILD_ROOT
export TERM=""

for pkg in main extra language
do
   cd $pkg
   for dir in *.[0-9]
   do
       cd $dir
       make install TMPDIR=%{_tmppath} DESTDIR=$RPM_BUILD_ROOT DISTPKG=redhat
       cd ..
   done
   cd ..
done

#Move aurecord to arch-dependent dir
archdir=%{_libexecdir}/octave/packages/`octave-config -p CANONICAL_HOST_TYPE`-%{octave_api}
audiover=`basename $RPM_BUILD_ROOT%{_datadir}/octave/packages/audio-*`
mkdir -p $RPM_BUILD_ROOT${archdir}/${audiover}
mv $RPM_BUILD_ROOT%{_datadir}/octave/packages/${audiover}/bin \
   $RPM_BUILD_ROOT${archdir}/${audiover}/


%clean
rm -rf $RPM_BUILD_ROOT


%post
octave -q -H --no-site-file --eval "pkg('rebuild');"

%postun
octave -q -H --no-site-file --eval "pkg('rebuild');"


%files
%defattr(-,root,root,-)
%{_datadir}/octave/packages/*
%{_libexecdir}/octave/packages/*


%changelog
* Thu Jan 10 2008 Quentin Spencer <qspencer@users.sf.net> 20071212-6
- Port 20071212 changes from devel branch for compatibility with octave 3.0.0.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2006.07.09-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 23 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-6
- Rebuild for updated libdap.

* Fri Sep 15 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-5
- Rebuild for FC6.

* Fri Aug 25 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-4
- New build for octave 2.9.8.
- Patch bug in imread.m
- Patch LOADPATH bug.
- Fix configure command so that m files containing paths are
  correctly generated.

* Tue Jul 11 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-3
- New build for octave 2.9.7.
- Disable mex related functions (they are in octave now).

* Tue Jul 11 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-2
- Patch legend.m.

* Mon Jul 10 2006 Quentin Spencer <qspencer@users.sf.net> 2006.07.09-1
- New release. Old patches and associated specfile cruft removed.

* Wed May  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-4
- Bug fix for #190481

* Thu Apr 27 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-3
- Add fixes for octcdf (from the author), which changes the dependency
  from netcdf to libnc-dap. (This requires autoconf temporarily.)

* Wed Apr 19 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-2
- New release for octave 2.9.5.
- Patch added for incompatibilities between octave 2.9.4 and 2.9.5.

* Fri Mar 17 2006 Quentin Spencer <qspencer@users.sf.net> 2006.03.17-1
- New release. Remove old patches.

* Sat Feb 18 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-5
- Amend patch0 to correctly deal with 64-bit indexing.

* Thu Feb 16 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-4
- Patch the fixed point code so that g++ 4.1 compiles it.

* Fri Feb  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-3
- Fix permissions on octlink.sh and add more to the patch.

* Fri Feb  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-2
- Add new build dependencies on ImageMagick-c++-devel and netcdf-devel.
  (The ImageMagick-c++-devel indirectly brings in the necessary
  modular X devel modules, such as libXt-devel and others).
- Define CPPFLAGS so it finds the netcdf headers.

* Fri Feb  3 2006 Quentin Spencer <qspencer@users.sf.net> 2006.01.28-1
- New upstream release.
- Patch so it will build correctly with octave 2.9.x.
- Change installation paths so they now depend on the octave API version
  rather than the octave version, which will make updates less frequent.

* Wed Nov  2 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-5
- Rebuild for new versions of ginac and cln.
- Query octave to get octave version dependency.

* Wed Aug  3 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-4
- Hardcode the octave version dependency. Using rpm to query for this
  information was producing wrong results on the new build system.

* Wed Aug  3 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-3
- Remove some BuildRequires that are now dependencies of octave-devel.

* Tue Aug  2 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-2
- Change GiNaC-devel to ginac-devel to reflect package name change.

* Fri Jun 17 2005 Quentin Spencer <qspencer@users.sf.net> 2005.06.13-1
- New upstream release. Now requires pcre-devel to build.
- Corrected instructions on creating patched source tarball.
- Remove explicit BuildRequires for c++ compiler and libs
  (not needed and causes build failure in the build system for x86_64).
- Add patch for problem with main/plot/legend.m
- Add fftw3-devel to BuildRequires.

* Sat Jun 11 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-7
- Cleanup of unneeded things in build section

* Mon Apr 25 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-7
- Changed license (some functions are GPL, BSD, and public domain,
  so the collection is licensed as public domain).
- Moved ugly path hacks from build to install so that RPM_BUILD_ROOT
  doesn't end up in the code (which it did before).
- Replaced upstream tarball with patched version that removed GPL
  incompatible code.

* Thu Apr 21 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-6
- Added GiNaC-devel BuildRequires

* Tue Mar 29 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-5
- Rebuild for octave-2.1.69

* Mon Mar 28 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-4
- Rebuild for octave-2.1.68

* Thu Feb 24 2005 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-3
- Updated spec file to get octave version at build time.

* Wed Nov 17 2004 Quentin Spencer <qspencer@users.sf.net> 2004.11.16-2
- Revised package description.

* Tue Jun 15 2004 Quentin Spencer <qspencer@users.sf.net>
- Added qhull support.

* Tue Feb  4 2003 Quentin Spencer <qspencer@users.sf.net>
- First Version, loosely based on Red Hat's spec file for octave.
