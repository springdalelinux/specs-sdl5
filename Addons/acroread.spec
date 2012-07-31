%define destdir /usr/lib/acroread
Summary: Adobe Acrobat(R) Reader
Name: acroread
Version: 9.4.7
Release: 1.12%{?dist}
License: Commercial
ExclusiveArch: %{ix86}
Group: Applications/Publishing
Source: AdbeRdr%{version}-1_i486linux_enu.tar.bz2
Source10: acroread-expr.patch
Source20: libstdc++.so.6.0.7
Url: http://www.adobe.com/products/acrobat/readstep2.html
BuildRoot: %{_tmppath}/%{name}-root
Obsoletes: acrobat
%define __os_install_post %{nil}
%define ldaplib %( ls -tr /usr/lib/libldap-*.so.[0-9] 2>/dev/null | grep -v libldap_r | grep -v libldapcpp | grep '\.so' | tail -n 1 | cut -d/ -f4- )
%define lberlib %( ls -tr /usr/lib/liblber-*.so.[0-9] 2>/dev/null | grep -v liblber_r | grep '\.so' | tail -n 1 | cut -d/ -f4- )
Requires: %{ldaplib} %{lberlib} gnome-speech openldap xdg-utils libgnome
BuildRequires: which /bin/awk /usr/bin/ldd gnome-speech openldap
AutoReqProv: 0

%description
Acrobat Reader is a browser, which allows to view, distribute and print
the documents in portable document format (PDF). This package includes
the Acrobat Reader.

%package plugin
Summary: Adobe Acrobat(R) Reader plugin for browsers
Requires: webclient acroread = %{version}
Group: Applications/Publishing
Obsoletes: acroread-plugin-mozilla

%description plugin
Acrobat Reader is a browser, which allows to view, distribute and print
the documents in portable document format (PDF). This package includes
a plugin for browsers like firefox.


%prep
%setup -q -c %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{destdir}
tar -x -f AdobeReader/ILINXR.TAR -C $RPM_BUILD_ROOT/%{destdir}
tar -x -f AdobeReader/COMMON.TAR -C $RPM_BUILD_ROOT/%{destdir}

%if "%{?rhel}" == "4"
install -m 755 %{SOURCE20} $RPM_BUILD_ROOT/%{destdir}/Adobe/Reader9/Reader/intellinux/lib
pushd $RPM_BUILD_ROOT/%{destdir}/Adobe/Reader9/Reader/intellinux/lib
ln -s libstdc++.so.6.0.7 libstdc++.so.6
popd
%endif

mkdir -p $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins
ln -s %{destdir}/Adobe/Reader9/Browser/intellinux/nppdf.so $RPM_BUILD_ROOT/%{_libdir}/mozilla/plugins/nppdf.so

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
ln -s %{destdir}/Adobe/Reader9/bin/acroread $RPM_BUILD_ROOT/%{_bindir}/acroread

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
ln -s %{destdir}/Adobe/Reader9/Resource/Shell/acroread.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1

install_dir="$RPM_BUILD_ROOT%{destdir}/Adobe/Reader9/Reader"

#if [ ! -e /usr/lib/libldap.so ]
#then
        rm -f "$install_dir/intellinux/lib/libldap.so" 2>/dev/null
        #LIB_LDAP="`ls -tr /usr/lib/libldap.so*  2>/dev/null | tail -n 1`"
        #if [ "$LIB_LDAP" = "" ]
        #then
        #        LIB_LDAP="`ls -tr /usr/lib/libldap-* 2>/dev/null | grep -v libldap_r | grep -v libldapcpp | grep '\.so' | tail -n 1`"
        #fi
		LIB_LDAP=/usr/lib/%{ldaplib}
        if [ "$LIB_LDAP" != "" ]
        then
                ln -s "$LIB_LDAP" "$install_dir/intellinux/lib/libldap.so"
        fi
#fi
#if [ ! -e /usr/lib/liblber.so ]
#then
        rm -f "$install_dir/intellinux/lib/liblber.so" 2>/dev/null
        #LIB_LBER="`ls -tr /usr/lib/liblber.so* 2>/dev/null | tail -n 1`"
        #if [ "$LIB_LBER" = "" ]
        #then
                LIB_LBER="`ls -tr /usr/lib/liblber-* 2>/dev/null | grep -v liblber_r | grep '\.so' | tail -n 1`"
        #fi
			LIB_LBER=/usr/lib/%{lberlib}
        if [ "$LIB_LBER" != "" ]
        then
                ln -s "$LIB_LBER" "$install_dir/intellinux/lib/liblber.so"
        fi
#fi

    configured_dir="intellinux"
    lib_dir="$install_dir/$configured_dir/lib"

    TESTSPEECHEXEC=`which test-speech 2>/dev/null || echo NONE`
    if [ "$TESTSPEECHEXEC" != "NONE" ]; then
        rm -f "$lib_dir/libORBit-2.so" 2>/dev/null
        rm -f "$lib_dir/libbonobo-2.so" 2>/dev/null
        rm -f "$lib_dir/libbonobo-activation.so" 2>/dev/null
        rm -f "$lib_dir/libgnomespeech.so" 2>/dev/null

        lib_orbit2="`ldd $TESTSPEECHEXEC 2>/dev/null | grep -i libORBit-2.* | cut -d '>' -f2 | cut -d '(' -f 1 |awk '{print $1}' `"
        lib_bonobo="`ldd $TESTSPEECHEXEC 2>/dev/null | grep -i bonobo-2.* | cut -d '>' -f2 | cut -d '(' -f 1 |awk '{print $1}' `"
        lib_bonoboactivation="`ldd $TESTSPEECHEXEC 2>/dev/null | grep -i bonobo-activation.* | cut -d '>' -f2 | cut -d '(' -f 1 |awk '{print $1}' `"
        lib_gnomespeech="`ldd $TESTSPEECHEXEC 2>/dev/null | grep -i libgnomespeech.* | cut -d '>' -f2 | cut -d '(' -f 1 |awk '{print $1}' `"

        if [ -f "$lib_orbit2" -a -f "$lib_bonobo" -a -f "$lib_bonoboactivation" -a -f "$lib_gnomespeech" ]; then
            ln -s "$lib_orbit2" "$lib_dir/libORBit-2.so"
            ln -s "$lib_bonobo" "$lib_dir/libbonobo-2.so"
            ln -s "$lib_bonoboactivation" "$lib_dir/libbonobo-activation.so"
            ln -s "$lib_gnomespeech" "$lib_dir/libgnomespeech.so"
        fi
    fi

%post
#
# Check a given file in given path
#

Which()
{
  OLD_IFS="$IFS"
  IFS=":"
  status=1
  
  for i in $PATH; do
    if [ -x "$i/$1" ]; then
      echo "$i/$1"
      status=0
      break
    fi
  done
    
  IFS="$OLD_IFS"
  return $status
}


ReadInstallDir="%{destdir}"

install_icon()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-icon-resource install "$@" >/dev/null 2>&1
}


install_desktop_menu()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-menu uninstall --mode system "$@" >/dev/null 2>&1
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-menu uninstall --mode user "$@" >/dev/null 2>&1
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-menu install "$@" >/dev/null 2>&1
}


install_desktop_icon()
{
    eval desktop_file="\$$#"
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-icon uninstall "$@" >/dev/null 2>&1
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-icon install "$@" >/dev/null 2>&1 && chmod 777 "$HOME/Desktop/`basename "$desktop_file"`" 2>/dev/null
}


install_mime()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-mime install "$@" >/dev/null 2>&1
}


InstallIcons()
{
    install_dir="$1/Adobe/Reader9/Resource/Icons"

    for icon_size in 16 20 22 24 32 36 48 64 96 128 192; do
        install_icon --noupdate --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/AdobeReader9.png"
        install_icon --noupdate --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/adobe.pdf.png"
        install_icon --noupdate --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/adobe.pdf.png" 'application-pdf'
        install_icon --noupdate --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.fdf.png"
        install_icon --noupdate --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.fdf.png" 'application-fdf'
        install_icon --noupdate --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.pdx.png"
        install_icon --noupdate --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.pdx.png" 'application-pdx'
        install_icon --noupdate --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xdp+xml.png"
        install_icon --noupdate --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xdp+xml.png" 'application-xdp+xml'
        install_icon --noupdate --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xfdf.png"
        install_icon --noupdate --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xfdf.png" 'application-xfdf'
    done
}

KDE_BASE_DIR="/usr"

GNOME_BASE_DIR="/usr"

InstallIcons "$ReadInstallDir"
install_mime --novendor "$ReadInstallDir/Adobe/Reader9/Resource/Support/AdobeReader.xml"

for i in application/pdf application/vnd.adobe.xfdf application/vnd.fdf application/vnd.adobe.xdp+xml application/vnd.adobe.pdx application/fdf application/xdp application/xfdf application/pdx
do
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-mime default "AdobeReader.desktop" "$i" >/dev/null 2>&1
done

install_desktop_menu --novendor "$ReadInstallDir/Adobe/Reader9/Resource/Support/AdobeReader.desktop"
install_desktop_icon --novendor "$ReadInstallDir/Adobe/Reader9/Resource/Support/AdobeReader.desktop"
PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-icon-resource forceupdate >/dev/null 2>&1

exit 0

%preun
if [ "$1" != "0" ] ; then
exit 0;
fi 

uninstall_icon()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-icon-resource uninstall "$@" >/dev/null 2>&1
}


uninstall_desktop_menu()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-menu uninstall "$@" >/dev/null 2>&1
}


uninstall_desktop_icon()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-desktop-icon uninstall "$@" >/dev/null 2>&1
}


uninstall_mime()
{
    PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-mime uninstall "$@" >/dev/null 2>&1
}

unset_mime()
{
    for i in application/pdf application/vnd.adobe.xfdf application/vnd.fdf application/vnd.adobe.xdp+xml application/vnd.adobe.pdx application/fdf application/xdp application/xfdf application/pdx; do
        PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-mime unset "$@" "${i}"
    done
}


UnInstallIcons()
{
    install_dir="$1/Adobe/Reader9/Resource/Icons"

    for icon_size in 16 22 24 32 48 64 128; do
        uninstall_icon --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/AdobeReader9.png"
        uninstall_icon --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/adobe.pdf.png"
        uninstall_icon --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/adobe.pdf.png" 'application-pdf'
        uninstall_icon --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.fdf.png"
        uninstall_icon --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.fdf.png" 'application-fdf'
        uninstall_icon --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.pdx.png"
        uninstall_icon --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.pdx.png" 'application-pdx'
        uninstall_icon --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xdp+xml.png"
        uninstall_icon --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xdp+xml.png" 'application-xdp+xml'
        uninstall_icon --novendor --context apps --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xfdf.png"
        uninstall_icon --novendor --context mimetypes --size $icon_size "$install_dir/${icon_size}x${icon_size}/vnd.adobe.xfdf.png" 'application-xfdf'
    done
}


ReadInstallDir="%{destdir}"
UnInstallIcons "$ReadInstallDir"
uninstall_desktop_menu "$ReadInstallDir/Adobe/Reader9/Resource/Support/AdobeReader.desktop"
uninstall_desktop_icon "$ReadInstallDir/Adobe/Reader9/Resource/Support/AdobeReader.desktop"
unset_mime "AdobeReader.desktop"

PATH="$ReadInstallDir/Adobe/Reader9/Reader/intellinux/bin:$PATH" xdg-icon-resource forceupdate >/dev/null 2>&1

%postun
if [ "$1" != "0" ] ; then
exit 0;
fi 

MkTempInternal()
{
    if [ "${mktemp_count+set}" != "set" ]; then
        mktemp_count="0"
    fi

    mktemp_file="/tmp/acrobat.$$.${mktemp_count}"

    while /usr/bin/test -e "$mktemp_file"
    do
        mktemp_count="`expr $mktemp_count + 1`"
        mktemp_file="/tmp/acrobat.$$.${mktemp_count}"
    done

    touch "$mktemp_file" && chmod 600 "$mktemp_file" && echo "$mktemp_file"
}

MkTemp()
{
    template="tmp.XXXXXXXXXX";
    MKTEMP="`which mktemp 2>/dev/null`";
    if [ "$MKTEMP" != "" ]; then
	    :
    else
	    MKTEMP="MkTempInternal";
    fi

    $MKTEMP /tmp/acrobat.$template
}


ReadInstallDir="%{destdir}"
## kill synchronizerapp
tmpfile="`MkTemp`"
ps -ef 2>/dev/null > "$tmpfile"

synchronizerapp_pid="`awk '{ print $8, $2 }' < "$tmpfile" | grep -w "^$ReadInstallDir/Adobe/Reader9/Reader/intellinux/SynchronizerApp" | awk '{ print $NF; exit }'`"

if [ -z "$synchronizerapp_pid" ]; then
    ps auwwwxg 2>/dev/null > "$tmpfile"
    synchronizerapp_pid="`awk '{ print $11, $2 }' < "$tmpfile" | grep -w "^$ReadInstallDir/Adobe/Reader9/Reader/intellinux/SynchronizerApp" | awk '{ print $NF; exit }'`"

    if [ -z "$synchronizerapp_pid" ]; then
        rm -f "$tmpfile"
        exit 0
    fi
fi

rm -f "$tmpfile"

if [ -n "$synchronizerapp_pid" ]; then
    kill -KILL "$synchronizerapp_pid"
fi

exit 0


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AdobeReader/ReadMe.htm
%dir %{destdir}
%dir %{destdir}/Adobe
%{destdir}/Adobe/Reader9
%{_bindir}/acroread
%{_mandir}/man1/acroread.1.gz

%files plugin
%defattr(-, root, root)
%{_libdir}/mozilla/plugins/nppdf.so


%changelog
* Fri Mar 19 2010 Josko Plazonic <plazonic@math.princeton.edu>
- add workaround for rhel4 compatibility (i.e. include a custom
  built libstdc++.so.6 from gcc 4.0.4)

* Wed Apr 18 2007 Josko Plazonic <plazonic@math.princeton.edu>
- do not deposit icons into default.kde - use crystalsvg instead

* Tue Apr 10 2007 Josko Plazonic <plazonic@math.princeton.edu>
- update icon cache, just in case

* Fri Apr  7 2007 Josko Plazonic <plazonic@math.princeton.edu>
- adapt the package for PU_IAS 5, in particular take care of
  selinux as the plugin requires special fixing

* Wed Jan 10 2007 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 7.0.9

* Fri Mar 25 2005 Josko Plazonic <plazonic@math.princeton.edu>
- upgrade to 7

* Thu Dec 16 2004 Josko Plazonic <plazonic@math.princeton.edu>
- security upgrade to 5.10

* Thu Jun 24 2004 Thomas Uphill <uphill@ias.edu>
- security upgrade to 5.09

* Sun Sep 28 2003 Josko Plazonic <plazonic@math.princeton.edu>
- security upgrade to 5.08

* Wed Jun 18 2003 Josko Plazonic <plazonic@math.princeton.edu>
- security upgrade to 5.07

* Sat May 31 2003 Josko Plazonic <plazonic@math.princeton.edu>
- in order to get plugger out of the way made acroread-mozilla
  plugin have name znppdf.so

* Wed Apr 30 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for RH 9 with the trick LANG=en_US to get it to work

* Wed Jul 03 2002 Josko Plazonic <plazonic@math.princeton.edu>
- adapted for acrobat 5.05 and RH 7.3, rebuilt 

* Mon Aug 14 2000 Preston Brown <pbrown@redhat.com>
- require netscape-common not netscape-communicator (#16088)

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Tue Jul 11 2000 Than Ngo <than@redhat.de>
- rebuilt

* Mon Jul 03 2000 Tim Powers <timp@redhat.com>
- fixed install section so that regular users can build

* Mon Jul 03 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon May 22 2000 Ngo Than <than@redhat.de>
- rename to arcoread
- remove /etc/X11/wmconfig
- remove /usr/lib/acrobat/ReadMe

* Mon May 22 2000 Ngo Than <than@redhat.de>
- initial RPM for 7.0 
