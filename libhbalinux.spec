Name:           libhbalinux
Version:        1.0.17
Release:        2%{?dist}
Summary:        FC-HBAAPI implementation using scsi_transport_fc interfaces
Group:          System Environment/Libraries
License:        LGPLv2
URL:            http://www.open-fcoe.org
# This source was cloned from upstream git
Source0:        %{name}-%{version}.tar.gz
Patch0:         libhbalinux-1.0.13-conf.patch
BuildRequires:  libhbaapi-devel >= 2.2.9-2
BuildRequires:  libpciaccess-devel libtool automake
Requires:       libhbaapi >= 2.2.9-2

%description
SNIA HBAAPI vendor library built on top of the scsi_transport_fc interfaces.

%package devel
Summary:        A file needed for libhbalinux application development
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
The libhbalinux-devel package contains the library pkgconfig file.

%prep
%setup -q
%patch0 -p1 -b .conf

%build
./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post
/sbin/ldconfig
ORG=org.open-fcoe.libhbalinux
LIB=%{_libdir}/libhbalinux.so.2.0.2
STR="$ORG	$LIB"
CONF=%{_sysconfdir}/hba.conf
if test -f $CONF; then
  grep -E -q ^[[:space:]]*$ORG[[:space:]]+$LIB $CONF
  if test $? -ne 0; then
    echo $STR >> $CONF;
  fi
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    ORG=org.open-fcoe.libhbalinux
    CONF=%{_sysconfdir}/hba.conf
    if test -f $CONF; then
        grep -v $ORG $CONF > %{_sysconfdir}/hba.conf.new
        mv %{_sysconfdir}/hba.conf.new %{_sysconfdir}/hba.conf
    fi
fi

%files
%defattr(-,root,root,-)
%doc README COPYING
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%changelog
* Thu Dec 17 2015 Chris Leech <cleech@redhat.com> - 1.0.16-2
- 1074125 rebase to upstream v1.0.17

* Thu Jun 20 2013 Petr Šabata <contyk@redhat.com> - 1.0.16-1
- 1.0.16 bump, documentation and autotools scripts updates (#829810)
- Fix an old bogus date in the changelog

* Thu Aug 16 2012 Petr Šabata <contyk@redhat.com> - 1.0.14-1
- 1.0.14 bump, no code changes (#819936)

* Thu Feb 16 2012 Petr Šabata <contyk@redhat.com> - 1.0.13-1
- 1.0.13 bump + 47d8dca, "Set SerialNumber to 'Unknown' if not found"  (#788510)
- Subpackage the pkgconfig file

* Thu Jul 14 2011 Petr Sabata <contyk@redhat.com> - 1.0.12-1
- Update to 1.0.12
- Resolves: rhbz#719584
- Related: rhbz#695941

* Wed Apr 27 2011 Petr Sabata <psabata@redhat.com> - 1.0.10-3
- Do not delete our hba.conf reference during future upgrades
- Resolves: rhbz#700007

* Thu Mar 31 2011 Petr Sabata <psabata@redhat.com> - 1.0.10-2
- Avoid NULL dereference when parsing supported_classes sys entry
- Remove redundant buildroot definition
- Resolves: rhbz#690014

* Mon May 24 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.10-1
- rebased to 1.0.10, bugfix release (see git changelog for more info)

* Wed Jan 13 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.9-2
- new tarball matching official 1.0.9 release (pulled from git)

* Fri Dec 04 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.9-20091204git
- rebased to the latest version in upstream git

* Thu Jul 30 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.8-1
- rebase of libhbalinux, spec file adjusted to match changes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-3
- replaced unofficial 1.0.7 source tarball with official one
- update of Makefile, part of it moved to postinstall section
  of spec file

* Tue Mar 31 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-2
- minor changes in spec file

* Mon Mar 2 2009 Chris Leech <christopher.leech@intel.com> - 1.0.7-1
- initial build

