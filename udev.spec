#
# TODO:
# - is there a reason _not_ to build scsi_id? Adds no dependencies.
#
# Conditional build:
%bcond_with	initrd	# build udev-initrd
%bcond_without	dbus	# build DBUS extra package
%bcond_without	selinux # build SELinux extra package
%bcond_without	scsi_id # build scsi_id extra package
#
Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	025
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	4f4c0ace4307cb1c73d9f5365fe6c946
%if %{with dbus}
BuildRequires:	dbus-devel >= 0.20
%endif
%if %{with selinux}
BuildRequires:	libselinux-devel >= 1.10
%endif
BuildRequires:	pkgconfig
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

%package dbus
Summary:	DBUS extra package for udev
Summary(es):	Paquete adicional de DBUS para udev
Summary(pl):	Dodatkowy pakiet DBUS dla udev
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	dbus >= 0.20-2

%description dbus
DBUS extra package for udev.

%description dbus -l es
Paquete adicional de DBUS para udev.

%description dbus -l pl
Dodatkowy pakiet DBUS dla udev.

%prep
%setup -q

%build
EXTRAS=""
%if %{with dbus}
EXTRAS="$EXTRAS extras/dbus"
%endif
%if %{with selinux}
EXTRAS="$EXTRAS extras/selinux"
%endif
%if %{with scsi_id}
EXTRAS="$EXTRAS extras/scsi_id"
%endif

%if %{with initrd}
%{__make} \
%ifarch athlon
	ARCH=i386 \
%endif
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=true \
	udev
	
cp -a udev udev-initrd
%{__make} clean
%endif

%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_LOG=true \
	EXTRAS="$EXTRAS"

%install
rm -rf $RPM_BUILD_ROOT

EXTRAS=""
%if %{with dbus}
EXTRAS="$EXTRAS extras/dbus"
%endif
%if %{with selinux}
EXTRAS="$EXTRAS extras/selinux"
%endif
%if %{with scsi_id}
EXTRAS="$EXTRAS extras/scsi_id"
%endif

install -d $RPM_BUILD_ROOT%{_prefix}/sbin

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	EXTRAS="$EXTRAS"

%if %{with initrd}
install -m755 udev-initrd $RPM_BUILD_ROOT%{_sbindir}
%endif

%if %{with dbus}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/default/udev_dbus.dev
ln -s %{_prefix}/sbin/udev_dbus $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/default/udev_dbus.dev
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart 1>&2
fi

%preun
if [ -f /var/lock/subsys/messagebus ]; then
	/etc/rc.d/init.d/messagebus restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HOWTO-udev_for_dev README TODO
%doc docs/{overview,udev_vs_devfs,libsysfs.txt,udev-*.pdf,RFC-dev.d}
%attr(755,root,root) %{_sbindir}/udev*
%if %{with initrd}
%exclude %{_sbindir}/udev-initrd
%endif
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %dir %{_sysconfdir}/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(750,root,root) %{_sysconfdir}/dev.d
%if %{with dbus}
%exclude %{_sysconfdir}/dev.d/default/*dbus*
%endif
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
%if %{with scsi_id}
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config
%attr(755,root,root) %{_sbindir}/scsi_id
%endif
%{_mandir}/man8/*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/udev-initrd
%endif

%if %{with dbus}
%files dbus
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/sbin/*dbus
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dbus*/system.d/*
%endif
