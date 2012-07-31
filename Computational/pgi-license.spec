%define licensedir /opt/pgi

Summary: Contains the license for PGI compilers for use on Princeton University Campus
Name: pgi-license
Version: 1.0
Release: 0%{?dist}
License: Commercial
Group: Development/Languages
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
This rpm contains the Princeton University license for PGI compilers.  

It just points to the appropriate license server.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{licensedir}
cat > $RPM_BUILD_ROOT%{licensedir}/license.dat <<ENDLICENSE
SERVER raas03.Princeton.EDU 00065bf65e09 27012
USE_SERVER
ENDLICENSE

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{licensedir}
%{licensedir}/license.dat
