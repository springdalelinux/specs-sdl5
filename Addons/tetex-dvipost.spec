%define real_name dvipost
%{!?_texmf: %define _texmf %(eval "echo `kpsewhich -expand-var '$TEXMFMAIN'`")}

Name:           tetex-%{real_name}
Version:        1.1
Release:        7%{?dist}
Summary:        LaTeX post filter command to support change bars and overstrike mode

Group:          Applications/Publishing
License:        GPL
URL:            http://efeu.cybertec.at/
Source0:        http://efeu.cybertec.at/%{real_name}.tar.gz
Patch0:		%{name}-destdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	tetex-latex
BuildRequires: /usr/bin/kpsewhich

Requires:	tetex-latex

%description
The command dvipost is a post procesor for dvi files, created by latex
or tex. It is used for special modes, which normally needs the support
of dvi drivers (such as dvips). With dvipost, this features could be
implemented independent of the preferred driver. Currently, the post
processor supports layout raster, change bars and overstrike mode.

%prep
%setup -q -n %{real_name}-%{version}
%patch0 -p1


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /usr/bin/texhash


%postun -p /usr/bin/texhash


%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_texmf}/tex/latex/misc/*

%doc README COPYING NOTES dvipost.html
%{_mandir}/man*/*


%changelog
* Sat Apr 21 2007 José Matos <jamatos[AT]fc.up.pt> - 1.1-7
- Rebuild (for F7).

* Mon Sep 11 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1-6
- Rebuild for FC6

* Sat May  6 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1-5
- Clean up spec file

* Thu Apr 27 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1-4
- Rename package to tetex-dvipost

* Thu Apr 27 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1-3
- Capitalize Summary, fix spell error in description, rework
  invocation of post and postun calls (thanks to Patrice Dumas)
- Add tetex-latex to Requires and BuildRequires.
- Add tetex-fonts to Requires to satisfy direct dependency on texhash

* Thu Apr 27 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1-2
- Add new entries to %%doc and expand description

* Wed Apr 26 2006 José Matos <jamatos[AT]fc.up.pt> - 1.1-1
- First build

