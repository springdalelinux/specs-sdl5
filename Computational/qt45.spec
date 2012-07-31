Summary: The shared library for the Qt GUI toolkit
Name: qt45
Version: 4.5.3
Release: 1
License: GPL/QPL
Group: System Environment/Libraries
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url: http://www.troll.no
Source0: ftp://ftp.troll.no/qt/source/qt-x11-opensource-src-%{version}.tar.gz
#Source1: designer.desktop
#Source2: assistant.desktop
#Source3: linguist.desktop
#Source4: qtconfig.desktop
#Source5: designer4
#Source6: assistant4
#Source7: linguist4
#Source8: qtconfig4

%define qt_dirname qt45
%define qtdir %{_libdir}/%{qt_dirname}
%define qt_docdir %{_docdir}/qt-devel-%{version}
%define qt_libdir %{qtdir}/%{_lib}

%if "%{_lib}" == "lib64"
%define platform linux-g++-64
%else
%define platform linux-g++
%endif

# buildmysql: Build MySQL plugins
%define buildmysql 1

# buildpsql: Build Postgres plugins
%define buildpsql 1

# buildodbc: Build ODBC plugins
%define buildodbc 1

# buildodbc: Build sqlite plugins
%define buildsqlite 1

Requires(post): fileutils /etc/ld.so.conf.d
Requires(postun): fileutils /etc/ld.so.conf.d
Requires: rpm

BuildRequires: libmng-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: giflib-devel
BuildRequires: perl
BuildRequires: sed
BuildRequires: findutils
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libXcursor-devel
BuildRequires: libXext-devel
BuildRequires: libXft-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXt-devel
BuildRequires: libX11-devel
BuildRequires: xorg-x11-proto-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: dbus-devel

%if %{buildmysql}
BuildRequires: mysql-devel
%endif

%if %{buildpsql}
BuildRequires: postgresql-devel
%endif

%if %{buildodbc}
BuildRequires: unixODBC-devel
%endif

%if %{buildsqlite}
BuildRequires: sqlite-devel
%endif

%package devel
Summary: Development files for the Qt GUI toolkit
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: freetype-devel
Requires: zlib-devel
Requires: fontconfig-devel
Requires: libpng-devel
Requires: libjpeg-devel
Requires: libmng-devel
Requires: mesa-libGL-devel
Requires: mesa-libGLU-devel
Requires: xorg-x11-proto-devel
Requires: libXrender-devel
Requires: libXrandr-devel
Requires: libXcursor-devel
Requires: libXinerama-devel
Requires: libXft-devel
Requires: libXext-devel
Requires: libX11-devel
Requires: libXt-devel
Requires: libSM-devel
Requires: libICE-devel
Requires: libXi-devel

Obsoletes: %{name}-config < %{version}-%{release}
Provides:  %{name}-config = %{version}-%{release}

%package doc
Summary: API documentation, demos and example programs for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
Provides: %{name}-assistant = %{version}-%{release}

%if %{buildodbc}
%package odbc
Summary: ODBC drivers for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%endif

%if %{buildmysql}
%package mysql
Summary: MySQL drivers for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%endif

%if %{buildpsql}
%package postgresql
Summary: PostgreSQL drivers for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%endif

%if %{buildsqlite}
%package sqlite
Summary: SQLite drivers for Qt's SQL classes
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%endif

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains the shared library needed to run qt
applications, as well as the README files for qt.

%description devel
The qt-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler.

Install qt-devel if you want to develop GUI applications using the Qt
toolkit.

%description doc
The qt-doc package contains the man pages, the HTML documentation and
example programs.

Install qt-devel-docs if you want to develop GUI applications using the Qt
toolkit.

%if %{buildodbc}
%description odbc
ODBC driver for Qt's SQL classes (QSQL)
%endif

%if %{buildmysql}
%description mysql
MySQL driver for Qt's SQL classes (QSQL)
%endif

%if %{buildpsql}
%description postgresql
PostgreSQL driver for Qt's SQL classes (QSQL)
%endif

%if %{buildsqlite}
%description sqlite
SQLite driver for Qt's SQL classes (QSQL)
%endif

%prep
%setup -q -n qt-x11-opensource-src-%{version}

#%patch1 -p1 -b .assistant4
#%patch2 -p1
#%patch3 -p1 -b .demos

# set correct FLAGS
perl -pi -e "s|-O2|%{optflags}|g" mkspecs/%{platform}/qmake.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
  perl -pi -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
  perl -pi -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi

%build
# build shared, threaded (default) libraries
echo yes | ./configure -v \
  -opensource \
  -no-rpath \
  -prefix %{qtdir} \
  -docdir %{qt_docdir} \
  -libdir %{qt_libdir} \
  -platform %{platform} \
  -release \
  -no-separate-debug-info \
  -shared \
  -largefile \
  -qt-gif \
  -system-zlib \
  -system-libpng \
  -system-libjpeg \
%if %{buildmysql}
  -plugin-sql-mysql \
  -I%{_includedir}/mysql \
  -L%{_libdir}/mysql \
%endif
%if %{buildpsql}
  -plugin-sql-psql \
%endif
%if %{buildodbc}
  -plugin-sql-odbc \
%endif
%if %{buildsqlite}
  -plugin-sql-sqlite \
%endif
  -stl \
  -cups \
  -sm \
  -xinerama \
  -xrender \
  -xshape \
  -xrandr \
  -xkb \
  -xcursor \
  -fontconfig

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install INSTALL_ROOT=%{buildroot}

# install demos examples
find {examples,demos} -type f -name "Makefile" | xargs rm -f
find {examples,demos} -type d -name "*.???" | xargs rm -rf
cp -a demos examples %{buildroot}%{qtdir}/

mkdir -p %{buildroot}%{_bindir}/
#install -m 755 %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{buildroot}%{_bindir}/

# Add desktop files
#mkdir -p %{buildroot}%{_datadir}/applications
#desktop-file-install \
#  --dir %{buildroot}%{_datadir}/applications \
#  --vendor="%{name}" \
#  --add-category="X-Fedora" \
#  %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}

# remove .la files
rm -f %{buildroot}%{qt_libdir}/*.la

# fix file permission
find %{buildroot}%{qtdir}/mkspecs -type f | xargs chmod 644

#sed -i -e "s|-L%{_builddir}/qt-x11-opensource-src-%{version}/lib ||g" %{buildroot}%{qt_libdir}/*.pc
#sed -i -e "s|-L%{_builddir}/qt-x11-opensource-src-%{version}/lib ||g" %{buildroot}%{qt_libdir}/*.prl
#
#mkdir -p %{buildroot}%{_libdir}/pkgconfig/
#mv %{buildroot}/%{qt_libdir}/*.pc %{buildroot}%{_libdir}/pkgconfig/

mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{qt_libdir}" > %{buildroot}/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# install icons
#mkdir %{buildroot}%{_datadir}/pixmaps
#install -m 644 tools/assistant/images/designer.png %{buildroot}%{_datadir}/pixmaps/designer4.png
#install -m 644 tools/assistant/images/assistant.png %{buildroot}%{_datadir}/pixmaps/assistant4.png
#install -m 644 tools/assistant/images/linguist.png %{buildroot}%{_datadir}/pixmaps/linguist4.png

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc changes-4.5.3 FAQ.txt INSTALL LGPL_EXCEPTION.txt LICENSE.GPL3 LICENSE.LGPL README
%dir %{qtdir}
%dir %{qtdir}/bin/
%dir %{qt_libdir}
%dir %{qtdir}/plugins/
%dir %{qtdir}/plugins/sqldrivers/
%{qtdir}/bin/*

/etc/ld.so.conf.d/*
%{qt_libdir}/lib*.so.*
%{qtdir}/plugins/codecs/
%{qtdir}/plugins/iconengines/
%{qtdir}/plugins/imageformats/
%{qtdir}/plugins/accessible/
%{qtdir}/plugins/inputmethods/
%{qtdir}/plugins/graphicssystems
%{qtdir}/plugins/script

%files devel
%defattr(-,root,root,-)
%{qtdir}/bin/lrelease*
%{qtdir}/bin/lconvert
%{qtdir}/bin/lupdate*
%{qtdir}/bin/moc*
%{qtdir}/bin/qmake*
%{qtdir}/bin/qt3to4
%{qtdir}/bin/rcc*
%{qtdir}/bin/uic*
%{qtdir}/bin/designer*
%{qtdir}/bin/linguist*
%{qtdir}/bin/pixeltool
%{qtdir}/bin/qdbus
%{qtdir}/bin/qdbuscpp2xml
%{qtdir}/bin/qdbusxml2cpp
%exclude %{qtdir}/bin/qtdemo
%{qtdir}/include/
%{qtdir}/mkspecs/
%{qt_libdir}/*.so
%{qt_libdir}/*.a
%{qt_libdir}/*.prl
%{qtdir}/phrasebooks/
%{qtdir}/q3porting.xml
%{qtdir}/plugins/designer/
%{qtdir}/%{_lib}/pkgconfig/*pc

%files doc
%defattr(-,root,root,-)
%doc %{qt_docdir}
%{qtdir}/demos/
%{qtdir}/examples/
%{qtdir}/bin/assistant*

%if %{buildodbc}
%files odbc
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlodbc*
%endif

%if %{buildpsql}
%files postgresql
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlpsql*
%endif

%if %{buildmysql}
%files mysql
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlmysql*
%endif

%if %{buildsqlite}
%files sqlite
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlite*
%endif

%changelog
* Tue May 04 2010 Josko Plazonic <plazonic@math.princeton.edu> 4.5.3-1
- update to 4.5.3, fix up pkgconfig files for 64 bit arches

* Wed Sep 30 2009 Thomas Uphill <uphill@ias.edu> 4.5.2
- update to 4.5.2

* Mon Oct 23 2006 Than Ngo <than@redhat.com> 4.2.1-1
- update to 4.2.1

* Thu Oct 05 2006 Than Ngo <than@redhat.com> 4.1.4-12
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Than Ngo <than@redhat.com> 4.1.4-11
- fix #203492, get rid of dependency of pkg-config 

* Fri Sep 22 2006 Than Ngo <than@redhat.com> 4.1.4-10
- fix #203492, Qt4 Config can not be launched

* Thu Aug 31 2006 Than Ngo <than@redhat.com> 4.1.4-9
- fix multilib issue #204785

* Tue Aug 22 2006 Than Ngo <than@redhat.com> 4.1.4-8
- fix #203492, Qt4 Config can not be launched

* Tue Aug 08 2006 Than Ngo <than@redhat.com> 4.1.4-7
- drop the gcc workaround, problem fixed in gcc/g++

* Mon Jul 17 2006 Than Ngo <than@redhat.com> 4.1.4-6
- disable fvisibility temporary as gcc workaround

* Fri Jul 14 2006 Tim Powers <timp@redhat.com> - 4.1.4-5
- rebuild

* Thu Jul 06 2006 Than Ngo <than@redhat.com> 4.1.4-4 
- fix s390/s390x build problem

* Thu Jul 06 2006 Than Ngo <than@redhat.com> 4.1.4-3
- add missing desktop files

* Wed Jul 05 2006 Than Ngo <than@redhat.com> 4.1.4-2
- cleanup specfile

* Mon Jul 03 2006 Than Ngo <than@redhat.com> 4.1.4-1
- 4.1.4

* Thu Jun 15 2006 Than Ngo <than@redhat.com> 4.1.3-1
- update to 4.1.3
- merge changes from qt4 in Extras

* Fri May 12 2006 Than Ngo <than@redhat.com> 4.1.2-1
- update to 4.1.2
- add subpackage qt-devel-docs

* Mon Feb 27 2006 Than Ngo <than@redhat.com> 4.1.1-0.1
- update to 4.1.1

* Tue Dec 20 2005 Than Ngo <than@redhat.com> 4.1.0-0.1
- update to 4.1.0

* Fri Sep 09 2005 Than Ngo <than@redhat.com> 4.0.1-0.1
- update to 4.0.1
