Summary: Open source version of IBM's Visualization Data Explorer 
Name: dx
Version: 4.4.4
Release: 3%{?dist}
URL: http://www.opendx.org/
Group: Applications/Engineering
Source0: http://opendx.npaci.edu/source/%{name}-%{version}.tar.gz
Source1: %{name}.desktop
Patch0: %{name}-rpm.patch
License: IBM Public License
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: bison
BuildRequires: desktop-file-utils
BuildRequires: flex
BuildRequires: hdf-devel
BuildRequires: ImageMagick-devel
#FIXME doesn't build currently
#BuildRequires: java-devel
BuildRequires: openmotif-devel
BuildRequires: libGL-devel
BuildRequires: libGLU-devel
BuildRequires: libtool
BuildRequires: libXinerama-devel
BuildRequires: libXpm-devel
BuildRequires: netcdf-devel
BuildRequires: openssh-clients
Requires: openssh-clients

%description
OpenDX is a uniquely powerful, full-featured software package for the
visualization of scientific, engineering and analytical data: Its open
system design is built on familiar standard interface environments. And its
sophisticated data model provides users with great flexibility in creating
visualizations.

%package devel
Summary: OpenDX module development headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
If you want to write a module to use in the Data Explorer Visual Program
Editor, or in the scripting language, you will need this package.

%prep
%setup -q
%patch0 -p1 -b .r
# fix debuginfo rpmlint warnings
chmod a-x src/exec/{dxmods,dpexec,hwrender}/*.{c,h}

%build
autoreconf --force --install
%configure \
	--disable-static \
	--enable-shared \
	--with-jni-path=%{java_home}/include \
	--without-javadx \
	--disable-dependency-tracking \
	--enable-smp-linux \
	--enable-new-keylayout \
	--with-rsh=%{_bindir}/ssh
                        
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

ln -s ../../%{_lib}/dx/bin_linux $RPM_BUILD_ROOT%{_datadir}/dx/

mv $RPM_BUILD_ROOT%{_libdir}/arch.mak $RPM_BUILD_ROOT%{_includedir}/dx/

install -d $RPM_BUILD_ROOT%{_datadir}/pixmaps
sed -e 's/"R. c #b4b4b4",/"R. c none",/' src/uipp/ui/icon50.xpm > $RPM_BUILD_ROOT%{_datadir}/pixmaps/dx.xpm
desktop-file-install --vendor fedora \
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
	--add-category X-Fedora \
	%{SOURCE1}

# cleanup buildroot
rm -rf $RPM_BUILD_ROOT%{_datadir}/dx/doc
rm     $RPM_BUILD_ROOT%{_datadir}/dx/lib/outboard.c
rm     $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog LICENSE NEWS doc/README*
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/dx
%{_datadir}/dx
%{_mandir}/*/*
%{_datadir}/pixmaps/*.xpm
%{_datadir}/applications/*.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/dx
%{_includedir}/*.h
%{_libdir}/lib*.so

%changelog
* Wed Jul 04 2007 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-3
- fix menu icon transparency (#207841)
- drop redundant BRs
- fix some rpmlint warnings
- build against openmotif for EL-5

* Wed Sep 27 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-2
- rebuild against lesstif

* Fri Sep 22 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.4-1
- updated to 4.4.4

* Sun Sep 17 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-5
- fix make -jN build

* Sun Sep 03 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-4
- moved arch.mak to _includedir/dx
- fixed program startup from the main ui

* Sat Sep 02 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-3
- removed -samples, will package separately
- disable java parts completely for now
- fixed build on fc6
- moved non-binary stuff to _datadir

* Tue Aug 29 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-2
- simplified autotools invocation
- added dist tag

* Tue Aug 22 2006 Dominik Mierzejewski <rpm@greysector.net> 4.4.0-1
- renamed to dx
- package samples
- install desktop file and icon
- use ssh instead of rsh
- run ldconfig for libs

* Sat Aug 19 2006 Dominik Mierzejewski <rpm@greysector.net>
- fixed remaining paths
- split off -devel package
- added missing BRs
- smp_mflags work again
- TODO: java parts

* Fri Aug 18 2006 Dominik Mierzejewski <rpm@greysector.net>
- initial build
- fix lib paths