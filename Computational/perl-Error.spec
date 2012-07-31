%define perlmod Error
Summary: %{perlmod} interface
Name: perl-%{perlmod}
Version: 0.17015
Release: 1%{?dist}
Packager: Josko Plazonic <plazonic@math.princeton.edu>
License: Unknown
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://search.cpan.org/search?mode=module&query=Error
Source: %{perlmod}-%{version}.tar.gz
Buildarch: noarch

%description
The Error package provides two interfaces. Firstly Error provides
a procedural interface to exception handling. Secondly Error is a
base class for errors/exceptions that can either be thrown, for
subsequent catch, or can simply be recorded.

Errors in the class Error should not be thrown directly, but the
user should throw errors from a sub-class of Error


%prep
%setup -q -n %{perlmod}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=$RPM_BUILD_ROOT%{_prefix} 
make OPTIMIZE="$RPM_OPT_FLAGS"
make test

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT$installarchlib
%makeinstall
rm -f `find $RPM_BUILD_ROOT -type f -name perllocal.pod -o -name .packlist`

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT%{_prefix} -type f -print | \
	sed "s@^$RPM_BUILD_ROOT@@g" > %{name}-%{version}-%{release}-filelist
if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(644,root,root,755)
%doc README Change* examples

%changelog
* Fri Aug 18 2006 Josko Plazonic <plazonic@math.princeton.edu>
- initial build

