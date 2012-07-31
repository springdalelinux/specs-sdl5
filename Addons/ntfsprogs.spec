Name:		ntfsprogs
Version:	1.13.1
Release:	6%{?dist}
Summary:	NTFS filesystem libraries and utilities
Source0:	http://download.sf.net/linux-ntfs/%{name}-%{version}.tar.gz
Patch0:		ntfsprogs-1.13.1-build-extras-by-default.patch
License:	GPL
URL:		http://www.linux-ntfs.org/
Group:		System Environment/Base
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	glib2-devel, gnome-vfs2-devel, libtool
BuildRequires:	libgcrypt-devel, gnutls-devel

%description
The Linux-NTFS project (http://www.linux-ntfs.org/) aims to bring full support
for the NTFS filesystem to the Linux operating system.  The ntfsprogs package
currently consists of a library and utilities such as mkntfs, ntfscat, ntfsls, 
ntfsresize, and ntfsundelete (for a full list of included utilities see man 8 
ntfsprogs after installation).

%package gnomevfs
Summary:	NTFS GNOME virtual filesystem module
Group:		System Environment/Base
Requires:	%{name} = %{version}-%{release}
Requires:	glib2, gnome-vfs2

%description gnomevfs
This package contains the NTFS GNOME virtual filesystem (VFS) module which
allows GNOME VFS clients to seamlessly utilize the NTFS library (libntfs).

%package devel
Summary:	Headers and libraries for libntfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the header files and libraries needed to link software
with the NTFS library (libntfs).

%prep
%setup -q
%patch0 -p1

%build
# If we need to enable the fuse module, we'd change this.
# The ntfs-3g stuff is better than what is here currently, so we'll let people use it.
%configure --enable-gnome-vfs --disable-fuse-module --disable-static --enable-test --enable-crypto
make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# We're not including ntfsmount, so we don't need the manpages
rm -rf $RPM_BUILD_ROOT%{_mandir}/man8/ntfsmount*

# Libtool files go bye bye
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/libntfs-gnomevfs.la

# Clear up symlink confusion by making a copy
rm -rf $RPM_BUILD_ROOT/sbin/mkfs.ntfs
cp -a $RPM_BUILD_ROOT%{_sbindir}/mkntfs $RPM_BUILD_ROOT/sbin/mkfs.ntfs

# runlist isn't really useful
rm -rf $RPM_BUILD_ROOT%{_bindir}/runlist

# Also, these static libs aren't really useful.
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/libntfs-gnomevfs.a

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING CREDITS ChangeLog NEWS README TODO.include TODO.libntfs TODO.ntfsprogs 
%doc doc/attribute_definitions doc/attributes.txt doc/compression.txt doc/tunable_settings 
%doc doc/system_files.txt doc/system_security_descriptors.txt
%{_bindir}/*
%{_sbindir}/*
/sbin/mkfs.ntfs
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/mkfs.ntfs.8*
%{_mandir}/man8/ntfs[^m][^o]*.8*
%{_libdir}/libntfs.*so.*

%files gnomevfs
%defattr(-,root,root,-)
%{_mandir}/man8/libntfs-gnomevfs.8*
%{_libdir}/gnome-vfs-2.0/modules/libntfs-gnomevfs.so.*
%config(noreplace) %{_sysconfdir}/gnome-vfs-2.0/modules/libntfs.conf

%files devel
%defattr(-,root,root,-)
%doc doc/CodingStyle doc/template.h doc/template.c
%{_includedir}/*
%{_libdir}/libntfs.so
%{_libdir}/gnome-vfs-2.0/modules/libntfs-gnomevfs.so

%changelog
* Wed Jul 11 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.13.1-6
- build and install "extra" binaries by default (I was accidentally installing the scripts, not the binaries)
  This better resolves bz 247398 (thanks to Martin Riarte)

* Mon Jul  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.13.1-5
- don't package items which say they should never be installed (resolves bz 247398)

* Wed Jun 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.13.1-4
- fix packaging mistake (resolve bz 245329)

* Sat Oct 21 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.13.1-3
- really fix rpath
- nuke static libs
- build the "extra" files and install them
- get rid of "runlist"

* Sat Oct 21 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.13.1-2
- enable crypto
- enable test suite
- use system libtool to eliminate rpath for lib64

* Fri Oct 20 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.13.1-1
- initial release for Fedora, deuglify upstream spec
