Summary: Conversion between character sets and surfaces
Name: recode
Version: 3.6
Release: 22%{?dist}
License: GPL
Group: Applications/File
Source: http://recode.progiciels-bpi.ca/archives/recode-%{version}.tar.gz
Patch0: recode.patch
Patch1: recode-3.6-getcwd.patch
Url: http://recode.progiciels-bpi.ca/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): /sbin/install-info
Requires(post): /sbin/ldconfig
Requires(preun): /sbin/install-info
Requires(postun): /sbin/ldconfig


%description
The `recode' converts files between character sets and usages.
It recognises or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations.  Most RFC 1345 character sets
are supported.

%package devel
Summary: Header files and static libraries for development using recode
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The `recode' library converts files between character sets and usages.
The library recognises or produces nearly 150 different character sets
and is able to transliterate files between almost any pair. When exact
transliteration are not possible, it may get rid of the offending
characters or fall back on approximations. Most RFC 1345 character sets
are supported.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .getcwd

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall
%find_lang %{name}

# remove unpackaged file from the buildroot
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# remove libtool archives
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/recode.info.gz %{_infodir}/dir --entry="* recode: (recode).                        Conversion between character sets and surfaces." || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/recode.info.gz %{_infodir}/dir --entry="* recode: (recode).                        Conversion between character sets and surfaces." || :
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING* ChangeLog NEWS README THANKS TODO
%{_mandir}/*/*
%{_infodir}/recode.info*
%{_bindir}/*
%{_libdir}/*.so.0*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Fri Sep 01 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-22
- rebuild

* Mon Feb 13 2006 Zoltan Kota <z.kota[AT]gmx.net> 3.6-21
- rebuild

* Thu Dec 22 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-20
- rebuild

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-19
- fix requires
- disable static libs and remove libtool archives
- add %%doc

* Fri Aug 26 2005 Zoltan Kota <z.kota[AT]gmx.net> 3.6-18
- add dist tag
- specfile cleanup

* Thu May 26 2005 Bill Nottingham <notting@redhat.com> 3.6-17
- rebuild for Extras

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.6-16
- cleanup

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.6-15
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 3.6-14
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Than Ngo <than@redhat.com> 3.6-11 
- add a patch file from kota@szbk.u-szeged.hu (bug #115524)

* Thu Nov 20 2003 Thomas Woerner <twoerner@redhat.com> 3.6-10
- Fixed RPATH (missing make in %%build)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 3.6-7
- rebuild on all arches
- remove unpackaged file from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Bill Nottingham <notting@redhat.com> 3.6-4
- add ldconfig %post/%postun

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 3.6-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 13 2001 Than Ngo <than@redhat.com> 3.6-1
- initial RPM for 8.0
