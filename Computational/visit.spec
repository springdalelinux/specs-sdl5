%define visitversion 2.2.1
%define	numvers %( echo %{visitversion} | tr -d . )
%define subvers %( echo %{visitversion} | tr . _ )
%define tarballs AdvIO-1.2.tar.gz BoxLib-2010.10.01.tar.gz H5Part-1.6.2.tar.gz ITAPS-FMDB-1.1-30Aug10.tar.gz ITAPS-GRUMMP-0.5.0-03Jun10.tar.gz ITAPS-MOAB-3.99-10Jun10.tar.gz IceT-1-0-0.tar.gz Imaging-1.1.6.tar.gz MesaLib-7.8.2.tar.gz Python-2.6.4.tgz Xdmf-2.1.tar.gz adios-1.2.1.tar.gz cfitsio3006.tar.gz cgns-3.0.8-Source.tar.gz cmake-2.8.3.tar.gz exodusii-4.98.tar.gz fastbit-ibis1.2.0.tar.gz gdal-1.7.1.tar.gz hdf-4.2.5.tar.gz hdf5-1.8.4.tar.gz libccmio-2.6.1.tar.gz mxml-2.6.tar.gz netcdf-4.1.1.tar.gz pyparsing-1.5.2.tar.gz qt-everywhere-opensource-src-4.6.1.tar.gz silo-4.8.tar.gz szip-2.1.tar.gz vtk-5.0.0g.tar.gz

%if 0%{?rhel} > 5
%define	openmpiversion	1.4.3
%else
%define openmpiversion  1.3.3
%endif
%define openmpiflavor gcc

%define destdir /usr/local/visit/%{visitversion}

# type: string (root path to install modulefiles)
%{!?modulefile_path: %define modulefile_path /usr/local/share/Modules/modulefiles/}
# type: string (subdir to install modulefile)
%{!?modulefile_subdir: %define modulefile_subdir visit}
# type: string (name of modulefile)
%{!?modulefile_name: %define modulefile_name %{version}}
%define openmpiloadmodule module load openmpi/%{openmpiflavor}

# Do not bytecompile or hardlink python stuff, also no need for jar stuff
%define __os_install_post    \
    /usr/lib/rpm/redhat/brp-compress \
    /usr/lib/rpm/redhat/brp-strip %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-static-archive %{__strip} \
    /usr/lib/rpm/redhat/brp-strip-comment-note %{__strip} %{__objdump} \
%{nil}

Name:		visit%{numvers}
Version:	%{visitversion}
Release:	4%{?dist}
Summary:	VisIt is a free interactive parallel visualization and graphical analysis tool for viewing scientific data
Group:		Scientific/Applications
License:	BSD
URL:		https://wci.llnl.gov/codes/visit/
Source0:	build_visit%{subvers}
Source1:	visit%{version}.tar.gz
%{expand:%(i=10; for j in %{tarballs}; do echo Source$i: $j; i=$[ $i + 1 ]; done| tee /tmp/abcd1.out)}
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# The following are mostly taken from python src.rpm requires, as we are compiling it ourselves best to have them
BuildRequires:	bzip2-devel zlib-devel openssl-devel gcc-c++ tar 
BuildRequires:	readline-devel gmp-devel ncurses-devel gdbm-devel expat-devel  
BuildRequires:	libX11-devel pkgconfig tcl-devel tk tix tk-devel tix-devel tcl
BuildRequires:	sqlite-devel autoconf db4-devel
BuildRequires:	libffi-devel valgrind-devel  
# The following may be required by VTK, not sure so the entire Xlib thing is here
BuildRequires:	libXScrnSaver-devel libXau-devel libXaw-devel libXcomposite-devel libXcursor-devel libXdamage-devel
BuildRequires:	libXevie-devel libXext-devel libXfixes-devel libXfont-devel libXft-devel libXi-devel libXinerama-devel 
BuildRequires:	libXmu-devel libXp-devel libXpm-devel libXrandr-devel libXrender-devel libXres-devel libXt-devel 
BuildRequires:	libXtst-devel libXv-devel libGL-devel
# likely be needed by QT
BuildRequires:	libtiff-devel libpng-devel fontconfig-devel libGLU-devel
# needed by HDF4
BuildRequires:	bison byacc flex

BuildRequires:	gcc-gfortran
BuildRequires:	tar
BuildRequires:	openmpi-%{openmpiflavor}-devel = %{openmpiversion}

Requires:	environment-modules
Requires:	openmpi-%{openmpiflavor} >= %{openmpiversion}

# do not try to do provides, ends up offering all kinds of things it should not
AutoProv:	0
Provides:	visit%{numvers} = %{version}-%{release}
Provides:	visit = %{visitversion}
Provides:	visit = %{visitversion}-%{release}

# other requires specific to os
%if 0%{?rhel} < 6
BuildRequires:	librdmacm-devel
%endif

%description
VisIt is a free interactive parallel visualization and graphical analysis tool
for viewing scientific data on Unix and PC platforms. Users can quickly 
generate visualizations from their data, animate them through time, manipulate
them, and save the resulting images for presentations. VisIt contains a rich
set of visualization features so that you can view your data in a variety of
ways. It can be used to visualize scalar and vector fields defined on two- and
three-dimensional (2D and 3D) structured and unstructured meshes. VisIt was 
designed to handle very large data set sizes in the terascale range and yet
can also handle small data sets in the kilobyte range

%package devel
Summary: Development libraries and include files for visit
Group: Development/Libraries
Requires: %{name} = %{version}
AutoProv: 0
Provides: visit%{numvers}-devel = %{version}-%{release}
Provides: visit-devel = %{visitversion}
Provides: visit-devel = %{visitversion}-%{release}

%description devel
Development libraries and include files for visit

%prep
%setup -n %{name} -c -T
# first copy the build script and the visit tarball
cp %{SOURCE0} %{SOURCE1} .
# next copy everything else
for j in %{tarballs}; do
	cp %{_sourcedir}/$j .
done

%build
# configure openmpi
. /etc/profile.d/modules.sh
module load openmpi
# set vars for it
export PAR_COMPILER=mpic++
export PAR_INCLUDE=/usr/local/openmpi/%{openmpiversion}/%{openmpiflavor}/%{_arch}/include

./build_visit%{subvers} --adios --advio --boxlib --ccmio --cfitsio --cgns --console \
  --exodus --fastbit --gdal --h5part --hdf4 --hdf5 --netcdf --no-icet \
  --parallel --python-module --silo --szip --xdmf

cd visit%{version}/src
make package

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{destdir}

cd visit%{version}/src
./svn_bin/visit-install -c princeton %{version} linux-%{_arch} $RPM_BUILD_ROOT%{destdir}

chmod -R a+rX,og-w,u+w $RPM_BUILD_ROOT%{destdir}

mkdir -p $RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}
cat <<EOF >$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{version}
#%Module

proc ModulesHelp { } {
   puts stderr "This module adds VisIt %{version} to various paths"
}

module-whatis   "Sets up VisIt %{version} in your environment"

%{openmpiloadmodule}
prepend-path PATH "%{destdir}/bin"
#prepend-path LD_LIBRARY_PATH "%{destdir}/%{version}/linux-%{_arch}/lib"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{destdir}
%exclude %{destdir}/%{version}/linux-%{_arch}/archives
%exclude %{destdir}/%{version}/linux-%{_arch}/include
%exclude %{destdir}/%{version}/linux-%{_arch}/lib/python/include
%exclude %{destdir}/%{version}/linux-%{_arch}/libsim
%dir %{modulefile_path}/%{modulefile_subdir}
%{modulefile_path}/%{modulefile_subdir}/%{version}

%files devel
%defattr(-,root,root,-)
%{destdir}/%{version}/linux-%{_arch}/archives
%{destdir}/%{version}/linux-%{_arch}/include
%{destdir}/%{version}/linux-%{_arch}/lib/python/include
%{destdir}/%{version}/linux-%{_arch}/libsim


%changelog
* Fri Apr 15 2011 Josko Plazonic <plazonic@math.princeton.edu>
- add support for puias5 builds

* Wed Apr 13 2011 Josko Plazonic <plazonic@math.princeton.edu>
- initial build based on Michael Chupa's notes
