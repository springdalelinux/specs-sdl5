%define licensedir /opt/intel/licenses

Summary: Contains the license for Intel Compilers for use on Princeton University Campus
Name: intel-license
Version: 1.0
Release: 0.PU_IAS.2cluster
License: Commercial
Group: Development/Languages
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
This rpm contains the Princeton University license for Intel compilers.  

It just points to the appropriate license server.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{licensedir}
cat > $RPM_BUILD_ROOT%{licensedir}/intel.client.license.dat <<ENDLICENSE
SERVER ernie.Princeton.EDU 00065BF65E09 28518
USE_SERVER
ENDLICENSE
cd $RPM_BUILD_ROOT%{licensedir}
ln -s intel.client.license.dat intel.license.lic 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{licensedir}
%dir %{licensedir}/..
%{licensedir}/intel*
