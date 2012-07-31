Source10: kmodtool
%define kmodtool bash %{SOURCE10}
%{!?kversion: %define kversion 2.6.18-194.3.1.el5}
# hint: this can he overridden with "--define kversion foo" on the rpmbuild command line, e.g.
# --define "kversion 2.6.16-1.2096_FC5"

%define kmod_name pvfs2
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""
%ifarch ppc
%define smpvar smp
%endif
%ifarch i686 x86_64 ia64
%define xenvar xen
#define kdumpvar kdump
%endif
%ifarch i686
%define PAEvar PAE
%endif
%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?kdumpvar} %{?PAEvar}}
# hint: this can he overridden with "--define kvariant foo bar" on the rpmbuild command line, e.g.
# --define 'kvariant "" smp' 

# we need tis
%define mrelease  2%{?dist}

Name:		pvfs2
Summary:	Parallel virtual file system 2
Version:	2.8.2
Release:        %{mrelease}
License:	LGPL/GPL
Group: 		System Environment/Base
URL: 		http://www.pvfs.org/pvfs2/
Source0: 	ftp://ftp.parl.clemson.edu/pub/pvfs2/pvfs-%{version}.tar.gz
Patch2:		pvfs2-%{version}.filestweak.patch
Buildroot:	%{_tmppath}/%{name}-buildroot
ExclusiveArch:  i686 x86_64
BuildRequires:	db4-devel openssl-devel tetex-dvips tetex-latex latex2html ghostscript
Requires:	%{name}-libs = %{version}-%{release}
BuildRequires: libibverbs libibverbs-devel

%description
Parallel virtual file system 2

%package karma
Group:          System Environment/Base
Summary:	karma GUI for Parallel virtual file system 2
Requires: %{name} = %{version}-%{release}
BuildRequires:	SDL-devel SDL_ttf-devel gtk2-devel

%description karma
karma GUI for Parallel virtual file system 2

%package libs
Group:          System Environment/Base
Summary:        Parallel virtual file system 2 libraries

%description libs
Parallel virtual file system 2 libraries

%package devel
Group:          System Environment/Development
Summary:        Parallel virtual file system 2 development files
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Parallel virtual file system 2 development files

# magic hidden here:
%{expand:%(%{kmodtool} rpmtemplate_kmp %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%prep
%setup -q -c pvfs
%patch2 -p0 -b .filestweak
mkdir kernel

%build
cd pvfs-%{version}
# Kill the stack protection and fortify source stuff...it slows things down
# and pvfs hasn't been audited for it yet
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=.//' | sed -e 's/-fstack-protector//'`
%ifarch x86_64
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%endif
%configure --with-kernel=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu} --with-openib=/usr --enable-shared
#configure --with-kernel=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu} --enable-shared
# clean first to fix a bug in building
make clean
make
make docs
make kernapps

# now build modules
cd src/kernel/linux-2.6
make clean
cd ..
for kvariant in %{kvariants} ; do
	cp -a linux-2.6 _kmod_build_${kvariant}
	ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}-%{_target_cpu}
	pushd _kmod_build_$kvariant
		make -C "${ksrc}" SUBDIRS=${PWD} M=${PWD} modules %{?_smp_mflags}
	popd
done

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}
cd pvfs-%{version}
%makeinstall
mkdir -p $RPM_BUILD_ROOT/%{_initrddir}
install -m 755 examples/pvfs2-server.rc $RPM_BUILD_ROOT/%{_initrddir}/pvfs2-server
install -m 755 examples/pvfs2-client.rc $RPM_BUILD_ROOT/%{_initrddir}/pvfs2-client
mkdir -p $RPM_BUILD_ROOT/sbin
# mount.pvfs2 should not be required for 2.6 kernels
#for i in mount.pvfs2 pvfs2-client pvfs2-client-core; do
for i in pvfs2-client pvfs2-client-core; do
	install -m 755 src/apps/kernel/linux/$i $RPM_BUILD_ROOT/sbin
done

# install modules
cd src/kernel
for kvariant in %{kvariants}
do
	pushd _kmod_build_$kvariant
	mkdir 		 -p $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}
	install -m 644 *.ko $RPM_BUILD_ROOT/lib/modules/%{kverrel}${kvariant}/extra/%{kmod_name}
	popd
done
# Temporarily executable for stripping, fixed later in %%files.
chmod u+x $RPM_BUILD_ROOT/lib/modules/*/extra/%{kmod_name}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig
/sbin/chkconfig --add pvfs2-server
/sbin/chkconfig --add pvfs2-client

%postun -p /sbin/ldconfig

%preun
if [ "$1" -eq 0 ]; then
	/sbin/chkconfig --del pvfs2-server
	/sbin/chkconfig --del pvfs2-client
fi

%files
%defattr(-,root,root,-)
%doc pvfs-%{version}/doc/*.pdf pvfs-%{version}/COPYING pvfs-%{version}/README pvfs-%{version}/ChangeLog 
%{_bindir}/pvfs*
%{_sbindir}/*
/sbin/*
%{_mandir}/*/*
%{_initrddir}/*

%files karma
%defattr(-,root,root,-)
%{_bindir}/karma

%files libs
%defattr(-,root,root,-)
%{_libdir}/libpv*so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libpv*a
%{_libdir}/libpv*so

%changelog
* Thu Jan 03 2008 Josko Plazonic <plazonic@math.princeton.edu>
- new version - 2.7.0

* Thu Sep 12 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for PU_IAS 5

* Thu Jun 22 2006 Josko Plazonic <plazonic@math.princeton.edu>
- Rebuild for 2.6 kernel (2/2WS)
