Summary:	Simple graphics library
Name:		libgfx
Version:	1.1.0
Release:	0%{?dist}
License:	other/free
Group:		System Environment/Libraries
URL:		http://graphics.cs.uiuc.edu/~garland/software/libgfx.html
Source0:	http://graphics.cs.uiuc.edu/~garland/dist/libgfx-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	fltk-devel

%description
The purpose of this library is to simplify the creation of computer graphics 
software. Specifically, it is targeted towards cross-platform development 
using the OpenGL rendering API and the FLTK interface toolkit. It attempts 
to provide facilities which are useful in the majority of graphics programs. 

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" %configure
cd src
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}
install -m 644 src/libgfx.a $RPM_BUILD_ROOT%{_libdir}
cp -r include/gfx $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc CHANGES.txt README.txt doc/*
%{_libdir}/libgfx.a
%{_includedir}/gfx

%changelog
* Wed Apr  4 2007 Josko Plazonic <plazonic@math.princeton.edu>
- version upgrade

* Tue Feb 22 2005 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
