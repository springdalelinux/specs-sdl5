Name:		fvwm
Version:	2.5.26
Release:	2%{?dist}.2
Summary:	Highly configurable multiple virtual desktop window manager

Group:		User Interface/X
License:	GPLv2+
URL:		http://www.fvwm.org/
Source0:	ftp://ftp.fvwm.org/pub/fvwm/version-2/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Source2:	http://www.cl.cam.ac.uk/~pz215/fvwm-scripts/scripts/fvwm-xdg-menu.py


Patch0:		fvwm-2.5.21-xdg-open.patch
Patch1:		fvwm-2.5.21-mimeopen.patch
Patch2:		fvwm-2.5.21-menu-generate.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gettext libX11-devel libXt-devel libXext-devel libXinerama-devel libXpm-devel
BuildRequires:	libXft-devel libXrender-devel
BuildRequires:	libstroke-devel readline-devel libpng-devel fribidi-devel
BuildRequires:	librsvg2-devel
Requires:	xterm %{_bindir}/mimeopen

# for fvwm-bug
Requires:	%{_sbindir}/sendmail

# for fvwm-menu-headlines
Requires:	xdg-utils

# for auto-menu generation
Requires:	ImageMagick pyxdg

# PPC doesn't have fribidi, because there is no Client RHEL
ExcludeArch:	ppc


%description
Fvwm is a window manager for X11. It is designed to
minimize memory consumption, provide a 3D look to window frames,
and implement a virtual desktop.


%prep
%setup -q
%patch0 -p1 -b .htmlview
%patch1 -p1 -b .mimeopen
%patch2 -p1 -b .menu-generate

# Filter out false Perl provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(FVWM::.*)\|perl(FvwmCommand)\|perl(General::FileSystem)\|perl(General::Parse)/d'
EOF

%define __perl_provides %{_builddir}/%{name}-%{version}/%{name}-prov
chmod +x %{__perl_provides}


# Filter false requires for old perl(Gtk) and for the above provides
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(Gtk)\|perl(FVWM::Module::Gtk)\|perl(FVWM::.*)\|perl(FvwmCommand)\|perl(General::FileSystem)\|perl(General::Parse)/d'
EOF

%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
%find_lang FvwmScript
%find_lang FvwmTaskBar
cat FvwmScript.lang FvwmTaskBar.lang >> %{name}.lang

# Fedora doesn't have old Gtk Perl
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/perllib/FVWM/Module/Gtk.pm
rm $RPM_BUILD_ROOT%{_libexecdir}/%{name}/%{version}/FvwmGtkDebug

# xsession
install -D -m0644 -p %{SOURCE1} \
	$RPM_BUILD_ROOT%{_datadir}/xsessions/%{name}.desktop

# menus
install -D -m0755 -p %{SOURCE2} \
	$RPM_BUILD_ROOT%{_bindir}/fvwm-xdg-menu


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS ChangeLog COPYING
%{_bindir}/*
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/*
%{_datadir}/xsessions/%{name}.desktop


%changelog
* Fri Feb  6 2009 Adam Goode <adam@spicenitz.org> - 2.5.26-2.2
- ExcludeArch ppc, there is no Client RHEL for PPC

* Fri Feb  6 2009 Adam Goode <adam@spicenitz.org> - 2.5.26-2.1
- Change Requires for EL-5

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 2.5.26-2
- RPM 4.6 fix for patch tag

* Wed Jun  4 2008 Adam Goode <adam@spicenitz.org> - 2.5.26-1
- Upgrade to new release
- Remove module_list patch, fixed in upstream

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 2.5.24-2
- Really fix segfault (#382321)

* Sun Dec  2 2007 Adam Goode <adam@spicenitz.org> - 2.5.24-1
- New upstream release
- Fixes segfault (#382321)

* Tue Oct  2 2007 Adam Goode <adam@spicenitz.org> - 2.5.23-3
- Change htmlview to xdg-open (thanks, Ville Skyttä !)

* Mon Sep 10 2007 Adam Goode <adam@spicenitz.org> - 2.5.23-2
- Don't add gnome-libs-devel to BR (not on ppc64?)

* Mon Sep 10 2007 Adam Goode <adam@spicenitz.org> - 2.5.23-1
- New upstream release

* Tue Aug 21 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-5
- Update license tag
- Rebuild for buildid

* Thu Mar 15 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-4
- Don't patch configure, just patch a few files

* Thu Mar  8 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-3
- Rebuild configure with autoconf >= 2.60 (for datarootdir)
- Filter out local Perl libraries from provides and requires

* Wed Feb 28 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-2
- Shorten description
- Enable auto-generate menus in the Setup Form config generator
- Use htmlview instead of netscape
- Use mimeopen instead of EDITOR
- Add more Requires

* Sun Jan 21 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-1
- New specfile for Fedora
