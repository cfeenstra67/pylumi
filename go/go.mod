module _pylumi

go 1.15

require (
	github.com/blang/semver v3.5.1+incompatible
	github.com/cfeenstra67/pylumi/go/pylumi v1.3.0
	github.com/pulumi/pulumi/sdk/v3 v3.21.0
)

replace github.com/cfeenstra67/pylumi/go/pylumi => ./pylumi
