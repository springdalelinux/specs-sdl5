# $Id: gaim-encryption.spec 5222 2007-03-07 13:57:18Z thias $
# Authority: dag
# ExclusiveDist: fc6 el5

Summary: RSA encryption support for Gaim
Name: pidgin-encryption
Version: 3.0
Release: 1%{?dist}
License: GPL
Group: Applications/Internet
URL: http://pidgin-encrypt.sourceforge.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://downloads.sf.net/pidgin-encrypt/pidgin-encryption-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: pidgin-devel >= 2.0.0, gtk2-devel, nss-devel, nspr-devel
Requires: pidgin >= 2.0.0
Obsoletes: gaim-encryption

%description
RSA encryption support for Gaim.

%prep
%setup -n %{name}-%{version}

%build
%configure \
    --with-nspr-includes="`nspr-config --includedir`" \
    --with-nspr-libs="`nspr-config --libdir`" \
    --with-nss-includes="`nss-config --includedir`" \
    --with-nss-libs="`nss-config --libdir`"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc CHANGELOG COPYING NOTES README TODO WISHLIST
%dir %{_libdir}/pidgin/
%exclude %{_libdir}/pidgin/encrypt.a
%exclude %{_libdir}/pidgin/encrypt.la
%{_libdir}/pidgin/encrypt.so
%{_datadir}/pixmaps/pidgin/pidgin-encryption/crypto.png

%changelog
* Fri Jun 29 2007 Thomas Uphill <uphill@ias.edu>
- initial pidgin version
