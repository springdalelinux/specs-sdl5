%define licensedir /opt/pathscale/license

Summary: Contains the license for Pathscale compilers for use on Princeton University Campus
Name: pathscale-license
Version: 1.0
Release: 0.PU_IAS.5
License: Commercial
Group: Development/Languages
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
This rpm contains the Princeton University license for Pathscale compilers.  

It just points to the appropriate license server.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{licensedir}
cat > $RPM_BUILD_ROOT%{licensedir}/pscsubscription.xml <<ENDLICENSE
    <copyright text="Copyright 2004, PathScale, Inc. All rights reserved.  Use of this file is permitted only in compliance the terms of your agreement with PathScale.  Modification may disable the software, and is prohibited."/>
    <version value="1.5"/>
    <seats num="2" duration="15" interval="5"/>
    <customer name="Princeton University" id="6022304"/>
    <subscription model="Floating" issuedate="2008-02-19/03:31:05" duration="365" limit="hard" grace="30" log="false" perpetual="true" host="0F3B398913A7BDF9ED165D31740A96E9283EE5A1"/>
    <overage limit="60" period="1440" allowance="0"/>
    <languages value="CC,C,FORTRAN77,FORTRAN90"/>
    <products value="Compiler,Debugger"/>
    <users value="" exclusive="true"/>
    <phonehome value="false" host="dmv.pathscale.com" port="80"/>
    <daemon host="raas03" port="7143"/>
    <checksum value="620000903" value2="2919934980"/>
ENDLICENSE

%clean
rm -rf %{buildroot}

%post
# very lame but for now we need this
if ! grep -qw raas03 /etc/hosts; then
	echo '128.112.130.63 raas03.princeton.edu raas03' >> /etc/hosts
fi

%files
%defattr(-,root,root)
%dir /opt/pathscale
%dir %{licensedir}
%{licensedir}/pscsubscription.xml
