#
# Conditional build:
%bcond_without	initrd	# build without udev-initrd
#
%define dev_ver 3.0.0
Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	032
Release:	0.1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	6df7392c3f5fe44d7cf261a0d2497b99
Source1:	%{name}.rules
Source2:	%{name}.permissions
Source3:	%{name}.conf
Source4:	start_udev
Patch0:		%{name}-025-volsbin.patch
Patch1:		%{name}-029-chassis.patch
Patch2:		%{name}-029-moreconf.patch
Patch3:		%{name}-030-selinux.patch
Patch4:		%{name}-030-rhsec.patch
Patch5:		%{name}-030-symlink.patch
Patch6:		%{name}-030-cloexec.patch
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	hotplug >= 2003_08_05
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		extras		extras/scsi_id extras/volume_id

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u¿ytkownika dla j±der 2.5 i
wy¿szych.

%package initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description initrd
A userspace implementation of devfs - static binary for initrd.

%description initrd -l pl
Implementacja devfs w przestrzeni u¿ytkownika - statyczna binarka dla
initrd.

%package dev
Summary:	dev replacement using udev
Summary(pl):	Zamiennik dev z u¿yciem udev
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	dev = %{dev_ver}
Obsoletes:	dev
Obsoletes:	MAKEDEV
Conflicts:	kernel < 2.4

%description dev
dev replacement using udev.

%description dev -l pl
Zamiennik dev z u¿yciem udev.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%if %{with initrd}
%{__make} \
%ifarch athlon
	ARCH=i386 \
%endif
	udevdir=/dev \
	CC="%{__cc}" \
	LD="%{__cc} %{rpmldflags} -static" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS=""

cp -a udev initrd-udev
%{__make} clean
%endif

%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS="%{extras}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_prefix}/sbin,/udev}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/{rules.d,permissions.d,scripts}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/{default,block}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	EXTRAS="%{extras}"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.permissions
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-udev.rules
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/permissions.d/50-udev.permissions
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/start_udev

mv $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/net/hotplug.dev $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts/
ln -s ../../udev/scripts/hotplug.dev $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/net/

%if %{with initrd}
install -m755 initrd-udev $RPM_BUILD_ROOT%{_sbindir}/initrd-udev
ln -s initrd-udev $RPM_BUILD_ROOT%{_bindir}/udevstart.initrd
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HOWTO-udev_for_dev README TODO
%doc docs/{overview,udev_vs_devfs,libsysfs.txt,udev-*.pdf,RFC-dev.d}
%attr(755,root,root) %{_sbindir}/*
%if %{with initrd}
%exclude %{_sbindir}/*initrd*
%endif
%attr(755,root,root) %{_bindir}/*

%config(missingok) %{_sysconfdir}/dev.d/net/hotplug.dev
%attr(755,root,root) %dir %{_sysconfdir}/dev.d/
%attr(755,root,root) %dir %{_sysconfdir}/dev.d/default

%attr(755,root,root) %dir %{_sysconfdir}/udev/
%attr(755,root,root) %dir %{_sysconfdir}/udev/rules.d/
%attr(755,root,root) %dir %{_sysconfdir}/udev/permissions.d/
%attr(755,root,root) %dir %{_sysconfdir}/udev/scripts/

%attr(755,root,root) %{_sysconfdir}/udev/scripts/hotplug.dev

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/udev.conf
%config(noreplace) %verify(not size mtime md5)  %{_sysconfdir}/udev/rules.d/50-udev.rules
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/permissions.d/50-udev.permissions

%config(missingok) %{_sysconfdir}/hotplug.d/default/10-udev.hotplug

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config

%{_mandir}/man8/*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*initrd*
%endif
