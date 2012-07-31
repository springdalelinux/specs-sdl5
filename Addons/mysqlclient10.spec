Name: mysqlclient10
Version: 3.23.58
Release: 9.2.1%{?dist}
Summary: Backlevel MySQL shared libraries.
License: LGPL
Group: Applications/Databases
URL: http://www.mysql.com

Source0: http://www.mysql.com/Downloads/MySQL-3.23/mysql-%{version}.tar.gz
Source5: my_config.h
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh 
Patch1: mysql-3.23.54-libdir.patch
Patch2: mysql-errno.patch
Patch8: mysql-3.23.58-config.patch
Patch9: mysql-3.23.58-security.patch
Patch10: mysql-no-atomic.patch
Patch11: mysql-buffer-warning.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prereq: /sbin/ldconfig, /sbin/install-info, grep,  fileutils, chkconfig
BuildRequires: gperf, perl, readline-devel
BuildRequires: gcc-c++, ncurses-devel, zlib-devel
BuildRequires: libtool automake autoconf
Requires: bash
Provides: libmysqlclient.so.10   libmysqlclient.so.10.0.0 
Provides: libmysqlclient_r.so.10 libmysqlclient_r.so.10.0.0

# Working around perl dependency checking bug in rpm FTTB. Remove later.
%define __perl_requires %{SOURCE999}

# Force include and library files into a nonstandard place
%{expand: %%define _origincludedir %{_includedir}}
%{expand: %%define _origlibdir %{_libdir}}
%define _includedir %{_origincludedir}/mysql3
%define _libdir %{_origlibdir}/mysql3

%description
This package contains backlevel versions of the MySQL client libraries
as shipped with Red Hat Linux 9 for use with applications linked against
them.  These shared libraries were created using MySQL 3.23.58.

%package devel

Summary: Backlevel files for development of MySQL applications.
License: LGPL
Group: Applications/Databases
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed for
developing MySQL applications using backlevel client libraries.

%prep
%setup -q -n mysql-%{version}
%patch1 -p1
%patch2 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

libtoolize --force
aclocal
automake
autoconf
autoheader

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
%ifarch alpha
# Can't link C++ objects into an executable without this. Odd!
# -ECL 2002-12-19
CFLAGS="$CFLAGS -fPIC"
%endif
CXXFLAGS="$CFLAGS -fno-rtti -fno-exceptions"
export CFLAGS CXXFLAGS

%configure \
	--without-readline \
	--without-debug \
	--enable-shared \
	--with-extra-charsets=complex \
	--without-bench \
	--localstatedir=/var/lib/mysql \
	--with-unix-socket-path=/var/lib/mysql/mysql.sock \
	--with-mysqld-user="mysql" \
	--with-extra-charsets=all \
	--enable-local-infile \
	--enable-large-files=yes --enable-largefile=yes \
	--enable-thread-safe-client \
	--with-named-thread-libs="-lpthread"

make %{?_smp_mflags}
make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

install -m 644 include/my_config.h $RPM_BUILD_ROOT%{_includedir}/mysql/my_config_`uname -i`.h
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/

# We want the .so files both in regular _libdir (for execution) and
# in special _libdir/mysql3 directory (for convenient building of clients).
# The ones in the latter directory should be just symlinks though.
mkdir -p ${RPM_BUILD_ROOT}%{_origlibdir}/mysql
pushd ${RPM_BUILD_ROOT}%{_origlibdir}/mysql
mv -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient.so.10.*.* .
mv -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so.10.*.* .
cp -p -d ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient*.so.* .
popd
pushd ${RPM_BUILD_ROOT}%{_libdir}/mysql
ln -s ../../mysql/libmysqlclient.so.10.*.* .
ln -s ../../mysql/libmysqlclient_r.so.10.*.* .
popd

# Put the config script into special libdir
cp -p $RPM_BUILD_ROOT%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql

rm -rf $RPM_BUILD_ROOT%{_prefix}/mysql-test
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/mysql
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_libexecdir}
rm -rf $RPM_BUILD_ROOT%{_infodir}/*
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/*

mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_origlibdir}/mysql" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING COPYING.LIB

%{_origlibdir}/mysql/libmysqlclient*.so.*
/etc/ld.so.conf.d/*

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}

%changelog
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.23.58-9.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.23.58-9.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.23.58-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 15 2005 Tom Lane <tgl@redhat.com> 3.23.58-9
- fix my_config.h for 64-bit and ppc platforms

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 3.23.58-8
- oops, looks like we want uname -i not uname -m

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 3.23.58-7
- Make my_config.h architecture-independent for multilib installs;
  put the original my_config.h into my_config_$ARCH.h
- Add license info (COPYING, COPYING.LIB) to the shipped documentation
- Add -fwrapv to CFLAGS so that gcc 4.1 doesn't break it
- Add mysql-buffer-warning.patch to silence build system security warning

* Fri Apr  8 2005 Tom Lane <tgl@redhat.com> 3.23.58-6
- Avoid dependency on <asm/atomic.h>, cause it won't build anymore on ia64.
- Override configure thread library test to suppress HAVE_LINUXTHREADS check

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 3.23.58-5
- Rebuild with gcc4.

* Fri Oct 29 2004 Tom Lane <tgl@redhat.com> 3.23.58-4
- Seems we do need to export mysqld_error.h after all.

* Fri Oct 29 2004 Tom Lane <tgl@redhat.com> 3.23.58-3
- Handle ldconfig more cleanly (put a file in /etc/ld.so.conf.d/).
- Make .so files in devel be just symlinks to those in main package.

* Thu Oct 28 2004 Tom Lane <tgl@redhat.com> 3.23.58-2
- Install libraries and mysql_config under %%{_libdir}/mysql3/mysql,
  to provide an easier way to build dependent packages.

* Wed Oct 27 2004 Tom Lane <tgl@redhat.com> 3.23.58-1
- Update to latest 3.x release, add relevant patches from mysql package
- add -devel subpackage to allow building other packages against LGPL libs

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Patrick Macdonald <patrickm@redhat.com> 3.23.56-1
- created - originated from the mysql package
- removed all other files and install/uninstall/test procedures
- changed description
