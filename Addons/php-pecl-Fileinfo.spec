%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %(php-config --version 2>/dev/null || echo 0)

Summary: 	Fileinfo is a PHP extension that wraps the libmagic library
Name: 		php-pecl-Fileinfo
Version: 	1.0.4
Release: 	3%{?dist}
License: 	PHP License
Group: 		Development/Languages
URL: 		http://pecl.php.net/package/Fileinfo

Source: 	http://pecl.php.net/get/Fileinfo-%{version}.tgz
Source1:	PHP-LICENSE-3.01
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:		fixconfigure.patch

Provides: 	php-pecl(Fileinfo),
Provides:	php-Fileinfo
Requires: 	php-api = %{php_apiver}
BuildRequires: 	php-devel
BuildRequires:	file

%description
This extension allows the retrieval of file type information for the vast
majority of files.  This information may include such information as dimensions
or compression quality of images, duration of sound files, etc...

Additionally, it can also be used to retrieve the MIME type for a particular
file, and for text files, the proper language encoding.

%prep
%setup -c -q
%{__install} -m 644 -c %{SOURCE1} Fileinfo-%{version}/LICENSE

%patch0 -p0 -b .fixconfigure

%build
cd Fileinfo-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
cd Fileinfo-%{version}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/Fileinfo.ini << 'EOF'
; Enable Filinfo extension module
extension=fileinfo.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc Fileinfo-%{version}/LICENSE Fileinfo-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/Fileinfo.ini
%{php_extdir}/fileinfo.so

%changelog
* Mon Apr 16 2007 Brandon Holbrook <fedora AT theholbrooks DOT org> 1.0.4-3
- magic.h is now part of file-devel, not file. Changed buildreqs

* Sat Apr 14 2007 Brandon Holbrook <fedora AT theholbrooks DOT org> 1.0.4-2
- Added a patch to config.m4 that fixes improper detection of the system's magic database file [bz 235110]

* Fri Dec 29 2006 Brandon Holbrook <fedora AT theholbrooks DOT org> 1.0.4-1
- Bumped to upstream 1.0.4

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.0.3-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 17 2006 Brandon Holbrook <fedora AT theholbrooks DOT org> 1.0.3-2
- Strict Requires: php_api
- Grammatically correct Summary + Description

* Wed Sep 13 2006 Brandon Holbrook <fedora AT theholbrooks DOT org> 1.0.3-1
- initial RPM
