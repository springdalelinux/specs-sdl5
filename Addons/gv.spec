Summary: A X front-end for the Ghostscript PostScript(TM) interpreter
Name: gv
Version: 3.6.2
Release: 2%{?dist}
License: GPL
Group: Applications/Publishing
Requires: ghostscript
URL: http://www.gnu.org/software/gv/
Source0: ftp://ftp.gnu.org/gnu/gv/gv-%{version}.tar.gz
Patch0: gv-3.5.8-buffer.patch
Patch1: gv-3.6.1-pkglibdir.patch
Patch2: gv-3.6.2-CVE-2006-5864.patch
BuildRequires: /usr/bin/makeinfo
BuildRequires: Xaw3d-devel, /usr/bin/desktop-file-install
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/install-info, /usr/bin/update-mime-database
Requires(post): /usr/bin/update-desktop-database
Requires(preun): /sbin/install-info
Requires(postun): /usr/bin/update-mime-database
Requires(postun): /usr/bin/update-desktop-database


%description
Gv is a user interface for the Ghostscript PostScript(TM) interpreter.
Gv can display PostScript and PDF documents on an X Window System.


%prep
%setup -q
%patch0 -p1 -b .buffer
%patch1 -p1 -b .pkglibdir
%patch2 -p1 -b .CVE-2006-5864


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Still provide link
ln $RPM_BUILD_ROOT%{_bindir}/gv $RPM_BUILD_ROOT%{_bindir}/ghostview

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

cat > gv.desktop <<EOF
[Desktop Entry]
Name=Ghostview PostScript/PDF Viewer
GenericName=PostScript/PDF Viewer
Comment="View PostScript and PDF files"
Type=Application
Icon=postscript-viewer.png
MimeType=application/postscript;application/pdf;
StartupWMClass=GV
Exec=gv
EOF

desktop-file-install --vendor=fedora \
       --add-category=Applications\
       --add-category=Graphics \
       --add-category=X-Fedora \
       --dir %{buildroot}%{_datadir}/applications/ \
       gv.desktop

# Remove info dir file
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/usr/bin/update-mime-database /usr/share/mime > /dev/null 2>&1 || :
/usr/bin/update-desktop-database /usr/share/applications > /dev/null 2>&1 || :


%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%postun
if [ $1 = 0 ]; then
    /usr/bin/update-mime-database /usr/share/mime > /dev/null 2>&1 || :
    /usr/bin/update-desktop-database /usr/share/applications > /dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/ghostview
%{_bindir}/gv
%{_datadir}/gv/
%{_datadir}/applications/fedora-gv.desktop
%{_datadir}/info/gv.info.gz
%{_mandir}/man1/gv.*

%changelog
* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.2-2
- Apply patch from Mandriva to fix CVE-2006-5864/bug 215136

* Wed Oct 11 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.2-1
- Update to 3.6.2

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.1-8
- Rebuild for FC6

* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.1-7
- Rebuild for gcc/glibc changes

* Wed Feb  1 2006 Orion Poplawski <orion@cora.nwra.com> 3.6.1-6
- Remove info dir file

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-5
- Rebuild

* Thu Oct 27 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-4
- Add patch find app defaults file (#171848)
- Add BR: /usr/bin/makeinfo to properly build .info file (#171849)

* Thu Oct 20 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-3
- Fixup .desktop file, add Comment and StartupWMClass

* Thu Oct 20 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-2
- Trim install paragraph from Description
- Add MimeType to desktop and update mime and desktop databases
- Fix info file handling

* Mon Oct 17 2005 Orion Poplawski <orion@cora.nwra.com> 3.6.1-1
- Updated to 3.6.1
- Fedora Extras version

* Sun Sep 19 2004 Dan Williams <dcbw@redhat.com> 3.5.8-29
- Fix .desktop file (#125849)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 14 2004 Dan Williams <dcbw@redhat.com> 3.5.8-27
- display empty page when input file has size 0 (#100538)

* Fri May 14 2004 Dan Williams <dcbw@redhat.com> 3.5.8-26
- fix argv array size (#80672)

* Tue May  4 2004 Bill Nottingham <notting@redhat.com> 3.5.8-25
- fix desktop file (#120190)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 3.5.8-21
- rebuild on all arches

* Tue Nov 19 2002 Bill Nottingham <notting@redhat.com> 3.5.8-20
- rebuild

* Tue Sep 24 2002 Bill Nottingham <notting@redhat.com>
- fix handling of certain postscript/pdf headers
- use mkstemp

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Bill Nottingham <notting@redhat.com>
- remove anti-aliasing change; it causes problems

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Fri Jan 25 2002 Bill Nottingham <notting@redhat.com>
- fix anti-aliasing (#58686)

* Fri Jul 13 2001 Bill Nottingham <notting@redhat.com>
- fix some build issues (#48983, #48984)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- add filename quoting patch from debian
- rebuild in new build environment

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new libXaw3d

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Mon Jan 23 1999 Michael Maher <mike@redhat.com>
- fixed bug #272, changed group

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built pacakge for 6.0

* Sat Aug 15 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Thu Nov 06 1997 Cristian Gafton <gafton@redhat.com>
- we are installin a symlink to ghostview

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- updated to 3.5.8

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 15 1997 Erik Troan <ewt@redhat.com>
- added ghostscript requirement, added errlist patch for glibc.
