Summary: A dummy libXft.so.1 library
Name: libXft1
Version: 1.0
Release: 0%{?dist}
License: GPL
Group: System Environment/Libraries 
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: libXft
%ifarch %{ix86}
Provides: libXft.so.1
%endif
%ifarch x86_64
Provides: libXft.so.1()(64bit)  
%endif

%description
A dummy libXft.so.1 library - just a symlink to
libXft.so.2.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_libdir}
cd %{buildroot}/%{_libdir}
ln -sf libXft.so.2 libXft.so.1

%clean
rm -rf %{buildroot}

%files
%attr(0755,root,root) %{_libdir}/libXft.so.1
