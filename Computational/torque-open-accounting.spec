%if "%{?rhel}" < "6"
%define privdir /var/spool/PBS/server_priv
%else
%define privdir /var/lib/torque/server_priv
%endif

Summary: A simple wrapper to open up torque server_priv directory
Name: torque-open-accounting
Version: 0.1
Release: 1%{?dist}
License: Commercial
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
A simple wrapper to open up torque server_priv directory

%prep

%build

%install

%clean

%triggerin -- torque-scheduler, torque-server
if [ -d %{privdir} ]; then
	chmod 755 %{privdir}
fi

%post
if [ -d %{privdir} ]; then
	chmod 755 %{privdir}
fi

%files
%defattr(-,root,root,-)

%changelog
* Tue May 08 2012 Josko Plazonic <plazonic@math.princeton.edu>
- initial built
