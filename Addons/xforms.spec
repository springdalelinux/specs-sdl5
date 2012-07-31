
Name:    xforms
Summary: XForms toolkit library
Version: 1.0.90
Release: 8%{?dist}

License: LGPL
Group:   System Environment/Libraries
URL:     http://www.nongnu.org/xforms/
Source0: http://savannah.nongnu.org/download/xforms/xforms-%{version}.tar.gz
Source1: http://savannah.nongnu.org/download/xforms/xforms-%{version}.tar.gz.sig 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# TODO: remove -lc (all), -lm (most) linker steps
Patch1: xforms-1.0.90-prelink.patch

BuildRequires: libjpeg-devel
BuildRequires: libGL-devel
%define x_deps xorg-x11-devel
%if "%{?fedora}" > "4" || "%{?rhel}" > "4"
%define x_deps libX11-devel libXpm-devel
%endif
BuildRequires: %{x_deps}

# import/export: png, sgi (optional?)
Requires: netpbm-progs
# import eps,ps (optional?)
#Requires: ghostscript


%description
XForms is a GUI toolkit based on Xlib for X Window Systems. It
features a rich set of objects, such as buttons, sliders, and menus
etc. integrated into an easy and efficient object/event callback
execution model that allows fast and easy construction of
X-applications. In addition, the library is extensible and new objects
can easily be created and added to the library.


%package devel
Summary: Development files for the XForms toolkit library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{x_deps}
Requires: libjpeg-devel
%description devel
%{summary}.


%prep

%setup -q

%patch1 -p1 -b .prelink


%build

%configure \
  --disable-static \
  --enable-optimization="$RPM_OPT_FLAGS"

make %{?_smp_mflags} X_PRE_LIBS=""


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

## Unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc COPYING.LIB Copyright ChangeLog NEWS README
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/lib*.so
%{_mandir}/man*/*


%changelog 
* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-8
- fc6 respin

* Tue Aug 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-7
- cleanup

* Wed Mar 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-6
- -devel: Req: libjpeg-devel(flimage), libXpm-devel

* Mon Jan 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-5
- prelink.patch: fix undefined symbols in (shared) lib(s)

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-4
- BR: libXpm-devel
- -devel: Req: libX11-devel 

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-3
- BR: libGL-devel
- #BR: libXpm-devel (coming soon)

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-2
- BR: libGL.so.1 -> BR: %%x_pkg-Mesa-libGL 
- remove legacy crud

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.90-1
- 1.0.90
- new version removes use-of/references-to xmkmf,/usr/X11R6 (#170942)

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Nov 23 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.2
- update for Fedora Core support
- remove extraneous macros

* Fri May 30 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.1
- BuildRequires: libtiff-devel
- add few more %%doc files.

* Fri Apr 02 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.0
- fedora-ize package.

* Mon Jan 20 2003 Rex Dieter <rexdieter at sf.net> 1.0-0
- 1.0-release
- redhat-ize specfile

