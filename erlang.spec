Summary:	OpenSource Erlang/OTP
Summary(pl):	Erlang/OTP z otwartymi ¼ród³ami
Name:		otp
Version:	R9C_2
Release:	0.1
Epoch:		1
License:	distributable
Group:		Development/Languages
%define		_version	%(echo %{version} | tr _ -)
Source0:	http://www.erlang.org/download/%{name}_src_%{_version}.tar.gz
URL:		http://www.erlang.org/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	flex
BuildRequires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Erlang is a programming language designed at the Ericsson Computer
Science Laboratory. Open-source Erlang is being released to help
encourage the spread of Erlang outside Ericsson.

%description -l pl
Erlang to jêzyk programowania opracowany w Ericsson Computer Science
Laboratory. Open-source Erlang zosta³ wydany, aby pomóc w
rozpowszechnianiu Erlanga poza Ericssonem.

%prep
%setup -q -n %{name}_src_%{_version}

%build
%{__autoconf}
cd lib
%{__autoconf}
cd erl_interface
%{__autoconf}
cd ../gs
%{__autoconf}
cd ../megaco
%{__autoconf}
cd ../snmp
%{__autoconf}
cd ../../erts/
%{__autoconf}
cd ..
%configure
ERL_TOP=`pwd`; export ERL_TOP
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
