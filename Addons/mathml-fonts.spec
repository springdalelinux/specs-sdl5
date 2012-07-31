
%define fontdir       %{_datadir}/fonts/mathml

Summary: Mathematical symbol fonts
Name:    mathml-fonts
Version: 1.0 
Release: 21%{?dist}

URL:     http://www.mozilla.org/projects/mathml/fonts/
License: Distributable
Group:   User Interface/X
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## Sources
Source1: find_symbol_font.sh
# Install as:
%define find_symbol_dir  %{_libexecdir}/%{name}
%define find_symbol_font %{find_symbol_dir}/find_symbol_font.sh

## Mathematica fonts
#  License: http://support.wolfram.com/mathematica/systems/windows/general/latestfonts.html (non-distributable)
%{?_with_mathematica:Source10: http://support.wolfram.com/mathematica/systems/windows/general/MathFonts_TrueType.exe}
## TeX fonts
# Bakoma TeX fonts, http://wiki.lyx.org/FAQ/Qt
Source20: ftp://ftp.lyx.org/pub/lyx/contrib/BaKoMa4LyX-1.1.zip
# extras (cmbx10)
Source21: ftp://tug.ctan.org/tex-archive/fonts/cm/ps-type1/bakoma/ttf/cmbx10.ttf
#Now included in BaKoMa4LyX-1.1
#Source22: ftp://tug.ctan.org/tex-archive/fonts/cm/ps-type1/bakoma/ttf/eufm10.ttf

## Design Science fonts, URL: http://www.dessci.com/en/dl/fonts/
Source30: http://www.dessci.com/en/dl/MathTypeTrueTypeFonts.asp
Source31: http://www.dessci.com/en/support/eula/fonts/mtextralic.htm

BuildRequires: cabextract
BuildRequires: unzip

# we're pretty much useless without it, and use fc-cache in scriptlets 
# but, fontconfig will run fc-cache on install, so what's the big deal?
#Prereq: fontconfig

# Provide lyx upstream contrib rpms
Provides: latex-xft-fonts = 0.1
Provides: latex-bakoma4lyx-fonts = 1

%description
This package contains fonts required to display mathematical
symbols.  Applications supported include:
* mozilla-based browsers (including firefox, seamonkey) to display MathML
* lyx
* kformula (koffice)


%prep
%setup -T -c -n %{name}

## Math'ca
%{?_with_mathematica:unzip %{SOURCE10}}

## TeX fonts
# BaKoMa4Lyx
%setup -T -D -n %{name} -a 20
# cmbx
install -p -m644 %{SOURCE21} .

## MathType fonts (mtextra)
cabextract %{SOURCE30}
install -p -m644 %{SOURCE31} .


%build
# blank


%install
rm -rf "$RPM_BUILD_ROOT"

install -d $RPM_BUILD_ROOT%{fontdir}

install -p -m644 \
  %{?_with_mathematica:math{1,2,4}___.ttf} \
  *10.ttf mtextra.ttf \
  $RPM_BUILD_ROOT%{fontdir}/

# find_symbol_font
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{find_symbol_font}

# "touch" all fonts.dir, fonts.scale, etc files we've got flagged as %ghost
touch $RPM_BUILD_ROOT%{fontdir}/{fonts.cache-1,Symbol.pfa,SY______.PFB}


%triggerin -- acroread,AdobeReader_enu
%{find_symbol_font} ||:

%triggerun -- acroread,AdobeReader_enu
if [ $2 -eq 0 ]; then
  fc-cache -f %{fontdir} 2> /dev/null ||: 
fi

%post
%{find_symbol_font} ||:
fc-cache -f %{fontdir} 2> /dev/null ||: 

%postun
if [ $1 -eq 0 ]; then
  fc-cache 2> /dev/null ||: 
fi


%files
%defattr(-,root,root)
%doc Licence.txt mtextralic.htm Readme.txt
%dir %{find_symbol_dir}
%{find_symbol_font}
%dir %{fontdir}
%{fontdir}/*.[ot]tf
%ghost %{fontdir}/Symbol.pfa
%ghost %{fontdir}/SY______.PFB
%ghost %{fontdir}/fonts.cache-*


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Jun 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-21
- update to BaKoMa4Lyx-1.1 (includes eufm10.ttf)
- update %%description

* Fri Oct 28 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-20
- newer fontconfig's create/use fonts.cache-2 too (#171978)

* Wed Oct 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-19
- use cabextract on MathTypeTrueTypeFonts
- include mtextralic.htm (MathType/mtextra license)

* Thu Sep 15 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-18
- replace latex-xft-fonts with bakoma4lyx
- remove non-distributable Math'ca fonts (#168405)

* Wed Aug  3 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.0-17
- update for acroread7 (and SY_____.PFB) (#133709)
- include/use find_symbol_font.sh helper script
- readd %%postun
- update latex-xft-fonts URL
- remove legacy crud

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Apr 26 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.14
- remove touch-y Symbol.pfa stuff. (-:
- rework acroread triggers

* Mon Apr 26 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.13
- removed not-needed %%postun
- Prereq: fontconfig
- rework handling of acroread's Symbol.pfa

* Sun Apr 25 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.12
- fix typo in %%triggerun -- acroread
- don't use chkfontpath at all

* Sat Apr 24 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.11
- BR: XFree86-font-utils
- add comment regarding lyx fonts
- remove use of mkfontdir -e which causes build failure on FC2.
- remove deprecated Xft1 bits
- add %%trigger for acroread, to rebuild font.cache-1 when/if
  Symbol.pfa becomes available/unavailable.

* Tue Jan 13 2004 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.10
- loosen Require's

* Mon Dec 22 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.9
- fix %%postun

* Sat Nov 22 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.8
- make %%install step cleaner with no overwrites.

* Sat Nov 22 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.7
- cleanup for fedora submission

* Wed Oct 29 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.6
- add cmbx10 for (koffice's) kformula.
- remove unused PS Type1 fonts from src.rpm

* Wed Oct 22 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.5
- remove crud from %%post

* Mon Oct 20 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.4
- Provides: latex-xft-fonts
- Add a few additional fonts for lyx.

* Tue Oct 14 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.2
- Xft1: add path to /etc/X11/XftConfig, if needed.
- we're Xft-only, don't add to xfs's fontpath (to avoid X crashes
  on rh73/XFree-4.2/Xft1)

* Mon Oct 13 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.1
- Contrary to what http://mozilla.org/projects/mathml/fonts says,
  according to mozilla bug 128153c#76,#c81 you need ttf fonts, *not*
  type1 PS fonts.

* Wed Sep 10 2003 Rex Dieter <rexdieter at sf.net> 0:1.0-0.fdr.0
- fedora'ize
- include mtextra.pfb from http://www.dessci.com/

* Mon Nov 11 2002 Rex Dieter <rdieter at unl.edu> 1.0-0
- include latest Mathematica 4.1 fonts + CMSY10,CMEX10
- Require type1inst with added/fixed ams/wri font foundries
- prefer Math*.pfa over Math*.pfb as type1inst seems to
  incorrectly identify some of the pfb versions.

