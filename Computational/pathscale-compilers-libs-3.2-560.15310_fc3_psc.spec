%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}
%define modulesdestination /opt/share/Modules/modulefiles

# The name of the modules RPM
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}

Summary: Runtime libraries for the PathScale(TM) Compiler Suite.
Name: pathscale32-compilers-libs
Version: 3.2
%define shortversion %( echo %{version} | cut -b1 )
%define numversion 0%( echo %{version} | tr -d . )
Release: 560.15310_fc3_psc.1.PU_IAS.5
License: LGPL, GPL and proprietary
Group: Development/Languages
Packager: PathScale Builder <builder@pathscale.com>
Vendor: PathScale, LLC.
URL: http://www.pathscale.com/
BuildArch: x86_64
Source: pathscale-compilers-libs-3.2-560.15310_fc3_psc.i386.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/sh, grep
Requires: %{modules_rpm_name}
Provides: libinstr.so.1, libinstr.so.1()(64bit), libinstr.so.1(LIBINSTR_1.0), libinstr.so.1(LIBINSTR_1.0)(64bit), libmpath.so.1, libmpath.so.1()(64bit), libmpath.so.1(LIBMPATH_1.0), libmpath.so.1(LIBMPATH_1.0)(64bit), libmpath.so.1(LIBMPATH_PRIVATE), libmpath.so.1(LIBMPATH_PRIVATE)(64bit), libmv.so.1, libmv.so.1()(64bit), libmv.so.1(LIBMV_1.0), libmv.so.1(LIBMV_1.0)(64bit), libopenmp.so.1, libopenmp.so.1()(64bit), libopenmp.so.1(LIBOPENMP_1.0), libopenmp.so.1(LIBOPENMP_1.0)(64bit), libpathfortran.so.1, libpathfortran.so.1()(64bit), libpathfortran.so.1(LIBPATHFORTRAN_1.0), libpathfortran.so.1(LIBPATHFORTRAN_1.0)(64bit), libpathfortran.so.1(LIBPATHFORTRAN_PRIVATE_1.0), libpathfortran.so.1(LIBPATHFORTRAN_PRIVATE_1.0)(64bit), libpscrt.so.1, libpscrt.so.1()(64bit), libpscrt.so.1(LIBPSCRT_1.0), libpscrt.so.1(LIBPSCRT_1.0)(64bit), pathscale-compilers-libs = 3.2-560.15310_fc3_psc
Obsoletes: pathscale-base
BuildRequires: findutils

%description
The pathscale-compilers-libs package contains shared libraries used at
runtime by programs compiled with the PathScale(TM) Compiler Suite.

Originally done with rpm version 4.3.2,
built on eng-05.pathscale.com at Mon Jun 16 20:37:22 2008
from pathscale-c-3.2-560.15310_fc3_psc.src.rpm with opt flags -O2 -g -pipe -m32 -march=i386 -mtune=pentium4

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
chmod -R a+rX .
find . -name lib\*so.1 -exec chmod a+rx '{}' \;
cd opt/pathscale
mkdir %{version}
# just so that there is something there when we use modules on nodes
mkdir %{version}/bin
mkdir %{version}/man
mv lib %{version}
popd

mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/pathscale/%{version}

cat > $RPM_BUILD_ROOT%{modulesdestination}/pathscale/%{version}/64 <<ENDDEFAULT
#%Module1.0#####################################################################
##
## %{compiler} %{intelversion} %{inteltype} modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Pathscale compilers %{version} bits"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for the Pathscale compilers %{version} bits"
prepend-path    PATH            /opt/pathscale/%{version}/bin
prepend-path    MANPATH         /opt/pathscale/%{version}/man
prepend-path    LD_LIBRARY_PATH /opt/pathscale/%{version}/lib/%{version}:/opt/pathscale/%{version}/lib/%{version}/32
set     version      "3.2.3"
ENDDEFAULT

cat > $RPM_BUILD_ROOT%{modulesdestination}/pathscale/.modulerc-pathscale-%{numversion}-64 <<ENDGENERIC
#%Module
module-alias pathscale/%{shortversion} pathscale/%{version}
ENDGENERIC
mkdir $RPM_BUILD_ROOT%{modulesdestination}/pathscale/%{shortversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/pathscale/%{shortversion}/.modulerc-pathscale-%{numversion}-64 <<ENDMOREGENERIC
#%Module
module-alias pathscale/%{shortversion}/64 pathscale/%{version}/64
ENDMOREGENERIC

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%dir /opt/pathscale/
%dir /opt/pathscale/%{version}
%dir /opt/pathscale/%{version}/*
%dir /opt/pathscale/%{version}/lib/%{version}
/opt/pathscale/%{version}/lib/%{version}/32/lib*
/opt/pathscale/%{version}/lib/%{version}/lib*
%dir %{modulesdestination}/pathscale
%dir %{modulesdestination}/pathscale/%{version}
%{modulesdestination}/pathscale/%{version}/64
%dir %{modulesdestination}/pathscale/%{shortversion}
%{modulesdestination}/pathscale/.modulerc-pathscale-%{numversion}-64
%{modulesdestination}/pathscale/%{shortversion}/.modulerc-pathscale-%{numversion}-64
