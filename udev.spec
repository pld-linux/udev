#
# Conditional build:
%bcond_with	initrd	# build udev-initrd
#
%define dev_ver 3.0.0
Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	032
Release:	1.9
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	6df7392c3f5fe44d7cf261a0d2497b99
Source1:	%{name}.sysconfig
Source2:	%{name}.hotplug
Patch0:		%{name}-start_udev.patch
Patch1:		%{name}-permissions.patch
Patch2:		%{name}-rules.patch
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	hotplug >= 2003_08_05
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

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

%build
%if %{with initrd}
%{__make} \
%ifarch athlon
	ARCH=i386 \
%endif
	udevdir=/dev \
	CC="%{__cc}" \
	LD="%{__cc} -static" \
	%{!?debug:DEBUG=false} \
	OPTIMALIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	EXTRAS="" \
	USE_LOG=true \
	udev
	
cp -a udev udev.static
%{__make} clean
%endif

EXTRAS="extras/scsi_id extras/volume_id"

%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_LOG=true \
	EXTRAS="$EXTRAS"

%install
rm -rf $RPM_BUILD_ROOT

EXTRAS="extras/scsi_id extras/volume_id"

install -d $RPM_BUILD_ROOT{%{_prefix}/sbin,/dev,/etc/sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	EXTRAS="$EXTRAS"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default/10-udev.hotplug

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/udev
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default/10-udev.hotplug
install extras/start_udev $RPM_BUILD_ROOT%{_sbindir}

%if %{with initrd}
install udev.static $RPM_BUILD_ROOT%{_sbindir}
ln -sf udev.static $RPM_BUILD_ROOT%{_sbindir}/udevstart.static
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HOWTO-udev_for_dev README TODO
%doc docs/{overview,udev_vs_devfs,libsysfs.txt,udev-*.pdf,RFC-dev.d}
%attr(755,root,root) %{_sbindir}/udev*
%attr(755,root,root) %{_sbindir}/start_udev
%attr(755,root,root) %{_prefix}/sbin/udev*
%if %{with initrd}
%exclude %{_sbindir}/*.static
%endif
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %dir %{_sysconfdir}/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(750,root,root) %{_sysconfdir}/dev.d
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/scsi_id
%{_mandir}/man8/*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*.static
%endif

%files dev
%defattr(644,root,root,755)
