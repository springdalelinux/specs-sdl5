%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}
Summary: Substitute Headers for Intel(R) C++ Compiler for Intel(R) EM64T-based applications, Version 9.1 (9.1.051)
Name: intel-isubhe91051
Version: 9.1.051
Release: 1
License: GPL
Group: Development/Languages
Packager: developer.support@intel.com
Vendor: Intel Corporation
BuildArch:x86_64
Prefix: /opt/intel/cce/9.1.051
Source: intel-isubhe91051-9.1.051-1.em64t.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Provides: intel-isubhe91051 = 9.1.051-1

%description

Originally done with rpm version 4.0.4,
built on pidt-rh73-2.jf.intel.com at Wed May 30 12:42:49 2007
from intel-isubhe91051-9.1.051-1.src.rpm with opt flags -O2

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%dir %attr(0755,root,root) /opt/intel/cce/9.1.051
%dir %attr(0755,root,root) /opt/intel/cce/9.1.051/bin
%attr(0755,root,root) /opt/intel/cce/9.1.051/bin/uninstall.sh
%dir %attr(0755,root,root) /opt/intel/cce/9.1.051/substitute_headers
%attr(0644,root,root) /opt/intel/cce/9.1.051/substitute_headers/libio.tar.gz
