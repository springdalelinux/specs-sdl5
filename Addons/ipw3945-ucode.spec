Summary: firmware for ipw3945
Name: ipw3945-ucode
Version: 1.14.2
Release: 0%{?dist}
License: GPL
Group: System Environment/Kernel
URL: http://bughost.org/ipw3945/ucode/
Source: http://bughost.org/ipw3945/ucode/%{name}-%{version}.tgz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
firmware for the Intel Pro/Wireless 3945 ABG chipset

%prep
%setup

%install
mkdir -p $RPM_BUILD_ROOT/lib/firmware
cp ipw3945.ucode $RPM_BUILD_ROOT/lib/firmware

%clean
%{__rm} -rf %{buildroot}

%files 
%defattr(-, root, root, 0755)
%doc README.%{name} LICENSE.%{name}
/lib/firmware/ipw3945.ucode

%changelog
* Fri Apr 13 2007 Thomas Uphill <uphill@ias.edu>
- PU_IAS 5 build
