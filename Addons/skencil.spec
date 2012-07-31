Name:           skencil
Version:        0.6.17
Release:	10%{?dist}

Summary:        Vector drawing program

Group:          Applications/Multimedia
License:        LGPL, GPL, Historical Permission Notice and Disclaimer
URL:            http://www.skencil.org
Source0:        http://dl.sf.net/sketch/skencil-0.6.17.tar.gz
Source1:        skencil-logo.png
Patch0:         skencil-0.6.17-fonts.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:	python-imaging-devel
BuildRequires:	PyXML
BuildRequires:  tk-devel
BuildRequires:  tcl-devel
BuildRequires:	libXext-devel
BuildRequires:	libX11-devel
BuildRequires:  desktop-file-utils
Requires:       tkinter
Requires:	python-imaging
Requires:	PyXML
Requires:       xorg-x11-fonts-Type1
Requires:       urw-fonts
Requires:       ghostscript-fonts
Requires:       xorg-x11-fonts-75dpi
Requires:       xorg-x11-fonts-ISO8859-1-75dpi
Requires(post):   shared-mime-info, desktop-file-utils
Requires(postun): shared-mime-info, desktop-file-utils

%description
Skencil is an interactive vector drawing program for X (similar to XFig
or tgif). It is written almost completely in Python, an object oriented
interpreted programming language.

Skencil was originally named "Sketch" (it was renamed with release
0.6.16) and the name "Sketch" is still used in many places.


%prep
%setup -q
%patch0 -p1
grep -rl lib/ . | xargs perl -pi -e's,lib/,%{_lib}/,g'
grep -rl lib\' . | xargs perl -pi -es,lib\',%{_lib}\',g

%build
find \( -name \*.sk -or -name \*.ppm -or -name \*.jpg \) -exec chmod 644 \{\} \;
%{__python} setup.py configure --with-nls
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --prefix=%{_prefix} --dest-dir=$RPM_BUILD_ROOT
install -p Tools/mkfontdb.py $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/
ln -s %{_libdir}/%{name}-%{version}/mkfontdb.py $RPM_BUILD_ROOT%{_bindir}/mkfontdb
install -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/pixmaps/skencil-logo.png

cat > skencil.desktop <<EOF
[Desktop Entry]
Name=Skencil
GenericName=A vector drawing program
Comment=The Skencil vector drawing program
Exec=skencil
Icon=skencil-logo.png
Terminal=false
Type=Application
Encoding=UTF-8
X-Desktop-File-Install-Version=0.9
MimeType=image/x-sk
StartupNotify=true
StartupWMClass=Sketch
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/packages
cat > $RPM_BUILD_ROOT%{_datadir}/mime/packages/skencil.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="image/x-sk">
        <comment xml:lang="en">Skencil document</comment>
        <glob pattern="*.sk"/>
  </mime-type>
</mime-info>
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora                     \
        --add-category X-Fedora                          \
        --add-category Application                       \
        --add-category Graphics                          \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications    \
        skencil.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%postun
%{_bindir}/update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :

%files
%defattr(-,root,root,-)
%doc Doc Examples Misc README INSTALL BUGS CREDITS COPYING TODO PROJECTS FAQ NEWS
%doc --parents */README */COPYING
%{_libdir}/skencil-*
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/mime/packages/*


%changelog
* Sat Feb  3 2007 Gerard Milmeister <gemi@bluewin.ch> - 0.6.17-10
- fix font files

* Sat Feb  3 2007 Gerard Milmeister <gemi@bluewin.ch> - 0.6.17-9
- fix font paths

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.6.17-8
- Rebuild for FE6

* Sat Feb 18 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.6.17-7
- Removed xorg-x11-devel dependency

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 0.6.17-5
- Rebuild for Fedora Extras 5

* Mon Aug 15 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.6.17
- New Version 0.6.17
- patch no longer necessary

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.6.16-6
- add patch from upstream bug 10345 to fix build with python2.4 (#158408)

* Wed May 25 2005 Jeremy Katz <katzj@redhat.com> - 0.6.16-5
- buildrequire desktop-file-utils (ignacio, #156245)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.6.16-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Feb 22 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.6.16-2
- Remove buildroot paths from within python compiled code.
- Some minor standard spec fixes.
- Parts of the skencil package are licenced differently than LGPL
  (looked one up via opensource.org).

* Mon Feb 14 2005 Gerard Milmeister <gemi@bluewin.ch> - 0.6.16-1
- First release for Extras
- Added mime type, icon and desktop file

* Thu Mar  4 2004 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Sync with embedded specfile (Andrew Grimberg <tykeal@bardicgrove.org>)
- Symlinks to %%{_bindir} are without extension now
- Add mkfontdb.py.
- Remove --imaging-include switch, folder is autodetected.

* Sun Feb 29 2004 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Initial build.

