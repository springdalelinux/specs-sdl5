# local installation point for modules
%define localmoduledir /usr/local/share/Modules/modulefiles
%define optmoduledir /opt/share/Modules/modulefiles

Name:           environment-modules
Version:        3.2.3
Release:        20%{?dist}
Summary:        Provides dynamic modification of a user's environment

Group:          System Environment/Base
License:        GPL
URL:            http://modules.sourceforge.net/
Source0:        http://dl.sf.net/modules/modules-%{version}.tar.bz2
Source1:	modulecmd.tcl
Source2:	modulecmd.tcl.original
Patch1:		modules-xrstrtok.patch
Patch2:		modules-pbstweak.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  tcl-devel, tclx-devel
Requires:	tclx, tcl

%description
The Environment Modules package provides for the dynamic modification of
a user's environment via modulefiles.

Each modulefile contains the information needed to configure the shell
for an application. Once the Modules package is initialized, the
environment can be modified on a per-module basis using the module
command which interprets modulefiles. Typically modulefiles instruct
the module command to alter or set shell environment variables such as
PATH, MANPATH, etc. modulefiles may be shared by many users on a system
and users may have their own collection to supplement or replace the
shared modulefiles.

Modules can be loaded and unloaded dynamically and atomically, in an
clean fashion. All popular shells are supported, including bash, ksh,
zsh, sh, csh, tcsh, as well as some scripting languages such as perl.

Modules are useful in managing different versions of applications.
Modules can also be bundled into metamodules that will load an entire
suite of different applications.


%prep
%setup -q -n modules-%{version}
%patch1 -p1 -b .xrstrtok
%patch2 -p1 -b .pbstweak
# change the default man path
perl -pi -e 's|/usr/man|/usr/share/man:/usr/man:/usr/local/share/man:/usr/local/man:/usr/X11R6/man|'g cmdPath.c

%build
%configure --disable-versioning --prefix=%{_datadir} --exec-prefix=%{_datadir}/Modules
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
ln -s %{_datadir}/Modules/init/bash $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.sh
ln -s %{_datadir}/Modules/init/csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.csh
# we will be placing our modules mostly in %{localmoduledir} and %{optmoduledir}
mkdir -p $RPM_BUILD_ROOT%{localmoduledir}
mkdir -p $RPM_BUILD_ROOT%{optmoduledir}
cat > $RPM_BUILD_ROOT/%{_datadir}/Modules/init/.modulespath <<ENDLOCALMODULESPATH
#  Modulepath initial setup
#  ========================
#
#  This file defines the initial setup for the module files search path.
#  Comments may be added anywhere, which begin on # and continue until the
#     end of the line
#  Each line containing a single path will be added to the MODULEPATH
#     environment variable. You may add as many as you want - just
#     limited by the maximum variable size of your shell.
#
#                               # location of version files
#/usr/share/Modules/$MODULE_VERSION/modulefiles # Module pkg modulefiles (if versioning)
/usr/share/Modules/modulefiles                                  # General module files
# /usr/share/Modules/your_contribs                      # Edit for your requirements
%{localmoduledir}
%{optmoduledir}
ENDLOCALMODULESPATH

mv $RPM_BUILD_ROOT%{_bindir}/modulecmd $RPM_BUILD_ROOT%{_bindir}/modulecmd-bin
#cat > $RPM_BUILD_ROOT%{_bindir}/modulecmd <<ENDCMD
##!/bin/bash
#MALLOC_CHECK_=0 /usr/bin/modulecmd-bin "\$@"
#ENDCMD
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/modulecmd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.GPL README TODO
%{_sysconfdir}/profile.d/*
%{_bindir}/modulecmd-bin
%attr(755,root,root) %{_bindir}/modulecmd
%{_datadir}/Modules/
%{_mandir}/man1/module.1.gz
%{_mandir}/man4/modulefile.4.gz
%dir %{localmoduledir}
%dir %{localmoduledir}/..
%dir %{optmoduledir}
%dir %{optmoduledir}/..
%dir %{optmoduledir}/../..

%changelog
* Mon Feb 28 2011 Josko Plazonic <plazonic@math.princeton.edu>
- allow use of -d in addition to -delim

* Mon Mar  3 2008 Josko Plazonic <plazonic@math.princeton.edu>
- fix a case where tcsh login shell user tries to pbs submit
  a bash script

* Fri Feb 15 2008 Josko Plazonic <plazonic@math.princeton.edu>
- fix a bug with number sorting (do not trim too many 0s...)

* Thu Dec 13 2007 Josko Plazonic <plazonic@math.princeton.edu> 
- sort .modulerc* files before using them, or else they are 
  useless...

* Mon Oct 22 2007 Josko Plazonic <plazonic@math.princeton.edu>
- compare all strings directory by directory

* Sat Sep 15 2007 Josko Plazonic <plazonic@math.princeton.edu>
- load not only .modulerc but anything beginning with .modulerc

* Tue Sep 11 2007 Josko Plazonic <plazonic@math.princeton.edu>
- modify module sorting so that 10 > 9 (i.e. try to use number
  sorting for numbers rather then strings)

* Mon Sep 10 2007 Josko Plazonic <plazonic@math.princeton.edu>
- replace binary module command with the tcl version

* Tue Dec 01 2006 Josko Plazonic <plazonic@math.princeton.edu>
- added local and opt module dirs

* Tue Aug 28 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-2
- Rebuild for FC6

* Fri Jun  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-1
- Update to 3.2.3

* Fri May  5 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.2-1
- Update to 3.2.2

* Fri Mar 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1

* Thu Feb  9 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0p1-1
- Update to 3.2.0p1

* Fri Jan 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-2
- Add profile.d links

* Tue Jan 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Fedora Extras packaging
