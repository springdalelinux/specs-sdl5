Name:              libstroke
Version:           0.5.1
Release:           21%{?dist}

Summary:           A stroke interface library
License:           GPLv2
Url:               http://www.etla.net/%{name}/

Source:            http://www.etla.net/%{name}/%{name}-%{version}.tar.gz
Group:             System Environment/Libraries
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:     gtk+-devel
BuildRequires:     libtool
BuildRequires:     pkgconfig

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

Patch0:            libstroke-aclocal.patch
Patch1:            libstroke-multilib.patch


%description
LibStroke is a stroke interface library.  Strokes are motions
of the mouse that can be interpreted by a program as a command.

%package -n %{name}-devel
Summary:           Development files for the libstroke library
Group:             Development/Libraries
Requires:          %{name} = %{version}-%{release} automake

%description -n %{name}-devel
Development files for the libstroke library.


%package -n libgstroke
Summary:           Optional libgstroke files
Group:             System Environment/Libraries
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description -n libgstroke
GNOME version of LibStroke (libgstroke).
LibStroke is a stroke interface library.  Strokes are motions
of the mouse that can be interpreted by a program as a command.

%package -n libgstroke-devel
Summary:           Development files for the libstroke library
Group:             Development/Libraries
Requires:          libgstroke = %{version}-%{release}
Requires:          %{name} = %{version}-%{release} automake

%description -n libgstroke-devel
Development files for the libgstroke library.


%package -n javastroke
Summary:           Optional java files
Group:             System Environment/Libraries
Requires:          %{name} = %{version}-%{release}

%description -n javastroke
Java interface for stroke and example application

%prep
%setup -q

%patch0 -p1 -b .aclocal
%patch1 -p1 -b .multilib

# fix RHBZ # 465030
%if 0%{?fedora} < 11
cp -p %{_datadir}/libtool/config.sub .
cp -p %{_datadir}/libtool/config.guess .
%else
cp -p %{_datadir}/libtool/config/config.sub .
cp -p %{_datadir}/libtool/config/config.guess .
%endif

%build
%configure \
    --disable-static \
    --with-x=yes
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make INSTALL="%{__install} -p" install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/stroke/java
cp -p javastroke/*.java  %{buildroot}%{_datadir}/stroke/java


rm %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}


%files -n %{name}
%defattr(-,root,root)
%doc README COPYRIGHT ChangeLog NEWS AUTHORS TODO CREDITS
%{_libdir}/libstroke.so.*

%files -n %{name}-devel
%defattr(-,root,root)
%doc doc/standard_strokes*
%{_datadir}/aclocal/libstroke.m4
%{_libdir}/libstroke.so
%{_includedir}/stroke.h


%files -n libgstroke
%defattr(-,root,root)
%doc README COPYRIGHT ChangeLog NEWS AUTHORS TODO CREDITS
%{_libdir}/libgstroke.so.*

%post -n libgstroke -p /sbin/ldconfig

%postun -n libgstroke -p /sbin/ldconfig

%files -n libgstroke-devel
%defattr(-,root,root)
%doc README.libgstroke
%{_datadir}/aclocal/libgstroke.m4
%{_libdir}/libgstroke.so
%{_includedir}/gstroke.h


%files -n javastroke
%defattr(-,root,root)
%doc javastroke/README
%{_datadir}/stroke/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%Changelog
* Mon Dec 29 2008 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-21
- fix for EL-5 build; pdgconfig as BR

* Sat Dec 20 2008 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-20
- fix for rawhide's libtool 2.2.6

* Sat Dec 20 2008 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-19
- rebuild for proper tagging

* Sat Dec 20 2008 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-18
- fix for x86_64 build fix RHBZ # 465030

* Mon Jun 16 2008 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-17
- Bugfix 449516 FTBFS libstroke-0.5.1-17.fc9

* Thu Aug 23 2007 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-16
- mass rebuild for fedora 8 - ppc32

* Tue Jun 26 2007 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-15
- patch for multilib #241448

* Thu Mar 01 2007 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-14
- patch for underquoted definitions #226886

* Mon Feb 26 2007 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-13
- Fixed multilibs issues for rawhide

* Fri Sep 01 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-12
- Removed automake as BR

* Fri Sep 01 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-11
- fixed ownership of directories

* Wed Aug 30 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-10
- Removed duplicates

* Wed Aug 30 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-9
- Removed "conflicts: libstroke-devel"

* Wed Aug 30 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-8
- fixed ownership of directories

* Wed Aug 30 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-7
- rebuilt for FC5 and later with minor fixes

* Tue Aug 29 2006 Chitlesh Goorah <chitlesh@fedoraproject.org> - 0.5.1-6
- rebuilt for FC5 and later with minor fixes

* Sun Apr 2 2006 Wojciech Kazubski <wk at ire.pw.edu.pl> - 0.5.1-5
- rebuilt for FC5,
- specfile cleanups

* Sun Jun 19 2005 Wojciech Kazubski <wk at ire.pw.edu.pl>
- rebuilt for Fedora Core 4

* Thu May 5 2005 Wojciech Kazubski <wk at ire.pw.edu.pl>
- re-divided

* Sat Dec 11 2004 Wojciech Kazubski <wk at ire.pw.edu.pl>
- rebuilt for Fedora Core 3

* Tue Feb 4 2003 Wojciech Kazubski <wk at ire.pw.edu.pl>
- libstroke-gnome splited.

* Wed Dec 19 2001 Wojciech Kazubski <wk at ire.pw.edu.pl>
- first RedHat version.