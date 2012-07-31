Name: stardict-dic-zh_TW
Summary: Traditional Chinese(zh_TW) dictionaries for StarDict
Version: 2.4.2
Release: 3%{?dist}
Group: Applications/System
License: GPL
URL: http://stardict.sourceforge.net

Source0: http://downloads.sourceforge.net/stardict/stardict-cdict-big5-2.4.2.tar.bz2
Source1: http://downloads.sourceforge.net/stardict/stardict-cedict-big5-2.4.2.tar.bz2
Source2: http://downloads.sourceforge.net/stardict/stardict-langdao-ce-big5-2.4.2.tar.bz2
Source3: http://downloads.sourceforge.net/stardict/stardict-langdao-ec-big5-2.4.2.tar.bz2
Source4: http://downloads.sourceforge.net/stardict/stardict-oxford-big5-2.4.2.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch

Requires: stardict >= 2.4.2

%description
Traditional Chinese(zh_TW) dictionaries for StarDict.
These dictionaries are included currently:
cdict-big5, cedict-big5, langdao-ce-big5, langdao-ec-big5,
oxford-big5.
You can download more at: http://stardict.sourceforge.net

%prep
%setup -c -T -n %{name}-%{version}
%setup -q -n %{name}-%{version} -D -T -a 0
%setup -q -n %{name}-%{version} -D -T -a 1
%setup -q -n %{name}-%{version} -D -T -a 2
%setup -q -n %{name}-%{version} -D -T -a 3
%setup -q -n %{name}-%{version} -D -T -a 4

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic
cp -rf stardict-* ${RPM_BUILD_ROOT}%{_datadir}/stardict/dic/

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_datadir}/stardict/dic/*

%changelog
* Wed Jun 27 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-3
- Separate spec files for each language's dictionaries.

* Fri Jun 22 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-2
- Small fixes according to Parag AN's suggestion.

* Thu Jun 21 2007 Hu Zheng <zhu@redhat.com> - 2.4.2-1
- Initial build for Fedora

