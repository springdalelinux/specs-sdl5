Name:      libgeotiff
Version:   1.2.5
Release:   5%{?dist}
Summary:   GeoTIFF format library
Group:     System Environment/Libraries
License:   MIT
URL:       http://www.remotesensing.org/geotiff/geotiff.html
Source:    ftp://ftp.remotesensing.org/pub/geotiff/libgeotiff/%{name}-%{version}.tar.gz
Patch0:    libgeotiff-soname.patch
Patch1:    libgeotiff-multilib.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: doxygen
BuildRequires: libtiff-devel libjpeg-devel proj-devel zlib-devel

%description
GeoTIFF represents an effort by over 160 different remote sensing, 
GIS, cartographic, and surveying related companies and organizations 
to establish a TIFF based interchange format for georeferenced 
raster imagery.

%package devel
Summary: Development Libraries for the GeoTIFF file format library
Group: Development/Libraries
Requires: pkgconfig libtiff-devel
Requires: %{name} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .soname~
%patch1 -p1 -b .multilib~

# fix wrongly encoded files from tarball
set +x
for f in `find . -type f` ; do
   if file $f | grep -q ISO-8859 ; then
      set -x
      iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
         mv -f ${f}.tmp $f
      set +x
   fi
   if file $f | grep -q CRLF ; then
      set -x
      sed -i -e 's|\r||g' $f
      set +x
   fi
done
set -x

# remove junks
find . -name ".cvsignore" -exec rm -rf '{}' \;

%build

# disable -g flag removal
sed -i 's| \| sed \"s\/-g \/\/\"||g' configure

# use gcc -shared instead of ld -shared to build with -fstack-protector
sed -i 's|LD_SHARED=@LD_SHARED@|LD_SHARED=@CC@ -shared|' Makefile.in

%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name}/ \
        --with-proj               \
        --with-tiff               \
        --with-jpeg               \
        --with-zip
# WARNING
# disable %{?_smp_mflags}
# it breaks compile

make

%install
rm -rf $RPM_BUILD_ROOT

# install libgeotiff
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

# install manualy some file
install -p -m 755 bin/makegeo %{buildroot}%{_bindir}

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
rm -rf %{buildroot}%{_libdir}/*.a
echo  >> %{buildroot}%{_datadir}/epsg_csv/codes.csv

# generate docs
doxygen

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README
%doc docs/*.txt docs/*.html
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_bindir}/makegeo
%{_libdir}/libgeotiff.so.*
%dir %{_datadir}/epsg_csv
%attr(0644,root,root) %{_datadir}/epsg_csv/*.csv

%files devel
%defattr(-,root,root,-)
%doc docs/api
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0644,root,root) %{_includedir}/%{name}/*.inc
%{_libdir}/libgeotiff.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.2.5-4
- Fix FTBFS: use gcc -shared instead of ld -shared to compile with -fstack-protector

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.5-2
- disable smp build for koji

* Mon Sep 15 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.5-1
- new bugfix release

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.4-2
- Fix multilib issue by removal of datetime in doxygen footers

* Sun Jan 06 2008 Balint Cristian <rezso@rdsor.ro> - 1.2.4-1
- Rebuild for final release.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.4-0.5.rc1
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 1.2.4-0.4.rc1
- Rebuild for RH #249435

* Tue Jul 24 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.3.rc1
- codes are under MIT
- pkg-config cflags return fix
- epsg_csv ownership

* Mon Jul 23 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.2.rc1
- fix debuginfo usability
- move header files to the subdirectory
- specify the full URL of the source
- leave *.inc headers included
- libgeotiff-devel should require libtiff-devel
- works to keep timestamps on the header files installed
- docs proper triage

* Mon Jul 23 2007 Balint Cristian <cbalint@redhat.com> 1.2.4-0.1.rc1
- initial pack for fedora
- add pkgconfig file
- add soname versioning patch
