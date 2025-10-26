#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_without	tests		# unit tests
%bcond_with	tests_net	# functional tests, localhost networking required

Summary:	Very fast asynchronous FTP server library for Python
Summary(pl.UTF-8):	Bardzo szybka biblioteka asynchronicznego serwera FTP dla Pythona
Name:		python3-pyftpdlib
Version:	2.1.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pyftpdlib/
Source0:	https://files.pythonhosted.org/packages/source/p/pyftpdlib/pyftpdlib-%{version}.tar.gz
# Source0-md5:	68632ce84491dfc2d2a4cc1426fd4d14
URL:		https://github.com/giampaolo/pyftpdlib/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pyOpenSSL
%if "%{py3_ver}" >= "3.12"
BuildRequires:	python3-pyasynchat
BuildRequires:	python3-pyasyncore
%endif
BuildRequires:	python3-pytest
#BuildRequires:	python3-pytest-instafail
#BuildRequires:	python3-pytest-xdist
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
Suggests:	python3-pyOpenSSL
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python FTP server library provides a high-level portable interface to
easily write very efficient, scalable and asynchronous FTP servers
with Python. It is the most complete RFC-959 FTP server implementation
available for Python programming language.

%description -l pl.UTF-8
Biblioteka serwera FTP dla Pythona udostępnia wysokopoziomowy,
przenośny interfejs do łatwego tworzenia bardzo wydajnych,
skalowalnych i asynchronicznych serwerów FTP w Pythonie. Jest to
najpełniejsza implementacja serwera FTP wg RFC-959 dostępna dla tego
języka programowania.

%package apidocs
Summary:	API documentation for Python pyftpdlib module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pyftpdlib
Group:		Documentation

%description apidocs
API documentation for Python pyftpdlib module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pyftpdlib.

%prep
%setup -q -n pyftpdlib-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests \
%if %{without tests_net}
	--ignore tests/test_functional.py \
	--ignore tests/test_functional_ssl.py \
	--ignore tests/test_servers.py
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install
%{__rm} $RPM_BUILD_ROOT%{_bindir}/ftpbench

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}
%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	$RPM_BUILD_ROOT%{_examplesdir}/python3-pyftpdlib-%{version}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst LICENSE README.rst
%{py3_sitescriptdir}/pyftpdlib
%{py3_sitescriptdir}/pyftpdlib-%{version}-py*.egg-info
%{_examplesdir}/python3-pyftpdlib-%{version}

%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
