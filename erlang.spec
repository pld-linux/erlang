# NOTE: Building requires working DNS setup. Build may hang
#       even if _only_ first dns specified in resolv.conf
#       is unreachable.
# TODO
# - separate -devel (at least header files!)
# - modularize (odbc, etc)
# - manuals to %{_mandir}
# - investigate fPIC.patch
#
# Conditional build:
%bcond_with	java		# Java support
%bcond_without	odbc		# unixODBC support
%bcond_without	doc		# documentation
%bcond_without	systemd		# systemd support
%bcond_without	wx		# wxWidgets GUI (observer, debugger, et)
#

%define		otp		%(echo %version | cut -f1 -d.)
%define		erts_version	17.1.1

Summary:	OpenSource Erlang/OTP
Summary(pl.UTF-8):	Erlang/OTP z otwartymi źródłami
Name:		erlang
Version:	29.1.2
Release:	2
Epoch:		2
%define		_version	%(echo %{version} | tr _ -)
License:	Apache v2.0
Group:		Development/Languages
Source0:	https://github.com/erlang/otp/archive/OTP-%{version}.tar.gz
# Source0-md5:	5ee3e77d6badc04dbd8e96dcf53ede5f
Source2:	epmd.service
Source3:	epmd.socket
Source4:	epmd@.service
Source5:	epmd@.socket
Patch0:		%{name}-fPIC.patch
Patch1:		x32.patch
Patch3:		%{name}-ac.patch
URL:		http://www.erlang.org/
%{?with_java:BuildRequires:	/usr/bin/jar}
BuildRequires:	autoconf >= 2.69
%{?with_doc:BuildRequires:	ex_doc >= 0.40.4}
BuildRequires:	flex
%{?with_java:BuildRequires:	jdk >= 1.2}
%{?with_wx:BuildRequires:	OpenGL-GLU-devel}
%{?with_wx:BuildRequires:	OpenGL-devel}
BuildRequires:	libsctp-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	perl-base
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.007
%{?with_systemd:BuildRequires:	systemd-devel}
%if %{with wx}
BuildRequires:	wxGTK3-unicode-devel >= 1:3.0.2
BuildRequires:	wxGTK3-unicode-gl-devel >= 1:3.0.2
%endif
BuildRequires:	zlib-devel
BuildRequires:	zstd-static >= 1.5.6
%if %{with odbc}
BuildRequires:	unixODBC-devel
%else
BuildConflicts:	unixODBC-devel
%endif
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
%{?with_systemd:Requires:	systemd-units >= 38}
# dynamically loaded libsctp.so.1
Suggests:	libsctp
Provides:	erlang(OTP) = %otp
Provides:	erlang(OTP) = %{lua:print(macros.otp - 1)}
Provides:	erlang(OTP) = %{lua:print(macros.otp - 2)}
Provides:	group(epmd)
Provides:	user(epmd)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _erl_target %(echo %{_build}%{?_gnu} | sed -e's/amd64/x86_64/;s/athlon/i686/;s/ppc/powerpc/;s/x32/x86_64/')

%description
Erlang is a programming language designed at the Ericsson Computer
Science Laboratory. Open-source Erlang is being released to help
encourage the spread of Erlang outside Ericsson.

%description -l pl.UTF-8
Erlang to język programowania opracowany w Ericsson Computer Science
Laboratory. Open-source Erlang został wydany, aby pomóc w
rozpowszechnianiu Erlanga poza Ericssonem.

%package debugger
Summary:	Erlang debugger
Summary(pl.UTF-8):	Debugger dla Erlanga
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-wx = %{epoch}:%{version}-%{release}

%description debugger
Graphical debugger for Erlang programs.

%description debugger -l pl.UTF-8
Graficzny debugger dla programów w Erlangu.

%package et
Summary:	Erlang Event Tracer
Summary(pl.UTF-8):	Event Tracer dla Erlanga
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-wx = %{epoch}:%{version}-%{release}

%description et
Event Tracer (ET) for recording and graphical presentation of Erlang
events.

%description et -l pl.UTF-8
Event Tracer (ET) do rejestrowania i graficznej prezentacji zdarzeń
w Erlangu.

%package observer
Summary:	Erlang system observer
Summary(pl.UTF-8):	Narzędzie do obserwacji systemów w Erlangu
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-et = %{epoch}:%{version}-%{release}
Requires:	%{name}-wx = %{epoch}:%{version}-%{release}

%description observer
Graphical tool for observing characteristics of Erlang systems, with
crashdump viewer, etop and trace tool builder (ttb).

%description observer -l pl.UTF-8
Graficzne narzędzie do obserwacji systemów w Erlangu, wraz z
przeglądarką zrzutów awaryjnych, etop i ttb.

%package reltool
Summary:	Erlang release management tool
Summary(pl.UTF-8):	Narzędzie do zarządzania wydaniami w Erlangu
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	%{name}-wx = %{epoch}:%{version}-%{release}

%description reltool
Release management tool for Erlang/OTP with graphical frontend.

%description reltool -l pl.UTF-8
Narzędzie do zarządzania wydaniami Erlang/OTP z interfejsem
graficznym.

%package wx
Summary:	wxWidgets binding for Erlang
Summary(pl.UTF-8):	Wiązanie wxWidgets dla Erlanga
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description wx
wxWidgets GUI library binding for Erlang.

%description wx -l pl.UTF-8
Wiązanie biblioteki graficznej wxWidgets dla Erlanga.

%package doc
Summary:	Erlang documentation
Summary(pl.UTF-8):	Dokumentacja do Erlanga
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description doc
Erlang documentation.

%description doc -l pl.UTF-8
Dokumentacja do Erlanga.

%prep
%setup -q -n otp-OTP-%{_version}
#%%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1

%build
./otp_build update_configure --no-commit

# --without-wx breaks the build of debugger, observer and et (they need the wx
# beams), so without wx only wx-config is hidden and the wx driver is skipped
%configure \
%ifarch %{ix86}
%ifnarch %{x86_with_sse2}
	ac_cv_sizeof__Float16=0 \
%endif
%endif
%ifarch sparc
	CFLAGS="%{rpmcflags} -mv8plus" \
%endif
%if %{with wx}
	WX_CONFIG_NAME=%{_bindir}/wx-gtk3-unicode-config \
%else
	ac_cv_path_WX_CONFIG_PATH=no \
%endif
	--disable-builtin-zlib \
	--disable-builtin-zstd \
	--disable-silent-rules \
	%{__enable_disable systemd} \
	--with-javac%{!?with_java:=no} \
	--with-ssl-lib-subdir=%{_lib} \
	%{?with_odbc:--with-odbc} \
	%{?with_wx:--with-wx}

rm -f lib/ssl/SKIP
ERL_TOP=`pwd`; export ERL_TOP
# lib/odbc builds odbcserver only when ODBC_CAN_BUILD_DRIVER is set in make's
# environment, configure does not export it: https://github.com/erlang/otp/issues/11705
 %{__make} -j1 \
	TARGET="%{_erl_target}" \
	%{?with_odbc:ODBC_CAN_BUILD_DRIVER=true} \
	|| { find . -name erl_crash.dump | xargs cat ; exit 1 ; }

%if %{with doc}
LC_ALL=C.UTF-8 \
%{__make} -j1 docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	TARGET="%{_erl_target}" \
	%{?with_odbc:ODBC_CAN_BUILD_DRIVER=true} \
	INSTALL_PREFIX=$RPM_BUILD_ROOT

%if %{with doc}
env ERL_LIBS="$RPM_BUILD_ROOT%{_libdir}/erlang/lib" \
	%{__make} install-docs \
		DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with systemd}
install -D -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/epmd.service
install -D -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/epmd.socket
install -D -p %{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/epmd@.service
install -D -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/epmd@.socket
%endif

%{__sed} -i -e"s#$RPM_BUILD_ROOT##" \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/bin/{erl,start,start_erl}

%{__sed} -i -e '1s,/usr/bin/env escript,/usr/bin/escript,' \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/lib/diameter-*/bin/diameterc \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/lib/edoc-*/bin/edoc \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/lib/snmp-*/bin/snmpc \
	$RPM_BUILD_ROOT%{_libdir}/%{name}/lib/snmp-*/src/compiler/snmpc.src

#cp -r man $RPM_BUILD_ROOT%{_libdir}/%{name}
#find $RPM_BUILD_ROOT%{_libdir}/%{name}/man -type f | xargs gzip -9

# some files in the library need +x, so we build the list here
echo "%%defattr(644,root,root,755)" > lib.list
find $RPM_BUILD_ROOT%{_libdir}/%{name}/lib -type d \
	| %{__sed} -e"s#^$RPM_BUILD_ROOT%{_libdir}/%{name}/#%%dir %%{_libdir}/%%{name}/#" >> lib.list
find $RPM_BUILD_ROOT%{_libdir}/%{name}/lib -type f -perm -500 \
	| %{__sed} -e"s#^$RPM_BUILD_ROOT%{_libdir}/%{name}/#%%attr(755,root,root) %%{_libdir}/%%{name}/#" >> lib.list
find $RPM_BUILD_ROOT%{_libdir}/%{name}/lib -type f '!' -perm -500 \
	| %{__sed} -e"s#^$RPM_BUILD_ROOT%{_libdir}/%{name}/#%%{_libdir}/%%{name}/#" >> lib.list
for app in debugger et observer reltool wx; do
	%{__grep} "/lib/$app-[0-9]" lib.list > $app.list
	%{__grep} -v "/lib/$app-[0-9]" lib.list > lib.list.tmp
	%{__mv} lib.list.tmp lib.list
done

%if %{with doc}
# Move noarch docs to _datadir
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/erts-%{erts_version}
%{__mv} $RPM_BUILD_ROOT{%{_libdir},%{_datadir}}/%{name}/doc
%{__ln} -s %{_datadir}/%{name}/doc $RPM_BUILD_ROOT%{_libdir}/%{name}/doc
%{__mv} $RPM_BUILD_ROOT{%{_libdir},%{_datadir}}/%{name}/erts-%{erts_version}/doc
%{__ln} -s %{_datadir}/%{name}/erts-%{erts_version}/doc $RPM_BUILD_ROOT%{_libdir}/%{name}/erts-%{erts_version}/doc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 352 epmd
%useradd -u 352 -r -d /usr/share/empty -s /bin/false -c "Erlang Port Mapper Daemon User" -g epmd epmd

%post
%if %{with systemd}
%systemd_post epmd.service
%endif

%preun
%if %{with systemd}
%systemd_preun epmd.service
%endif

%postun
if [ "$1" = "0" ]; then
	%userremove epmd
	%groupremove epmd
fi
%if %{with systemd}
%systemd_reload
%endif

%files -f lib.list
%defattr(644,root,root,755)
%doc AUTHORS README.md SECURITY
%attr(755,root,root) %{_bindir}/ct_run
%attr(755,root,root) %{_bindir}/dialyzer
%attr(755,root,root) %{_bindir}/epmd
%attr(755,root,root) %{_bindir}/erl
%attr(755,root,root) %{_bindir}/erlc
%attr(755,root,root) %{_bindir}/escript
%attr(755,root,root) %{_bindir}/run_erl
%attr(755,root,root) %{_bindir}/to_erl
%attr(755,root,root) %{_bindir}/typer
%dir %{_libdir}/erlang
%dir %{_libdir}/%{name}/bin
%attr(755,root,root) %{_libdir}/%{name}/bin/ct_run
%attr(755,root,root) %{_libdir}/%{name}/bin/dialyzer
%attr(755,root,root) %{_libdir}/%{name}/bin/epmd
%attr(755,root,root) %{_libdir}/%{name}/bin/erl
%attr(755,root,root) %{_libdir}/%{name}/bin/erl_call
%attr(755,root,root) %{_libdir}/%{name}/bin/erlc
%attr(755,root,root) %{_libdir}/%{name}/bin/escript
%attr(755,root,root) %{_libdir}/%{name}/bin/no_dot_erlang.boot
%attr(755,root,root) %{_libdir}/%{name}/bin/run_erl
%attr(755,root,root) %{_libdir}/%{name}/bin/start
%attr(755,root,root) %{_libdir}/%{name}/bin/start_erl
%attr(755,root,root) %{_libdir}/%{name}/bin/to_erl
%attr(755,root,root) %{_libdir}/%{name}/bin/typer
%{_libdir}/%{name}/bin/start*.*
%dir %{_libdir}/%{name}/erts-%{erts_version}
%{_libdir}/%{name}/erts-%{erts_version}/man
%{_libdir}/%{name}/erts-%{erts_version}/src
%{_libdir}/%{name}/erts-%{erts_version}/include
%dir %{_libdir}/%{name}/erts-%{erts_version}/lib
%dir %{_libdir}/%{name}/erts-%{erts_version}/lib/internal
%{_libdir}/%{name}/erts-%{erts_version}/lib/internal/liberts_internal*.a
%{_libdir}/%{name}/erts-%{erts_version}/lib/internal/libethread.a
%{_libdir}/%{name}/erts-%{erts_version}/lib/internal/README
#%{_libdir}/%{name}/erts-%{erts_version}/*.ear
%dir %{_libdir}/%{name}/erts-%{erts_version}/bin
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/beam*
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/ct_run
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/dialyzer
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/e*
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/heart*
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/inet_gethost
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/run_erl
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/start
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/to_erl
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/typer
%attr(755,root,root) %{_libdir}/%{name}/erts-%{erts_version}/bin/yielding_c_fun
%{_libdir}/%{name}/erts-%{erts_version}/bin/start*.*
# (file list dynamically generated) %{_libdir}/%{name}/lib
%dir %{_libdir}/%{name}/misc
%attr(755,root,root) %{_libdir}/%{name}/misc/*
%{_libdir}/%{name}/releases
%{_libdir}/%{name}/usr
%if %{with doc}
%doc %{_libdir}/%{name}/man
%endif
%attr(755,root,root) %{_libdir}/%{name}/Install

%if %{with doc}
%{_libdir}/%{name}/doc
%endif
%{_libdir}/%{name}/erts-%{erts_version}/doc

%if %{with systemd}
%{systemdunitdir}/epmd.service
%{systemdunitdir}/epmd.socket
%{systemdunitdir}/epmd@.service
%{systemdunitdir}/epmd@.socket
%endif

%files debugger -f debugger.list
%defattr(644,root,root,755)

%files et -f et.list
%defattr(644,root,root,755)

%files observer -f observer.list
%defattr(644,root,root,755)

%files reltool -f reltool.list
%defattr(644,root,root,755)

%files wx -f wx.list
%defattr(644,root,root,755)

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/erts-%{erts_version}
%{_datadir}/%{name}/doc
%{_datadir}/%{name}/erts-%{erts_version}/doc
%endif
