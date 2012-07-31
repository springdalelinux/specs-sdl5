Summary: A Dynamical Systems Toolkit (Tcl/Tk Version)
Name: dstool-tk
Version: 0.1
Release: 7%{?dist}
License: Distributable (check README)
Group: Scientific/Applications
BuildRoot: %{_tmppath}/%{name}-buildroot
Icon: dstool.xpm
Source0: ftp://macomb.cam.cornell.edu/pub/dstool/Version_tk/dstool_tk.tar.gz
Source1: ftp://macomb.cam.cornell.edu/pub/dstool/Version_tk/ds_doc.tar.gz
Patch0: dstool_tk-linux_compile_and_install.patch
Patch1: dstool_tk_linux_fixproblem.patch
URL: ftp://macomb.cam.cornell.edu/pub/dstool/
Vendor: Cornell University, Center of Applied Mathematics, Ithaca, NY 14853 <dstool_bugs@macomb.tn.cornell.edu>
Packager: Ayub Yaqub, University College London, Centre for Nonlinear Dynamics & its Applications, London, WC1E 6BT <ayub.yaqub@ucl.ac.uk>
BuildRequires: tcl, tcl-devel, tclx, tclx-devel, tk, tk-devel, perl

%description
A Dynamical Systems Toolkit. This software is very useful in the visual study of nonlinear systems and Chaos, as well as finding numerical solutions to differential equations. It has the ability to plot flows and maps in both 2D & 3D phase space (for 3D install Geomview @ http://www.geomview.com). One can also define Poincare surfaces & plot bifurcation diagrams. A number of prebuilt models are included for study - e.g. Lorenz System.

This rpm package has been built from a stable beta (or was it alpha?) version. Nevertheless many extra features are only available in this Tcl/Tk version, which is newer than Version 2.0 Alpha for xview (OpenWindows).

DsTool is property of Cornell University, Center of Applied Math, Ithaca, NY 14853 <dstool_bugs@macomb.tn.cornell.edu>.

This quality Linux rpm uses pristine sources and is courtesy of Ayub Yaqub <ayub.yaqub@ucl.ac.uk>.

%prep
#cd $RPM_BUILD_DIR
#rm -rf *
#zcat $RPM_SOURCE_DIR/dstool_tk.tar.gz | tar -xvf -
#chown -R root.root .
#chmod -R a+rX,g-w,o-w *
%setup -c -a 1 -a 0
%patch0 -p1
%patch1 -p1


%build
DSTOOL=$RPM_BUILD_DIR/%{name}-%{version}
ARCH=linux
export DSTOOL ARCH
make depend ARCH=linux DSTOOL=$RPM_BUILD_DIR/%{name}-%{version} X11_LIBS="-L%{_libdir} -lX11"
make all ARCH=linux DSTOOL=$RPM_BUILD_DIR/%{name}-%{version} X11_LIBS="-L%{_libdir} -lX11"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dstool_tk/src/models
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dstool_tk/src/include
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dstool_tk/bin/linux
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dstool_tk/site_specific
mkdir -p $RPM_BUILD_ROOT%{_datadir}/dstool_tk/config
cp site_specific/Prolog.ps $RPM_BUILD_ROOT%{_datadir}/dstool_tk/site_specific
cp config/* $RPM_BUILD_ROOT%{_datadir}/dstool_tk/config
cp src/include/* $RPM_BUILD_ROOT%{_datadir}/dstool_tk/src/include
cp -R my_dstool lib $RPM_BUILD_ROOT%{_datadir}/dstool_tk/
install -m 755 bin/dstool_tk bin/dscat $RPM_BUILD_ROOT%{_bindir}
install -m 755 bin/linux/dstool_tk $RPM_BUILD_ROOT%{_datadir}/dstool_tk/bin/linux
install -m 644 dstool_tk.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -R help oogl tcl $RPM_BUILD_ROOT%{_datadir}/dstool_tk
rm -rf src/models/*.o
cp -R src/models $RPM_BUILD_ROOT%{_datadir}/dstool_tk/src
chmod -R a+rX,og-w,u+w $RPM_BUILD_ROOT%{_datadir}/dstool_tk
# finally, replace /usr/local/ with just /usr/ in certain files:
pushd $RPM_BUILD_ROOT
perl -pi -e 's|/usr/local/|/usr/|g' ./usr/bin/dstool_tk ./usr/share/dstool_tk/config/* ./usr/share/dstool_tk/my_dstool/{Makefile,README} ./usr/share/dstool_tk/my_dstool/bin/dstool_tk
popd
perl -pi -e 's|/usr/local/|/usr/|g'  README.LINUX README INSTALL

%files
%defattr(-,root,root)
%doc README README.LINUX INSTALL VERSION changes ds_doc/userman/userman.ps.gz ds_doc/userman/userman.dvi.gz
%{_bindir}/ds*
%{_datadir}/dstool_tk
%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Apr  3 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuild for 5 - fixup dependencies and move to /usr from
  /usr/local

* Tue May 06 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for RH 9

* Fri Jul 05 2002 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS, from my SRPMS for 7.2

* Thu Oct 19 2000 Josko Plazonic <plazonic@math.princeton.edu>
- fixed printing to files from within dstool, a couple of other
  things and reorganized the package to better fit local user needs
