.PHONY: all
.PHONY: clean
.PHONY: docs
.PHONY: package
.PHONY: test

all: package

clean:
	@dotnet clean
	@find . -type d -name target -or -name bin -or -name obj | xargs rm -r
	@find . -type d -name _site | xargs rm -r

test:
	@dotnet test

docs:
	@dotnet tool run docfx docfx.json

package:
	@dotnet pack --output target --configuration Release \
	--include-symbols --include-source

push:
	find target -type f -name '*.nupkg' | sort | head -n 1 | xargs -I % \
	dotnet nuget push % --source https://api.nuget.org/v3/index.json \
	--api-key $(API_KEY)
