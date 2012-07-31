Name:           fuse-sshfs
Version:        2.2
Release:        5%{?dist}
Summary:        FUSE-Filesystem to access remote filesystems via SSH

Group:          System Environment/Base
License:        GPLv2
URL:            http://fuse.sourceforge.net/sshfs.html
Source0:        http://downloads.sourceforge.net/fuse/sshfs-fuse-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:       sshfs = %{version}-%{release}
Requires:       fuse >= 2.2
Requires:	openssh-clients
BuildRequires:  fuse-devel >= 2.2
BuildRequires:  glib2-devel >= 2.0
BuildRequires:	openssh-clients

%description
This is a FUSE-filesystem client based on the SSH File Transfer Protocol.
Since most SSH servers already support this protocol it is very easy to set
up: i.e. on the server side there's nothing to do.  On the client side
mounting the filesystem is as easy as logging into the server with ssh.

%prep
%setup -q -n sshfs-fuse-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ.txt NEWS README
%{_bindir}/sshfs
%if 0%{?rhel}
# if openssh-clients < 4.4
%{_libdir}/sshnodelay.so
%endif
%{_mandir}/man1/sshfs.1.gz

%changelog
* Sun Sep 27 2009 Peter Lemenkov <lemenkov@gmail.com> 2.2-5
- No need for versioning in (Build)Requires for openssh-clients

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.2-4
- Rebuilt with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  9 2008 Peter Lemenkov <lemenkov@gmail.com> 2.2-1
- Ver. 2.2

* Sun Sep 28 2008 Peter Lemenkov <lemenkov@gmail.com> 2.1-1
- Ver. 2.1

* Mon May 19 2008 Peter Lemenkov <lemenkov@gmail.com> 2.0-1
- Ver. 2.0

* Sat Feb  9 2008 Peter Lemenkov <lemenkov@gmail.com> 1.9-2
- Rebuild for GCC 4.3

* Wed Jan 23 2008 Peter Lemenkov <lemenkov@gmail.com> 1.9-2
- Added missing Requires and BuildRequires - openssh-clients >= 4.4

* Wed Jan 23 2008 Peter Lemenkov <lemenkov@gmail.com> 1.9-1
- Ver. 1.9
- Added provides: sshfs
- Modified License field according to Fedora policy.

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 1.7-2
- Rebuild for FC6

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 1.7-1
- New version
- Rebuild for FC6

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> - 1.6-2
- added missing sshnodelay.so

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> - 1.6-1
- Version 1.6

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 1.4-2
- small cosmetic fixes

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 1.4-1
- Version 1.4

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.2-3
- Use dist

* Fri Nov 04 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.2-2
- Update deps

* Fri Oct 28 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.2-1
- Initial RPM release.
