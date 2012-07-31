Summary: A documentation system for C/C++
Name: doxygen16
Version: 1.6.1
Release: 6%{?dist}
Epoch: 1
Url: http://www.stack.nl/~dimitri/doxygen/index.html
Source0: ftp://ftp.stack.nl/pub/users/dimitri/doxygen-%{version}.src.tar.gz
Patch1: doxygen-1.6.0-config.patch
Patch2: doxygen-1.6.0-timestamp.patch
Group: Development/Tools
# No version is specified.
License: GPL+

BuildRequires: perl
BuildRequires: tetex-dvips
BuildRequires: tetex
BuildRequires: tetex-latex
BuildRequires: ghostscript
BuildRequires: gettext
BuildRequires: flex
BuildRequires: bison

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Doxygen can generate an online class browser (in HTML) and/or a
reference manual (in LaTeX) from a set of documented source files. The
documentation is extracted directly from the sources. Doxygen can
also be configured to extract the code structure from undocumented
source files.

%package doxywizard
Summary: A GUI for creating and editing configuration files
Group: User Interface/X
Requires: %{name} = %{epoch}:%{version}
BuildRequires: qt46-devel => 4.4

%description doxywizard
Doxywizard is a GUI for creating and editing configuration files that
are used by doxygen.

%prep
%setup -q -n doxygen-%{version}

%patch1 -p1 -b .config
%patch2 -p1 -b .timestamp

%build
unset QTDIR

./configure \
   --prefix %{_prefix} \
   --shared \
   --with-doxywizard \
   --release

# workaround for "Error: operand out of range", language.cpp needs to be splitted
%ifarch ppc64
make -C src Makefile.libdoxygen
sed -i -e "s|-o ../objects/language.o|-fno-merge-constants -fsection-anchors -o ../objects/language.o|" src/Makefile.libdoxygen
%endif

make %{?_smp_mflags} all
make docs

pushd doc
../bin/doxygen
popd

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# convert into utf-8
iconv --from=ISO-8859-1 --to=UTF-8 LANGUAGE.HOWTO > LANGUAGE.HOWTO.new
touch -r LANGUAGE.HOWTO LANGUAGE.HOWTO.new
mv LANGUAGE.HOWTO.new LANGUAGE.HOWTO

# drop -x bit
find examples -type f | xargs chmod -x

sed -i -e "s|#!perl|#! /usr/bin/perl|" examples/tag/html/installdox

# fix multilib issue
cat examples/Makefile | grep -v QTDIR | grep -v QMAKE | > examples/Makefile1
mv -f examples/Makefile1 examples/Makefile

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LANGUAGE.HOWTO README examples
%doc html
%{_bindir}/doxygen
%{_bindir}/doxytag
%{_mandir}/man1/doxygen.1*
%{_mandir}/man1/doxytag.1*

%files doxywizard
%defattr(-,root,root)
%{_bindir}/doxywizard
%{_mandir}/man1/doxywizard*

%changelog
* Tue Jul 26 2011 Than Ngo <than@redhat.com> - 1:1.6.1-6
- Resolves: bz#690076, Invalid BuildRequires on qt-devel

* Wed Jul 13 2011 Than Ngo <than@redhat.com> - 1:1.6.1-5
- Resolves: bz#690076, Invalid BuildRequires on qt-devel

* Tue Jun 29 2010 Than Ngo <than@redhat.com> - 1:1.6.1-4
- Resolves: bz#605147, fix multilib issue

* Fri Dec 18 2009 Than Ngo <than@redhat.com> - 1:1.6.1-3
- drop _default_patch_fuzz
- bz#225709, merged review

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:1.6.1-1.1
- Rebuilt for RHEL 6

* Tue Aug 25 2009 Than Ngo <than@redhat.com> - 1.6.1-1
- 1.6.1

* Mon Aug 24 2009 Than Ngo <than@redhat.com> - 1.6.0-2
- fix #516339, allow to enable/disable timstamp to avoid the multilib issue
  HTMP_TIMESTAMP is disable by default

* Fri Aug 21 2009 Than Ngo <than@redhat.com> - 1.6.0-1
- 1.6.0

* Mon Aug 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.9-3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 03 2009 Than Ngo <than@redhat.com> - 1.5.9-1
- 1.5.9

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Than Ngo <than@redhat.com> 1.5.8-1
- 1.5.8

* Mon Oct 06 2008 Than Ngo <than@redhat.com> 1.5.7.1-1
- 1.5.7.1

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.6-3
- fix license tag

* Wed May 21 2008 Than Ngo <than@redhat.com> 1.5.6-2
- rebuild

* Mon May 19 2008 Than Ngo <than@redhat.com> 1.5.6-1
- 1.5.6

* Fri Mar 14 2008 Than Ngo <than@redhat.com> 1.5.5-3
- apply patch to not break partial include paths, thanks to Tim Niemueller

* Wed Feb 20 2008 Than Ngo <than@redhat.com> 1.5.5-2
- apply patch to make doxygen using system libpng/zlib

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 1.5.5-1
- 1.5.5

* Wed Nov 28 2007 Than Ngo <than@redhat.com> 1.5.4-1
- 1.5.4

* Fri Aug 10 2007 Than Ngo <than@redhat.com> - 1:1.5.3-1
- 1.5.3

* Thu Apr 12 2007 Than Ngo <than@redhat.com> - 1:1.5.2-1
- 1.5.2

* Fri Nov 03 2006 Than Ngo <than@redhat.com> 1:1.5.1-2
- 1.5.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.7-1.1
- rebuild

* Mon Jun 12 2006 Than Ngo <than@redhat.com> 1:1.4.7-1
- update to 1.4.7

* Thu Jun 08 2006 Than Ngo <than@redhat.com> 1:1.4.6-5
- fix build problem in mock #193358 

* Fri May 12 2006 Than Ngo <than@redhat.com> 1:1.4.6-4
- apply patch to fix Doxygen crash on empty file #191392 
- html docs #187177 

* Wed Mar 08 2006 Than Ngo <than@redhat.com> 1:1.4.6-3
- fix typo bug #184400

* Mon Mar 06 2006 Than Ngo <than@redhat.com> 1:1.4.6-2
- fix build problem #184042

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.6-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.4.6-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Than Ngo <than@redhat.com> 1.4.6-1
- 1.4.6

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 1.4.5-3
- apply patch to fix build problem with gcc-4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com>
- fix references to /usr/X11R6

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- 1.4.5

* Mon Sep 19 2005 Than Ngo <than@redhat.com> 1:1.4.4-2
- move doxywizard man page to subpackge doxywizard

* Thu Jul 21 2005 Than Ngo <than@redhat.com> 1:1.4.4-1
- update to 1.4.4

* Tue Jun 14 2005 Than Ngo <than@redhat.com> 1.4.3-1
- 1.4.3

* Thu Mar 31 2005 Than Ngo <than@redhat.com> 1:1.4.2-1
- 1.4.2

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 1:1.4.1-2
- rebuilt against gcc-4

* Wed Jan 19 2005 Than Ngo <than@redhat.com> 1:1.4.1-1
- update to 1.4.1

* Sun Oct 10 2004 Than Ngo <than@redhat.com> 1:1.3.9.1-1
- update to 1.3.9.1

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 1:1.3.9-1
- update to 1.3.9

* Sun Jul 25 2004 Than Ngo <than@redhat.com> 1:1.3.8-1
- update to 1.3.8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Than Ngo <than@redhat.com> 1.3.7-1
- update to 1.3.7, bug #119340

* Sun Apr 04 2004 Than Ngo <than@redhat.com> 1:1.3.6-2
- fix qt-mt linking problem

* Thu Feb 26 2004 Than Ngo <than@redhat.com> 1:1.3.6-1
- update to 1.3.6
- added more buildrequires, #110752

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Dec 17 2003 Than Ngo <than@redhat.com> 1:1.3.5-1
- 1.3.5 release

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1:1.3.4-1
- update to 1.3.4
- doxsearch was removed

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without qt/doxywizard

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May  6 2003 Than Ngo <than@redhat.com> 1.3-1
- 1.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 27 2002 Than Ngo <than@redhat.com> 1.2.18-2
- use gnu install

* Sat Nov  9 2002 Than Ngo <than@redhat.com> 1.2.18-1.2
- fix some build problem

* Tue Oct 15 2002 Than Ngo <than@redhat.com> 1.2.18-1
- 1.2.18

* Wed Aug 28 2002 Than Ngo <than@redhat.com> 1.2.17-1
- 1.2.17 fixes many major bugs

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.13-5
- rebuild against qt 3.0.3-10

* Fri Mar  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.13-4
- rebuild against qt 3.0.2

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 1.2.14-2
- rebuild against qt 2.3.2

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.14-1
- 1.2.14

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jan 06 2002 Than Ngo <than@redhat.com> 1.2.13.1-1
- update to 1.2.13.1
- fixed build doxywizard with qt3

* Sun Dec 30 2001 Jeff Johnson <jbj@redhat.com> 1.2.13-1
- update to 1.2.13

* Sun Nov 18 2001 Than Ngo <than@redhat.com> 1.2.12-1
- update to 1.2.12
- s/Copyright/License

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Wed Jun 13 2001 Than Ngo <than@redhat.com>
- update tp 1.2.8.1
- make doxywizard as separat package
- fix to use install as default

* Tue Jun 05 2001 Than Ngo <than@redhat.com>
- update to 1.2.8

* Tue May 01 2001 Than Ngo <than@redhat.com>
- update to 1.2.7
- clean up specfile
- patch to use RPM_OPT_FLAG

* Wed Mar 14 2001 Jeff Johnson <jbj@redhat.com>
- update to 1.2.6

* Wed Feb 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Tue Dec 26 2000 Than Ngo <than@redhat.com>
- update to 1.2.4
- remove excludearch ia64
- bzip2 sources

* Mon Dec 11 2000 Than Ngo <than@redhat.com>
- rebuild with the fixed fileutils

* Mon Oct 30 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.2.3.

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.2.2.
- enable doxywizard.

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- 1.2.1 is latest stable, so we upgrade before Winston is released.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun 30 2000 Florian La Roche <laroche@redhat.de>
- fix QTDIR detection

* Fri Jun 09 2000 Preston Brown <pbrown@redhat.com>
- compile on x86 w/o optimization, revert when compiler fixed!!

* Wed Jun 07 2000 Preston Brown <pbrown@redhat.com>
- use newer RPM macros

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- add to distro.

* Tue May  9 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- recompile with current Qt (2.1.0/1.45)

* Wed Jan  5 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.0.0.
- recompile with qt-2.0.1 if available.
- relocatable package.

* Mon Nov  8 1999 Tim Powers <timp@redhat.com>
-updated to 0.49-991106

* Tue Jul 13 1999 Tim Powers <timp@redhat.com>
- updated source
- cleaned up some stuff in the spec file

* Thu Apr 22 1999 Jeff Johnson <jbj@redhat.com>
- Create Power Tools 6.0 package.
