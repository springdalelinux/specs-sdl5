Name: freetds
Summary: Implementation of the TDS (Tabular DataStream) protocol
Version: 0.64
Release: 6%{?dist}
Group: System Environment/Libraries
License: LGPL 
URL: http://www.freetds.org/
Source:	ftp://ftp.ibiblio.org/pub/Linux/ALPHA/freetds/stable/freetds-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: unixODBC-devel
BuildRequires: doxygen, docbook-style-dsssl
Patch0: freetds-0.64-makefile-doc.patch
 

%description 
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib, CT-Lib, and ODBC.


%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.


%prep 
%setup -q
%patch0 -p1

# cleanup the initial source
sed -i 's/\r//' doc/tds_ssl.html
sed -i '1 s,#!.*/perl,#!%{__perl},' samples/*.pl doc/api_status.txt

find doc/ samples/ COPYING* -type f -print0 | xargs -0 chmod -x
find . -name "*.[ch]" -print0 | xargs -0 chmod -x

# cause to rebuild docs
rm doc/doc/freetds-%{version}/reference/index.html
rm doc/doc/freetds-%{version}/userguide/index.htm

 
%build 
%configure \
	--disable-dependency-tracking \
	%{!?_with_static: --disable-static} \
	--with-tdsver="4.2" \
	--with-unixodbc="%{_prefix}" \
	--enable-msdblib \
	--enable-sybase-compat

# avoid any rpath
sed -i -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
	-e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} DOCBOOK_DSL="`rpm -ql docbook-style-dsssl | fgrep html/docbook.dsl`"

chmod -x samples/*.template

 
%install 
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

rm -f samples/Makefile* samples/*.in samples/README


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
 

%clean 
rm -rf $RPM_BUILD_ROOT
 

%files 
%defattr(-, root, root, -) 
%{_bindir}/*
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/*.conf
%doc AUTHORS BUGS COPYING* NEWS README TODO 
%doc doc/*.html doc/doc/freetds-%{version}/userguide
%{_mandir}/*/*

 
%files devel 
%defattr (-, root, root) 
%doc samples doc/doc/freetds-%{version}/reference
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%{_includedir}/*
 

%changelog 
* Fri Jun 15 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-6 
- bump release to provide update path over Livna

* Wed Jun 13 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-5
- spec file cleanups
- allowed for Fedora (no patent issues exist), clarification by
  James K. Lowden <jklowden [AT] freetds.org>
- approved for Fedora (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Wed Aug  2 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- approved for Livna (review by Hans de Goede <j.w.r.degoede@hhs.nl>)

* Tue Aug  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-4
- add patch to fix sed scripts in the doc/ Makefile
- avoid using rpath in binaries
- cleanup in samples/ dir

* Thu Jul 27 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-3
- rebuild userguide too.
- move reference docs to -devel

* Mon Jul 24 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-2
- Properly clear extra executable bit in source
- Regenerate docs using doxygen

* Thu Jul 20 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.64-1
- Upgrade to 0.64
- Some spec file and distro cleanups

* Tue Sep 20 2005 V.C.G.Yeah <VCGYeah@iname.com> - 0.63-1
- Upgrade to 0.63
- spec file cleanups
- build static libs conditional

* Thu Sep  2 2004 V.C.G.Yeah <VCGYeah@iname.com> - 0.62.4-1Y
- Updated to release 0.62.4.
- Leave includes in system default include dir (needed for php-mssql build)

* Mon May 17 2004 Dag Wieers <dag@wieers.com> - 0.62.3-1
- Updated to release 0.62.3.

* Wed Feb 04 2004 Dag Wieers <dag@wieers.com> - 0.61.2-0
- Added --enable-msdblib configure option. (Dean Mumby)
- Updated to release 0.61.2.

* Fri Jun 13 2003 Dag Wieers <dag@wieers.com> - 0.61-0
- Initial package. (using DAR)
