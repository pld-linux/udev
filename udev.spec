#
# Conditional build:
%bcond_without	initrd	# build without udev-initrd
#
%define dev_ver 3.0.0
Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	064
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	589a5fd80ca2c85874e81cc767e6fdeb
Source1:	%{name}.rules
Source3:	%{name}.conf
Source4:	start_udev
Source5:	devmap_name.tar.gz
# Source5-md5:	f72f557299436af5d6ad66815b80a641
Source6:	%{name}-check-cdrom.sh
Patch0:		%{name}-strnlen.patch
BuildRequires:	device-mapper-devel
BuildRequires:	libselinux-devel >= 1.17.13
BuildRequires:	sed >= 4.0
%{?with_initrd:BuildRequires:	dietlibc-static}
Requires:	coreutils
Requires:	hotplug >= 2003_08_05
Obsoletes:	udev-dev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		extras		extras/ata_id extras/dasd_id extras/chassis_id extras/floppy extras/run_directory extras/scsi_id extras/usb_id extras/volume_id

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

%prep
%setup -q -a5
%patch0 -p1
sed -i -e 's#gcc#$(CC)#g' devmap_name/Makefile

%build
%if %{with initrd}
%{__make} \
%ifarch athlon
	ARCH=i386 \
%endif
	udevdir=/udev \
	CC="%{_target_cpu}-dietlibc-gcc" \
	LD="%{_target_cpu}-dietlibc-gcc %{rpmldflags} -static" \
	%{!?debug:DEBUG=false} \
	OPTFLAGS="%{rpmcflags} -Dclearenv\(\)=environ=NULL" \
	USE_KLIBC=false \
	USE_LOG=true \
	USE_SELINUX=false \
	EXTRAS=""

cp -a udev initrd-udev
%{__make} clean
%endif

%{__make} -C devmap_name \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%{__make} \
	udevdir=/udev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}" \
	USE_KLIBC=false \
	USE_LOG=true \
	EXTRAS="%{extras}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_prefix}/sbin,/udev}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/{rules.d,scripts}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/{default,block,net,snd}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	EXTRAS="%{extras}"

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/init.d/udev

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-udev.rules
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/udev.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/start_udev
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts/check-cdrom.sh

install etc/dev.d/net/hotplug.dev $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
ln -s ../../udev/scripts/hotplug.dev $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/net/
ln -s /sbin/udevsend $RPM_BUILD_ROOT%{_sysconfdir}/hotplug.d/default/10-udev.hotplug

%if %{with initrd}
install -m755 initrd-udev $RPM_BUILD_ROOT%{_sbindir}/initrd-udev
ln -s initrd-udev $RPM_BUILD_ROOT%{_sbindir}/udevstart.initrd
%endif

install devmap_name/devmap_name $RPM_BUILD_ROOT%{_sbindir}/devmap_name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ HOWTO-udev_for_dev README RELEASE-NOTES TODO
%doc docs/{overview,udev_vs_devfs,libsysfs.txt,RFC-dev.d}
%attr(755,root,root) %{_sbindir}/*
%dir /udev
%if %{with initrd}
%exclude %{_sbindir}/*initrd*
%endif
%attr(755,root,root) %{_bindir}/*

%config(missingok) %{_sysconfdir}/dev.d/net/hotplug.dev
%attr(755,root,root) %dir %{_sysconfdir}/dev.d
%attr(755,root,root) %dir %{_sysconfdir}/dev.d/default
%attr(755,root,root) %dir %{_sysconfdir}/dev.d/net
%attr(755,root,root) %dir %{_sysconfdir}/dev.d/snd

%attr(755,root,root) %dir %{_sysconfdir}/udev
%attr(755,root,root) %dir %{_sysconfdir}/udev/rules.d
%attr(755,root,root) %dir %{_sysconfdir}/udev/scripts

%attr(755,root,root) %{_sysconfdir}/udev/scripts/hotplug.dev
%attr(755,root,root) %{_sysconfdir}/udev/scripts/check-cdrom.sh

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/udev.conf
%config(noreplace) %verify(not size mtime md5)  %{_sysconfdir}/udev/rules.d/50-udev.rules

%config(missingok) %{_sysconfdir}/hotplug.d/default/10-udev.hotplug

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/scsi_id.config

%{_mandir}/man8/*

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*initrd*
%endif
