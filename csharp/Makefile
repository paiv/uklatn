.PHONY: all
.PHONY: package

all: package

test:
	@dotnet test

package:
	@dotnet pack --include-symbols --include-source

push:
	@dotnet nuget push
