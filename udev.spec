# TODO:
# - write init.d script for multipathd
# - write preambules for subpackages and uncomment %%files
#
# Conditional build:
%bcond_with	initrd    # build udev-initrd
%bcond_without	selinux   # does't build selinux support
%bcond_without	dbus      # does't build DBUS support
%bcond_without	libsysfs  # does't build scsi_id and multipath-tools (need sysfsutils-devel)
%bcond_without	devmapper # does't build multipath-tools
#
Summary:	A userspace implementation of devfs
Summary(pl.UTF-8):   Implementacja devfs w przestrzeni użytkownika
Name:		udev
Version:	025
Release:	0.1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	4f4c0ace4307cb1c73d9f5365fe6c946
Patch0:		%{name}-libsysfs.patch
Patch1:		%{name}-dm.patch
Patch2:		%{name}-DESTDIR.patch
Patch3:		%{name}-provision.patch
BuildRequires:	dbus-devel >= 0.20
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%{?with_selinux:BuildRequires:	libselinux-devel >= 1.10}
%{?with_dbus:BuildRequires:	dbus-devel}
%{?with_libsysfs:BuildRequires:	sysfsutils-devel}
%{?with_devmapper:BuildRequires:	device-mapper-devel}
Requires:	coreutils
Requires:	dbus >= 0.20-2
Requires:	hotplug >= 2003_08_05
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika dla jąder 2.5 i
wyższych.

%package initrd
Summary:	A userspace implementation of devfs - static binary for initrd
Summary(pl.UTF-8):   Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla initrd
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description initrd
A userspace implementation of devfs - static binary for initrd.

%description initrd -l pl.UTF-8
Implementacja devfs w przestrzeni użytkownika - statyczna binarka dla
initrd.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%if %{with initrd}
%{__make} \
%ifarch athlon
	ARCH=i386 \
%endif
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_DBUS=false \
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
	USE_DBUS=true

%if %{with selinux}
%{__make} \
	-C extras/selinux \
	%{!?debug:DEBUG=false} \
	CFLAGS="%{rpmcflags}" \
	LD="%{__cc}" \
	CC="%{__cc}" 
%endif	
%if %{with dbus}
%{__make} \
	-C extras/dbus \
	%{!?debug:DEBUG=false} \
	CFLAGS="%{rpmcflags}" \
	LD="%{__cc}" \
	CC="%{__cc}" 
%endif

%{__make} \
	-C extras/chassis_id \
	%{!?debug:DEBUG=false} \
	CFLAGS="%{rpmcflags}" \
	LD="%{__cc}" \
	CC="%{__cc}" 
	
%if %{with libsysfs}
%{__make} \
	-C extras/scsi_id \
	%{!?debug:DEBUG=false} \
	CFLAGS="%{rpmcflags}" \
	LD="%{__cc}" \
	CC="%{__cc}" 
	
%if %{with devmapper}
%{__make} \
	-C extras/multipath-tools \
	%{!?debug:DEBUG=false} \
	CFLAGS="%{rpmcflags}" \
	LD="%{__cc}" \
	CC="%{__cc}" \
	DMOBJS=-ldevmapper \
	SYSFSOBJS=-lsysfs \
	CRT0= \
	LIB= \
	LIBGCC=
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
# for udev_dbus
install -d $RPM_BUILD_ROOT{/usr/sbin,/etc/dev.d/default}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	USE_DBUS=true

%if %{with selinux}
%{__make} \
	-C extras/selinux \
	DESTDIR=$RPM_BUILD_ROOT \
	install
%endif
%if %{with dbus}
%{__make} \
	-C extras/dbus \
	DESTDIR=$RPM_BUILD_ROOT \
	install
%endif

install -m755 extras/chassis_id/chassis_id $RPM_BUILD_ROOT/%{_sbindir}
install extras/chassis_id/provision.tbl $RPM_BUILD_ROOT/%{_sysconfdir}

%if %{with libsysfs}
%{__make} \
	-C extras/scsi_id \
	DESTDIR=$RPM_BUILD_ROOT \
	install
%if %{with devmapper}	
%{__make} \
	-C extras/multipath-tools \
	DESTDIR=$RPM_BUILD_ROOT \
	rcdir=%{_initrddir} \
	install
%endif
%endif
%if %{with initrd}	
install -m755 udev-initrd $RPM_BUILD_ROOT%{_sbindir}
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
%doc docs/{overview,udev_vs_devfs,libsysfs.txt,udev-*.pdf,RFC-dev.d,rh_udev_for_dev.txt}
%doc docs/{persistent_naming,writing_udev_rules}
%doc extras/{ide-devfs.sh,scsi-devfs.sh,name_cdrom.pl,start_udev}
%attr(755,root,root) %{_sbindir}/udev
%attr(755,root,root) %{_sbindir}/udevd
%attr(755,root,root) %{_sbindir}/udevsend
%attr(755,root,root) %{_sbindir}/udevstart
%attr(755,root,root) %{_bindir}/udevtest
%attr(755,root,root) %{_bindir}/udevinfo
%attr(750,root,root) %dir %{_sysconfdir}/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dbus*/system.d/*
%{_mandir}/man8/udev.8*
%{_mandir}/man8/udevd.8*
%{_mandir}/man8/udevinfo.8*
%{_mandir}/man8/udevstart.8*
%{_mandir}/man8/udevtest.8*
%dir %{_sysconfdir}/dev.d
%dir %{_sysconfdir}/dev.d/net
%dir %{_sysconfdir}/dev.d/default
%attr(755,root,root) %{_sysconfdir}/dev.d/net/hotplug.dev

%if %{with selinux}
#%files selinux
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/udev_selinux
%endif

#%files chassis_id
%defattr(644,root,root,755)
#%doc extras/chassis_id/README
%attr(755,root,root) %{_sbindir}/chassis_id
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/provision.tbl

%if %{with libsysfs}
#%files scsi_id
%defattr(644,root,root,755)
#%doc extras/scsi_id/{README,ChangeLog,release-notes,TODO,gen_scsi_id_udev_rules.sh}
%attr(755,root,root) %{_sbindir}/scsi_id
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config
%{_mandir}/man8/scsi_id.8*

%if %{with devmapper}
#%files multipath
%defattr(644,root,root,755)
#%doc extras/multipath-tools/{AUTHOR,ChangeLog,README}
%attr(755,root,root) %{_sbindir}/multipath
%attr(755,root,root) %{_sbindir}/devmap_name
%attr(755,root,root) %{_bindir}/multipathd
#rewrite for PLD
#/etc/rc.d/init.d/multipathd
%{_sysconfdir}/hotplug.d/scsi/multipath.hotplug
%{_mandir}/man8/multipath.8*
%{_mandir}/man8/devmap_name.8*
%endif
%endif

%if %{with dbus}
#%files dbus
%defattr(644,root,root,755)
%attr(755,root,root) /usr/sbin/udev_dbus
%{_sysconfdir}/dbus-1/system.d/*
%endif

%if %{with initrd}
%exclude %{_sbindir}/udev-initrd

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/udev-initrd
%endif
