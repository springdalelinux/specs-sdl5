Summary: FreeFem++
Name: freefem++
Version: 3.12
Release: 1%{?dist}
License: GNU
Group: Applications/Scientific
Source: %{name}-%{version}.tar.gz
BuildRequires: gcc-gfortran
BuildRequires:  atlas-devel
BuildRequires:  bison
BuildRequires:  fftw-devel
BuildRequires:  flex
BuildRequires:  fltk-devel
BuildRequires:  gcc-gfortran
BuildRequires:  freeglut-devel
BuildRequires:  ImageMagick
BuildRequires:  lapack-devel
BuildRequires:  libGLU-devel
BuildRequires:  libXpm-devel
BuildRequires:  libXt-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  lam-devel
BuildRequires:  suitesparse-devel
Requires:	freeglut
Requires:	suitesparse
Requires:	libgfortran

BuildRoot: /tmp/%{name}-%{version}-%{release}-root

%description
FreeFem++ is an implementation of a language dedicated to the finite element method. It enables you to solve Partial Differential Equations (PDE) easily.
Problems involving PDE (2d, 3d) from several branches of physics such as fluid-structure interactions require interpolations of data on several meshes and their manipulation within one program. FreeFem++ includes a fast 2^d-tree-based interpolation algorithm and a language for the manipulation of data on multiple meshes (as a follow up of bamg).

FreeFem++ is written in C++ and the FreeFem++ language is a C++ idiom. It runs on any Unix-like OS (with g++ version 3 or higher, X11R6 or OpenGL with GLUT) Linux, FreeBSD, Solaris 10, Microsoft Windows ( 2000, NT, XP, Vista,7 ) and MacOS X (native version using OpenGL). FreeFem++ replaces the older freefem and freefem+.


%prep
%setup 

%build
%configure
touch examples++-load/WHERE_LIBRARY
make

%install
DESTDIR=$RPM_BUILD_ROOT
export DESTDIR
make install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING ChangeLog HISTORY HISTORY_BEFORE_2005 INNOVATION INSTALL NEWS README README_ARPACK README_CVS README_CW TODO
%{_bindir}/FreeFem++*
%{_bindir}/bamg
%{_bindir}/cvmsh2
%{_bindir}/drawbdmesh
%{_bindir}/ff*
%{_prefix}/lib/ff++/%{version}
%{_datadir}/%{name}/%{version}

%changelog
* Wed Feb 9 2011 Thomas Uphill <uphill@ias.edu>
- initial build
