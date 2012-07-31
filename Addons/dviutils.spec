Name        	: dviutils
Version     	: 1.0
Release     	: 11%{?dist}
Group       	: Applications/Publishing
Summary     	: A set of utilities to rearrange dvi-documents.
License     	: GPL
Icon        	: TEX.gif
Requires    	: tetex-xdvi 
BuildRoot   	: /var/tmp/%{name}-buildroot

Source0: ftp://ftp.dante.de/tex-archive/dviware/dvibook.tar.gz
Patch0: dvibook-redhat.patch
Patch1: dviutils-1.0-ansi_valist.patch
Patch2: dviutils-errno.patch
Patch3: dviutils-cfixes.patch

%Description
These utilities re-arrange TeX DVI files, creating DVI files as
output.  Dvibook rearranges pages so that the file can be printed as a
booklet on a duplex printer.
Dvitodvi rearranges pages according to a complex page specification.
It can be used to rearrange for booklet printing, extract odd or even
pages, overlay pages, and many other functions.


%prep
rm -rf $RPM_BUILD_ROOT

%setup -c
%patch0
%patch1 -p3 -b .ansi_valist
%patch2 -p1
%patch3 -p1 -b .cfixes

%build
cd dvibook
xmkmf
make Makefiles
make CDEBUGFLAGS="$RPM_OPT_FLAGS" GETOPT=
cd ..


%install

mkdir -p $RPM_BUILD_ROOT/usr/{bin,share/man/man1} 
cd dvibook 
make install BINDIR=$RPM_BUILD_ROOT/usr/bin
make install.man MANDIR=$RPM_BUILD_ROOT/usr/share/man/man1

cd $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc dvibook/README
/usr/bin/*
/usr/share/man/man1/*


%changelog
* Thu Dec 20 2001 Aleksey Nogin <ayn2@cornell.edu>
- Simplified a little

* Fri Jun  8 2001 Gerald Teschl <gerald@esi.ac.at>
- Created from caldera src rpm


