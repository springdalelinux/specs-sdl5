# Default provider build options (MySQL, Postgres, unixODBC, LDAP, FreeTDS)
#
# Package build options:
# --with db2
# --with oracle
# --with sybase
# --without ldap
# --without mdb
# --without mysql
# --without odbc
# --without postgres
# --without tds
# --without xbase
# 

%define           IBMDB2   0
%define           ORACLE   0
%define           SYBASE   0
%define           LDAP     1
%define           MDB      1
%define           MYSQL    1
%define           ODBC     1
%define           POSTGRES 1
%define           FREETDS  1
%define           XBASE    1

%{?_with_db2:%define IBMDB2     1}
%{?_with_oracle:%define ORACLE  1}
%{?_with_sybase:%define SYBASE  1}
%{?_without_ldap:%define LDAP   0}
%{?_without_mdb:%define MDB     0}
%{?_without_mysql:%define MYSQL 0}
%{?_without_odbc:%define ODBC   0}
%{?_without_postgres:%define POSTGRES 0}
%{?_without_tds:%define FREETDS 0}
%{?_without_xbase:%define XBASE 0}

Name:             libgda
Epoch:            1
Version:          3.0.1
Release:          6%{?dist}.1
Summary:          Library for writing gnome database programs
Group:            System Environment/Libraries
License:          LGPLv2+
URL:              http://www.gnome-db.org/
Source:           http://ftp.gnome.org/pub/GNOME/sources/%{name}/3.0/%{name}-%{version}.tar.bz2
Patch1:           libgda-3.0.0-man.patch
Patch2:           libgda-3.0.1-ldap.patch
Patch4:           libgda-3.0.1-mdb-64bit.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:    pkgconfig >= 0.8
BuildRequires:    glib2-devel >= 2.0.0
BuildRequires:    libxslt-devel >= 1.0.9
BuildRequires:    ncurses-devel
BuildRequires:    libxml2-devel readline-devel db4-devel gamin-devel
BuildRequires:    gtk-doc scrollkeeper gettext flex bison perl(XML::Parser)
# note we do not provide these, they no longer exist
Obsoletes:        %{name}-sharp < %{epoch}:%{version}-%{release}
Obsoletes:        %{name}-sharp-devel < %{epoch}:%{version}-%{release}

%if %{FREETDS}
BuildRequires:    freetds-devel
%endif

%if %{MYSQL}
BuildRequires:    mysql-devel
%endif

%if %{POSTGRES}
BuildRequires:    postgresql-devel
%endif

%if %{ODBC}
BuildRequires:    unixODBC-devel
%endif

%if %{MDB}
BuildRequires:    mdbtools-devel
%endif

%if %{LDAP}
BuildRequires:    openldap-devel
%endif

%if %{XBASE}
BuildRequires:    xbase-devel
%endif

%description
libgda is a library that eases the task of writing
gnome database programs.


%package devel
Summary:          Development libraries and header files for libgda
Group:            Development/Libraries
Requires:         glib2-devel >= 2.0.0
Requires:         libxslt-devel >= 1.0.9
Requires:         db4-devel libxml2-devel pkgconfig
Requires:         %{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains the header files and libraries needed to write
or compile programs that use libgda.


%package sqlite
Summary:          SQLite provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-sqlite < %{epoch}:%{version}-%{release}
Provides:         gda-sqlite = %{epoch}:%{version}-%{release}
%description sqlite
This package includes the libgda SQLite provider.

%package sqlite-devel
Summary:          SQLite provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-sqlite = %{epoch}:%{version}-%{release}
%description sqlite-devel
This package includes the pkgconfig file for the libgda SQLite provider.


%if %{FREETDS}
%package freetds
Summary:          FreeTDS provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-freetds < %{epoch}:%{version}-%{release}
Provides:         gda-freetds = %{epoch}:%{version}-%{release}
%description freetds
This package includes the libgda FreeTDS provider.

%package freetds-devel
Summary:          FreeTDS provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-freetds = %{epoch}:%{version}-%{release}
%description freetds-devel
This package includes the pkgconfig file for the libgda FreeTDS provider.
%endif

%if %{IBMDB2}
%package ibmdb2
Summary:          IBM DB2 provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-ibmdb2 < %{epoch}:%{version}-%{release}
Provides:         gda-ibmdb2 = %{epoch}:%{version}-%{release}
%description ibmdb2
This package includes the libgda IBM DB2 provider.

%package ibmdb2-devel
Summary:          IBM DB2 provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-ibmdb2 = %{epoch}:%{version}-%{release}
%description ibmdb2-devel
This package includes the pkgconfig file for the libgda IBM DB2 provider.
%endif

%if %{MYSQL}
%package mysql
Summary:          MySQL provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-mysql < %{epoch}:%{version}-%{release}
Provides:         gda-mysql = %{epoch}:%{version}-%{release}
%description mysql
This package includes the libgda MySQL provider.

%package mysql-devel
Summary:          MySQL provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-mysql = %{epoch}:%{version}-%{release}
%description mysql-devel
This package includes the pkgconfig file for the libgda MySQL provider.
%endif

%if %{ODBC}
%package odbc
Summary:          ODBC provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-odbc < %{epoch}:%{version}-%{release}
Provides:         gda-odbc = %{epoch}:%{version}-%{release}
%description odbc
This package includes the libgda ODBC provider.

%package odbc-devel
Summary:          ODBC provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-odbc = %{epoch}:%{version}-%{release}
%description odbc-devel
This package includes the pkgconfig file for the libgda ODBC provider.
%endif

%if %{ORACLE}
%package oracle
Summary:          Oracle provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-oracle < %{epoch}:%{version}-%{release}
Provides:         gda-oracle = %{epoch}:%{version}-%{release}
%description oracle
This package includes the libgda Oracle provider.

%package oracle-devel
Summary:          Oracle provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-oracle = %{epoch}:%{version}-%{release}
%description oracle-devel
This package includes the pkgconfig file for the libgda Oracle provider.
%endif

%if %{POSTGRES}
%package postgres
Summary:          PostgreSQL provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-postgres < %{epoch}:%{version}-%{release}
Provides:         gda-postgres = %{epoch}:%{version}-%{release}
%description postgres
This package includes the libgda PostgreSQL provider.

%package postgres-devel
Summary:          PostgreSQL provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-postgres = %{epoch}:%{version}-%{release}
%description postgres-devel
This package includes the pkgconfig file for the libgda PostgreSQL provider.
%endif

%if %{SYBASE}
%package sybase
Summary:          Sybase provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-sybase < %{epoch}:%{version}-%{release}
Provides:         gda-sybase = %{epoch}:%{version}-%{release}
%description sybase
This package includes the libgda Sybase provider.

%package sybase-devel
Summary:          Sybase provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-sybase = %{epoch}:%{version}-%{release}
%description sybase-devel
This package includes the pkgconfig file for the libgda Sybase provider.
%endif

%if %{MDB}
%package mdb
Summary:          MDB provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-mdb < %{epoch}:%{version}-%{release}
Provides:         gda-mdb = %{epoch}:%{version}-%{release}
%description mdb
This package includes the libgda MDB provider.

%package mdb-devel
Summary:          MDB provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-mdb = %{epoch}:%{version}-%{release}
%description mdb-devel
This package includes the pkgconfig file for the libgda MDB provider.
%endif
		
%if %{LDAP}
%package ldap
Summary:          LDAP provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
Obsoletes:        gda-ldap < %{epoch}:%{version}-%{release}
Provides:         gda-ldap = %{epoch}:%{version}-%{release}
%description ldap
This package includes the libgda LDAP provider.

%package ldap-devel
Summary:          LDAP provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         pkgconfig
Requires:         %{name}-ldap = %{epoch}:%{version}-%{release}
%description ldap-devel
This package includes the pkgconfig file for the libgda LDAP provider.
%endif

%if %{XBASE}
%package xbase
Summary:          XBASE provider for libgda
Group:            System Environment/Libraries
Requires:         %{name} = %{epoch}:%{version}-%{release}
%description xbase
This package includes the GDA XBASE provider.

%package xbase-devel
Summary:          XBASE provider for libgda pkgconfig file
Group:            Development/Libraries
Requires:         %{name}-xbase = %{epoch}:%{version}-%{release}, pkgconfig
%description xbase-devel
This package includes the pkgconfig file for the libgda XBASE provider.
%endif


%prep
%setup -q
%patch1 -p1 -b .man
%patch2 -p1 -b .ldap
%patch4 -p1 -b .64bit
# fix ppc64 postgres detection
sed -i 's/x86_64\* | sparc64\*) lib="lib64";;/x86_64\* | sparc64\* | powerpc64\*) lib="lib64";;/' \
  configure configure.in
# stop autoxxx rerunning because of our patches above
touch aclocal.m4
touch `find -name Makefile.in`


%build
CONFIG="--disable-static --disable-dependency-tracking"

%if %{FREETDS}
CONFIG="$CONFIG --with-tds"
%else
CONFIG="$CONFIG --without-tds"
%endif

%if %{IBMDB2}
CONFIG="$CONFIG --with-ibmdb2"
%else
CONFIG="$CONFIG --without-ibmdb2"
%endif

%if %{MYSQL}
CONFIG="$CONFIG --with-mysql"
%else
CONFIG="$CONFIG --without-mysql"
%endif

%if %{POSTGRES}
CONFIG="$CONFIG --with-postgres"
%else
CONFIG="$CONFIG --without-postgres"
%endif

%if %{ODBC}
CONFIG="$CONFIG --with-odbc"
%else
CONFIG="$CONFIG --without-odbc"
%endif

%if %{ORACLE}
CONFIG="$CONFIG --with-oracle"
%else
CONFIG="$CONFIG --without-oracle"
%endif

%if %{SYBASE}
CONFIG="$CONFIG --with-sybase"
%else
CONFIG="$CONFIG --without-sybase"
%endif

%if %{MDB}
CONFIG="$CONFIG --with-mdb"
%else
CONFIG="$CONFIG --without-mdb"
%endif

%if %{LDAP}
CONFIG="$CONFIG --with-ldap"
%else
CONFIG="$CONFIG --without-ldap"
%endif

%if %{XBASE}
CONFIG="$CONFIG --with-xbase"
%else
CONFIG="$CONFIG --without-xbase"
%endif

%configure $CONFIG
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# work around gda-report-test-3.0 linking failing because of the disabling of
# rpath above
export LD_LIBRARY_PATH=`pwd`/libsql/.libs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Cleanup unnecessary, unpackaged files
rm $RPM_BUILD_ROOT/%{_libdir}/libgda-3.0/providers/*.la
rm $RPM_BUILD_ROOT/%{_libdir}/*.la
rm $RPM_BUILD_ROOT/%{_sysconfdir}/libgda-3.0/sales_test.db

%find_lang libgda-3.0


%post -p /sbin/ldconfig

%post devel
if which scrollkeeper-update >/dev/null 2>&1; then scrollkeeper-update; fi

%postun -p /sbin/ldconfig

%postun devel
if which scrollkeeper-update >/dev/null 2>&1; then scrollkeeper-update; fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f libgda-3.0.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README NEWS
%config(noreplace) %{_sysconfdir}/libgda-3.0
%{_bindir}/*
%{_datadir}/libgda-3.0
%{_libdir}/*.so.*
%dir %{_libdir}/libgda-3.0
%dir %{_libdir}/libgda-3.0/providers
# note this file really should be in its own subpackage too, but libgda
# needs to have atleast one provider present to be of any use.
%{_libdir}/libgda-3.0/providers/libgda-bdb.so
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/libgda-3.0
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgda-3.0.pc
%{_libdir}/pkgconfig/libgda-bdb-3.0.pc

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-sqlite.so

%files sqlite-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-sqlite-3.0.pc

%if %{FREETDS}
%files freetds
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-freetds.so

%files freetds-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-freetds-3.0.pc
%endif

%if %{IBMDB2}
%files ibmdb2
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-ibmdb2.so

%files ibmdb2-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-imdb2-3.0.pc
%endif

%if %{MYSQL}
%files mysql
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-mysql.so

%files mysql-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-mysql-3.0.pc
%endif

%if %{ODBC}
%files odbc
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-odbc.so

%files odbc-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-odbc-3.0.pc
%endif

%if %{ORACLE}
%files oracle
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-oracle.so

%files oracle-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-oracle-3.0.pc
%endif

%if %{POSTGRES}
%files postgres
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-postgres.so

%files postgres-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-postgres-3.0.pc
%endif

%if %{SYBASE}
%files sybase
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-sybase.so

%files sybase-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-sybase-3.0.pc
%endif

%if %{MDB}
%files mdb
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-mdb.so

%files mdb-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-mdb-3.0.pc
%endif

%if %{LDAP}
%files ldap
%defattr(-,root,root,-)
%{_libdir}/libgda-3.0/providers/libgda-ldap.so

%files ldap-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-ldap-3.0.pc
%endif

%if %{XBASE}
%files xbase
%defattr(-,root,root)
%{_libdir}/libgda-3.0/providers/libgda-xbase.so

%files xbase-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libgda-xbase-3.0.pc
%endif


%changelog
* Mon Sep 22 2008 Lubomir Rintel <lkundrak@v3.sk> - 3.0.1-6.1
- Back into using embedded sqlite for el5
- Add ncurses-devel dependency, that's missing from readline-devel

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 3.0.1-6
- Rebuild for deps

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-5
- Rebuild to fix untranslated strings on x86_64 in
  /usr/share/libgda-3.0/sqlite_specs_drop_index.xml
  which caused multilib problems (bz 342101)

* Fri Aug 17 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-4
- Fix building on ppc64 again (patch configure not configure.in, now we are
  no longer running autoconf)

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-3
- Enable microsoft access (mdb) support now that mdbtools is in Fedora
- Enable xBase (dBase, Clipper, FoxPro) support, it seems that xbase has been
  available for quite a while now
- Switch from using mysqlclient10 to using mysql-libs for the msql provider

* Wed Aug  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-2
- Build against system sqlite instead of own private copy (this is possible now
  that the system sqlite is of a high enough version) 
- Enable FreeTDS provider (FreeTDS is in Fedora now)
- Update License tag for new Licensing Guidelines compliance

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-1
- New upstream release 3.0.1
- Remove mono bindings sub-package as upstream no longer includes them

* Thu May 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-12
- Don't build mono/sharp bits on ppc64
- Fixup packaging of sharp bindings to match the mono packaging guidelines

* Fri Dec 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-11
- Rebuild for new postgres

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-10
- FE6 Rebuild

* Tue Jun 20 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-9
- Add BuildRequires: libtool hopefully _really_ fixing building with the new
  stripped mock config. (Drop BR: autoconf which is implied by BR: automake).

* Thu Jun 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-8
- Add BuildRequires: automake, autoconf to fix building with the new even more
  stripped mock config.

* Sat Jun 10 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-7
- Add BuildRequires: gettext, bison, flex, gamin-devel to fix building with
  new stripped mock config.

* Thu May 11 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-6
- Move Obsoletes and Provides for plugins out of the plugins %%description,
  so that they actually Obsolete and Provide instead of showing up in rpm -qi
  (bug 191213).

* Thu May  4 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-5
- Add patch3 fixing a couple of x86_64 bugs (bz 190366)

* Mon Feb 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-4
- Bump release and rebuild for new gcc4.1 and glibc.
- Make sqlite plugin use system sqlite not build in version
- Make sqlite plugin a seperate package again
- Attempt to properly install C-sharp/mono bindings
- Add %%{?dist} for consistency with my other packages
- Remove static lib from -devel package

* Tue Jan 17 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-3
- Make -sharp package Require the main package.

* Mon Jan 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-2
- Remove unneeded requires (.so reqs are automaticly picked up by rpm).
- Add BuildRequires for building libgda-sharp

* Sun Nov 27 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-1
- New upstream version
- Drop 4 intergrated patches
- Removed sqlite configurability, it is now an internal part of the upstream
  sources.

* Fri Aug  5 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.2.0-8
- Remove libgda.la file from devel package.

* Sat Jun 25 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.2.0-7
- Added Patch4: libgda-1.2.0-libdir.patch which fixes loading of
  database providers on platforms with a lib64 dir. Thanks to:
  Bas Driessen <bas.driessen@xobas.com> for the patch.
- Enabled building of libgda-ldap and libgda-sqlite by default.

* Tue Jun 21 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.2.0-6
- rebuild so that we depend on the proper version of libpq.so (#160917)
- change names of database providers from gda-xxx to libgda-xxx (#160917)

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-5
- rebuild with gcc4

* Fri Feb 11 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-4
- well, that was moronic

* Wed Feb 10 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-3
- bandaid

* Wed Feb  9 2005 Jeremy Katz <katzj@redhat.com> - 1:1.2.0-2
- rebuild to try to fix broken dep

* Fri Feb 4 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-1
- bump to latest version
- drop integrated break warning patch
- update configure patch

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 1:1.0.4-5
- Rebuilt for new readline.

* Sat Oct 30 2004 Caolan McNamara <caolanm@redhat.com> 1:1.0.4-4
- Use mysqlclient10

* Fri Oct  8 2004 Caolan McNamara <caolanm@redhat.com> 1:1.0.4-3
- #rh135043# Extra BuildRequires

* Thu Sep  9 2004 Bill Nottingham <notting@redhat.com> 1:1.0.4-2
- %%defattr

* Thu Aug 12 2004 Caolan McNamara <caolanm@redhat.com> 1:1.0.4-1
- Initial Red Hat import
- patch for missing break statement
- fixup devel package requirement pickiness
- autoconf patch to pick up correct mysql path from mysql_config (e.g. x64)
- autoconf patch to just look in the normal place for postgres first

* Tue Mar 11 2003 David Hollis <dhollis@davehollis.com>
- Fix --with-tds & --without-tds to match what configure wants

* Tue Jan 28 2003 Yanko Kaneti <yaneti@declera.com>
- Remove the idl path
- Include gda-config man page
- add --without-* for disabled providers
- package and use the omf/scrollkeeper bits

* Tue Dec 31 2002 David Hollis <dhollis@davehollis.com>
- Added sqlite-devel buildreq
- Include gda-config-tool man page

* Mon Aug 19 2002 Ben Liblit <liblit@acm.org>
- Fixed version number substitutions

- Removed some explicit "Requires:" prerequisites that RPM will figure
  out on its own.  Removed explicit dependency on older MySQL client
  libraries

- Required that the ODBC development package be installed if we are
  building the ODBC provider

- Created distinct subpackages for each provider, conditional on that
  provider actually being enabled; some of these will need to be
  updated as the family of available providers changes

- Updated files list to match what "make install" actually installs

- Added URL tag pointing to GNOME-DB project's web site

* Tue Feb 26 2002 Chris Chabot <chabotc@reviewboard.com>
- Added defines and configure flags for all supported DB types

* Mon Feb 25 2002 Chris Chabot <chabotc@reviewboard.com>
- Cleaned up formatting
- Added Requirements
- Added defines for postgres, mysql, odbc support

* Thu Feb 21 2002 Chris Chabot <chabotc@reviewboard.com>
- Initial spec file
