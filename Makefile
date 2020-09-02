src := SPECS/sshguard-firewalld.spec SOURCES/* $(MAKEFILE_LIST)

all: RPMS/x86_64/sshguard-firewalld-1.7.1-1.el7.x86_64.rpm
RPMS/x86_64/sshguard-firewalld-1.7.1-1.el7.x86_64.rpm: $(src)
	rpmbuild -ba $< --define "_topdir $$(pwd)" --define "debug_package %{nil}"

clean:
	-rm -rf BUILD BUILDROOT

distclean: clean
	-rm -rf RPMS SRPMS
