%define libname MixKit
Summary: QSlim and other applications from SlimKit collection of surface modelling tools
Name: QSlim
Version: 2.1
Release: 2%{?dist}
License: GPL
Group: Scientific/Applications
BuildRoot: /tmp/%{name}-buildroot
Source: http://graphics.cs.uiuc.edu/~garland/dist/qslim-%{version}.tar.gz
URL: http://graphics.cs.uiuc.edu/~garland/software/qslim.html
Vendor: Michael Garland garland@uiuc.edu
Packager: Josko Plazonic Mathematics Dept. PU <plazonic@math.princeton.edu>
BuildRequires: gcc-c++, fltk-devel

%description
This is the SlimKit collection of surface modeling tools.  Most of the
programs in this collection simply provide an interface to the
underlying functionality of the MixKit library (see MixKit's README.txt).

The primary component of this package is the QSlim 2.1 surface
simplification tool located in the tools/qslim directory.  Please
consult tools/qslim/QSlim.txt for further information.  There are also
several useful programs in tools/filters/ for manipulating SMF model
files.

%package -n %{libname}
Summary: %{libname} Software Library for surface modelling and simplification algorithms
Group: Scientific/Libraries

%description -n %{libname}
%{libname} is a Software Library for surface modelling, it contains also
simplification algorithms, experimental super-minimal scripting interface and 
other features.

%changelog
* Fri May 02 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for RH 9

* Wed Dec 05 2001 Josko Plazonic <plazonic@math.princeton.edu>
- initial packaging release

%prep
%setup -q -n qslim-%{version}

%build
cd libgfx
CFLAGS="$RPM_OPT_FLAGS -fpermissive" CXXFLAGS="$CFLAGS" %configure
make -C src
cd ../mixkit
CFLAGS="$RPM_OPT_FLAGS -fpermissive" CXXFLAGS="$CFLAGS" FFLAGS="$CFLAGS" %configure
make -C src
cd ../tools
for i in *; do
	make -C $i
done
cd ../examples
make
#perl -pi -e 's|/\* #undef MIX_ANSI_IOSTREAMS \*/|#define MIX_ANSI_IOSTREAMS 1|' mixcfg.h

%install
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/mixkit
cp tools/cluster/qcluster tools/qslim/qslim tools/qslim/qvis $RPM_BUILD_ROOT/%{_prefix}/bin/
cp `find tools/filters/ -type f -perm +111` $RPM_BUILD_ROOT/%{_prefix}/bin/
cp mixkit/src/libmix.a $RPM_BUILD_ROOT/%{_libdir}/
cp mixkit/src/[mMs]*.h $RPM_BUILD_ROOT/%{_includedir}/mixkit/
gzip mixkit/*.txt

%files
%defattr(-,root,root)
%doc tools/qslim/QSlim.txt
%{_prefix}/bin/*

%files -n %{libname}
%defattr(-,root,root)
%doc mixkit/*.txt* mixkit/doc/SMF.txt
%{_libdir}/libmix.a
%{_includedir}/mixkit

%clean
rm -rf $RPM_BUILD_ROOT
