Summary: A Hebrew spell checker
Name: hspell
Version: 1.0
Release: 4%{?dist}
URL: http://ivrix.org.il/projects/spell-checker/
Source: http://ivrix.org.il/projects/spell-checker/hspell-%{version}.tar.gz
License: GPL
Group: Applications/Text
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: zlib-devel
Obsoletes: hspell-fat
Provides: hspell-fat = %{version}-%{release}

%description
Hspell is a Hebrew SPELLer . It currently provides a mostly spell-like 
interface (gives the list of wrong words in the input text), but can also 
suggest corrections (-c). It also provides a true (yet incomplete) 
morphological analizer (-l), that prints all known meanings of a Hebrew 
string.

On typical documents Hspell recognizes the majority of correct words. However,
users must take into account that it still will not recognize *all* the correct
words; The dictionary is still not complete, and this situation will continue
to improve in the next releases. On the other hand, barring bugs Hspell should
not recognize incorrect words - extreme attention has been given to the
correctness and consistency of the dictionary.

%description -l he
Hspell הוא מאיית עברי, המספק (בינתיים) מנשק דמוי-spell - פולט רשימה של המילים
השגויות המופיעות בקלט. רשימת המילים שלנו נכבדת, אולם היא איננה שלמה עדיין - יש
מילים תקניות שאינן מוכרות והן מדווחות כשגיאות. הקפדנו מאוד על-מנת שמילים שהוא
*כן* מכיר יאויתו נכונה על-פי כללי האקדמיה העברית לכתיב חסר ניקוד )"כתיב מלא"(.
כמו כן, Hspell מספק (-l) מנתח מורפולוגי אמתי (אם-כי לא שלם) אשר מדפיס את כל
המשמעויות האפשריות של מחרוזת אותיות עברית.

%package devel
Summary: Library and include files for Hspell, the hebrew spell checker
Group: Applications/Text
Requires: %{name} = %{version}-%{release}

%description devel
Library and include files for applications that want to use Hspell.

%description -l he devel
ספרייה וקובצי כותרת עבור יישומים שרוצים להשתמש ב-Hspell.

%prep
%setup -q
sed -i -e '/^\s\+strip\s/d' Makefile.in

%build
%configure --enable-fatverb --enable-linginfo
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README WHATSNEW COPYING
%{_bindir}/hspell
%{_bindir}/hspell-i
%{_bindir}/multispell
%{_mandir}/man1/hspell.1*
%{_datadir}/hspell/

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libhspell.a
%{_mandir}/man3/hspell.3*

%changelog
* Sun Jul  9 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-4
- bump version to mend upgrade path. Bug #197125
* Sat May 20 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-3
- do not strip the binary, create useful defuginfo package (Bug #192437).
* Sun May 15 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-2
- new upstream release.
- Hebrew description converted to utf8.
* Tue Feb 28 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-7
- Rebuild for Fedora Extras 5
* Mon Sep 26 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-6
- Add the text of the GPL to the binary package. It seems that I'll do anything
  to make my sponsor Tom happy.
* Thu Sep 23 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-5
- According to Tom's request, distribute the fat version.
- Add short Hebrew description to the devel package.
* Thu Sep 20 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-4
- Distribute the "slim" flavor, as I suspect it is better suited for the casual
  user (even though I personally enjoy the chubby morphological analizer).
* Mon Sep 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-3
- minor spec file cleanups, eliminate "fat" variant
* Thu Sep 15 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-2
- version 0.9, some magic to silence rpmlint
* Fri Jun  4 2004 Dan Kenigsberg <danken@cs.technion.ac.il> 0.8-1
- Some cleanups, and a devel package
* Fri Dec 20 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.7-1
- Changes for version 0.7
* Tue Jul 29 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.6-1
- Tiny changes for the C frontend
* Fri May  2 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.5-1
- create the "fat" variant
* Mon Feb 17 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.3-2
- The release includes only the compressed database.
- Added signature, and some other minor changes.
* Sun Jan  5 2003 Tzafrir Cohen <tzafrir@technion.ac.il> 0.2-1
- Initial build.
