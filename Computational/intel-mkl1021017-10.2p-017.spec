%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles/intel-mkl
%define modulesversion 10.2
%define modulesminorversion 025
%define install_dir /opt/intel/mkl/10.2.2.%{modulesminorversion}

Summary: Intel(R) Math Kernel Library 10.2 for Linux*
Name: intel-mkl102%{modulesminorversion}
Version: 10.2p
Release: %{modulesminorversion}.5%{?dist}
License: Copyright (c) 2008 Intel Corporation
Group: Development/Libraries
Vendor: Intel Corporation
URL: http://www.intel.com/software/products/perflib
Prefix: /opt/intel/mkl/10.2.2.%{modulesminorversion}
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/sh
%ifarch i486
%define intelbits 32
%define intellibdir 32
%endif
%ifarch x86_64
%define intelbits 64
%define intellibdir em64t
%endif
Provides: intel-mkl102%{modulesminorversion} = 10.2p-%{modulesminorversion}
Requires: intel-mkllib%{modulesminorversion}
Requires: environment-modules >= 3.2.3
ExclusiveArch: i486 x86_64

%description
The Intel(R) Math Kernel Library (Intel(R) MKL) for Linux* is composed of highly
optimized mathematical functions for engineering, scientific and financial
applications requiring high performance on Intel(R) platforms. The functional
areas of the library include linear algebra consisting of LAPACK and BLAS,
Discrete Fourier Transforms (DFT), vector transcendental functions (vector math
library/VML), and vector statistical functions (VSL). Intel MKL is optimized for
the features and capabilities of the latest Intel microprocessors.

%package devel
Group: Development/Libraries
Summary: Intel(R) Math Kernel Library 10.2 for Linux* development files
Requires: intel-mkllibdev%{modulesminorversion} intel-mkl102%{modulesminorversion}
Provides: intel-mkl102%{modulesminorversion}-devel = 10.2p-%{modulesminorversion}

%description devel
This rpm just contains relevant development requirements.

%install

mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/%{modulesversion}/%{modulesminorversion}
cat > $RPM_BUILD_ROOT%{modulesdestination}/%{modulesversion}/%{modulesminorversion}/%{intelbits} <<ENDDEFAULT
#%Module1.0#####################################################################
##
## intel-mkl %{version} %{intelbits}bit modulefile
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using Intel MKL libraries version %{version} %{intelbits} bits"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for Intel MKL libraries version %{version} %{intelbits} bit"

prepend-path    INCLUDE %{install_dir}/include
prepend-path    CPATH   %{install_dir}/include
prepend-path    FPATH   %{install_dir}/include
prepend-path    LD_LIBRARY_PATH %{install_dir}/lib/%{intellibdir}
prepend-path    LIBRARY_PATH    %{install_dir}/lib/%{intellibdir}
prepend-path    MANPATH %{install_dir}/man
setenv		OMP_NUM_THREADS	1
ENDDEFAULT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,root,-)
%dir %{modulesdestination}
%dir %{modulesdestination}/%{modulesversion}
%dir %{modulesdestination}/%{modulesversion}/%{modulesminorversion}
%{modulesdestination}/%{modulesversion}/%{modulesminorversion}/%{intelbits}

%files devel
%defattr(0755,root,root,-)

