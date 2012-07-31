Summary: Princeton ph replacement script
Name: princeton-ph
Version: 0.2
Release: 2%{?dist}
Source0: ph
License: Free
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-root
BuildArch: noarch
Requires: openldap-clients >= 2.0.0

%description
This is a simple, Princeton specific, ph replacement script.
ph command accepts one argument and queries princeton LDAP
servers for information on registered users - name, address,
email, phone number and info may be returned.

As of now, it doesn't support any advanced options of original
ph command.

%prep

%build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/ph

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/ph

%changelog
* Fri Feb 10 2012 Josko Plazonic <plazonic@math.princeton.edu>
- adjust for change in cn

* Fri Apr 06 2007 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for PU_IAS 5

* Thu May 01 2003 Josko Plazonic <plazonic@math.princeton.edu>
- rebuilt for 9, with requirement for openldap-client

* Mon Feb 18 2002 Josko Plazonic <plazonic@math.princeton.edu>
- initial release as rpm

