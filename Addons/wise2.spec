Name:           wise2
Version:        2.2.0
Release:        4%{?dist}
Summary:        Tools for comparison of biopolymers

Group:          Applications/Engineering
## Everything is licensed under a BSD-style license except for
## the HMMer2 libraries and models directory which are GPLv2+
## see LICENSE files for details. 
License:        BSD and GPLv2+
URL:            http://www.ebi.ac.uk/Wise2/
Source0:        ftp://ftp.ebi.ac.uk/pub/software/unix/wise2/wise%{version}.tar.gz
Patch0:         wise2-build.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Wise2 is a package focused on comparisons of biopolymers, commonly DNA
sequence and protein sequence.  A strength of Wise2 is the
comparison of DNA sequence at the level of its protein
translation. This comparison allows the simultaneous prediction of
gene structure with homology based alignment.

%prep
%setup -q -n wise%{version}

## don't run "welcome.csh"
%patch0 -p0

## fix interpreter in examples
sed -i 's#/usr/local/bin/perl#/usr/bin/perl#' docs/gettex.pl
## fix perms 
chmod -x test_data/rrm.HMM

## pull out licenses
for i in base dynlibsrc dyc
do
    cp src/$i/LICENSE LICENSE.$i
done
cp src/models/GNULICENSE LICENSE.GPL

%build
cd src
## removed "{?_smp_mflags}", does not support parallel build
make CC=gcc CFLAGS="-c $RPM_OPT_FLAGS" all

%install
rm -rf $RPM_BUILD_ROOT
cd src/bin
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
for i in dba dnal estwise estwisedb genewise genewisedb genomewise psw pswdb
do
    %{__install} $i $RPM_BUILD_ROOT/%{_bindir} 
done
cd -
# install architecture-independent data and config files
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/wise2
cd wisecfg
%{__install} -pm 644 * $RPM_BUILD_ROOT%{_datadir}/wise2

# install scripts to automatically set the WISECONFIGDIR environment variable
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
echo "export WISECONFIGDIR=%{_datadir}/wise2/" > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/wise2.sh
echo "setenv WISECONFIGDIR %{_datadir}/wise2/" > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/wise2.csh

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs test_data
%doc INSTALL LICENSE README LICENSE.base LICENSE.dynlibsrc LICENSE.dyc LICENSE.GPL
%{_bindir}/*
%{_datadir}/wise2
%config(noreplace) %{_sysconfdir}/profile.d/*

%changelog
* Sat Feb  9 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.2.0-4
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering

* Thu Aug 16 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.2.0-3
- Clarify license as BSD and GPLv2+

* Mon Apr 12 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.2.0-2
- Pass $RPM_OPT_FLAGS to compiler as per suggestion from Ralf Corsepius.

* Mon Apr 11 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.2.0-1
- Initial Fedora package.
