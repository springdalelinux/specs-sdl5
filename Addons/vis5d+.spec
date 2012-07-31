Summary: A free volumetric rendering program based on Vis5d
Name: vis5d+
Version: 1.2.1
Release: 2%{?dist}
License: GPL
Group: Scientific/Applications
BuildRoot:  /var/tmp/%{name}-%{version}-root
Source: http://prdownloads.sourceforge.net/vis5d/vis5d+-%{version}.tar.gz
Source1: vis5d-data.tar.gz
Patch1: vis5d-ffixes.patch
URL: http://vis5d.sourceforge.net/
Packager: Josko Plazonic <plazonic@math.princeton.edu>
BuildRequires: netcdf-devel MixKit libgfx mesa-libGL-devel mesa-libGLU-devel
BuildRequires: gcc-gfortran libX11-devel ImageMagick-devel docbook-utils

%description
Vis5D is a system for interactive visualization of large 5-D gridded data 
sets such as those produced by numerical weather models. One can make 
isosurfaces, contour line slices, colored slices, volume renderings, etc of 
data in a 3-D grid, then rotate and animate the images in real time. There's 
also a feature for wind trajectory tracing, a way to make text anotations for
publications, support for interactive data analysis, etc.

%package examples
Summary: Example maps and data for Vis5D+
Group: Scientific/Applications
Requires: %{name}

%description examples
This package contains example maps and data for Vis5D+.

%changelog
* Thu Jul 11 2002 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for 7.3

* Wed Oct 05 2001 Josko Plazonic <plazonic@math.princeton.edu>
- initial package release

%prep
%setup
%patch1 -p1 -b .ffixes


%build
perl -pi -e 's|V5D_LIBS_AUX=""|V5D_LIBS_AUX="-lgfx"|' configure
LDFLAGS="-L%{_libdir}/netcdf-3" CFLAGS="$RPM_OPT_FLAGS -I/usr/include/netcdf-3" CXXFLAGS="$RPM_OPT_FLAGS -I/usr/include/netcdf-3 -fpermissive" ./configure --prefix=%{_prefix} --with-netcfg --with-mixkit=%{_libdir} --with-x \
	--with-netcdf=%{_libdir}/netcdf-3 \
        --exec-prefix=%{_exec_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --sysconfdir=%{_sysconfdir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --libdir=%{_libdir} \
        --libexecdir=%{_libexecdir} \
        --localstatedir=%{_localstatedir} \
        --sharedstatedir=%{_sharedstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir}
make

%install 
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/vis5d+
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/{locale,vis5d+}
%makeinstall
cp hole.v5d $RPM_BUILD_ROOT/%{_datadir}/vis5d+/
find . -type d -name CVS -exec rm -rf "{}" ";" || :
cd $RPM_BUILD_ROOT/%{_datadir}/vis5d+/
tar xzvf %{SOURCE1}

%files
%defattr(-,root,root)
%doc AUTHORS doc/*
%{_bindir}/*
%{_includedir}/vis5d+
%{_datadir}/locale/*/*/*
%{_datadir}/vis5d+/EARTH.TOPO
%{_datadir}/vis5d+/OUTLSUPW
%{_datadir}/vis5d+/OUTLUSAM
%{_libdir}/*

%files examples
%defattr(-,root,root)
%doc userfuncs contrib
%{_datadir}/vis5d+/*.v5d

%clean
rm -rf $RPM_BUILD_DIR/%{name}*

%changelog
* Thu Aug 26 2004 Josko Plazonic <plazonic@math.princeton.edu>
- packaging fixes

* Fri May 02 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for RH 9
