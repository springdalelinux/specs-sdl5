Name:		SDL_ttf
Version:	2.0.8
Release:	2%{?dist}
Summary:	Simple DirectMedia Layer TrueType Font library

Group:		System Environment/Libraries
License:	LGPL
URL:		http://www.libsdl.org/projects/SDL_ttf/
Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
Patch1:		%{name}-2.0.7-freetype-internals.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	SDL-devel >= 1.2.4
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	zlib-devel


%description
This library allows you to use TrueType fonts to render text in SDL
applications.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.4


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch1 -p1 -b .freetype


%build
%configure --disable-dependency-tracking --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_libdir}/lib*.so.*


%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/SDL/


%changelog
* Thu Aug 31 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0.8-2
- Update for FC6.

* Sat Aug 26 2006 Brian Pepple <bpepple@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8.
- Simplify description & summary for devel package.

* Mon Feb 13 2006 Brian Pepple <bdpepple@ameritech.net> - 2.0.7-4
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 14 2005 Brian Pepple <bdpepple@ameritech.net> - 2.0.7-3
- Add patch for Bug #171020.

* Thu Sep 29 2005 Brian Pepple <bdpepple@ameritech.net> - 2.0.7-2
- General spec formatting changes.
- Rebuild for FC4 upgrade path.

* Sun Sep 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 2.0.7-1
- 2.0.7, patches applied upstream.
- Require SDL-devel in -devel.
- Build with dependency tracking disabled.
- Don't ship static libs.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.0.6-5
- rebuilt

* Wed Mar 21 2004 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.4
- fix build on FC2-test (bug #1436

* Mon Nov 10 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.3
- add missing buildreq zlib-devel

* Sun Aug 24 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.2
- address issues in #631
- add full URL to source
- better description for -devel package

* Sat Aug 23 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.6-0.fdr.1
- Fedoraize
- patch to compile on RH9

* Wed Jan 19 2000 Sam Lantinga
- converted to get package information from configure
* Sun Jan 16 2000 Hakan Tandogan <hakan@iconsult.com>
- initial spec file

