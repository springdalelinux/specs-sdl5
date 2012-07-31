# compiler for which we are doing this
%define compiler intel
%if 0%{?rhel} > 5
%define openmpiversion 1.5.4
%define compilermajor 12
%define compilerminor 1
%else
%define openmpiversion 1.4.3
%define compilermajor 11
%define compilerminor 1
%endif

# node version build? comment out if yes
#define build_node 1

# various dependencies
%define hdf5version 1.8.8
# for convenience
%define hdf5base hdf5-%(echo %{hdf5version}|tr -d .)-%{compiler}
# modules defaults
%define modulefile_path_top /usr/local/share/Modules/modulefiles/paraview

%ifarch %{ix86}
%define bits 32
%else
%define bits 64
%endif

# deployment plan:
# top dir /usr/local/paraview
#                        /gcc/3.12.0
#                        /gcc/openmpi-1.5.4/3.12.0
#                        /intel-12.1/3.12.0
#                        /intel-12.1/openmpi-1.5.4/3.12.0

# now, depending on the compiler we need different things - place them all here for eacy access/changing
#
# GCC Compiler
%if "%{compiler}" == "gcc"
%define compilerruntime Requires: %{hdf5base} \
BuildRequires: openmpi-gcc-devel >= %{openmpiversion}
%define compilerruntimeopenmpi Requires: openmpi-gcc >= %{openmpiversion}, %{hdf5base}
%define compilerdevel Requires: %{hdf5base}-devel
%define compilerdevelopenmpi Requires: openmpi-gcc-devel >= %{openmpiversion}, %{hdf5base}-devel
%define localdir /usr/local/paraview/gcc/%{version}
%define localdiropenmpi /usr/local/paraview/gcc/openmpi-%{openmpiversion}/%{version}
# do nothing special for gcc for build prep
%define compilerbuildprep export CC='gcc' CXX='g++'
%define compilerbuildprepmodule %{nil}
# no alias
%define modulefile_compiler_alias %{nil}
%define compilershort gcc
%define compilerlong gcc
%define compilerversionnum 446
%define optflags -O3 -pipe -Wall
%endif
#
# Intel compiler
%if "%{compiler}" == "intel"
# these two are used to decide which version of intel we will be using to build it all
# and which version we will be providing
%define intelminrelease 6
%define compilerversion %{compilermajor}.%{compilerminor}
%define compilerversionnum %{compilermajor}%{compilerminor}
%define compilerruntime Requires: %{hdf5base} \
BuildRequires: openmpi-intel%{compilerversionnum}-devel >= %{openmpiversion}
%define compilerruntimeopenmpi Requires: openmpi-intel%{compilerversionnum} >= %{openmpiversion}, %{hdf5base}
%define compilerdevel Requires: intel-compiler%{compilermajor}-%{bits}-default-modules-devel >= %{compilerversion}-%{intelminrelease}, %{hdf5base}-devel
%define compilerdevelopenmpi Requires: openmpi-intel%{compilerversionnum}-devel >= %{openmpiversion}
%define localdir /usr/local/paraview/intel-%{compilerversion}/%{version}
%define localdiropenmpi /usr/local/paraview/intel-%{compilerversion}/openmpi-%{openmpiversion}/%{version}
# for intel we need to just specify our compilers
%if 0%{?rhel} > 5
%define compilerbuildprep export CC=icc CXX=icpc LDFLAGS="-Wl,--build-id"; module load intel
%else
%define compilerbuildprep export CC=icc CXX=icpc; module load intel
%endif
%define compilerbuildprepmodule module load intel/%{compilermajor}/%{bits}
# the following is used in above
%define compilershort intel-%{compilermajor}
%define compilerlong intel-%{compilerversion}
%define optflags -O3
%endif

# where modules really go
%define modulefile_path %{modulefile_path_top}/%{compilerlong}
# alias to make sure that module load paraview/gcc does not load paraview/gcc/openmpi
# also it makes sure that module load paraview/intel and paraview/intel-12 work
%define modulefile_compiler_alias %{modulefile_path_top}/.modulerc-%{compiler}-%{bits}-%{compilerversionnum}

%ifarch s390 s390
%global build_openmpi 0
%endif
%global build_mpich2 0
%{!?build_openmpi:%global build_openmpi 1}
%global pv_maj 3
%global pv_min 12
%global pv_patch 0
%global pv_majmin %{pv_maj}.%{pv_min}
%global rcver %{nil}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           paraview%{pv_maj}%{pv_min}%{pv_patch}-%{?build_node:node-}%{compiler}
Version:        %{pv_majmin}.%{pv_patch}
Release:        6.7%{?dist}
Summary:        Parallel visualization application

Group:          Applications/Engineering
License:        BSD
URL:            http://www.paraview.org/
Source0:        http://www.paraview.org/files/v%{pv_majmin}/ParaView-%{version}%{?rcver}.tar.gz
Source1:        paraview_22x22.png
Source2:        paraview.xml
#Add some needed includes
Patch1:         paraview-3.8.0-include.patch
#Patch to build with boost 1.48
#Reported upstream: http://paraview.org/Bug/view.php?id=12772
Patch2:         paraview-3.12.0-boost-1.48.0-bfs.patch
#Reported upstream: http://public.kitware.com/mantis/view.php?id=7023
Patch7:         paraview-3.2.2-hdf5.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%{compilerruntime}
BuildRequires:  cmake28
%if %{build_mpich2}
BuildRequires:  mpich2-devel
%endif
BuildRequires:  python-devel, tk-devel
BuildRequires:  %{hdf5base}-devel
BuildRequires:  zlib-devel, expat-devel, doxygen
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  wget
%if 0%{?rhel} > 5
BuildRequires:	boost-devel
%else
BuildRequires:  boost141-devel
Requires:	boost141
%endif
BuildRequires:  libjpeg-devel, libpng-devel, libtiff-devel
BuildRequires:  mesa-libOSMesa-devel mesa-libGL-devel mesa-libGLU-devel
BuildRequires:  libXt-devel
BuildRequires:  gnuplot
%if 0%{!?build_node:1}
%if 0%{?rhel} > 5
BuildRequires:  qt-devel
BuildRequires:  qt-assistant-adp-devel
BuildRequires:  qt-webkit-devel
%else
BuildRequires:	qt46-devel qt46-sqlite
Requires:	qt46-sqlite
%endif
BuildRequires:  freetype-devel
BuildRequires:  desktop-file-utils
BuildRequires:  graphviz
BuildRequires:  libtheora-devel
%endif
Requires: environment-modules

#-- Plugin: EyeDomeLighting disabled
#-- Plugin: Manta ray traced rendering disabled - Requires Manta
#-- Plugin: NetDMF file format reader disabled - Requires NetDMF
#-- Plugin: Override time requests disabled
#-- Plugin: Plugin for creating python coprocessing scripts disabled
#-- Plugin: Plugin to read NCAR VDF files disabled - Requires Vapor
#-- Plugin: Reader for *.bp files based on Adios disabled
#-- Plugin: Virtual Reality Private Network (VRPN) tracker disabled - Requires VRPN
#-- Plugin: Virtual Reality User Interface (VRUI) tracker disabled
#-- Plugin: Virtual Reality User Interface (VRUI) tracker enabled
#CMake Error at Plugins/VRUI/CMakeLists.txt:7 (FIND_PACKAGE):
#  Could not find module FindParaView.cmake or a configuration file for
#  package ParaView.
#  Adjust CMAKE_MODULE_PATH to find FindParaView.cmake or set ParaView_DIR to
#  the directory containing a CMake configuration file for ParaView.  The file
#  will have one of the following names:
#    ParaViewConfig.cmake
#    paraview-config.cmake
%define paraview_cmake_options \\\
	-DCMAKE_VERBOSE_MAKEFILE=ON \\\
	-DCMAKE_INSTALL_PREFIX:PATH=$LDESTDIR \\\
	-DCMAKE_INSTALL_LIBDIR:PATH=$LDESTDIR/%{_lib} \\\
	-DINCLUDE_INSTALL_DIR:PATH=$LDESTDIR/include \\\
	-DLIB_INSTALL_DIR:PATH=$LDESTDIR/%{_lib} \\\
	-DSYSCONF_INSTALL_DIR:PATH=$LDESTDIR/etc \\\
	-DSHARE_INSTALL_PREFIX:PATH=$LDESTDIR/share \\\
	-DLIB_SUFFIX=%{bits} \\\
	-DBUILD_SHARED_LIBS:BOOL=ON \\\
        -DPV_INSTALL_BIN_DIR:PATH=bin \\\
        -DPV_INSTALL_INCLUDE_DIR:PATH=include \\\
        -DPV_INSTALL_LIB_DIR:PATH=%{_lib} \\\
        -DCMAKE_CXX_COMPILER:FILEPATH=$CXX \\\
        -DCMAKE_C_COMPILER:FILEPATH=$CC \\\
        -DTCL_LIBRARY:PATH=tcl \\\
        -DTK_LIBRARY:PATH=tk \\\
        -DPARAVIEW_BUILD_PLUGIN_AdiosReader:BOOL=ON \\\
        -DPARAVIEW_BUILD_PLUGIN_CoProcessingScriptGenerator:BOOL=ON \\\
        -DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON \\\
        -DPARAVIEW_BUILD_PLUGIN_ForceTime:BOOL=ON \\\
        -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \\\
        -DPARAVIEW_INSTALL_THIRD_PARTY_LIBRARIES:BOOL=OFF \\\
        -DPARAVIEW_INSTALL_DEVELOPMENT:BOOL=ON \\\
        -DVTK_OPENGL_HAS_OSMESA:BOOL=ON \\\
        -DVTK_USE_BOOST:BOOL=ON \\\
        -DVTK_USE_INFOVIS:BOOL=OFF \\\
        -DVTK_USE_N_WAY_ARRAYS:BOOL=ON \\\
        -DVTK_USE_OGGTHEORA_ENCODER:BOOL=ON \\\
        -DVTK_USE_SYSTEM_EXPAT:BOOL=ON \\\
        -DVTK_USE_SYSTEM_FREETYPE:BOOL=ON \\\
        -DVTK_USE_SYSTEM_HDF5:BOOL=ON \\\
        -DVTK_USE_SYSTEM_JPEG:BOOL=ON \\\
        -DVTK_USE_SYSTEM_PNG:BOOL=ON \\\
        -DVTK_USE_SYSTEM_TIFF:BOOL=ON \\\
        -DVTK_USE_SYSTEM_ZLIB:BOOL=ON \\\
        -DXDMF_WRAP_PYTHON:BOOL=ON \\\
        -DBUILD_DOCUMENTATION:BOOL=ON \\\
        -DBUILD_EXAMPLES:BOOL=ON %{?build_node:-DPARAVIEW_BUILD_QT_GUI:BOOL=OFF}
%if 0%{?rhel} > 5
%define paraview_cmake_other_options %{nil}
%else
%define paraview_cmake_other_options \\\
	-DBOOST_INCLUDEDIR:PATH=/usr/include/boost141 \\\
	-DBOOST_LIBRARYDIR:PATH=/usr/lib64/boost141
%endif

%description
ParaView is an application designed with the need to visualize large data
sets in mind. The goals of the ParaView project include the following:

    * Develop an open-source, multi-platform visualization application.
    * Support distributed computation models to process large data sets.
    * Create an open, flexible, and intuitive user interface.
    * Develop an extensible architecture based on open standards.

ParaView runs on distributed and shared memory parallel as well as single
processor systems and has been successfully tested on Windows, Linux and
various Unix workstations and clusters. Under the hood, ParaView uses the
Visualization Toolkit as the data processing and rendering engine and has a
user interface written using a unique blend of Tcl/Tk and C++.

NOTE: The version in this package has NOT been compiled with MPI support.
%if %{build_openmpi}
Install the paraview-openmpi package to get a version compiled with openmpi.
%endif
%if %{build_mpich2}
Install the paraview-mpich2 package to get a version compiled with mpich2.
%endif
%if 0%{?build_node}
This build is tweaked for compute node installation and paraview executable
is not present.
%endif

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{compilerdevel}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%if 0%{?build_node}
This build is tweaked for compute node installation and paraview executable
is not present.
%endif

%package        doc
Summary:        Documentation files for ParaView
Group:          Applications/Engineering
Requires:       %{name} = %{version}-%{release}
%if 0%{?rhel} > 5
BuildArch:      noarch
%endif

%description    doc
%{summary}.


%if %{build_openmpi}
%package        openmpi
Summary:        Parallel visualization application
Group:          Applications/Engineering
Obsoletes:      %{name}-mpi < %{version}-%{release}
Provides:       %{name}-mpi = %{version}-%{release}
Requires:	environment-modules
%{compilerruntimeopenmpi}

%description    openmpi
This package contains copies of the ParaView server binaries compiled with
OpenMPI.  These are named pvserver_openmpi, pvbatch_openmpi, etc.

You will need to load the openmpi-%{_arch} module to setup your path properly.
%if 0%{?build_node}
This build is tweaked for compute node installation and paraview executable
is not present.
%endif

%package        openmpi-devel
Summary:        Development files for %{name}-openmpi
Group:          Development/Libraries
Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}
%{compilerdevelopenmpi}

%description    openmpi-devel
The %{name}-openmpi-devel package contains libraries and header files for
developing applications that use %{name}-openmpi.
%if 0%{?build_node}
This build is tweaked for compute node installation and paraview executable
is not present.
%endif
%endif

%if %{build_mpich2}
%package        mpich2
Summary:        Parallel visualization application
Group:          Applications/Engineering
Requires:       mpich2
Requires:	environment-modules

%description    mpich2
This package contains copies of the ParaView server binaries compiled with
mpich2.  These are named pvserver_mpich2, pvbatch_mpich2, etc.

You will need to load the mpich2-%{_arch} module to setup your path properly.

%if 0%{?build_node}
This build is tweaked for compute node installation and paraview executable
is not present.
%endif

%package        mpich2-devel
Summary:        Development files for %{name}-mpich2
Group:          Development/Libraries
Requires:       %{name}-mpich2%{?_isa} = %{version}-%{release}

%description    mpich2-devel
The %{name}-mpich2-devel package contains libraries and header files for
developing applications that use %{name}-mpich2.
%if 0%{?build_node}
This build is tweaked for compute node installation and paraview executable
is not present.
%endif
%endif


%prep
%setup -q -n ParaView-%{version}%{?rcver}
%patch1 -p1 -b .include
#patch2 -p1 -b .boost
%patch7 -p1 -b .hdf5
#Remove included hdf5 just to be sure
rm -r VTK/Utilities/vtkhdf5


%build
# setup modules here first, even if may not need them - will not hurt
. /etc/profile.d/modules.sh
%{compilerbuildprep}
%{compilerbuildprepmodule}
export MAKE='make'
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
mkdir fedora
pushd fedora
LDESTDIR=%{localdir}
module load hdf5/%{compiler}/%{hdf5version}
cmake .. \
        %{paraview_cmake_options} %{paraview_cmake_other_options}
make VERBOSE=1 %{?_smp_mflags}
module purge
popd
%if %{build_openmpi}
mkdir fedora-openmpi
pushd fedora-openmpi
module load openmpi/%{compiler}
module load hdf5/%{compiler}/%{hdf5version}
LDESTDIR=%{localdiropenmpi}
cmake .. \
        -DPARAVIEW_USE_MPI:BOOL=ON \
        -DICET_BUILD_TESTING:BOOL=ON \
        -DMPI_COMPILER:FILEPATH=mpicxx \
        %{paraview_cmake_options} %{paraview_cmake_other_options}
# Fixup forward paths
#sed -i -e 's,../%{_lib}/openmpi,..,' `find -name \*-forward.c`
make VERBOSE=1 %{?_smp_mflags}
module purge
popd
%endif
%if %{build_mpich2}
mkdir fedora-mpich2
pushd fedora-mpich2
%{_mpich2_load}
cmake .. \
        -DPV_INSTALL_BIN_DIR:PATH=%{_lib}/mpich2/bin \
        -DPV_INSTALL_INCLUDE_DIR:PATH=%{_lib}/mpich2/include/paraview \
        -DPV_INSTALL_LIB_DIR:PATH=%{_lib}/mpich2/lib/paraview \
        -DPARAVIEW_USE_MPI:BOOL=ON \
        -DICET_BUILD_TESTING:BOOL=ON \
        -DMPI_COMPILER:FILEPATH=%{_libdir}/mpich2/bin/mpicxx \
        %{paraview_cmake_options} %{paraview_cmake_other_options}
# Fixup forward paths
sed -i -e 's,../%{_lib}/mpich2,..,' `find -name \*-forward.c`
make VERBOSE=1 %{?_smp_mflags}
%{_mpich2_unload}
popd
%endif


%install
rm -rf $RPM_BUILD_ROOT

# setup modules here first, even if may not need them - will not hurt
. /etc/profile.d/modules.sh

#Fix permissions
find . \( -name \*.txt -o -name \*.xml -o -name '*.[ch]' -o -name '*.[ch][px][px]' \) -print0 | xargs -0 chmod -x

#Install the normal version
pushd fedora
%{compilerbuildprep}
%{compilerbuildprepmodule}
module load hdf5/%{compiler}/%{hdf5version}
export MAKE='make'
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
make install DESTDIR=$RPM_BUILD_ROOT

#Install vtk*Python.so by hand for now
cp -p bin/vtk*Python.so $RPM_BUILD_ROOT%{localdir}/%{_lib}/site-packages/paraview/vtk/
mv $RPM_BUILD_ROOT%{localdir}/%{_lib}/site-packages/paraview/vtk/vtkPV*Python.so $RPM_BUILD_ROOT%{localdir}/%{_lib}/site-packages/paraview/

#Cleanup vtk binaries
#rm $RPM_BUILD_ROOT%{_bindir}/vtk*
module purge
popd

%if %{build_openmpi}
# Install openmpi version
pushd fedora-openmpi
module load openmpi/%{compiler}
module load hdf5/%{compiler}/%{hdf5version}
make install DESTDIR=$RPM_BUILD_ROOT

##Install vtk*Python.so by hand for now
cp -p bin/vtk*Python.so $RPM_BUILD_ROOT%{localdiropenmpi}/%{_lib}/site-packages/paraview/vtk/
mv $RPM_BUILD_ROOT%{localdiropenmpi}/%{_lib}/site-packages/paraview/vtk/vtkPV*Python.so $RPM_BUILD_ROOT%{localdiropenmpi}/%{_lib}/site-packages/paraview/
module purge
popd
%endif

%if %{build_mpich2}
# Install mpich2 version
pushd fedora-mpich2
make install DESTDIR=$RPM_BUILD_ROOT

#Remove mpi copy of man pages
rm -rf $RPM_BUILD_ROOT%{_mandir}

#Install vtk*Python.so by hand for now
cp -p bin/vtk*Python.so $RPM_BUILD_ROOT%{_libdir}/mpich2/lib/paraview/site-packages/paraview/vtk/
mv $RPM_BUILD_ROOT%{_libdir}/mpich2/lib/paraview/site-packages/paraview/vtk/vtkPV*Python.so $RPM_BUILD_ROOT%{_libdir}/mpich2/lib/paraview/site-packages/paraview/
popd
%endif

mkdir -p ${RPM_BUILD_ROOT}%{modulefile_path}
# first the alias
cat <<ENDMODULEFILETRICK >$RPM_BUILD_ROOT/%{modulefile_compiler_alias}
#%Module
module-alias paraview/%{compilerlong} paraview/%{compilerlong}/%{version}
ENDMODULEFILETRICK
%if "%{compiler}" != "%{compilershort}"
echo "module-alias paraview/%{compilershort} paraview/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
echo "module-alias paraview/%{compilershort}/%{version} paraview/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
%endif
%if "%{compiler}" != "%{compilerlong}"
echo "module-alias paraview/%{compiler} paraview/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
echo "module-alias paraview/%{compiler}/%{version} paraview/%{compilerlong}/%{version}" >> $RPM_BUILD_ROOT/%{modulefile_compiler_alias}
%endif
cat <<ENDCOREMODULE > ${RPM_BUILD_ROOT}%{modulefile_path}/%{version}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# paraview rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds paraview %{version} for %{compilerlong} to various paths"
}

module-whatis   "Sets up paraview {version} for %{compilerlong} in your environment"

module load hdf5/%{compiler}/%{hdf5version}
%{compilerbuildprepmodule}
prepend-path PATH "%{localdir}/bin"
prepend-path LD_LIBRARY_PATH "%{localdir}/%{_lib}"
prepend-path LIBRARY_PATH "%{localdir}/%{_lib}"
#prepend-path MANPATH "%{localdir}/share/man"
setenv PARAVIEWDIR "%{localdir}"
append-path -d { } LDFLAGS "-L%{localdir}/%{_lib}"
append-path -d { } INCLUDE "-I%{localdir}/include"
append-path CPATH "%{localdir}/include"
append-path -d { } FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_LDFLAGS "-L%{localdir}/%{_lib}"
append-path -d { } LOCAL_INCLUDE "-I%{localdir}/include"
append-path -d { } LOCAL_CFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_FFLAGS "-I%{localdir}/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{localdir}/include"
ENDCOREMODULE

%if %{build_openmpi}
mkdir -p ${RPM_BUILD_ROOT}%{modulefile_path}/openmpi-%{openmpiversion}
cat <<ENDMODULEMPITRICK > ${RPM_BUILD_ROOT}%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
#%Module
module-alias paraview/%{compiler}/openmpi paraview/%{compilerlong}/openmpi-%{openmpiversion}
ENDMODULEMPITRICK
%if "%{compiler}" != "%{compilershort}"
echo "module-alias paraview/%{compilershort}/openmpi paraview/%{compilerlong}/openmpi-%{openmpiversion}" >> ${RPM_BUILD_ROOT}%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
%endif
%if "%{compiler}" != "%{compilerlong}"
echo "module-alias paraview/%{compilerlong}/openmpi paraview/%{compilerlong}/openmpi-%{openmpiversion}" >> ${RPM_BUILD_ROOT}%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
%endif
cat <<ENDOPENMPIMODULE > ${RPM_BUILD_ROOT}%{modulefile_path}/openmpi-%{openmpiversion}/%{version}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# paraview rpm).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds paraview %{version} for %{compilerlong} openmpi-%{openmpiversion} to various paths"
}

module-whatis   "Sets up paraview {version} for %{compilerlong} openmpi-%{openmpiversion} in your environment"

module load hdf5/%{compiler}/%{hdf5version}
module load openmpi/%{compilerversion}/%{openmpiversion}
prepend-path PATH "%{localdiropenmpi}/bin"
prepend-path LD_LIBRARY_PATH "%{localdiropenmpi}/%{_lib}"
prepend-path LIBRARY_PATH "%{localdiropenmpi}/%{_lib}"
#prepend-path MANPATH "%{localdiropenmpi}/share/man"
setenv PARAVIEWDIR "%{localdiropenmpi}"
append-path -d { } LDFLAGS "-L%{localdiropenmpi}/%{_lib}"
append-path -d { } INCLUDE "-I%{localdiropenmpi}/include"
append-path CPATH "%{localdiropenmpi}/include"
append-path -d { } FFLAGS "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_LDFLAGS "-L%{localdiropenmpi}/%{_lib}"
append-path -d { } LOCAL_INCLUDE "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_CFLAGS "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_FFLAGS "-I%{localdiropenmpi}/include"
append-path -d { } LOCAL_CXXFLAGS "-I%{localdiropenmpi}/include"
ENDOPENMPIMODULE
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc License_v1.2.txt
%if 0%{!?build_node:1}
%{localdir}/bin/paraview
%endif
%{localdir}/bin/pvbatch
%{localdir}/bin/pvblot
%{localdir}/bin/pvdataserver
%{localdir}/bin/pvpython
%{localdir}/bin/pvrenderserver
%{localdir}/bin/pvserver
%{localdir}/bin/smTestDriver
%{localdir}/bin/vtk*
%{localdir}/%{_lib}
%dir %{modulefile_path_top}
%dir %{modulefile_path}
%{modulefile_path}/%{version}
%{modulefile_compiler_alias}

%files devel
%defattr(-,root,root,-)
%{localdir}/bin/kwProcessXML
%{localdir}/include
%if 0%{!?build_node:1}
%dir %{localdir}/share
%dir %{localdir}/share/doc
%{localdir}/share/doc/paraview-%{pv_majmin}/
%endif

%if %{build_openmpi}
%files openmpi
%defattr(-,root,root,-)
%doc License_v1.2.txt
%if 0%{!?build_node:1}
%{localdiropenmpi}/bin/paraview
%endif
%{localdiropenmpi}/bin/pvbatch
%{localdiropenmpi}/bin/pvblot
%{localdiropenmpi}/bin/pvdataserver
%{localdiropenmpi}/bin/pvpython
%{localdiropenmpi}/bin/pvrenderserver
%{localdiropenmpi}/bin/pvserver
%{localdiropenmpi}/bin/smTestDriver
%{localdiropenmpi}/bin/vtk*
%{localdiropenmpi}/%{_lib}
%dir %{modulefile_path_top}
%dir %{modulefile_path}
%dir %{modulefile_path}/openmpi-%{openmpiversion}
%{modulefile_path}/.modulerc-openmpi-%{openmpiversion}
%{modulefile_path}/openmpi-%{openmpiversion}/%{version}

%files openmpi-devel
%defattr(-,root,root,-)
%{localdiropenmpi}/bin/kwProcessXML
%{localdiropenmpi}/include
%dir %{localdiropenmpi}/share
%{localdiropenmpi}/share/man
%if 0%{!?build_node:1}
%dir %{localdiropenmpi}/share/doc
%{localdiropenmpi}/share/doc/paraview-%{pv_majmin}/
%endif
%endif


%if %{build_mpich2}
%files mpich2
%defattr(-,root,root,-)
%doc License_v1.2.txt
%{_libdir}/mpich2/bin/pvbatch_mpich2
%{_libdir}/mpich2/bin/pvdataserver_mpich2
%{_libdir}/mpich2/bin/pvrenderserver_mpich2
%{_libdir}/mpich2/bin/pvserver_mpich2
%{_libdir}/mpich2/bin/smTestDriver_mpich2
%{_libdir}/mpich2/lib/paraview

%files mpich2-devel
%defattr(-,root,root,-)
%{_libdir}/mpich2/include/paraview/
%endif


%changelog
* Tue Dec 27 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-6
- vtkPV*Python.so needs to go into the paraview python dir
- Drop chrpath

* Fri Dec 16 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-5
- Oops, install vtk*Python.so, not libvtk*Python.so

* Mon Dec 12 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-4
- Install more libvtk libraries by hand and manually remove rpath

* Fri Dec 9 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-3
- Add patch from Petr Machata to build with boost 1.48.0

* Thu Dec 1 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-2
- Enable PARAVIEW_INSTALL_DEVELOPMENT and re-add -devel sub-package
- Install libvtk*Python.so by hand for now

* Thu Nov 10 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-1
- Update to 3.12.0

* Fri Oct 28 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-6
- Fixup forward paths for mpi versions (bug #748221)

* Thu Jun 23 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-5
- Add BR qtwebkit-devel, fixes FTBS bug 716151

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-4
- Rebuild for hdf5 1.8.7

* Tue Apr 19 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-3
- No need to move python install with 3.10.1

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 3.10.1-2
- no openmpi on s390(x)

* Mon Apr 18 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-1
- Update to 3.10.1
- Drop build patch fixed upstream

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.0-1
- Update to 3.10.0
- Drop lib and py27 patches fixed upstream
- Add patch for gcc 4.6.0 support
- Update system hdf5 handling
- Cleanup unused build options
- Build more plugins

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 3.8.1-5
- Rebuild for mpich2 soname bump

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 3.8.1-4
- Rebuild for new libOSMesa soname

* Thu Oct 7 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.1-3
- Remove any previous %%{_libdir}/paraview/paraview directories
  which prevent updates

* Tue Oct 5 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.1-2
- Disable install of third party libraries

* Fri Oct 1 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.1-1
- Update to 3.8.1
- Drop devel sub-package
- Drop installpath patch
- Drop hdf5-1.8 patch, build with hdf5 1.8 API
- Cleanup build

* Fri Jul 30 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.0-4
- Add patch to support python 2.7

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.0-2
- Drop doc sub-package

* Tue Jun 1 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.0-1
- Update to 3.8.0
- Update demo patch
- Update hdf5 patch
- Drop old documentation patches
- Add patch to add needed include headers
- Add patch from upstream to fix install path issue

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.6.2-4
- BR qt-assistant-adp-devel
- Don't Require qt4-assistant, should be qt-assistant-adp now, and it (or qt-x11
  4.6.x which Provides it) gets dragged in anyway by the soname dependencies

* Fri Feb 19 2010 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-3
- More MPI packaging changes

* Tue Feb 16 2010 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-2
- Conform to updated MPI packaging guidelines
- Build mpich2 version

* Mon Jan 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-1
- Update to 3.6.2

* Thu Nov 19 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-7
- New location for openmpi (fixes FTBFS bug #539179)

* Mon Aug 31 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-6
- Don't ship lproj, conflicts with vtk

* Thu Aug 27 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-5
- Specify PV_INSTALL_LIB_DIR as relative path, drop install prefix patch
- Update assitant patch to use assistant_adp, don't ship assistant-real

* Wed Aug 26 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-4
- Disable building various plugins that need OverView

* Tue Aug 25 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-3
- Disable building OverView - not ready yet

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.6.1-2
- rebuilt with new openssl

* Wed Jul 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-1
- Update to 3.6.1

* Thu May 7 2009 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-5
- Update doc patch to look for help file in the right place (bug #499273)

* Tue Feb 24 2009 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-4
- Rebuild with hdf5 1.8.2, gcc 4.4.0
- Update hdf5-1.8 patch to work with hdf5 1.8.2
- Add patch to allow build with Qt 4.5
- Move documentation into noarch sub-package

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 3.4.0-3
- rebuild with new openssl

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.4.0-2
- Rebuild for Python 2.6

* Fri Oct 17 2008 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-1
- Update to 3.4.0 final

* Thu Oct 2 2008 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-0.20081002.1
- Update 3.4.0 CVS snapshot
- Update gcc43 patch
- Drop qt patch, upstream now allows compiling against Qt 4.4.*

* Mon Aug 11 2008 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-0.20080811.1
- Update 3.3.1 CVS snapshot
- Update hdf5 patch to drop upstreamed changes
- Fix mpi build (bug #450598)
- Use rpath instead of ls.so conf files so mpi and non-mpi can be installed at
  the same time
- mpi package now just ships mpi versions of the server components
- Drop useless mpi-devel subpackage
- Update hdf5 patch to fix H5pubconf.h -> H5public.h usage

* Wed May 20 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.3.0-0.20080520.1
- Update to 3.3.0 CVS snapshot
- Update qt and gcc43 patches, drop unneeded patches
- Add openssl-devel, gnuplot, and wget BRs
- Update license text filename
- Set VTK_USE_RPATH to off, needed with development versions
- Run ctest in %%check - still need to exclude more tests

* Wed Mar 5 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-5
- Rebuild for hdf5 1.8.0 using compatability API define and new patch

* Mon Feb 18 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Add patch to compile with gcc 4.3

* Fri Jan 18 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-3
- Add patch to fix parallel make
- Obsolete demos package (bug #428528)

* Tue Dec 18 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-2
- Name ld.so.conf.d file with .conf extension
- Drop parallel make for now

* Mon Dec 03 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1
- Use macros for version numbers
- Add patches to fix documentation install location and use assistant-qt4,
  not install copies of Qt libraries, and not use rpath.
- Install ld.so.conf.d file
- Fixup desktop files

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.0.2-2
- Update license tag to BSD
- Fix make %%{_smp_mflags}
- Rebuild for ppc32

* Wed Jul 11 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.0.2-1
- Update to 3.0.2
- Turn mpi build back on
- Add devel packages
- Remove demo package no longer in upstream
- Use cmake macros

* Thu Mar 08 2007 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-6
- Don't build mpi version until upstream fixes the build system

* Fri Dec 22 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-5
- Fix .so permissions
- Patch for const issue
- Patch for new cmake
- Build with openmpi

* Thu Dec 14 2006 - Jef Spaleta <jspaleta@gmail.com> - 2.4.4-4
- Bump and build for python 2.5

* Fri Oct  6 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-3
- Install needed python libraries to get around make install bug

* Wed Oct  4 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-2
- Re-enable OSMESA support for FC6
- Enable python wrapping

* Fri Sep 15 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-1
- Update to 2.4.4

* Thu Jun 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-8
- No OSMesa support in FC5
- Make data sub-package pull in main package (bug #193837)
- A patch from CVS to fix vtkXOpenRenderWindow.cxx
- Need lam-devel for FC6

* Fri Apr 21 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-7
- Re-enable ppc

* Mon Apr 17 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-6
- Exclude ppc due to gcc bug #189160

* Wed Apr 12 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-5
- Cleanup permissions

* Mon Apr 10 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-4
- Add icon and cleanup desktop file

* Mon Apr 10 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-3
- Add VTK_USE_MANGLE_MESA for off screen rendering
- Cleanup source permisions
- Add an initial .desktop file
- Make requirement on -data specific to version
- Don't package Ice-T man pages and cmake files

* Thu Apr  6 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-2
- Add mpi version

* Tue Apr  4 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-1
- Initial Fedora Extras version
