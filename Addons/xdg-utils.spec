
Summary: Basic desktop integration functions 
Name:    xdg-utils
Version: 1.0.2
Release: 4%{?dist}

URL:     http://portland.freedesktop.org/ 
Source0: http://portland.freedesktop.org/download/xdg-utils-%{version}%{?beta}.tgz
License: MIT 
Group:   System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Patch1: xdg-utils-1.0.2-mimeopen.patch
Patch2: xdg-utils-1.0.1-typo.patch
Patch3: xdg-utils-1.0.1-htmlview.patch
Patch4: xdg-utils-1.0.2-CVE-2008-0386.patch

Requires: coreutils
Requires: desktop-file-utils
## kde-config
#Requires(hint): kdelibs
## update-gtk-icon-cache
#Requires(hint): gtk2
## htmlview patch
#Requires(hint): htmlview links
## mimeopen generic default
#Requires(hint): %{_bindir}/mimeopen
#Requires(hint): perl-File-MimeInfo 
Requires: which


%description
The %{name} package is a set of simple scripts that provide basic
desktop integration functions for any Free Desktop, such as Linux.
They are intended to provide a set of defacto standards.  
This means that:
*  Third party software developers can rely on these xdg-utils
   for all of their simple integration needs.
*  Developers of desktop environments can make sure that their
   environments are well supported
*  Distribution vendors can provide custom versions of these utilities

The following scripts are provided at this time:
* xdg-desktop-menu      Install desktop menu items
* xdg-desktop-icon      Install icons to the desktop
* xdg-icon-resource     Install icon resources
* xdg-mime              Query information about file type handling and
                        install descriptions for new file types
* xdg-open              Open a file or URL in the user's preferred application
* xdg-email             Send mail using the user's preferred e-mail composer
* xdg-screensaver       Control the screensaver


%prep
%setup -q -n %{name}-%{version}%{?beta}

%patch1 -p1 -b .mimeopen
%patch2 -p1 -b .typo
%patch3 -p1 -b .htmlview
%patch4 -p1 -b .CVE-2008-0386


%build
%configure

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE README TODO
%{_bindir}/xdg-*
%{_mandir}/man1/xdg-*


%clean
rm -rf %{buildroot}


%changelog
* Fri Jan 25 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.0.2-4
- Fix for CVE-2008-0386 (#429513)

* Fri Jan 18 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-3
- fix mimeopen support (#429280)
- spec cosmetics: cleanup macro usage

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-2
- Requires: which (#312601)

* Sun Jun 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-1
- xdg-utils-1.0.2

* Mon Apr 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-3
- add htmlview,links to browser fallbacks

* Tue Dec 19 2006 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-2
- fix typo in xdg-icon-resource manpage

* Mon Nov 06 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.1-1
- xdg-utils-1.0.1

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net 1.0-3
- actually *use* mimeopen patch (#210797)

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-2
- prefer mimeopen as generic default (#210797)

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-1
- 1.0(final)

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.9.rc1
- update %%description (#208926)

* Wed Sep 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.8.rc1
- 1.0rc1

* Fri Sep 15 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.7.beta4
- 1.0beta4

* Mon Aug 21 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.6.beta3
- 1.0beta3

* Thu Jul 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.5.20060721
- Release: append/use %%{?dist}

* Wed Jul 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.4.20060721
- specfile cosmetics, tabs -> spaces
- %%makeinstall -> make install DESTDIR=...

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.3.20060721
- 20060721 snapshot
- optgnome.patch

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.2.beta1
- Requires: desktop-file-utils

* Mon Jul 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-0.1.beta1
- 1.0beta1

