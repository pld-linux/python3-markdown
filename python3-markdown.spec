#
# Conditional build:
%bcond_with	doc	# documentation
%bcond_without	tests	# unit tests

%define 	module	markdown
Summary:	Markdown implementation in Python 3
Summary(pl.UTF-8):	Implementacja formatu Markdown w Pythonie 3
Name:		python3-%{module}
Version:	3.3.3
Release:	2
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/markdown/
Source0:	https://files.pythonhosted.org/packages/source/M/Markdown/Markdown-%{version}.tar.gz
# Source0-md5:	034e3bccfde211d44b4a7a69cb290ba0
URL:		https://pypi.org/project/markdown/
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools >= 36.6
%if %{with tests}
BuildRequires:	python3-PyYAML
%if "%{py3_ver}" <= "3.8"
BuildRequires:	python3-importlib_metadata
%endif
%endif
%if %{with doc}
BuildRequires:	python3-mkdocs >= 1.0
BuildRequires:	python3-mkdocs-nature
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Conflicts:	python-markdown < 3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python 3 implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%description -l pl.UTF-8
Ten pakiet zawiera implementację formatu Markdown Johna Grubera w
Pythonie 3. Jest prawie całkowicie zgodna z implementacją wzorcową,
choć jest kilka znanych problemów.

%prep
%setup -q -n Markdown-%{version}

%build
%py3_build

%if %{with tests}
%{__python3} -m unittest discover tests
%endif

%if %{with doc}
mkdocs-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install
# rename binary
%{__mv} $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py3_ver}}
# default binary
ln -s markdown_py-%{py3_ver} $RPM_BUILD_ROOT%{_bindir}/markdown_py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md docs/{change_log,extensions,authors.md,cli.md,favicon.ico,index.md,py.png,reference.md}
%attr(755,root,root) %{_bindir}/markdown_py
%attr(755,root,root) %{_bindir}/markdown_py-%{py3_ver}
%{py3_sitescriptdir}/markdown
%{py3_sitescriptdir}/Markdown-%{version}-py*.egg-info
