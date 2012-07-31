# 32 or 64?
%ifarch x86_64
%define archbits x86_64-rhel3-dynamic
%else
%define archbits x86-rhel3-dynamic
%endif

# No need to strip binaries
%define __os_install_post %{nil}

%define condor_version 6.9.5
#define condor_root /var/condor
%define condor_user condor
%define condor_uid 39262
%define condor_group condor
%define condor_gid 39262

#############################################################################
# Preamble Section
#############################################################################

Summary: Condor High Performance Computing project
Name: condor
Version: %{condor_version}
Release: cses.4%{?dist}
License: Other
Group: System Environment/Daemons
#Source0: condor-%{condor_version}-linux-%{archbits}.tar.gz
Source1: condor.init
Source2: condor_config
Source3: condor_profile
Source4: condor_cshrc
# Include both packages so both can be built
Source5: condor-%{condor_version}-linux-x86-rhel3-dynamic.tar.gz
Source6: condor-%{condor_version}-linux-x86_64-rhel3-dynamic.tar.gz
Packager: %{?_packager:%{_packager}}%{!?_packager:%{_vendor}}
Vendor: %{?_vendorinfo:%{_vendorinfo}}%{!?_vendorinfo:%{_vendor}}
Distribution: %{?_distribution:%{_distribution}}%{!?_distribution:%{_vendor}}
Provides: condor
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
Requires: /usr/sbin/useradd /usr/sbin/groupadd
BuildRequires: tar
ExclusiveArch: i386 x86_64

%description
The goal of the Condor(R) Project is to develop, implement, deploy,
and evaluate mechanisms and policies that support High Throughput
Computing (HTC) on large collections of distributively owned computing
resources. Guided by both the technological and sociological
challenges of such a computing environment, the Condor Team has been
building software tools that enable scientists and engineers to
increase their computing throughput. 


#############################################################################
# Prepatory Section
#############################################################################
%prep
%ifarch i386
%setup -q -T -b 5
%else
%ifarch x86_64
%setup -q -T -b 6
%endif
%endif
mkdir release
tar -C release -xf release.tar

#############################################################################
# Install Section
#############################################################################
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}
cp -ar release/bin/* $RPM_BUILD_ROOT%{_bindir}
rm -f release/sbin/cleanup_relase release/sbin/install_release
cp -ar release/sbin/* $RPM_BUILD_ROOT%{_sbindir}
rm -rf release/bin release/sbin
mkdir -p $RPM_BUILD_ROOT%{_mandir}
cp -ar release/man/* $RPM_BUILD_ROOT%{_mandir}
rm -rf release/man
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -ar release/lib $RPM_BUILD_ROOT%{_libdir}/condor
rm -rf release/lib
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
cp -ar release/libexec $RPM_BUILD_ROOT%{_libexecdir}/condor
rm -rf release/libexec
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp -ar release/include $RPM_BUILD_ROOT%{_includedir}/condor
rm -f $RPM_BUILD_ROOT%{_includedir}/condor/chirp_client.h
cp -a release/src/chirp/chirp_client.h $RPM_BUILD_ROOT%{_includedir}/condor/chirp_client.h
rm -rf release/include

mkdir -p $RPM_BUILD_ROOT/etc/condor
cp %{SOURCE2} $RPM_BUILD_ROOT/etc/condor/condor_config
# now my mods to the configuration file
perl -pi -e '
# Note the location of our files
s|^RELEASE_DIR\s.*|RELEASE_DIR = %{_prefix}|,
s|^BIN\s.*|BIN = %{_bindir}|,
s|^SBIN\s.*|SBIN = %{_sbindir}|,
s|^LIB\s.*|LIB = %{_libdir}/condor|,
s|^LIBEXEC\s.*|LIBEXEC = %{_libexecdir}/condor|,
s|^INCLUDE\s.*|INCLUDE = %{_includedir}/condor|,
s|^LOG\s.*|LOG = /var/log/condor|,
s|^SPOOL\s.*|SPOOL = %{_localstatedir}/local/condor/spool|,
s|^EXECUTE\s.*|EXECUTE = %{_localstatedir}/local/condor/execute|,
s|^CRED_STORE_DIR\s.*|CRED_STORE_DIR = %{_localstatedir}/local/condor/cred_dir|,
s|^LOCAL_CONFIG_FILE\s.*|LOCAL_CONFIG_FILE = /etc/condor/\$(HOSTNAME).local|,
                                                        '   $RPM_BUILD_ROOT%{_sysconfdir}/condor/condor_config

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/condor

#cp %{SOURCE3} $RPM_BUILD_ROOT%{condor_root}/profile
#cp %{SOURCE4} $RPM_BUILD_ROOT%{condor_root}/cshrc

mkdir -p $RPM_BUILD_ROOT/var/log/condor
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/local/condor/{spool,execute,cred_dir}
pushd $RPM_BUILD_ROOT%{_localstatedir}/local/condor
ln -s /var/log/condor log
popd

#
#############################################################################
# Clean Section
#
#############################################################################
%clean
# Remove installed driver after rpm build finished
rm -rf $RPM_BUILD_ROOT

#############################################################################
# Pre (Un)Install Section
#############################################################################

%pre
if [ ! -n "`/usr/bin/id -g %{condor_group} 2>/dev/null`" ]; then
   /usr/sbin/groupadd -g %{condor_gid} %{condor_group} 2>/dev/null
fi

if [ ! -n "`/usr/bin/id -u %{condor_user} 2>/dev/null`" ]; then
   /usr/sbin/useradd -r -g %{condor_group} -d %{_localstatedir}/local/condor -s /sbin/nologin -u %{condor_uid} -c "Condor,207 87 Prospect Ave, 8-6033" %{condor_user} 
fi

%preun
if [ "$1" = 0 ]; then
	/sbin/service condor stop
	/sbin/chkconfig --del condor
fi

#############################################################################
# Post (Un)Install Section
#############################################################################
%post
touch /etc/condor/`hostname -s`.local

%postun
if [ "$1" = 0 ]; then
	rm -rf %{_localstatedir}/local/condor/
fi

#############################################################################
# Files Section
#############################################################################

%files
%defattr(-, root, root, -)
%doc README INSTALL examples release/src
%{_bindir}/*
%{_sbindir}/*
%{_includedir}/condor
%{_libdir}/condor
%{_libexecdir}/condor
%attr(-,%{condor_user},%{condor_group}) /var/log/condor
%dir %attr(-,%{condor_user},%{condor_group}) %{_localstatedir}/local/condor
%attr(-,%{condor_user},%{condor_group}) %{_localstatedir}/local/condor/*
%{_initrddir}/condor
%dir /etc/condor
%config(noreplace) /etc/condor/condor_config
%{_mandir}/man1/*

#############################################################################
# Changelog
#############################################################################
%changelog
* Mon Aug 13 2007 Jonathan Billings <jsbillin@princeton.edu>
- First attempt at making a spec file for condor
