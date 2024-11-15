.PHONY: all
.PHONY: bundle
.PHONY: package

VER := $(shell grep -m 1 '<version>' pom.xml | perl -pe 's/[^0-9.]+//g')
ZIPFILE = uklatn-$(VER).zip

all: bundle

test:
	@mvn test

package:
	@mvn clean deploy -DaltDeploymentRepository=local::file:./target/staging-deploy
	@cd ./target/staging-deploy/ ; find . | zip $(ZIPFILE) -@

bundle: package
	@cp ./target/staging-deploy/$(ZIPFILE) ./
