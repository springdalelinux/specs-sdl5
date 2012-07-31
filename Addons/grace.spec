# relative do datadir
%define type1fontdir fonts/default/Type1

Name:           grace
Version:        5.1.22
Release:        2.1%{?dist}
Summary:        Numerical Data Processing and Visualization Tool

License:        GPLv2+
# cephes is LGPL, see also Source3 and Source4
URL:            http://plasma-gate.weizmann.ac.il/Grace/
Source0:        ftp://plasma-gate.weizmann.ac.il/pub/grace/src/grace5/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.png
Source3:        cephes-license.email
Source4:        LICENSE.cephes
Patch0:         %{name}-gracerc-no_auxiliary.diff
Patch1:         %{name}-detect-netcdf.diff
Patch2:         http://ftp.de.debian.org/debian/pool/main/g/grace/grace_5.1.22-1.diff.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group:          Applications/Engineering

BuildRequires:  libjpeg-devel, libpng-devel, netcdf-devel
BuildRequires:  zlib-devel, fftw2-devel, t1lib-devel
BuildRequires:  xbae-devel, gcc-gfortran, libXmu-devel
BuildRequires:  desktop-file-utils
# to be able to generate FontDataBase
BuildRequires:  urw-fonts

#%if "%{fedora}" < "5"
#BuildRequires: xorg-x11-devel
#%else
BuildRequires: libXpm-devel
#%endif

Requires:      nedit
Requires:      xdg-utils
# /usr/share/fonts/default/Type1/
Requires:      urw-fonts

%description
Grace is a Motif application for two-dimensional data visualization.
Grace can transform the data using free equations, FFT, cross- and
auto-correlation, differences, integrals, histograms, and much
more. The generated figures are of high quality.  Grace is a very
convenient tool for data inspection, data transformation, and for
making figures for publications.


%package devel
Summary:        Files needed for grace development
Group:          Development/Libraries
License:        LGPLv2+
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
Install these files if you need to compile software that requires grace.


%prep
%setup -q
%patch0
%patch1

# avoid duplicating debian patch
%patch2 -p1
patch -p1 < debian/patches/tmpnam_to_mkstemp.diff

# remove stripping option to have meaningfull debuginfo packages
sed -i -e 's/^\(.*INSTALL_PROGRAM.*\) -s /\1 /' */Makefile
rm -rf Xbae T1lib

%build
cp %{SOURCE3} %{SOURCE4} .
%configure \
    --enable-editres \
    --with-editor=nedit \
    --with-helpviewer="xdg-open %s" \
    --with-printcmd="lpr" \
    --enable-grace-home=%{_datadir}/%{name} \
    --disable-pdfdrv \
    --with-x \
    --with-f77=gfortran \
    --with-extra-incpath=%{_includedir}/netcdf-3 \
    --with-extra-ldpath=%{_libdir}/netcdf-3 \
    --with-bundled-xbae=no

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f doc/*.1

mkdir -pm 755                               \
    %{buildroot}%{_bindir}                  \
    %{buildroot}%{_includedir}              \
    %{buildroot}%{_libdir}                  \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/apps \
    %{buildroot}%{_datadir}/applications    \
    %{buildroot}%{_mandir}/man1             \
    %{buildroot}%{_sysconfdir}/%{name}

##
# Let's have some sanity
#
pushd %{buildroot}%{_datadir}/%{name}
install -pm 755 bin/*   %{buildroot}%{_bindir}/
rm -rf bin
#ln -s %{_bindir} bin
ln -s ../../bin bin
cp -p lib/*   %{buildroot}%{_libdir}/
rm -rf lib
#ln -s %{_libdir} lib
ln -s ../../%_lib lib
install -pm 644 include/* %{buildroot}%{_includedir}/
rm -rf include
#ln -s %{_includedir} include
ln -s ../../include include
# use fonts from type1fontdir
rm -rf fonts/type1
ln -s ../../%{type1fontdir} fonts/type1
mv fonts/FontDataBase %{buildroot}%{_sysconfdir}/%{name}
#ln -s %{_sysconfdir}/%{name}/FontDataBase fonts/FontDataBase
ln -s ../../../../%{_sysconfdir}/%{name}/FontDataBase fonts/FontDataBase

# regenerate %{_sysconfdir}/%{name}/FontDataBase based on what is in
# type1fontdir and original FontDataBase content
FontDataBaseFile=%{buildroot}%{_sysconfdir}/%{name}/FontDataBase
rm -f $FontDataBaseFile.tmp
for file in %{_datadir}/%{type1fontdir}/*.pfb; do
  base=`basename $file .pfb`
  alias=
  if grep -qs $base $FontDataBaseFile; then
    # keep original aliases if the exist
    grep $base $FontDataBaseFile >> $FontDataBaseFile.tmp
  else
    # no original alias case. Use FullName from afm file and change space to -
    if [ -f %{_datadir}/%{type1fontdir}/$base.afm ]; then
      alias=`grep '^FullName' %{_datadir}/%{type1fontdir}/$base.afm | sed 's/^FullName *//' | sed 's/ *$//' | sed 's/ /-/g'`
    fi
    [ "z$alias" = 'z' ] && alias=$base
    echo "$alias $alias $base.pfb" >> $FontDataBaseFile.tmp
  fi
done
fontcount=`wc -l $FontDataBaseFile.tmp`
echo $fontcount | sed 's:%{buildroot}.*::' > $FontDataBaseFile
cat $FontDataBaseFile.tmp >> $FontDataBaseFile
rm $FontDataBaseFile.tmp

install -pm 644 doc/*.1 %{buildroot}%{_mandir}/man1/
# doc and example directories are removed from GRACE_HOME and put in %doc
rm -rf doc
#ln -s %{_docdir}/%{name}-%{version}/doc doc
ln -s ../doc/%{name}-%{version}/doc doc
rm -rf examples
#ln -s %{_docdir}/%{name}-%{version}/examples examples
ln -s ../doc/%{name}-%{version}/examples examples
# the convcal source file shouldn't be installed, it is removed here
rm -f auxiliary/convcal.c
# move config files to %{_sysconfdir} and do symlinks
for conf in gracerc templates gracerc.user; do
    mv $conf %{buildroot}%{_sysconfdir}/%{name}
    #ln -s %{_sysconfdir}/%{name}/$conf $conf
    ln -s ../../../%{_sysconfdir}/%{name}/$conf $conf
done
popd

##
# Desktop stuff
#
install -pm 644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
desktop-file-install --vendor fedora                   \
    --dir %{buildroot}%{_datadir}/applications          \
    %{SOURCE1}

# clean up docs
rm -rf __dist_doc
mkdir __dist_doc
cp -a doc __dist_doc
rm __dist_doc/doc/Makefile __dist_doc/doc/*.sgml

%clean
rm -rf %{buildroot}

%pre
# Fix broken update from old version
if [ -d /usr/share/grace/fonts/type1 ]; then
	rm -rf /usr/share/grace/fonts/type1
fi

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc ChangeLog CHANGES COPYRIGHT DEVELOPERS LICENSE README
%doc cephes-license.email LICENSE.cephes
%doc examples/ __dist_doc/doc/
%config(noreplace) %{_sysconfdir}/%{name}/
%{_bindir}/*
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/include
%exclude %{_datadir}/%{name}/lib
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/*/*
%{_mandir}/man*/*

%files devel
%defattr(-,root,root,-)
%doc grace_np/LICENSE
%{_includedir}/*
%{_datadir}/%{name}/include
%{_libdir}/libgrace_np.a
%{_datadir}/%{name}/lib


%changelog
* Sun Jan 25 2009 José Matos <jamatos@fc.up.pt> - 5.1.22-2
- Fix patch level used.

* Fri Jan 23 2009 José Matos <jamatos@fc.up.pt> - 5.1.22-1
- Upstream release (bug fixes).

* Wed Jan 23 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.21-8
- correct netcdf detection patch, thanks José.

* Wed Jan 23 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.21-7
- add support for previous netcdf version (in epel).
- drop support for monolithic X.

* Tue Jan 22 2008 Patrice Dumas <pertusus[AT]free.fr> - 5.1.21-6
- don't add the grace fonts to the X server fonts. Instead use the
  urw fonts. Regenerate the FontDataBase based on the urw fonts.
- use xdg-utils instead of htmlview.
- use relative links.
- add links to doc and examples in GRACE_HOME to have correct help.
- use debian patch.
- clean docs.

* Fri Sep 28 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.21-4
- Correctly detect netcdf (signature has changed).
- Add libXmu-devel as BR.
- Add conditional dependency on chkfontpath for <= F8.

* Thu Sep 27 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.21-3
- Remove dependency on chkfontpath, thanks to ajax for the patch. (#252277)

* Tue Aug 28 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.21-2
- License fix, rebuild for devel (F8).

* Thu Mar  8 2007 José Matos <jamatos[AT]fc.up.pt> - 5.1.21-1
- Update to 5.1.21 (#231434).
- Fix typo in description (#231435).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 5.1.20-6
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.20-5
- Fix incomplete change from pixmap to icons.

* Sun Sep 24 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.20-4
- Move icon from pixmaps to icons/highcolor/48x48/apps

* Sun Sep 24 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.20-3
- Use external xbae.
- Revert test for fedora macro so that it works by default for latest
  versions if the macro is not defined.

* Mon Sep 11 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.20-2
- Fix html documentation viewer. (#188696)

* Sun Jun 11 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.20-1
- New upstream version
- Do not ship debug files in -devel subpackage (#194769)

* Wed Apr 12 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.19-5
- Add htmlview as help viewer.

* Thu Feb 16 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.19-4
- Remove stripping option from Makefiles to have meaningfull debuginfo packages.
- Thanks to Ville Skyttä for the fix. (bz#180106)

* Thu Feb 16 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.19-3
- Unify spec file starting from FC-4.
- Rebuild for FC-5.

* Wed Feb  1 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.19-2
- Update BR from fftw to fftw2.
- Remove references to previous profile scripts.

* Fri Jan 13 2006 José Matos <jamatos[AT]fc.up.pt> - 5.1.19-1
- new upstream version
- remove name from Summary
- disable setting environment variable GRACE_HOME
- replace x11-xorg-devel by libXpm-devel in BuildRequires for FC-5.

* Mon Jan  9 2006 Patrice Dumas <dumas[AT]centre-cired.fr> - 5.1.18-7
- put config files in /etc
- licence is GPL and not BSD/GPL, as it is not dual licensed

* Wed Sep 14 2005 José Matos <jamatos[AT]fc.up.pt> - 5.1.18-6
- Require nedit as an explicit Require.

* Tue Sep 13 2005 José Matos <jamatos[AT]fc.up.pt> - 5.1.18-5
- Normalize buildroot and change default editor to nedit.

* Fri Sep  9 2005 José Matos <jamatos[AT]fc.up.pt> - 5.1.18-4
- Add license to cephes library as well as the original mail where permission is given.
- Move permission of profile.d files from 644 to 755.

* Sat Sep  3 2005 Patrice Dumas <dumas[AT]centre-cired.fr> - 5.1.18-3
- cleanup licences
- put examples/ and doc/ in %%doc
- remove duplicate manpages
- add patch to change fdf2fit path in graderc

* Sun Aug 21 2005 José Matos <jamatos[AT]fc.up.pt> - 5.1.18-2
- Add post and postun requires.

* Sat Aug 20 2005 José Matos <jamatos[AT]fc.up.pt> - 5.1.18-1

- Prepare for Fedora Extras submission, based on a previous spec file
  from Konstantin Ryabitsev (icon) and Seth Vidal from duke.edu
