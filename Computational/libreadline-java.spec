%define name            libreadline-java
%define version         0.8.0
%define editline_ver    2.9
%define release         13%{?dist}
%define src_dirs        org test
%define gcj_support     1

Name:                %{name}
Version:             %{version}
Release:             %{release}
Summary:             Java wrapper for the EditLine library
License:             LGPL
Source0:             http://download.sourceforge.net/java-readline/%{name}-%{version}-src.tar.gz
Url:                 http://java-readline.sf.net/
Requires:            libedit >= %{editline_ver}
Requires(post):      /sbin/ldconfig
Requires(postun):    /sbin/ldconfig
%if %{gcj_support}
BuildRequires:       gcc-java >= 4.1.1
BuildRequires:       java-gcj-compat-devel >= 1.0.31
Requires(post):      java-gcj-compat >= 1.0.31
Requires(postun):    java-gcj-compat >= 1.0.31
%else
BuildRequires:       java-devel >= 1.4.2
Requires:            java >= 1.4.2
%endif
BuildRequires:       jpackage-utils >= 0:1.5
BuildRequires:       libedit-devel >= %{editline_ver}
BuildRequires:       %{_libdir}/libtermcap.so
Group:               Development/Libraries
Buildroot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
AutoReqProv:         no

%description
Java-Readline is a port of EditLine for Java.  Or, to be more 
precise, it is a JNI-wrapper to Readline. It is distributed under 
the LGPL.

%package javadoc
Summary:             Javadoc for %{name}
Group:               Development/Libraries

%description javadoc
Javadoc for %{name}.

%package devel
Summary:             Development files for %{name}
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description devel
This package contains development files for %{name}.

%prep
%setup -q

%build
export JAVA_HOME=%{java_home}
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
%__make T_LIBS=JavaEditline #JavaReadline
%__make apidoc

# Fix debuginfo package
rm -f %{src_dirs}
for dir in %{src_dirs}; do
ln -s src/$dir
done

%install
rm -rf %{buildroot}

# jar
%__mkdir_p %{buildroot}%{_javadir}
%__install -m 644 %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)
# lib
%__mkdir_p %{buildroot}%{_libdir}
%__install -m 755 libJavaEditline.so %{buildroot}%{_libdir}/libJavaEditline.so.%{version}
(cd %{buildroot}%{_libdir} && ln -sf libJavaEditLine.so.%{version} libJavaEditline.so)

# javadoc
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
%__cp -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}

# natively compile
%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%__rm -rf %{buildroot}

%post
/sbin/ldconfig

%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun 
/sbin/ldconfig

%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc ChangeLog NEWS README README.1st VERSION COPYING.LIB
%{_libdir}/libJavaEditline.so.*
%{_javadir}/*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files devel
%defattr(0644,root,root,0755)
%{_libdir}/libJavaEditline.so

%changelog
* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-13
- Changed summary and description to describe the change to editline.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-12
- Remove dependency on readline and readline-devel.
- Add dependency on libedit{,-devel}, change make argument to JavaEditline
  from JavaReadline.

* Fri Sep 08 2006 Igor Foox <ifoox@redhat.com> 0.8.0-11
- Doubled percent signs in changelog section.
- Fixed dependency on readline to be >= instead of =.
- Move jar to %%{_javadir} from %%{_jnidir}
- Added dist tag.
- Added COPYING.LIB to doc files.

* Mon Jun 26 2006 Igor Foox <ifoox@redhat.com> 0.8.0-10jpp_3fc
- Moved the unversioned .so file into a -devel package 
- Changed Group of the -javadoc package to Development/Libraries

* Fri Jun 23 2006 Igor Foox <ifoox@redhat.com> 0.8.0-10jpp_2fc
- Remove Vendor and Distribution tags
- Change group to Development/Libraries
- Removed Epoch, and Epoch in Requires for libreadline
- Added (post) and (postun) to Requires of /sbin/ldconfig
- Changed Source0 to use the version and name macros
- Fixed debuginfo package

* Wed May 31 2006 Igor Foox <ifoox@redhat.com> 0:0.8.0-10jpp_1fc
- Natively compile
- Changed BuildRoot to what Extras expects

* Wed Nov 09 2005 Fernando Nasser <fnasser@redhat.com> 0:0.8.0-10jpp
- Rebuild for readline 5.0

* Tue Mar 29 2005 David Walluck <david@jpackage.org> 0:0.8.0-9jpp
- fix duplicate files in file list
- set java bins in path

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-8jpp
- Move jars into %%{_jnidir}

* Tue Nov 2 2004 Nicolas Mailhot <nim@jpackage.org> -  0:0.8.0-7jpp
- Replace build dep on termcap-devel with dep on %%{_libdir}/libtermcap.so
  (needed on RH/FC systems)

* Sat Oct 09 2004 David Walluck <david@jpackage.org> 0:0.8.0-6jpp
- rebuild for JPackage 1.5 devel

* Thu Jan 30 2003 David Walluck <david@anti-microsoft.org> 0:0.8.0-5jpp
- rebuild for JPackage 1.5

* Thu Jan 30 2003 David Walluck <david@anti-microsoft.org> 0.8.0-4jpp
- AutoReqProvides: no
- Strict requires on readline version and /sbin/ldconfig

* Sun Jan 26 2003 David Walluck <david@anti-microsoft.org> 0.8.0-3jpp
- set JAVA_HOME/bin in PATH

* Wed Jan 22 2003 David Walluck <david@anti-microsoft.org> 0.8.0-2jpp
- 1jpp was missing %%changelog
