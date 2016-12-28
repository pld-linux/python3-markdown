#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2	# python2 package
%bcond_without	python3	# python3 package

%define 	module	markdown
Summary:	Markdown implementation in Python 2
Summary(pl.UTF-8):	Implementacja formatu Markdown w Pythonie 2
Name:		python-%{module}
Version:	2.6.7
Release:	2
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/simple/markdown/
Source0:	https://files.pythonhosted.org/packages/source/M/Markdown/Markdown-%{version}.tar.gz
# Source0-md5:	a06f1c5d462b32e0e8da014e9eebb0d9
URL:		https://pythonhosted.org/Markdown/
BuildRequires:	python-devel
BuildRequires:	python-elementtree
%if %{with tests}
BuildRequires:	python-PyYAML
BuildRequires:	python-nose
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
%if %{with tests}
BuildRequires:	python3-PyYAML
BuildRequires:	python3-nose
%endif
%endif
Requires:	python-elementtree
Provides:	python-Markdown = %{version}-%{release}
Obsoletes:	python-Markdown = 2.2.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python 2 implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%description -l pl.UTF-8
Ten pakiet zawiera implementację formatu Markdown Johna Grubera w
Pythonie 2. Jest prawie całkowicie zgodna z implementacją wzorcową,
choć jest kilka znanych problemów.

%package -n python3-markdown
Summary:	Markdown implementation in Python 3
Summary(pl.UTF-8):	Implementacja formatu Markdown w Pythonie 3
Group:		Development/Languages/Python

%description -n python3-markdown
This is a Python 3 implementation of John Gruber's Markdown. It is
almost completely compliant with the reference implementation, though
there are a few known issues.

%description -n python3-markdown -l pl.UTF-8
Ten pakiet zawiera implementację formatu Markdown Johna Grubera w
Pythonie 3. Jest prawie całkowicie zgodna z implementacją wzorcową,
choć jest kilka znanych problemów.

%prep
%setup -q -n Markdown-%{version}

# remove shebangs
find markdown -type f -name '*.py' -exec sed -i -e '/^#!/{1D}' {} ';'

# fix line-ending
%undos docs/release-2.2.0.txt

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} ./run-tests.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} ./run-tests.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install
# rename binary
%{__mv} $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py3_ver}}
%endif

%if %{with python2}
%py_install
%py_postclean
# rename binary
%{__mv} $RPM_BUILD_ROOT%{_bindir}/markdown_py{,-%{py_ver}}
# 2.X binary is called by default for now
ln -s markdown_py-%{py_ver} $RPM_BUILD_ROOT%{_bindir}/markdown_py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md docs/{authors.txt,change_log.txt,cli.txt,index.txt,reference.txt,release-*.txt,siteindex.txt,extensions}
%attr(755,root,root) %{_bindir}/markdown_py
%attr(755,root,root) %{_bindir}/markdown_py-%{py_ver}
%{py_sitescriptdir}/markdown
%{py_sitescriptdir}/Markdown-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-markdown
%defattr(644,root,root,755)
%doc LICENSE.md README.md docs/{authors.txt,change_log.txt,cli.txt,index.txt,reference.txt,release-*.txt,siteindex.txt,extensions}
%attr(755,root,root) %{_bindir}/markdown_py-%{py3_ver}
%{py3_sitescriptdir}/markdown
%{py3_sitescriptdir}/Markdown-%{version}-py*.egg-info
%endif
