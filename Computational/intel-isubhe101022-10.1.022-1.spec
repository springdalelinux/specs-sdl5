%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}
Summary: Substitute Headers for Intel(R) C++ Compiler for applications running on Intel(R) 64, Version 10.1 (10.1.022)
Name: intel-isubhe101022
Version: 10.1.022
Release: 1
License: GPL
Group: Development/Languages
Packager: http://www.intel.com/software/products/support
Vendor: Intel Corporation
BuildArch: x86_64
Prefix: /opt/intel/cce/10.1.022
Source: intel-isubhe101022-10.1.022-1.em64t.rpm
BuildRoot: %{_tmppath}/%{name}-%{version}-root
AutoReqProv: 0
Requires: /bin/bash
Provides: intel-isubhe101022 = 10.1.022-1

%description

Originally done with rpm version 4.3.3,
built on pidt-linuxlab-99 at Fri Feb  6 13:55:39 2009
from intel-isubhe101022-10.1.022-1.src.rpm with opt flags -O2

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
rpm2cpio %{SOURCE0}|cpio -i -d
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%dir %attr(0755,root,root) /opt/intel/cce/10.1.022
%dir %attr(0755,root,root) /opt/intel/cce/10.1.022/bin
%attr(0755,root,root) /opt/intel/cce/10.1.022/bin/uninstall.sh
%dir %attr(0755,root,root) /opt/intel/cce/10.1.022/substitute_headers
%attr(0644,root,root) /opt/intel/cce/10.1.022/substitute_headers/libio.tar.gz
