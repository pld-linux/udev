Summary:	A userspace implementation of devfs
Summary(pl):	Implementacja devfs w przestrzeni u¿ytkownika
Name:		udev
Version:	008
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/kernel/hotplug/%{name}-%{version}.tar.bz2
# Source0-md5:	3d5662c7e2f2ad4277e18e3551b85166
BuildRequires:	glibc-static
BuildRequires:	sed >= 4.0
Requires:	coreutils
Requires:	hotplug >= 2003_08_05
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A userspace implementation of devfs for 2.5 and higher kernels.

%description -l pl
Implementacja devfs w przestrzeni u¿ytkownika dla j±der 2.5 i
wy¿szych.

%prep
%setup -q

%build
%{__make} \
	udevdir=/dev \
	CC="%{__cc}" \
	%{!?debug:DEBUG=false} \
	OPTIMIZATION="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/{udev,hotplug.d/default}}

install udev $RPM_BUILD_ROOT%{_sbindir}
install udev.conf udev.permissions udev.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev
install udev.8 $RPM_BUILD_ROOT%{_mandir}/man8

ln -s /sbin/udev $RPM_BUILD_ROOT/etc/hotplug.d/default/udev.hotplug

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ README TODO docs/{overview,udev-*.pdf}
%attr(750,root,root) %dir %{_sysconfdir}/udev
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/udev/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_sysconfdir}/hotplug.d/default/*.hotplug
%{_mandir}/man8/udev.8*
