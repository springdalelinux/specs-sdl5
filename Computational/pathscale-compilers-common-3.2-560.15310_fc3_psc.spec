%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}
Summary: Common files for the PathScale(TM) Compiler Suite.
Name: pathscale32-compilers
Version: 3.2
Release: 560.15310_fc3_psc.1.PU_IAS.5
License: GPL and proprietary
Group: Development/Languages
Packager: PathScale Builder <builder@pathscale.com>
Vendor: PathScale, LLC.
URL: http://www.pathscale.com/
BuildArch: x86_64
Prefix: /opt/pathscale
Source: pathscale-compilers-common-3.2-560.15310_fc3_psc.i386.rpm
Source1: pathscale-c-3.2-560.15310_fc3_psc.i386.rpm 
Source2: pathscale-c++-3.2-560.15310_fc3_psc.i386.rpm 
Source3: pathscale-f90-3.2-560.15310_fc3_psc.i386.rpm
Source4: pathscale-compilers-libs-lgpl-3.2-560.15310_fc3_psc.i386.rpm
Source5: pathscale-sub-client-3.2-231.469_fc3_psc.i386.rpm
Source6: pathscale-pathopt2-3.2-115.97_fc3_psc.i386.rpm
Source7: pathscale-pathdb-3.2-230.913_fc3_psc.x86_64.rpm
Source8: pathscale-pathdb-3.2-229.913_fc3_psc.i386.rpm
Source9: pathscale-compilers-docs-3.2-560.15310_fc3_psc.i386.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/sh, /usr/bin/python, be.so, binutils >= 2.12.90.0.15, glibc >= 2.2.5, glibc-devel >= 2.2.5, grep, ipl.so, libc.so.6, libc.so.6(GLIBC_2.0), libc.so.6(GLIBC_2.1), libc.so.6(GLIBC_2.1.3), libc.so.6(GLIBC_2.2), libc.so.6(GLIBC_2.2.3), libc.so.6(GLIBC_2.3), libc.so.6(GLIBC_2.3.4), libdl.so.2, libdl.so.2(GLIBC_2.0), libdl.so.2(GLIBC_2.1), libgcc_s.so.1, libgcc_s.so.1(GLIBC_2.0), libm.so.6, libm.so.6(GLIBC_2.0), libm.so.6(GLIBC_2.1), libmpath.so.1, libmv.so.1, libstdc++.so.6, libstdc++.so.6(CXXABI_1.3), libstdc++.so.6(GLIBCXX_3.4), make, pathscale-compilers-libs = 3.2-560.15310_fc3_psc, pathscale-sub-client = 3.2
Provides: barcelona.so, be.so, core.so, em64t.so, ipa.so, ipl.so, lno.so, opteron.so, whirl2c.so, whirl2f.so, wolfdale.so, wopt.so, pathscale-compilers-common = 3.2-560.15310_fc3_psc
Provides: pathscale-c++ = 3.2-560.15310_fc3_psc 
Provides: pathscale-f90 = 3.2-560.15310_fc3_psc 
Provides: pathscale-pathdb = 3.2-229.913_fc3_psc 
Provides: pathscale-pathdb = 3.2-230.913_fc3_psc
Provides: pathscale-c = 3.2-560.15310_fc3_psc
Provides: pathscale-pathopt2 = 3.2-115.97_fc3_psc
Provides: pathscale-sub-client = 3.2-231.469_fc3_psc
Provides: pathscale-compilers-libs-lgpl = 3.2-560.15310_fc3_psc
Obsoletes: pathscale-binutils <= 2.15.91.0.1, pathscale-binutils-docs <= 2.15.91.0.1, pathscale-gcc <= 3.3.1, pathscale-gnu-devel <= 2.3.3, pathscale-gnu-devel-docs <= 2.3.3, pathscale-libgcc <= 3.3.1
Requires: pathscale-license pathscale32-compilers-libs
Provides: pathscale-compilers = %{version}-%{release}

%description
The pathscale-compilers-common package contains files shared among
several components of the PathScale(TM) Compiler Suite.

Originally done with rpm version 4.3.2,
built on eng-05.pathscale.com at Mon Jun 16 20:37:22 2008
from pathscale-c-3.2-560.15310_fc3_psc.src.rpm with opt flags -O2 -g -pipe -m32 -march=i386 -mtune=pentium4

%package docs
Summary: Documentation for the PathScale(TM) Compiler Suite.
Group: Development/Documentation
Requires: %{name} = %{version}-%{release}
Provides: pathscale-compilers-docs = 3.2-560.15310_fc3_psc

%description docs
Documentation for the PathScale(TM) Compiler Suite.

Copyright 2007 PathScale, LLC.
Copyright 2006, 2007 QLogic Corporation. Copyright 2002, 2003, 2004,
2005 PathScale, Inc.  All Rights Reserved.  See the file
/opt/pathscale/share/doc/pathscale-compilers-3.2/LEGAL.pdf for legal notices.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
for i in %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9}; do
	rpm2cpio $i |cpio -i -d
done
chmod -R a+rX .
rm -f etc/profile.d/pathscale-compilers*
cd opt/pathscale
mkdir %{version}
mv bin  compat-gcc etc man include lib share %{version}/
cd %{version}/bin
ln -s pathdb-x86_64-%{version} pathdb
cd ../lib/%{version}
ln -sf /opt/pathscale/license/pscsubscription.xml pscsubscription.xml
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%dir /opt/pathscale/%{version}/bin
/opt/pathscale/%{version}/bin/*
/opt/pathscale/%{version}/compat-gcc
/opt/pathscale/%{version}/etc
/opt/pathscale/%{version}/include
/opt/pathscale/%{version}/share
%exclude /opt/pathscale/%{version}/share/doc
%dir /opt/pathscale/%{version}/lib
%dir /opt/pathscale/%{version}/lib/%{version}
%dir /opt/pathscale/%{version}/lib/%{version}/32
/opt/pathscale/%{version}/lib/%{version}/32/*
/opt/pathscale/%{version}/lib/%{version}/[a-zA-Z]*

%files docs
%defattr(-,root,root,755)
%dir /opt/pathscale/%{version}/man
/opt/pathscale/%{version}/man/*
/opt/pathscale/%{version}/share/doc
