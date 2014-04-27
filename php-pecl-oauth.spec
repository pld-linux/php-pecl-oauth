%define		php_name	php%{?php_suffix}
%define		modname	oauth
%define		status	stable
Summary:	%{modname} - consumer extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie klienckie
Name:		%{php_name}-pecl-%{modname}
Version:	1.2.3
Release:	4
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	99838d9a04b78058c7360dfd69c8593b
URL:		http://pecl.php.net/package/oauth/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	%{php_name}-hash
Requires:	php(core) >= 5.0.4
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OAuth is an authorization protocol built on top of HTTP which allows
applications to securely access data without having to store usernames
and passwords.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
OAuth to protokół autoryzacji zbudowany na bazie HTTP pozwalający
aplikacjom na bezpieczny dosŧęp do danych bez potrzeby przechowywania
nazw użytkownika czy haseł.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
find -newer LICENSE -o -print | xargs touch --reference %{SOURCE0}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc LICENSE
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}
