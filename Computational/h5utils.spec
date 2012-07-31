Summary: 	Utilities for Data Conversions from hdf5
Name: 		h5utils
Version: 	1.12.1
Release: 	2
License: 	GPL
Group: 		Productivity/Scientific/Electronics
Packager:	Werner Hoch <werner.ho@gmx.de>

URL: 		http://ab-initio.mit.edu/wiki/index.php/H5utils
Source0: 	%{name}-%{version}.tar.gz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root

Autoreqprov:	on

BuildRequires:	hdf5-devel, gsl-devel, zlib-devel, libpng-devel 
BuildRequires:	libjpeg-devel, hdf-devel

%description
h5utils is a set of utilities for visualization and conversion of
scientific data in the free, portable HDF5 format
(http://hdf.ncsa.uiuc.edu/HDF5/).  
Besides providing a simple tool for batch visualization as PNG images,
h5utils also includes programs to convert HDF5 datasets into the
formats required by other free visualization software (e.g. plain
text, Vis5d (http://www.ssec.wisc.edu/~billh/vis5d.html), and VTK
(http://public.kitware.com/VTK/))

%prep
%setup -q

%build
export LDFLAGS="-L %{_libdir}/hdf"
%configure
%{__make}

%install
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/h5utils
%{_datadir}/h5utils/*

%changelog
* Sun Feb 07 2010 - 1.12.1-2
- Source changed from .bz2 to .gz
* Sat Oct 10 2009 Werner Hoch <werner.ho@gmx.de> - 1.12.1
- new version 1.12.1
* Sun Nov 23 2008 Werner Hoch <werner.ho@gmx.de> - 1.11.1
- build fixes for factory
* Sun Jul 20 2008 Werner Hoch <werner.ho@gmx.de> - 1.11.1
- new version 1.11.1
* Sun Oct 21 2007 Werner Hoch <werner.ho@gmx.de> - 
- Initial build of version 1.10.1

