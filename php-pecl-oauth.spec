%define		modname	oauth
%define		status	stable
Summary:	%{modname} - consumer extension
Summary(pl.UTF-8):	%{modname} - rozszerzenie klienckie
Name:		php-pecl-%{modname}
Version:	1.1.0
Release:	1
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	26359ba5f04848e725a97c9aef9713b6
URL:		http://pecl.php.net/package/oauth/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Requires:	php-hash
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

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
