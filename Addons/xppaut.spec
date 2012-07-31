Summary: XPPAUT the differential equations tool
Name: xppaut
Version: 5.91
Release: 2%{?dist}
License: Distributable (check README)
Group: Scientific/Applications
BuildRoot: /tmp/%{name}-buildroot
Source0: ftp://ftp.math.pitt.edu/pub/bardware/xppaut%{version}.tar.gz
Source1: xpp.script
Patch0: xppaut5.4-mkavi_fix.patch
Patch1: xppaut5.5-errno.patch
Patch2: xppaut5.5-c++-fixes
Patch3: xppaut5.91-fixes2
URL: http://www.math.pitt.edu/~bard/xpp/xpp.html
Vendor: G. Bard Ermentrout Department of Mathematics University of Pittsburg
Packager: Josko Plazonic, Mathematics Department Princeton University <plazonic@math.princeton.edu>
Prefix: %{_prefix}
BuildRequires: gcc-c++ libX11-devel xorg-x11-xbitmaps

%description
XPPAUT is a tool for solving differential equations, difference equations, delay equations, functional equations, boundary value problems, and stochastic equations.

Packaged for local users at PACM and MATH department at Princeton University by Josko Plazonic.

%prep
%setup -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .fixes2

%build
make LDFLAGS="-L/usr/X11R6/%{_lib}"
cd mkavi
make mkavi

%install
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/share/xppaut
cp ode/* *.bitmap *.opt xppaut mkavi/mkavi $RPM_BUILD_ROOT/%{_prefix}/share/xppaut
ln -fs %{_prefix}/share/xppaut/xppaut $RPM_BUILD_ROOT/%{_prefix}/bin/xppaut
# install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_prefix}/bin/xpp
cat > $RPM_BUILD_ROOT/%{_prefix}/bin/xpp <<ENDSCRIPT
#!/bin/sh
echo "Launching xppaut..."
echo "Please note that *.ode configuration files reside in %{_prefix}/share/xppaut directory and documentation is in %{_docdir}/%{name}-%{version} directory."
%{_prefix}/bin/xppaut "\$@"
ENDSCRIPT
chmod a+rx $RPM_BUILD_ROOT/%{_prefix}/bin/xpp

chmod a+rx `find $RPM_BUILD_ROOT/%{_prefix}/share/ -type d -print`

%files
%defattr(-,root,root)
%doc README
%doc *.ps
%doc *.pdf
%doc *.tex
%doc help/*
%{_prefix}/bin/xpp*
%{_prefix}/share/xppaut

%clean
rm -rf $RPM_BUILD_DIR/xppaut*

%changelog
* Wed Apr  4 2007 Josko Plazonic <plazonic@math.princeton.edu>
- fixes for building in puias 5

* Thu Aug 26 2004 Josko Plazonic <plazonic@math.princeton.edu>
- packaging fixes, version upgraded previously

* Fri May 02 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for RH 9
