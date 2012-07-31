Name:            libgnomedb
Epoch:           1
Version:         3.0.0
Release:         6%{?dist}
Summary:         Library for writing gnome database programs
Group:           System Environment/Libraries
License:         LGPLv2+
URL:             http://www.gnome-db.org/
Source:          http://ftp.gnome.org/pub/GNOME/sources/%{name}/3.0/%{name}-%{version}.tar.bz2
Patch0:          libgnomedb-3.0.0-64bit.patch
BuildRoot:       %{_tmppath}/%{name}-%{version}-root
BuildRequires:   libgnomeui-devel libgda-devel openssl-devel
BuildRequires:   gtksourceview-devel
BuildRequires:   gettext scrollkeeper perl(XML::Parser) desktop-file-utils
Requires:        scrollkeeper hicolor-icon-theme
Requires(pre):   GConf2
Requires(post):  GConf2 /sbin/ldconfig
Requires(preun): GConf2
Requires(postun): /sbin/ldconfig
# note we do not provide these, they no longer exist
Obsoletes:       %{name}-sharp < %{epoch}:%{version}-%{release}
Obsoletes:       %{name}-sharp-devel < %{epoch}:%{version}-%{release}

%description
libgnomedb is a library that eases the task of writing
gnome database programs.


%package devel
Summary:         Development libraries and header files for libgnomedb
Group:           Development/Libraries
Requires:        %{name} = %{epoch}:%{version}-%{release}
Requires:        pkgconfig libgnomeui-devel libgda-devel
Requires(post):  scrollkeeper
Requires(postun): scrollkeeper

%description devel
This package contains the header files and libraries needed to write
or compile programs that use libgda.


%prep
%setup -q
%patch0 -p1 -z .64bit


%build
%configure --disable-static --disable-dependency-tracking --disable-gtk-doc
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# dirty hack to make building the gtkdocs work despite us disabling rpath
export LD_LIBRARY_PATH=`pwd`/libgnomedb/.libs:`pwd`/libgnomedb/plugins/.libs:`pwd`/libgnomedb-extra/.libs:`pwd`/libgnomedb-graph/.libs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p" \
  LIBGNOMEDB_DTDDIR=%{_datadir}/libgnomedb/dtd
%find_lang libgnomedb-3.0

# below is the desktop file and icon stuff.
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --vendor fedora --remove-category Application \
  --remove-category AdvancedSettings --delete-original \
  --add-category X-GNOME-SystemSettings \
  $RPM_BUILD_ROOT%{_datadir}/applications/database-properties-3.0.desktop

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
mv $RPM_BUILD_ROOT%{_datadir}/pixmaps/gnome-db.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps

# remove unpackaged files
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/libgnomedb/plugins/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/libglade/2.0/*.la

# put the demo in -devel %%doc
mv $RPM_BUILD_ROOT/%{_datadir}/gnome-db/demo .


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/libgnomedb-3.0.schemas >/dev/null || :
fi


%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/libgnomedb-3.0.schemas > /dev/null || :
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/libgnomedb-3.0.schemas > /dev/null || :
fi


%postun
/sbin/ldconfig
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%post devel
scrollkeeper-update -q -o %{_datadir}/omf/%{name} || :


%postun devel
scrollkeeper-update -q || :


%clean
rm -rf $RPM_BUILD_ROOT


%files -f libgnomedb-3.0.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS
%{_bindir}/*
%{_datadir}/pixmaps/libgnomedb-3.0
%{_datadir}/applications/fedora-database-properties-3.0.desktop
%{_datadir}/icons/hicolor/48x48/apps/gnome-db.png
%{_datadir}/gnome-db
%{_libdir}/*.so.*
%dir %{_libdir}/libgnomedb
%{_libdir}/libgnomedb/plugins
%{_libdir}/libglade/2.0/*
%config(noreplace) %{_sysconfdir}/gconf/schemas/*

%files devel
%defattr(-,root,root,-)
%doc demo
%{_includedir}/libgnomedb-3.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgnomedb-3.0.pc
%{_libdir}/pkgconfig/libgnomedb-extra-3.0.pc
%{_libdir}/pkgconfig/libgnomedb-graph-3.0.pc
%{_datadir}/omf/%{name}
%{_datadir}/gtk-doc/html/libgnomedb-3.0


%changelog
* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.0.0-6
- Autorebuild for GCC 4.3

* Thu Dec  6 2007 Jeremy Katz <katzj@redhat.com> - 1:3.0.0-5
- rebuild for new openssl

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.0-4
- Don't rebuild the documentation to avoid multilib conflicts (bz 342141)

* Mon Aug 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.0-3
- Update License tag for new Licensing Guidelines compliance

* Fri Jun 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.0-2
- Rebuild for new gtksourceview (bz 246202)

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.0-1
- New upstream release 3.0.0
- Remove mono bindings sub-package as upstream no longer includes them

* Thu May 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-15
- Don't build mono/sharp bits on ppc64

* Mon Apr 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-14
- Fix closing of the about dialog (bz 238404)

* Tue Mar 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-13
- Fix categories in fedora-database-properties.desktop file (bz 234164)
- Fixup packaging of sharp bindings to match the mono packaging guidelines

* Thu Jan 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-12
- Install icon under /usr/share/icons and don't reference it with an
  absolute path (bz 221101)

* Sun Sep 10 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-11
- Don't own /usr/share/omf (bug 205669)

* Tue Aug 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-10
- Add a few missing (split up) mono BuildRequires
- Specfile cleanup

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-9
- FE6 Rebuild

* Sat Jun 10 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-8
- Add BuildRequires: gettext to fix building with new stripped mock config.

* Thu May  4 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-7
- Add patch3 fixing a couple of x86_64 bugs (bz 190366)

* Fri Mar 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-6
- Add patch2 fixing bz 186517

* Mon Feb 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-5
- Bump release and rebuild for new gcc4.1 and glibc
- Attempt to properly install C-sharp/mono bindings
- Add %%{?dist} for consistency with my other packages
- Remove static lib from -devel package
- Handle gconf2 files as described on the wiki scriptlets page

* Tue Jan 17 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-4
- Put mono files only in sharp package and not in sharp and main package.
- Make -sharp package Require the main package.

* Mon Jan 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-3
- Remove unneeded requires (.so reqs are automaticly picked up by rpm).
- Add BuildRequires for building libgda-sharp

* Wed Nov 30 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-2
- Add BuildRequires for optional gtksourceview, unfortunatly the
  evolution-data-server in Fedora is too new for the evolution provider.

* Sun Nov 27 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-1
- New upstream version

* Thu Aug 18 2005 Jeremy Katz <katzj@redhat.com> - 1:1.2.0-5
- rebuild for devel changes

* Fri Aug  5 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.0-4
- Remove libgnomedb.la file from devel package.

* Wed Mar 02 2005 Caolan McNamara <caolanm@redhat.com> 1.2.0-3
- rebuild with gcc4

* Mon Feb 21 2005 Caolan McNamara <caolanm@redhat.com> 1.2.0-2
- rh#149232#/rh#149222# install .desktop to /usr/share/applications

* Fri Feb 04 2005 Caolan McNamara <caolanm@redhat.com> 1.2.0-1
- bump to latest stable version
- drop integrated patchs

* Tue Dec 07 2004 Caolan McNamara <caolanm@redhat.com> 1.0.4-4
- #rh142098# missing return

* Wed Oct 20 2004 Caolan McNamara <caolanm@redhat.com> 1.0.4-3
- #rh136069# Backport crashfix on no tables
- #rh136361# Move icon for gnome properties

* Fri Oct 08 2004 Caolan McNamara <caolanm@redhat.com> 1.0.4-2
- #rh135044# BuildRequires

* Thu Aug 12 2004 Caolan McNamara <caolanm@redhat.com>
- Initial Red Hat import
- patch for missing break statement
- fixup devel package requirement pickiness

* Tue Jan 28 2003 Yanko Kaneti <yaneti@delcera.com>
- Package and add the omf/scrollkeeper bits.
- --disable-gtk-doc to configure because the generated docs are in the tarball

* Mon Aug 19 2002 Ben Liblit <liblit@acm.org>
- Fixed version number substitutions
- Updated files list to match what "make install" actually installs
- Added URL tag pointing to GNOME-DB project's web site

* Mon Feb 25 2002 Chris Chabot <chabotc@reviewboard.com>
- Cleaned up formatting
- Added requirements

* Thu Feb 21 2002 Chris Chabot <chabotc@reviewboard.com>
- Initial spec file
