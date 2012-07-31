Name:           pstoedit
Version:        3.45
Release:        2%{?dist}
Summary:        Translates PostScript and PDF graphics into other vector formats

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://www.pstoedit.net/
Source0:        http://download.sourceforge.net/pstoedit/pstoedit-%{version}.tar.gz
Patch0:		pstoedit-3.44-cxxflags.patch
Patch1:         pstoedit-3.45-quiet.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	ghostscript
BuildRequires:	gd-devel
BuildRequires:  ImageMagick-c++-devel
BuildRequires:	libpng-devel
BuildRequires:	dos2unix
BuildRequires:	ghostscript
BuildRequires:	plotutils-devel

%description
Pstoedit converts PostScript and PDF files to various vector graphic
formats. The resulting files can be edited or imported into various
drawing packages. Pstoedit comes with a large set of integrated format
drivers


%package devel
Summary:        Headers for developing programs that will use %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       ImageMagick-c++-devel
Requires:	libpng-devel

%description devel
This package contains the header files needed for developing %{name}
applications


%prep
%setup -q
%patch0 -p1 -b .cxxflags
%patch1 -p1 -b .quiet
dos2unix doc/*.htm doc/readme.txt

%build
%configure --disable-static --with-emf --without-swf
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 doc/pstoedit.1 $RPM_BUILD_ROOT%{_mandir}/man1/
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, -)
%doc copying doc/readme.txt doc/index.htm doc/pstoedit.htm
%{_datadir}/pstoedit
%{_mandir}/man1/*
%{_bindir}/pstoedit
%{_libdir}/*.so.*
%{_libdir}/pstoedit


%files devel
%defattr(-, root, root, -)
%doc doc/changelog.htm
%{_includedir}/pstoedit
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%changelog
* Wed Jan 23 2008 Denis Leroy <denis@poolshark.org> - 3.45-2
- Updated to upstream 3.45
- Added quiet patch
- Updated license tag

* Thu Nov 23 2006 Denis Leroy <denis@poolshark.org> - 3.44-5
- Added libEMF support

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 3.44-4
- FE6 Rebuild

* Fri Aug 18 2006 Denis Leroy <denis@poolshark.org> - 3.44-3
- Added svg/libplot support

* Thu Jun 15 2006 Denis Leroy <denis@poolshark.org> - 3.44-2
- Added missing Requires and BuildRequires
- Patched configure to prevent CXXFLAGS overwrite

* Thu Jun  8 2006 Denis Leroy <denis@poolshark.org> - 3.44-1
- First version

