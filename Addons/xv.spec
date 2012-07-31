
%{!?dist:%define _with_modxorg 1}
%{?el5:  %define _with_modxorg 1}
%{?fc6:  %define _with_modxorg 1}
%{?fc5:  %define _with_modxorg 1}

Summary: An X based image file viewer and manipulator.
Name: xv
Version: 3.10a
Release: 26%{?dist}
License: Shareware
Group: Amusements/Graphics
Source0: ftp://ftp.cis.upenn.edu/pub/xv/xv-%{version}.tar.gz
Source1: xv-3.10a-jumbo-README.txt
Source2: xv.desktop
Patch1: xv-3.10a-jumbo-fix-patch-20050410.txt
Patch2: xv-3.10a-jumbo-enh-patch-20050501.txt
Url: http://www.trilon.com/xv/xv.html
BuildRoot: %{_tmppath}/%{name}-%{version}-root
%{?_with_modxorg:BuildRequires: libXt-devel, libXv-devel, libGL-devel, libGLU-devel, libXinerama-devel, libXvMC-devel}
%{!?_with_modxorg:BuildRequires: XFree86-devel}
%{!?_with_modxorg:%{!?_without_xvmc:BuildRequires: libXvMCW-devel}}
BuildRequires: libjpeg-devel zlib-devel libtiff-devel libpng-devel

%package docs
Summary: Document to xv
Requires: xv, ghostscript
Group: Amusements/Graphics

%description
Xv is an image display and manipulation utility for the X Window
System.  Xv can display GIF, JPEG, TIFF, PBM, PPM, X11 bitmap, Utah
Raster Toolkit RLE, PDS/VICAR, Sun Rasterfile, BMP, PCX, IRIS RGB, XPM,
Targa, XWD, PostScript(TM) and PM format image files.  Xv is also
capable of image manipulation like cropping, expanding, taking
screenshots, etc.

%description docs
Xv is an image display and manipulation utility for the X Window
System.  Xv can display GIF, JPEG, TIFF, PBM, PPM, X11 bitmap, Utah
Raster Toolkit RLE, PDS/VICAR, Sun Rasterfile, BMP, PCX, IRIS RGB, XPM,
Targa, XWD, PostScript(TM) and PM format image files.  Xv is also
capable of image manipulation like cropping, expanding, taking
screenshots, etc.

This package contains the document to xv.

%prep
%setup -q 
%patch1 -p1
%patch2 -p1
cp %{SOURCE1} .

# stuff from gentoo
        sed -i  -e 's/\(^JPEG.*\)/#\1/g' \
                        -e 's/\(^PNG.*\)/#\1/g' \
                        -e 's/\(^TIFF.*\)/#\1/g' \
                        -e 's/\(^LIBS = .*\)/\1 $(LDFLAGS) /g' Makefile

        # /usr/bin/gzip => /bin/gzip
        sed -i  -e 's#/usr\(/bin/gzip\)#\1#g' config.h

        # fix installation of ps docs.
        sed -i -e 's#$(DESTDIR)$(LIBDIR)#$(LIBDIR)#g' Makefile


%build
%if %{?_with_modxorg}
make CCOPTS="-O -DUSE_GETCWD -DLINUX -DUSLEEP -DDOJPEG -DDOPNG -DDOTIFF -DUSE_TILED_TIFF_BOTLEFT_FIX" LDFLAGS="-L/usr/X11R6/%{_lib} -ljpeg -lz -lpng -ltiff" LIBDIR=/usr/%{_lib}
%else
make CCOPTS="-O -DUSE_GETCWD -DLINUX -DUSLEEP -DDOJPEG -DDOPNG -DDOTIFF -DUSE_TILED_TIFF_BOTLEFT_FIX" LDFLAGS="-L/usr/%{_lib} -ljpeg -lz -lpng -ltiff" LIBDIR=/usr/%{_lib}
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}/man1 \
	$RPM_BUILD_ROOT%{_docdir}/%{name}

make	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	LIBDIR=$RPM_BUILD_ROOT%{_docdir}/%{name} \
	install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/xv.desktop

# we don't need it
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}/xvdocs.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README BUGS CHANGELOG IDEAS xv-3.10a-jumbo-README.txt
#%config /etc/X11/applnk/Graphics/xv.desktop
%{_datadir}/xv.desktop
%{_bindir}/*
%{_mandir}/man1/*

%files docs
%defattr(-,root,root)
%doc docs/{bmp.doc,epsf.ps,gif.ack,gif.aspect,gif87.doc,gif89.doc}
%doc docs/{help,xpm.ps,vdcomp.man,penn.policy,xv.ann,xv.blurb}
%doc docs/xvdocs.ps

%changelog
* Mon Apr 02 2007 Josko Plazonic <plazonic@math.princeton.edu>
- try to build for 5

* Sun Jul 02 2006 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt with jumbo patches

* Thu May 10 2004 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS 1, added 64 bit fixes

* Thu May 01 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for RH 9 with appropriate desktop icon

* Wed Aug 02 2000 Than Ngo <than@redhat.de>
- rebuilt against new libpng

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Than Ngo <than@redhat.de>
- use %%{_docdir}

* Tue Jul 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix doc inclusion

* Tue Jul 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't use /usr/doc directly
- use %%{_tmppath}

* Mon Jul 03 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed May 31 2000 Than Ngo <than@redhat.de>
- split into xv and xv-docs packages (Bug#11043)

* Tue May 30 2000 Ngo Than
- rebuild for 7.0
- gzip man pages
- remove wmconfig, add xv.desktop

* Fri Jul 30 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Fri Apr 23 1999 Bill Nottingham <notting@redhat.com>
- build for powertools
- apply a pile of patches

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 22 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry 

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- various spec file cleanups
- added patch to manipulate PNG files

* Mon Aug 25 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- incorporated new jpegv6 patch from the author's web site
