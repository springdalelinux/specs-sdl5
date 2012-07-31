%define perlmod File-Copy-Recursive
Summary: %{perlmod} interface
Name: perl-%{perlmod}
Version: 0.37
Release: 1%{dist}
Packager: Josko Plazonic <plazonic@math.princeton.edu>
License: GPL or Artistic
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Source: http://search.cpan.org/CPAN/authors/id/D/DM/DMUEY/%{perlmod}-%{version}.tar.gz
Buildarch: noarch

%description
Perl extension for recursively copying files and directories

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
%doc Changes README

%changelog
* Tue Aug 08 2006 Josko Plazonic <plazonic@math.princeton.edu>
- first build

