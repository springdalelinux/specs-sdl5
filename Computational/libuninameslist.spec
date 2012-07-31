Name:           libuninameslist
Version:        0.0
Release:        7.20060907%{?dist}

Summary:        Library that provides Unicode names and annotations

Group:          System Environment/Libraries
License:        BSD
URL:            http://libuninameslist.sourceforge.net
Source0:        http://dl.sf.net/libuninameslist/libuninameslist_src-20060907.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libuninameslist provides applications with access to Unicode name and
annotation data from the official Unicode databases. The information
is current as of Unicode 4.0.

%package        devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q -n libuninameslist


%build
%configure --enable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall incdir=$RPM_BUILD_ROOT%{_includedir}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*


%changelog
* Fri May 04 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0-7.20060907
- add dist for epel

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.0-6.20060907
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Kevin Fenzi <kevin@tummy.com> - 0.0-5.20060907
- Take over maintainership. 
- Update to 20060907

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.0-4.040707
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.2.040707
- Updated to 040707.

* Fri Jul  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.2.040701
- Updated to 040701.

* Mon Oct 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.0-0.fdr.2.030713
- Enable static libs, add -devel subpackage.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.030713
- Initial RPM release.
