Summary: clusterit is a collection of tools for distributed computing.
Name: clusterit
Version: 2.5
Release: 3%{?dist}
License: BSD with advertising clause (Tim Rightnour), BSD-style (John Bovey)
Group: System/Utilities
URL: http://www.garbled.net/clusterit.html
Source0: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-build
BuildRequires: perl man groff ncurses-devel gcc
%if "%{?rhel}" < "5"
BuildRequires: xorg-x11-devel
%else
BuildRequires: libXpm-devel libXt-devel libXext-devel libXmu-devel
BuildRequires: libX11-devel libSM-devel libICE-devel libXp-devel
%endif

%description
This is a collection of clustering tools to turn your ordinary
everyday pile of UNIX workstations into a speedy parallel beast.

It includes: 
       dsh -- Run a command on lots of machines in parallel.
       rseq -- Run a command on lots of machines in series.
       run -- Run a command on a random machine.
       jsh/jsd -- Run commands on a pool of machines, one per machine.
       pcp/pdf/prm -- distributed copy, df, and rm.
       dvt -- Use many machines interactively simultaneously.
       rvt -- Hacked version of xvt used by dvt to open the terminals.
       barrier/barrierd -- Synchonize your parallel shell scripts.

%prep
%setup -q

%build
%configure --prefix=${RPM_BUILD_ROOT}/usr
#make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
make

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man
%makeinstall

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Mon Oct 27 2008 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 2.5

* Thu Jun  2 2005 Tim Rightnour <root@garbled.net> -
- Fixed spec file to work with newer 2.3.1 release

* Sun Oct  3 2004 Tim Rightnour <root@garbled.net> - 
- Initial build.
