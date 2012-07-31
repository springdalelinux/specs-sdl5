Name:           xbae
Version:        4.60.4
Release:        5%{?dist}
Summary:        Motif matrix, caption and text input widgets
Group:          System Environment/Libraries
License:        BSD
URL:            http://xbae.sourceforge.net/
Source0:        http://ovh.dl.sourceforge.net/sourceforge/xbae/xbae-%{version}.tar.gz
# this fixes the link of the example using Wcl, it shouldn't be of use
# now that Wcl isn't buildrequired, but it is still better.
Patch0:         xbae-link_Mri_with_lXmp.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libXp-devel and libXext-devel are required by openmotif-devel or
# lesstif-devel
# Wcl-devel is only needed by an example, which adds the Xbae widgets to Wcl
BuildRequires:  libXpm-devel 
BuildRequires:  openmotif-devel
#BuildRequires:  lesstif-devel
# Wcl-devel should only needed by an example, which adds the Xbae widgets 
# to Wcl, so there is no real need for it.
#BuildRequires:  Wcl-devel
# needed for examples
BuildRequires:  libXmu-devel

# name with capitalized X was used for the xbae package shipped up to FC-1
Provides:       Xbae = %{version}-%{release}
Obsoletes:      Xbae < %{version}-%{release}

# to be sure that we link against lesstif even if openmotif provides the same
# soname
Requires:       openmotif

%description
XbaeMatrix is a free Motif(R) table widget (also compatible with the free 
LessTif) which presents an editable array of string data to the user in a 
scrollable table similar to a spreadsheet. The rows and columns of the Matrix 
may optionally be labelled. A number of "fixed" and "trailing fixed" rows 
or columns may be specified.

The XbaeCaption widget is a simple Motif manager widget that associates 
a label with a child.

In addition the XbaeInput widget is being distributed, a text input field 
that provides generic customised data entry and formatting for strings.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       openmotif-devel 
#Requires:       lesstif-devel 
Requires:       libXpm-devel
# for the aclocal directory
Requires:       automake
Provides:       Xbae-devel = %{version}-%{release}
Obsoletes:      Xbae-devel < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch -p1


%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}

# the configure test doesn't find the aclocal dir, so we install
# the .m4 file by hand
install -d -m755 $RPM_BUILD_ROOT%{_datadir}/aclocal
install -m644 ac_find_xbae.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_datadir}/Xbae/ Xbae-docs
# remove duplicate files
rm Xbae-docs/README
rm Xbae-docs/NEWS

# clean the examples
make -C examples clean
cp -pr examples code_examples
find code_examples -name '*akefile*' -exec rm {} \;
rm code_examples/extest
rm code_examples/testall
mv code_examples/builderXcessory/README Xbae-docs/examples/builderXcessory/
rm -rf code_examples/builderXcessory/
ln -s ../examples/builderXcessory/ code_examples/builderXcessory

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc Xbae-docs/* code_examples
%{_includedir}/Xbae/
%{_libdir}/*.so
%{_mandir}/man*/Xbae*
%{_datadir}/aclocal/*

%changelog
* Wed Apr  4 2007 Josko Plazonic <plazonic@math.princeton.edu>
- go back to openmotif

* Sun Dec 10 2006 Patrice Dumas <pertusus@free.fr> 4.60.4-5
- Requires automake is for -devel (#219047)

* Sat Sep  9 2006 Patrice Dumas <pertusus@free.fr> 4.60.4-4
- add BuildRequires libXmu-devel for examples

* Thu Aug 31 2006 Patrice Dumas <pertusus@free.fr> 4.60.4-3
- rebuild against lesstif
- add Obsolete/Provides for Xbae

* Fri Aug 25 2006 Patrice Dumas <pertusus@free.fr> 4.60.4-2
- remove dependency on Wcl-devel (was only of use for an example)
- clean docs

* Thu May 18 2006 Patrice Dumas <pertusus@free.fr> 4.60.4-1
- Packaged for fedora extras
