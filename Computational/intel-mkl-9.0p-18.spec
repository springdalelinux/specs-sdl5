%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}

# The destination location for modules files
%define modulesdestination /opt/share/Modules/modulefiles

%ifarch i386
%define intelbits 32
%define intellibdir 32
%endif
%ifarch x86_64
%define intelbits 64
%define intellibdir em64t
%endif

Summary: Intel(R) Math Kernel Library 9.0 for Linux*
Name: intel-mkl
Version: 9.0p
Release: 18.2%{?dist}
License: Copyright (c) 2006 Intel Corporation
Group: Development/Libraries
Vendor: Intel Corporation
URL: http://www.intel.com/software/products/perflib
Prefix: /opt/intel/mkl/9.0
Source: intel-mkl-9.0p-18.noarch.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/sh
Provides: intel-mkl = 9.0p-18
Requires: environment-modules >= 3.2.3
Requires: %{name}-common = %{version}-%{release}
ExclusiveArch: i386 x86_64 noarch

%description
The Intel(R) Math Kernel Library (Intel(R) MKL) for Linux* is composed of highly
optimized mathematical functions for engineering, scientific and financial
applications requiring high performance on Intel(R) platforms. The functional
areas of the library include linear algebra consisting of LAPACK and BLAS,
Discrete Fourier Transforms (DFT), vector transcendental functions (vector math
library/VML), and vector statistical functions (VSL). Intel MKL is optimized for
the features and capabilities of the latest Intel microprocessors.

Originally done with rpm version 4.0.4,
built on nnsrei021 at Fri Oct  6 04:06:23 2006
from intel-mkl-9.0p-18.src.rpm with opt flags -O2

%package        common
Summary:        Common files for intel-mkl library
Group:          Development/Libraries
AutoReqProv: 0

%description    common
Files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux version 9
that are common for all architectures.

%package        devel
Summary:        Development files for intel-mkl library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-devel-common = %{version}-%{release}
AutoReqProv: 0

%description    devel
Development files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux version 9.

%package	devel-common
Summary:        Development files for intel-mkl library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
AutoReqProv: 0

%description    devel-common
Development files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux version 9
that are common for all architectures.

%package	doc
Summary:        Documentation files for intel-mkl library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
AutoReqProv: 0

%description    doc
Documentation files for the Intel(R) Math Kernel Library (Intel(R) MKL) for Linux version 9.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
popd

chmod -R a+rwX,og-w $RPM_BUILD_ROOT/opt/intel

INSTALL_DIR=/opt/intel/mkl/9.0
CONFIG32=$RPM_BUILD_ROOT/$INSTALL_DIR/tools/environment/mklvars32
CONFIG64=$RPM_BUILD_ROOT/$INSTALL_DIR/tools/environment/mklvars64
CONFIGEM64T=$RPM_BUILD_ROOT/$INSTALL_DIR/tools/environment/mklvarsem64t


if [ -f "${CONFIG32}.sh" ] ; then
    echo "export INCLUDE=$INSTALL_DIR/include:"'$INCLUDE'>$CONFIG32.sh
    echo "export LD_LIBRARY_PATH=$INSTALL_DIR/lib/32:"'$LD_LIBRARY_PATH'>>$CONFIG32.sh
    echo "export MANPATH=$INSTALL_DIR/man:"'$MANPATH'>>$CONFIG32.sh
fi
    
if [ -f "${CONFIG64}.sh" ] ; then
    echo "export INCLUDE=$INSTALL_DIR/include:"'$INCLUDE'>$CONFIG64.sh
    echo "export LD_LIBRARY_PATH=$INSTALL_DIR/lib/64:"'$LD_LIBRARY_PATH'>>$CONFIG64.sh
    echo "export MANPATH=$INSTALL_DIR/man:"'$MANPATH'>>$CONFIG64.sh
fi

if [ -f "${CONFIGEM64T}.sh" ] ; then
    echo "export INCLUDE=$INSTALL_DIR/include:"'$INCLUDE'>$CONFIGEM64T.sh
    echo "export LD_LIBRARY_PATH=$INSTALL_DIR/lib/em64t:"'$LD_LIBRARY_PATH'>>$CONFIGEM64T.sh
    echo "export MANPATH=$INSTALL_DIR/man:"'$MANPATH'>>$CONFIGEM64T.sh
fi

if [ -f "${CONFIG32}.csh" ] ; then
    {
    echo "#! /bin/csh
    
    set MKLROOT=\"$INSTALL_DIR\"

    if (\$?INCLUDE) then
	setenv INCLUDE \"\${MKLROOT}/include:\$INCLUDE\"
    else
	setenv INCLUDE \"\${MKLROOT}/include\"
    endif

    if (\$?LD_LIBRARY_PATH) then
	setenv LD_LIBRARY_PATH \"\${MKLROOT}/lib/32:\$LD_LIBRARY_PATH\"
    else
	setenv LD_LIBRARY_PATH \"\${MKLROOT}/lib/32\"
    endif

    if !(\$?MANPATH) then
	setenv MANPATH \"\${MKLROOT}/man:\$MANPATH\"
    else
	setenv MANPATH \"\${MKLROOT}/man\"
    endif"
    }>${CONFIG32}.csh
fi

if [ -f "${CONFIG64}.csh" ] ; then
    {
    echo "#! /bin/csh
    
    set MKLROOT=\"$INSTALL_DIR\"

    if (\$?INCLUDE) then
	setenv INCLUDE \"\${MKLROOT}/include:\$INCLUDE\"
    else
	setenv INCLUDE \"\${MKLROOT}/include\"
    endif

    if (\$?LD_LIBRARY_PATH) then
	setenv LD_LIBRARY_PATH \"\${MKLROOT}/lib/64:\$LD_LIBRARY_PATH\"
    else
	setenv LD_LIBRARY_PATH \"\${MKLROOT}/lib/64\"
    endif

    if !(\$?MANPATH) then
	setenv MANPATH \"\${MKLROOT}/man:\$MANPATH\"
    else
	setenv MANPATH \"\${MKLROOT}/man\"
    endif"
    }>${CONFIG64}.csh
fi

if [ -f "${CONFIGEM64T}.csh" ] ; then
    {
    echo "#! /bin/csh
    
    set MKLROOT=\"$INSTALL_DIR\"

    if (\$?INCLUDE) then
	setenv INCLUDE \"\${MKLROOT}/include:\$INCLUDE\"
    else
	setenv INCLUDE \"\${MKLROOT}/include\"
    endif

    if (\$?LD_LIBRARY_PATH) then
	setenv LD_LIBRARY_PATH \"\${MKLROOT}/lib/em64t:\$LD_LIBRARY_PATH\"
    else
	setenv LD_LIBRARY_PATH \"\${MKLROOT}/lib/em64t\"
    endif

    if !(\$?MANPATH) then
	setenv MANPATH \"\${MKLROOT}/man:\$MANPATH\"
    else
	setenv MANPATH \"\${MKLROOT}/man\"
    endif"
    }>${CONFIGEM64T}.csh
fi

# we do not need this - an rpm should not be uninstalled with this anyway
rm -f $RPM_BUILD_ROOT/opt/intel/mkl/9.0/uninstall.sh
# we do not need itanium either
rm -rf $RPM_BUILD_ROOT/opt/intel/mkl/9.0/lib/64 $RPM_BUILD_ROOT/opt/intel/mkl/9.0/tools/support/data/chklic.x64
rm -rf $RPM_BUILD_ROOT/opt/intel/mkl/9.0/tools/environment/mklvars64*

%ifarch i386
rm -rf $RPM_BUILD_ROOT/opt/intel/mkl/9.0/lib/em64t $RPM_BUILD_ROOT/opt/intel/mkl/9.0/tools/support/data/chklic.em64t $RPM_BUILD_ROOT/opt/intel/mkl/9.0/tools/environment/mklvarsem64t*
%endif
%ifarch x86_64
rm -rf $RPM_BUILD_ROOT/opt/intel/mkl/9.0/lib/32 $RPM_BUILD_ROOT/opt/intel/mkl/9.0/tools/support/data/chklic.x32 $RPM_BUILD_ROOT/opt/intel/mkl/9.0/tools/environment/mklvars32*
%endif
%ifarch i386 x86_64
rm -rf $RPM_BUILD_ROOT/opt/intel/mkl/9.0/{doc,examples,include,interfaces,man,tests,tools/builder,tools/plugins,tools/support/iplid*}
%endif
%ifarch noarch
rm -rf $RPM_BUILD_ROOT/opt/intel/mkl/9.0/{lib,tools/support/data/*,tools/environment/*}
%endif

%ifarch i386 x86_64
mkdir -p $RPM_BUILD_ROOT%{modulesdestination}/intel-mkl/9
cat > $RPM_BUILD_ROOT%{modulesdestination}/intel-mkl/9/%{intelbits} <<ENDDEFAULT
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

prepend-path    INCLUDE $INSTALL_DIR/include
prepend-path    CPATH   $INSTALL_DIR/include
prepend-path    FPATH   $INSTALL_DIR/include
prepend-path    LD_LIBRARY_PATH $INSTALL_DIR/lib/%{intellibdir}
prepend-path    LIBRARY_PATH    $INSTALL_DIR/lib/%{intellibdir}
append-path -delim { } LOCAL_LDFLAGS "-L$INSTALL_DIR/lib/%{intellibdir}"
prepend-path    MANPATH $INSTALL_DIR/man

ENDDEFAULT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%ifarch noarch
%files common
%defattr(-,root,root)
%dir /opt/intel/mkl/9.0
%dir /opt/intel/mkl/9.0/tools
/opt/intel/mkl/9.0/tools/builder
/opt/intel/mkl/9.0/tools/plugins
%dir /opt/intel/mkl/9.0/tools/support
%dir /opt/intel/mkl/9.0/tools/support/data
/opt/intel/mkl/9.0/tools/support/iplid*
%dir /opt/intel/mkl/9.0/tools/environment

%files doc
%defattr(-,root,root)
/opt/intel/mkl/9.0/doc
/opt/intel/mkl/9.0/examples
/opt/intel/mkl/9.0/man
/opt/intel/mkl/9.0/tests

%files devel-common
%defattr(-,root,root)
/opt/intel/mkl/9.0/include
/opt/intel/mkl/9.0/interfaces
%endif

%ifarch i386 x86_64
%files devel
%defattr(-,root,root)
/opt/intel/mkl/9.0/lib/%{intellibdir}/lib*.a

%files
%defattr(-,root,root)
%dir /opt/intel/mkl/9.0/lib
%dir /opt/intel/mkl/9.0/lib/%{intellibdir}
/opt/intel/mkl/9.0/lib/%{intellibdir}/lib*.so
/opt/intel/mkl/9.0/tools/support/data/*
/opt/intel/mkl/9.0/tools/environment/*
%dir %{modulesdestination}/intel-mkl
%dir %{modulesdestination}/intel-mkl/9
%{modulesdestination}/intel-mkl/9/%{intelbits}
%endif
