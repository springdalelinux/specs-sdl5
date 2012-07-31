%define sgeinstloc %{_datadir}/sge

%define sgeupdate 5

%ifarch %{ix86}
%define sgearch lx26-x86
%else
%define sgearch lx26-amd64
%endif

Summary: Sun Grid Engine
Name: sge
Version: 6.1
Release: %{sgeupdate}.9%{?dist}
License: Distributable
Group: Applications/System
Source: ge-V61u%{sgeupdate}_TAG-src.tar.gz
Source1: drmaa-0.5.jar
Source2: sgeexecd
Source3: sgemaster
Source4: sge_settings.sh
Source5: sge_settings.csh
Source10: puias_default_template.conf
Patch0: gridengine-puias.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gcc openssl-devel krb5-devel db4-devel pam-devel ncurses-devel
BuildRequires: perl tcsh man groff findutils
BuildRequires: openmotif-devel libXpm-devel libXt-devel libXext-devel libXmu-devel
BuildRequires: libX11-devel libSM-devel libICE-devel libXp-devel 
BuildRequires: java-devel-gcj ant junit libreadline-java-devel javacc ant-junit ant-nodeps ant-swing
Requires: sge-common = %{version}
Requires: shadow-utils chkconfig perl
Requires: openssh-sge

%description
Sun Grid Engine

%package common
Summary: Sun Grid Engine common files
Group: Applications/System

%description common
Sun Grid Engine's common files.

%package sshdevel
Summary: Sun Grid Engine development files for building custom ssh
Group: Applications/System

%description sshdevel
Sun Grid Engine's development files - just used to compile custom ssh daemon.

%package gui
Summary: Sun Grid Engine graphical management tools
Group: Applications/System

%description gui
Sun Grid Engine graphical management tools - qmon only for now.

%package docs
Summary: Sun Grid Engine documentation
Group: Applications/System

%description docs
Sun Grid Engine's common documentation.

%package exec
Summary: Sun Grid Engine exec node related files
Group: Applications/System

%description exec
Sun Grid Engine's exec node related files

%package suid
Summary: Sun Grid Engine suid executables
Group: Applications/System
Requires: sge = %{version}

%description suid
Sun Grid Engine's suid executables.  Not needed by default since we are using
ssh instead of rsh and friends.

%prep
%setup -q -n %{name}-%{version} -c
%patch0 -p0 -b .puias
# this should not be there
perl -pi -e 's|-R/lib/lx26-amd64||' gridengine/source/3rdparty/qtcsh/LINUXAMD64_24/Makefile
# teach it where to look for DRMAA library
perl -pi -e "s,^DRMAAJ05BASE=.*,DRMAAJ05BASE=%{_sourcedir}," gridengine/source/scripts/distinst.site
# cleanup
rm -rf `find . -name CVS`

%build
export JAVA_HOME=/usr/lib/jvm/java-1.4.2-gcj
%ifarch x86_64
export SGE_INPUT_CFLAGS=-fPIC
%endif
cd gridengine/source
./aimk -only-depend
scripts/zerodepend
./aimk depend
./aimk
./aimk -htmlman

%install
export JAVA_HOME=/usr/lib/jvm/java-1.4.2-gcj
cd gridengine/source
mkdir tempinstall
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{sgeinstloc}
echo Y | scripts/distinst -basedir $RPM_BUILD_ROOT%{sgeinstloc} -vdir 6.1 -nobdb -noopenssl -allall
# now install some devel stuff
cp LINUX*/libuti.a LINUX*/liblck.a LINUX*/librmon.a 3rdparty/remote/LINUX*/libsgeremote.a $RPM_BUILD_ROOT%{sgeinstloc}/*/lib/lx*/
cd $RPM_BUILD_ROOT%{sgeinstloc}/*
# remove what we do not need
rm -rf dtrace ckpt/cpr_* ckpt/cray_* ckpt/README.{cpr,cray} catman doc/man*
# take care of man files
find man -type f -exec gzip "{}" \;

# exec spool dir
mkdir -p $RPM_BUILD_ROOT/var/spool/sge
# main spool dir
mkdir -p $RPM_BUILD_ROOT/var/sge/default
# possible berkeley dir
mkdir -p $RPM_BUILD_ROOT/var/sge/db

# startup scripts
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}

# default shell configs
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 %{SOURCE4} %{SOURCE5} $RPM_BUILD_ROOT/etc/profile.d

# default setup configs
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{sgeinstloc}/6.1/puias_default_template.conf

# default master install from above
cat > $RPM_BUILD_ROOT%{sgeinstloc}/6.1/puias_install_qmaster <<ENDMASTER
#!/bin/sh
export SGE_ROOT=%{sgeinstlock}/6.1
cd %{sgeinstloc}/6.1
./inst_sge -m -auto %{sgeinstloc}/6.1/puias_default_template.conf
ENDMASTER

# default execd install from above
cat > $RPM_BUILD_ROOT%{sgeinstloc}/6.1/puias_install_execd <<ENDMASTER
#!/bin/sh
export SGE_ROOT=%{sgeinstloc}
cd %{sgeinstloc}/6.1
./inst_sge -x -auto %{sgeinstloc}/6.1/puias_default_template.conf
ENDMASTER

chmod a+rx $RPM_BUILD_ROOT%{sgeinstloc}/6.1/puias_install*

ln -sf /var/sge/default $RPM_BUILD_ROOT%{sgeinstloc}/*/

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/useradd -M -o -u 88 -d /var/spool/sge -s /sbin/nologin -c "SGE User" sgeadmin > /dev/null 2>&1 || :

%post
check_service() {
	if ! grep -q ^$1 /etc/services; then
		echo "$1 $2/tcp" >> /etc/services
	fi
}
check_service sge_qmaster 6444
check_service sge_execd 6445
/sbin/chkconfig --add sgeexecd
/sbin/chkconfig --add sgemaster

%preun
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del sgeexecd
	/sbin/chkconfig --del sgemaster
fi

%postun
remove_service() {
	if grep -q "^$1 $2/tcp$" /etc/services; then
		perl -pi -e "s,^$1 $2/tcp\n,," /etc/services
	fi
}
if [ "$1" = 0 ]; then
	remove_service sge_qmaster 6444
	remove_service sge_execd 6445
	/usr/sbin/userdel sgeadmin > /dev/null 2>&1 || :
fi


%files
%defattr(-, root, root, 0755)
%dir %{sgeinstloc}/*/bin
%dir %{sgeinstloc}/*/utilbin
%dir %{sgeinstloc}/*/bin/*
%{sgeinstloc}/*/bin/*/*
%exclude %{sgeinstloc}/*/bin/*/qmon
%dir %{sgeinstloc}/*/utilbin/*
%{sgeinstloc}/*/utilbin/*/*
%exclude %{sgeinstloc}/*/utilbin/*/authuser
%exclude %{sgeinstloc}/*/utilbin/*/rlogin
%exclude %{sgeinstloc}/*/utilbin/*/rsh
%exclude %{sgeinstloc}/*/utilbin/*/testsuidroot
%dir %{sgeinstloc}/*/lib/lx*
%{sgeinstloc}/*/lib/lx*/lib*so*
%exclude %{sgeinstloc}/*/lib/lx*/libXltree*
%{sgeinstloc}/*/examples/jobsbin/lx*
%dir %attr(755,sgeadmin,sgeadmin) /var/spool/sge
%dir %attr(755,sgeadmin,root) /var/sge
%dir %attr(755,sgeadmin,root) /var/sge/default
%dir %attr(755,sgeadmin,root) /var/sge/db
%{_initrddir}/sge*
/etc/profile.d/sge*
%{sgeinstloc}/*/puias_install*

%files common
%defattr(-, root, root, 0755)
%dir %{sgeinstloc}
%dir %{sgeinstloc}/*
%doc %{sgeinstloc}/*/man
%exclude %{sgeinstloc}/*/man/*/qmon*
%dir %{sgeinstloc}/*/lib
%{sgeinstloc}/*/lib/*jar
%dir %{sgeinstloc}/*/3rd_party
%{sgeinstloc}/*/3rd_party/3*
%{sgeinstloc}/*/ckpt
%{sgeinstloc}/*/include
%{sgeinstloc}/*/inst*
%{sgeinstloc}/*/mpi
%{sgeinstloc}/*/pvm
%{sgeinstloc}/*/util
%{sgeinstloc}/6.1/default
%{sgeinstloc}/*/puias_default_template.conf

%files sshdevel
%defattr(-, root, root, 0755)
%{sgeinstloc}/*/lib/lx*/lib*.a

%files gui
%defattr(-, root, root, 0755)
%{sgeinstloc}/*/lib/lx*/libXltree*
%{sgeinstloc}/*/qmon
%{sgeinstloc}/*/man/*/qmon*
%{sgeinstloc}/*/bin/*/qmon
%{sgeinstloc}/*/3rd_party/qmon

%files docs
%defattr(-, root, root, 0755)
%doc %{sgeinstloc}/*/doc
%doc %{sgeinstloc}/*/examples
%exclude %{sgeinstloc}/*/examples/jobsbin/lx*

%files suid
%defattr(-, root, root, 0755)
%{sgeinstloc}/*/utilbin/*/authuser
%{sgeinstloc}/*/utilbin/*/rlogin
%{sgeinstloc}/*/utilbin/*/rsh
%{sgeinstloc}/*/utilbin/*/testsuidroot


%changelog
* Sun Jun 03 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
