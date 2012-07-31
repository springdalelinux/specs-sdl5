%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{default_extdir})
%define php_apiver %((echo %{default_apiver}; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_version:%define php_version %(php-config --version 2>/dev/null || echo %{default_version})}

%define modname mcrypt

Summary: 	Mcrypt extension module for PHP
Name: 		php-%{modname}
Version: 	5.1.6
Release: 	0%{?dist}
License: 	PHP License
Group: 		Development/Languages

Source: 	php-%{modname}-%{version}.tgz
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	php-%{modname}
Requires:	php-api = %{php_apiver}
Requires:	php-common = %{php_version}
BuildRequires: 	php-devel
BuildRequires:	libmcrypt-devel

%description
This is a dynamic shared object (DSO) for PHP that will add mcrypt support.

This is an interface to the mcrypt library, which supports a wide variety of
block algorithms such as DES, TripleDES, Blowfish (default), 3-WAY, SAFER-SK64,
SAFER-SK128, TWOFISH, TEA, RC2 and GOST in CBC, OFB, CFB and ECB cipher modes
and others.

%prep
%setup -c -q

%build
cd php*/ext/%{modname}
phpize
%configure --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd php*/ext/%{modname}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{modname}.ini << 'EOF'
; Enable %{modname} module
extension = %{modname}.so

[mcrypt]
;mcrypt.algorithms_dir =
;mcrypt.modes_dir =
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc php*/ext/%{modname}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{modname}.ini
%{php_extdir}/*so

%changelog
* Tue Apr 24 2007 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
