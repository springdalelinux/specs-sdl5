%define __os_install_post %{nil}
%define _enable_debug_packages %{nil}

%define acrodir /usr/lib/acroread

Summary: Additional Font Packs for Adobe Reader
Name: acroread-fontpacks
Version: 8.1
Release: 1%{?dist}
License: Commercial
Group: Applications/Publishing
Source: FontPack81_chs_i486-linux.tar.gz
Source1: FontPack81_cht_i486-linux.tar.gz
Source2: FontPack81_jpn_i486-linux.tar.gz
Source3: FontPack81_kor_i486-linux.tar.gz
Source4: FontPack81_xtd_i486-linux.tar.gz
Requires: acroread >= %{version}
BuildRoot: /var/tmp/%{name}-root

%description
This package contains Chinese simplified font pack 

%prep
%setup -q -c -n %{name}-%{version} -a 1 -a 2 -a 3 -a 4

%build
echo Nothing to build here

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{acrodir}
for i in CHSKIT/BINCOM.TAR CHSKIT/LANGCOM.TAR `ls */LANG*TAR | grep -v LANGCOM` xtdfont/XTDFONT.TAR; do
	tar -C $RPM_BUILD_ROOT%{acrodir} -xvf $i
done
rm -f $RPM_BUILD_ROOT%{acrodir}/{INSTALL,LICREAD.TXT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{acrodir}/Adobe/Reader8/Reader/intellinux/lib/lib*
%{acrodir}/Adobe/Reader8/Resource/*/*

%changelog
* Mon Dec 17 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial packaging
