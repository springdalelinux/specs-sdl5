Name:               zvbi
Version:            0.2.25
Release:            1%{?dist}
Summary:            Raw VBI, Teletext and Closed Caption decoding library
Group:              System Environment/Libraries
License:            GPL
URL:                http://zapping.sourceforge.net/ZVBI/index.html
Source0:            http://dl.sf.net/zapping/%{name}-%{version}.tar.bz2
Patch0:             zvbi-0.2.24-tvfonts.patch
BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:      doxygen
BuildRequires:      fontconfig
BuildRequires:      gettext
BuildRequires:      libpng-devel
BuildRequires:      libICE-devel
BuildRequires:      xorg-x11-font-utils
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service

%description
ZVBI provides functions to capture and decode VBI data. The vertical blanking
interval (VBI) is an interval in a television signal that temporarily suspends
transmission of the signal for the electron gun to move back up to the first
line of the television screen to trace the next screen field. The vertical
blanking interval can be used to carry data, since anything sent during the VBI
would naturally not be displayed; various test signals, closed captioning, and
other digital data can be sent during this time period.


%package devel
Summary:            Development files for zvbi
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig

%description devel
Development files for zvbi


%package fonts
Summary:            Fonts from zvbi converted to X11
Group:              User Interface/X
Requires(post):     fontconfig
Requires(postun):   fontconfig
Requires(post):     chkfontpath
Requires(postun):   chkfontpath
Obsoletes:          xawtv-tv-fonts < 3.95
Provides:           xawtv-tv-fonts >= 3.95

%description fonts
Fonts from zvbi converted for use with X11


%prep
%setup -q
%patch -p1 -b .orig

#Fix character encodings (note ChangeLog's encoding is broken, hence sed)
sed -i 's/\xC3\xB2/\xF2/g' ChangeLog
sed -i 's/\xC2\x81//g' ChangeLog
iconv -f iso8859-1 ChangeLog -t utf8 > ChangeLog.conv && /bin/mv -f ChangeLog.conv ChangeLog
iconv -f iso8859-1 README -t utf8 > README.conv && /bin/mv -f README.conv README


%build
# Note: We don't do --enable-static=no because static libs are needed to build
# x11font during compile time to convert zvbi fonts into x11 fonts. x11font
# is thrown away and not installed because it's not useful for anything else
%configure --disable-rpath --enable-v4l --enable-dvb --enable-proxy
make %{?_smp_mflags}

#Generate fonts, fonts.alias and fonts.dir
pushd contrib
./x11font
for font in *.bdf
do
    bdftopcf $font | gzip -9 -c > ${font%.bdf}.pcf.gz
done
mkfontdir -x .bdf .
cat >fonts.alias <<EOF
teletext   -ets-teletext-medium-r-normal--*-200-75-75-c-120-iso10646-1
EOF
popd


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/fonts/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
make install DESTDIR=%{buildroot}

#Find locales
%find_lang %{name}

#Install init script
install -m0755 daemon/zvbid.init %{buildroot}%{_sysconfdir}/rc.d/init.d/zvbid

#Install fonts
install -m 0644 contrib/*.pcf.gz %{buildroot}%{_datadir}/fonts/%{name}
install -m 0644 contrib/fonts.* %{buildroot}%{_datadir}/fonts/%{name}

#%%ghost the fonts.cache-1 and fonts.dir
touch %{buildroot}%{_datadir}/fonts/%{name}/fonts.cache-1


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
/sbin/chkconfig --add zvbid


%postun
/sbin/ldconfig
if [ "$1" -ge "1" ]; then
    /sbin/service zvbid condrestart >/dev/null 2>&1 || :
fi


%preun
if [ $1 = 0 ]; then
    /sbin/service zvbid stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del zvbid
fi


%post fonts
fc-cache -f %{_datadir}/fonts/%{name} || :
chkfontpath -q -a %{_datadir}/fonts/%{name} || :


%postun fonts
if [ "$1" = "0" ]; then
    fc-cache -f %{_datadir}/fonts || :
    chkfontpath -q -r %{_datadir}/fonts/%{name} || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}*
%{_sbindir}/zvbid
%{_sysconfdir}/rc.d/init.d/zvbid
%{_libdir}/*.so.*
%{_mandir}/man1/*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%doc ABOUT-NLS AUTHORS BUGS ChangeLog COPYING NEWS README TODO


%files devel
%{_includedir}/libzvbi.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-0.2.pc


%files fonts
%dir %{_datadir}/fonts/%{name}
%{_datadir}/fonts/%{name}/*.gz
%{_datadir}/fonts/%{name}/fonts.dir
%{_datadir}/fonts/%{name}/fonts.alias
%ghost %{_datadir}/fonts/%{name}/fonts.cache-1


%changelog
* Sun May 27 2007 Ian Chapman <packages@amiga-hardware.com> 0.2.25-1%{?dist}
- Upgrade to 0.2.25

* Tue Mar 13 2007 Ian Chapman <packages@amiga-hardware.com> 0.2.24-1%{?dist}
- Upgrade to 0.2.24
- Convert README and ChangeLog to UTF-8
- Added patch for x11font to generate more font sizes useful for other
  applications such as xawtv (courtesy of Dmitry Butskoy)
- Fonts sub-rpm now obsoletes and provides xawtv-tv-fonts
- Split font generation and font installation into separate sections
- Various other minor changes to the spec
- Added xfs support for the fonts

* Fri Sep 01 2006 Ian Chapman <packages@amiga-hardware.com> 0.2.22-2%{?dist}
- Minor spec cleanups

* Tue Aug 29 2006 Ian Chapman <packages@amiga-hardware.com> 0.2.22-1%{?dist}
- Initial release