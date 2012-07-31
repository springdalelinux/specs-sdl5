# Pass --with externalfuse to compile against system fuse lib
# Default is internal fuse-lite.
%define with_externalfuse %{?_with_externalfuse:1}%{!?_with_externalfuse:0}

# For release candidates
# %%global subver -RC

Name:		ntfs-3g
Summary:	Linux NTFS userspace driver
Version:	2010.3.6
Release:	1%{?dist}
License:	GPLv2+
Group:		System Environment/Base
Source0:	http://tuxera.com/opensource/ntfs-3g-%{version}%{?subver}.tgz
Source1:	20-ntfs-config-write-policy.fdi
Patch0:		ntfs-3g-1.2216-nomtab.patch
URL:		http://www.ntfs-3g.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{with_externalfuse}
BuildRequires:	fuse-devel
Requires:	fuse
%endif
BuildRequires:	libtool, libattr-devel
Epoch:		2
Provides:	ntfsprogs-fuse = %{epoch}:%{version}-%{release}
Obsoletes:	ntfsprogs-fuse
Provides:	fuse-ntfs-3g = %{epoch}:%{version}-%{release}

%description
NTFS-3G is a stable, open source, GPL licensed, POSIX, read/write NTFS 
driver for Linux and many other operating systems. It provides safe 
handling of the Windows XP, Windows Server 2003, Windows 2000, Windows 
Vista, Windows Server 2008 and Windows 7 NTFS file systems. NTFS-3G can 
create, remove, rename, move files, directories, hard links, and streams; 
it can read and write normal and transparently compressed files, including 
streams and sparse files; it can handle special files like symbolic links, 
devices, and FIFOs, ACL, extended attributes; moreover it provides full 
file access right and ownership support.

%package devel
Summary:	Development files and libraries for ntfs-3g
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	pkgconfig

%description devel
Headers and libraries for developing applications that use ntfs-3g
functionality.

%prep
%setup -q -n %{name}-%{version}%{?subver}
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
%configure \
	--disable-static \
	--disable-ldconfig \
%if 0%{?_with_externalfuse:1}
	--with-fuse=external \
%endif
	--exec-prefix=/ \
	--bindir=/bin \
	--sbindir=/sbin \
	--libdir=/%{_lib}
make %{?_smp_mflags} LIBTOOL=%{_bindir}/libtool

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_lib}/*.la
rm -rf $RPM_BUILD_ROOT/%{_lib}/*.a

# make the symlink an actual copy to avoid confusion
rm -rf $RPM_BUILD_ROOT/sbin/mount.ntfs-3g
cp -a $RPM_BUILD_ROOT/bin/ntfs-3g $RPM_BUILD_ROOT/sbin/mount.ntfs-3g

# Actually make some symlinks for simplicity...
# ... since we're obsoleting ntfsprogs-fuse
cd $RPM_BUILD_ROOT/bin
ln -s ntfs-3g ntfsmount
cd $RPM_BUILD_ROOT/sbin
ln -s mount.ntfs-3g mount.ntfs-fuse
# And since there is no other package in Fedora that provides an ntfs 
# mount...
ln -s mount.ntfs-3g mount.ntfs

# Compat symlinks
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s /bin/ntfs-3g ntfs-3g
ln -s /bin/ntfsmount ntfsmount

# Put the .pc file in the right place.
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
mv $RPM_BUILD_ROOT/%{_lib}/pkgconfig/libntfs-3g.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/

# We get this on our own, thanks.
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}/README

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/10osvendor/
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/10osvendor/

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING CREDITS NEWS README
/sbin/mount.ntfs
%attr(754,root,root) /sbin/mount.ntfs-3g
/sbin/mount.ntfs-fuse
/bin/ntfs-3g
/bin/ntfsmount
/bin/ntfs-3g.probe
/bin/ntfs-3g.secaudit
/bin/ntfs-3g.usermap
%{_bindir}/ntfs-3g
%{_bindir}/ntfsmount
/%{_lib}/libntfs-3g.so.*
%{_mandir}/man8/*
%{_datadir}/hal/fdi/policy/10osvendor/20-ntfs-config-write-policy.fdi

%files devel
%defattr(-,root,root,-)
%{_includedir}/ntfs-3g/
/%{_lib}/libntfs-3g.so
%{_libdir}/pkgconfig/libntfs-3g.pc

%changelog
* Mon Mar  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.3.6-1
- update to 2010.3.6

* Mon Feb 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.2.6-1
- update to 2010.2.6-RC
- fix summary text

* Wed Jan 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.1.16-1
- update to 2010.1.16

* Fri Nov 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.11.14-2
- missing BuildRequires: libattr-devel

* Fri Nov 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.11.14-1
- update to 2009.11.14

* Fri Oct 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.10.5-0.1.RC
- bump to 2009.10.5-RC

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:2009.4.4-3
- Rebuilt with new fuse

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2009.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr  3 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.4.4-1
- update to 4.4, patch for mount issue merged

* Mon Mar 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.3.8-2
- Patch from upstream provided as temporary workaround for bz 486619

* Thu Mar 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.3.8-1
- update to 2009.3.8

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2009.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.2.1-2
- update fdi to fix nautilus mount bug

* Thu Feb 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.2.1-1
- update to 2009.2.1

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.1.1-1
- new release, new versioning scheme from upstream

* Thu Jan  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5222-0.2.RC
- move pkgconfig Requires to -devel package where it belongs

* Mon Dec 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5222-0.1.RC
- 1.5222-RC

* Tue Dec  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5130-1
- update to 1.5130

* Wed Oct 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-4
- fix hal file to properly ignore internal recovery partitions

* Wed Oct 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-3
- fix hal file to cover all mount cases (thanks to Richard Hughes)

* Mon Oct 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-2
- add fdi file to enable hal automounting

* Wed Oct 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-1
- update to 1.5012 (same code as 1.2926-RC)

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2926-0.1.RC
- update to 1.2926-RC (rawhide, F10)

* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2812-1
- update to 1.2812

* Sat Jul 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2712-1
- update to 1.2712

* Mon May  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2506-1
- update to 1.2506

* Tue Apr 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2412-1
- update to 1.2412

* Mon Mar 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2310-2
- update sources

* Mon Mar 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2310-1
- update to 1.2310
- make -n a noop (bz 403291)

* Tue Feb 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2216-3
- rebuild against fixed gcc (PR35264, bugzilla 433546)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:1.2216-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.2216-1
- update to 1.2216

* Tue Nov 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1120-1
- bump to 1.1120
- default to fuse-lite (internal to ntfs-3g), but enable --with externalfuse 
  as an option

* Thu Nov  8 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1104-1
- bump to 1.1104

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1030-1
- bump to 1.1030

* Sat Oct  6 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1004-1
- bump to 1.1004

* Thu Sep 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.913-2
- don't set /sbin/mount.ntfs-3g setuid

* Mon Sep 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.913-1
- bump to 1.913

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.826-1
- bump to 1.826
- glibc27 patch is upstreamed

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.810-1
- bump to 1.810
- fix license tag
- rebuild for ppc32

* Sun Jul 22 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.710-1
- bump to 1.710
- add compat symlinks

* Wed Jun 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.616-1
- bump to 1.616

* Tue May 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.516-1
- bump to 1.516
- fix bugzilla 232031

* Sun Apr 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.417-1
- bump to 1.417

* Sun Apr 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.416-1
- bump to 1.416
- drop patch0, upstreamed

* Wed Apr  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.328-2
- allow non-root users to mount/umount ntfs volumes (Laszlo Dvornik)

* Sat Mar 31 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.328-1
- bump to 1.328
- drop patch, use --disable-ldconfig instead

* Wed Feb 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.0-1
- 1.0 release!

* Fri Jan 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:0-0.9.20070118
- symlink to mount.ntfs

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:0-0.8.20070118
- bump to 20070118

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:0-0.7.20070116
- bump to latest version for all active dists

* Wed Jan  3 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.6.20070102
- bump to latest version (note that upstream fixed their date mistake)

* Wed Nov  1 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.5.20070920
- add an obsoletes for ntfsprogs-fuse
- make some convenience symlinks

* Wed Oct 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.4.20070920
- add some extra Provides

* Mon Oct 16 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.3.20070920
- add explicit Requires on fuse

* Mon Oct 16 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.2.20070920
- fixed versioning (bumped epoch, since it now shows as older)
- change sbin symlink to actual copy to be safe

* Sun Oct 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.20070920-1
- Initial package for Fedora Extras
