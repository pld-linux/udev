%bcond_without	initrd # don't build udev-initrd
#
Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	017
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	666679dfde71f098b0f607c49df69a38
BuildRequires:	dbus-devel >= 0.20
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	dbus >= 0.20-2
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
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description initrd
A userspace implementation of devfs - static binary for initrd.

%prep
%setup -q

%build
%if %{with initrd}
%{__make} \
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

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initdir=%{_initrddir} \
	USE_DBUS=true

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
%doc ChangeLog FAQ README TODO
%doc docs/{overview,udev_vs_devfs,libsysfs.txt,udev-*.pdf}
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,root) %dir %{_sysconfdir}/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dbus*/system.d/*
%{_mandir}/man8/*

%if %{with initrd}
%exclude %{_sbindir}/udev-initrd

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/udev-initrd
%endif
