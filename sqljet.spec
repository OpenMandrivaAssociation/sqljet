Name:           sqljet
Version:        1.0.4
Release:        4
Summary:        Pure Java SQLite

Group:          Development/Java
License:        GPLv2
URL:            http://sqljet.com/
# Obtained by sh fetch-sqljet.sh
Source0:        %{name}-%{version}.tar.xz
Source1:        fetch-sqljet.sh
Source2:        %{name}-browser.sh
Source3:        %{name}-browser.desktop
Patch0:         %{name}-javadoc.patch

BuildRequires:  ant
BuildRequires:  antlr
BuildRequires:  antlr3-java
BuildRequires:  antlr3-tool
BuildRequires:  easymock2
BuildRequires:  netbeans-platform
BuildRequires:  java-devel >= 1.6
BuildRequires:  junit4
BuildRequires:  desktop-file-utils
Requires:       antlr3-java
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils
BuildArch: noarch

%description
SQLJet is an independent pure Java implementation of a popular SQLite database
management system. SQLJet is a software library that provides API that enables
Java application to read and modify SQLite databases.

%package        browser
Group:          Development/Java
Summary:        SQLJet database browser
Requires:       %{name} = %{version}
Requires:       netbeans-platform

%description    browser
Utility for browsing SQLJet/SQLite databases.

%package        javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description    javadoc
API documentation for %{name}.

%prep
%setup -q
%patch0

find \( -name '*.class' -o -name '*.jar' \) -delete

pushd lib
ln -s %{_javadir}/antlr3-runtime.jar antlr-runtime-3.1.3.jar
popd
pushd sqljet-examples/browser/lib
ln -s %{_datadir}/netbeans/platform12/modules/org-netbeans-swing-outline.jar org-netbeans-swing-outline.jar
popd

# versions in pom xml are to be processed by ant, but we don't need that so just fix them here
sed -i 's/%sqljet.version%/%{version}/;s/%antlr.version%/3.1.3/' pom.xml

%build
export CLASSPATH=$(build-classpath antlr3-runtime antlr3 antlr stringtemplate easymock2 junit4)

ant jars osgi javadoc

jar umf sqljet/osgi/MANIFEST.MF build/sqljet.jar

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p  build/sqljet.jar %{buildroot}%{_javadir}/%{name}.jar
cp -p  build/sqljet-browser.jar  %{buildroot}%{_javadir}/%{name}-browser.jar

# maven metadata
mkdir -p %{buildroot}%{_mavenpomdir}
cp pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap org.tmatesoft.sqljet %{name} %{version} JPP %{name}

# javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp build/javadoc %{buildroot}%{_javadocdir}/%{name}

# browser scripts
install -d %{buildroot}%{_bindir}
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/%{name}-browser

desktop-file-install  --dir=%{buildroot}%{_datadir}/applications \
                      %{SOURCE3}

desktop-file-validate %{buildroot}/%{_datadir}/applications/sqljet-browser.desktop

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP-%{name}.pom
%doc COPYING README.txt
%{_javadir}/%{name}.jar

%files browser
%defattr(-,root,root,-)
%{_javadir}/%{name}-browser.jar
%{_bindir}/%{name}-browser
%{_datadir}/applications/%{name}-browser.desktop

%files javadoc
%defattr(-,root,root,-)
%doc COPYING
%doc %{_javadocdir}/*

