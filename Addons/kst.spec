Name:       kst
Version:    1.4.0
Release:    8%{?dist}
Summary:    A data viewing program for KDE

Group:      Applications/Engineering
License:    GPLv2+
URL:        http://kst.kde.org/
Source0:    ftp://ftp.kde.org/pub/kde/stable/apps/KDE3.x/scientific/kst-%{version}.tar.gz
Patch:      fix-open.diff
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: gettext 
BuildRequires: gsl-devel readline-devel ncurses-devel
BuildRequires: kdelibs-devel kdebindings-devel
BuildRequires: cfitsio-devel netcdf-devel
BuildRequires: desktop-file-utils

%description
Kst is a real-time data viewing and plotting tool with basic data analysis 
functionality. Kst contains many powerful built-in features and is 
expandable with plugins and extensions. Kst is a KDE application.

Main features of kst include:
  * Robust plotting of live "streaming" data.
  * Powerful keyboard and mouse plot manipulation.
  * Powerful plugins and extensions support.
  * Large selection of built-in plotting and data manipulation functions, 
    such as histograms, equations, and power spectra.
  * Color mapping and contour mapping capabilities for three-dimensional data.
  * Monitoring of events and notifications support.
  * Filtering and curve fitting capabilities.
  * Convenient command-line interface.
  * Powerful graphical user interface.
  * Support for several popular data formats.
  * Multiple tabs or windows. 

%package docs
Summary:    Documentation for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}

%description docs
Documentation, tutorial, and sample data for kst.

%package devel
Summary:    Development libraries and headers for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}

%description devel
Headers and libraries required when building against kst.

%package netcdf
Summary:    netcdf datasource plugin for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}

%description netcdf
A plugin allowing kst to open and read data in netcdf format.

%package fits
Summary:    fits datasource plugin for kst
Group:      Applications/Engineering
Requires:   %{name} = %{version}-%{release}
# Hack because cfitsio won't run if it's internal library version
# doesn't perfectly match between installed library and compiled
# against library.  Meh.
Requires:   cfitsio = %(rpm -q cfitsio --qf %{V})

%description fits
A plugin allowing kst to open and read data and images contained within 
fits files.  This includes healpix encoded fits files, and lfiio data.

%prep
%setup -q
%patch -p1

%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export KDEDIR=%{_prefix}
%configure --disable-dependency-tracking --disable-static \
  --disable-rpath \
  --with-qt-libraries=$QTDIR/lib \
  --with-qt-includes=$QTDIR/include \
  --with-extra-includes=%{_includedir}/cfitsio:%{_includedir}/netcdf-3 \
  --with-extra-libs=%{_libdir}:%{_libdir}/netcdf-3 --disable-debug
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make DESTDIR=%{buildroot} SUID_ROOT="" install

# Delete the nasty little .la files
# which we can't do as kst doesn't run without them.
#find %{buildroot} -wholename '*.la' | xargs rm -f

# Delete wmap and scuba2 datasources; it's a packaging bug at the 
# kst upstream end that they are installed in 1.4.0 (they are unfinished).
rm -f  %{buildroot}/%{_libdir}/kde3/kstdata_scuba.la \
       %{buildroot}/%{_libdir}/kde3/kstdata_scuba.so \
       %{buildroot}/%{_libdir}/kde3/kstdata_wmap.la \
       %{buildroot}/%{_libdir}/kde3/kstdata_wmap.so \
       %{buildroot}/%{_datadir}/services/kst/kstdata_scuba.desktop \
       %{buildroot}/%{_datadir}/services/kst/kstdata_wmap.desktop

%find_lang %{name}

# Make documentation symlinks relative
for x in %{buildroot}%{_defaultdocdir}/HTML/*/%{name}/
do
  ln -sf ../common $x
done

# Move desktop file to proper location
desktop-file-install --vendor=fedora \
  --add-category X-Fedora \
  --add-category Graphics \
  --add-category Qt \
  --add-category KDE \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applnk/Applications/Sciences/kst.desktop

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog INSTALL AUTHORS README COPYING kst/RELEASE.NOTES kst/NEWS

#binaries
%{_bindir}/kst
%{_bindir}/kstcmd
%{_bindir}/d2asc
#libraries
%{_libdir}/lib*.so.*
%{_libdir}/lib*.la
#update
%{_datadir}/apps/kconf_update/kstautosave11.upd
%{_datadir}/apps/kconf_update/kstrcmisc11.upd
#fonts
%dir %{_datadir}/apps/kst
%{_datadir}/apps/kst/fonts
#data plugins
%{_libdir}/kde3/kstdata_ascii.*
%{_libdir}/kde3/kstdata_dirfile.*
%{_libdir}/kde3/kstdata_frame.*
%{_libdir}/kde3/kstdata_indirect.*
%{_libdir}/kde3/kstdata_qimagesource.*
%{_datadir}/services/kst/kstdata_ascii.desktop
%{_datadir}/services/kst/kstdata_dirfile.desktop
%{_datadir}/services/kst/kstdata_frame.desktop
%{_datadir}/services/kst/kstdata_indirect.desktop
%{_datadir}/services/kst/kstdata_qimagesource.desktop
%{_datadir}/services/kst/kstobject_*.desktop
%{_datadir}/servicetypes/kst/kstdatasourceplugin.desktop
%{_datadir}/servicetypes/kst/kstbasicplugin.desktop
%{_datadir}/servicetypes/kst/kstdataobjectplugin.desktop
#plugins
%{_libdir}/kde3/kstplugins
%{_libdir}/kde3/kstobject_*
%dir %{_datadir}/servicetypes/kst
%{_datadir}/servicetypes/kst/kstplugin.desktop
%{_datadir}/servicetypes/kst/kstfilter.desktop
%{_libdir}/kde3/plugins/designer/
#extensions
%{_libdir}/kde3/kstextension_*
%dir %{_datadir}/services/kst
%{_datadir}/services/kst/kstextension_*.desktop
%{_datadir}/apps/kst/kstextension_*.rc
%{_datadir}/servicetypes/kst/kstextension.desktop
# UI file
%{_datadir}/apps/kst/kstui.rc
#desktop file
%{_datadir}/mimelnk/application/x-kst.desktop
%{_datadir}/applications/fedora-kst.desktop
#icons
%{_datadir}/icons/hicolor/22x22/actions/*.png
%{_datadir}/icons/locolor/16x16/apps/kst.png
%{_datadir}/icons/locolor/32x32/apps/kst.png
%{_datadir}/icons/hicolor/16x16/mimetypes/kst.png
%{_datadir}/icons/hicolor/32x32/mimetypes/kst.png
%{_datadir}/icons/locolor/16x16/mimetypes/kst.png
%{_datadir}/icons/locolor/32x32/mimetypes/kst.png
%{_datadir}/apps/kst/pics/*.png
#other
%{_datadir}/config/colors
%{_mandir}/man1/kst.1.gz

%files devel
%defattr(-,root,root)
%{_includedir}/kstdatasource.h
%{_includedir}/kstobject.h
%{_includedir}/kst_export.h
%{_includedir}/kstsharedptr.h
%{_includedir}/rwlock.h
%{_includedir}/kstdateparser.h
%{_includedir}/kstwaitcondition.h
%{_includedir}/kstext*.h
%{_includedir}/kstobjectcollection.h
%{_libdir}/lib*.so

%files docs
%defattr(-,root,root)
%{_datadir}/doc/HTML/*/kst
%{_datadir}/apps/kst/tutorial

%files fits
%defattr(-,root,root)
%{_libdir}/kde3/kstdata_fitsimage.*
%{_libdir}/kde3/kstdata_healpix.*
%{_libdir}/kde3/kstdata_lfiio.*
%{_datadir}/services/kst/kstdata_fitsimage.desktop
%{_datadir}/services/kst/kstdata_healpix.desktop
%{_datadir}/services/kst/kstdata_lfiio.desktop

%files netcdf
%defattr(-,root,root)
%{_libdir}/kde3/kstdata_netcdf.*
%{_datadir}/services/kst/kstdata_netcdf.desktop

%changelog
* Tue Aug 21 2007 Matthew Truch <matt at truch.net> - 1.4.0-8
- Add patch to fix open() call that was not compliant.  

* Thu Aug 2 2007 Matthew Truch <matt at truch.net> - 1.4.0-7
- Update License tag

* Mon Jul 23 2007 Matthew Truch <matt at truch.net> - 1.4.0-6
- Readd kdebindings-devel: KDE4 slipped; will readjust when appropriate.

* Mon Jul 23 2007 Matthew Truch <matt at truch.net> - 1.4.0-5
- kst never needed BR kdebase-devel
- Change BR to kdelibs3-devel for upcoming switch to KDE4 as primary.
- Remove BR kdebindings-devel; kst will use it's internal bindings which
  should suffice until kst 2.0 is released (and switch to KDE4).  
- Fix typo in version of Jesse's changelog entry below from 1.3.0-4 to 1.4.0-4

* Thu Jul 19 2007 Jesse Keating <jkeating@redhat.com> - 1.4.0-4
- Rebuild for new cfitsio

* Tue May 29 2007 Matthew Truch <matt at truch.net> - 1.4.0-3
- Recall that things get installed into %%{buildroot}

* Tue May 29 2007 Matthew Truch <matt at truch.net> - 1.4.0-2
- Remove wmap and scuba2 datasources.  They shouldn't have been included
  in the upstream release.  

* Thu May 17 2007 Matthew Truch <matt at truch.net> - 1.4.0-1
- Update to kst 1.4.0 release.  

* Mon Jan 8 2007 Matthew Truch <matt at truch.net> - 1.3.1-3
- Bump release to pick up newest cfitsio (3.030).

* Fri Jan 5 2007 Matthew Truch <matt at truch.net> - 1.3.1-2
- Include explicit Requires: for cfitsio exact version compiled against.  

* Fri Oct 20 2006 Matthew Truch <matt at truch.net> - 1.3.1-1
- Update to kst 1.3.1 bugfix release.

* Fri Sep 29 2006 Matthew Truch <matt at truch.net> - 1.3.0-2
- Bump release to maintain upgrade path.

* Wed Sep 27 2006 Matthew Truch <matt at truch.net> - 1.3.0-1
- Update to kst 1.3.0 release.

* Mon Aug 28 2006 Matthew Truch <matt at truch.net> - 1.2.1-2
- Bump release to force build in prep. for FC6.

* Thu Mar 23 2006 Matthew Truch <matt at truch.net> - 1.2.1-1
- Update to kst 1.2.1 bugfix release from upstream.

* Sun Mar 12 2006 Matthew Truch <matt at truch.net> - 1.2.0-10
- Yet another tweak to configure options.
- Bump build so new cfitsio version is picked up.

* Sun Feb 26 2006 Matthew Truch <matt at truch.net> - 1.2.0-9
- Improve qt lib and include configure options.

* Sun Feb 26 2006 Matthew Truch <matt at truch.net> - 1.2.0-8
- Bump release due to build issue.

* Sun Feb 26 2006 Matthew Truch <matt at truch.net> - 1.2.0-7
- Teach configure to properly find qt libs and includes.

* Fri Feb 17 2006 Matthew Truch <matt at truch.net> - 1.2.0-6
- Make desktop file appear in proper menu.

* Fri Feb 17 2006 Matthew Truch <matt at truch.net> - 1.2.0-5
- Use a better script for fixing non-relative doc symlinks.
- Install desktop file in proper Fedora location.

* Thu Feb 16 2006 Matthew Truch <matt at truch.net> - 1.2.0-4
- Fix compile flags.
- Take two at fixing non-relative symlinks.  
- Own doc kst directories.

* Wed Feb 15 2006 Matthew Truch <matt at truch.net> - 1.2.0-3
- Fix non-relative symlinks.

* Wed Feb 15 2006 Matthew Truch <matt at truch.net> - 1.2.0-2
- Own all directories.
- Remove redundant build requires.

* Tue Feb 14 2006 Matthew Truch <matt at truch.net> - 1.2.0-1
- Initial fedora specfile for kst based partially on spec file 
  included with kst source.
