Name: stardict-dic-ja
Summary: Japanese(ja) dictionaries for StarDict
Version: 2.4.2
Release: 3%{?dist}
Group: Applications/System
License: GPL
URL: http://stardict.sourceforge.net

Source0: http://downloads.sourceforge.net/stardict/stardict-edict-2.4.2.tar.bz2
Source1: http://downloads.sourceforge.net/stardict/stardict-jmdict-en-ja-2.4.2.tar.bz2
Source2: http://downloads.sourceforge.net/stardict/stardict-jmdict-ja-en-2.4.2.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch

Requires: stardict >= 2.4.2

%description
Japanese(ja) dictionaries for StarDict.
These dictionaries are included currently:
edict, jmdict-en-ja, jmdict-ja-en.
You can download more at: http://stardict.sourceforge.net

%prep
%setup -c -T -n %{name}-%{version}
%setup -q -n %{name}-%{version} -D -T -a 0
%setup -q -n %{name}-%{version} -D -T -a 1
%setup -q -n %{name}-%{version} -D -T -a 2

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

