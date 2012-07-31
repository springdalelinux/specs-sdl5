# $Id: mpg321.spec,v 1.2 2003/03/30 14:46:55 dude Exp $

Summary: An MPEG audio player.
Name: mpg321
Version: 0.2.10
Release: 3%{?dist}
License: GPL
Group: Applications/Multimedia
Source: http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch1: mpg321-0.2.10-security.patch
URL: http://mpg321.sourceforge.net/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libao-devel >= 0.8.0, libmad-devel >= 0.14.2b, libid3tag-devel
BuildRequires: zlib-devel
Obsoletes: mpg123

%description
mpg321 is a Free replacement for mpg123, a very popular command-line mp3
player. mpg123 is used for frontends, as an mp3 player and as an mp3 to
wave file decoder (primarily for use with CD-recording software.) In all 
of these capacities, mpg321 can be used as a drop-in replacement for
mpg123.

%prep
%setup -q
%patch1 -p1

%build
%configure --with-default-audio="alsa"
make

%install
rm -rf %{buildroot}
%makeinstall

%clean
rm -rf %{buildroot}

%files 
%defattr(-, root, root)
%doc AUTHORS BUGS ChangeLog COPYING HACKING NEWS README* THANKS TODO
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Apr 1 2007 Josko Plazonic <plazonic@math.princeton.edu>
- fix up dependencies and rebuild for 5

* Fri Jan 09 2004 Josko Plazonic <plazonic@math.princeton.edu>
- fix a small security problem

* Thu May 01 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for local use

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Mon Sep 30 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.2.10.
- Spec file cleanup.

* Tue Apr  9 2002 Bill Nottingham <notting@redhat.com> 0.2.9-3
- add patch from author to fix id3 segfaults (#62714)
- fix audio device fallback to match upstream behavior

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 0.2.9-2
- fix possible format string exploit
- add simple audio device fallback

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 0.2.9-1
- update to 0.2.9

* Thu Feb 21 2002 Bill Nottingham <notting@redhat.com>
- rebuild

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- update to 0.2.3, libmad is now separate

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- update to 0.1.5
- fix build with new libao

* Fri Jul 20 2001 Bill Nottingham <notting@redhat.com>
- initial build
