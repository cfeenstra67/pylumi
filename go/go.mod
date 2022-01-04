module _pylumi

go 1.15

require (
	github.com/blang/semver v3.5.1+incompatible
	github.com/cfeenstra67/pylumi/go/pylumi v1.2.2
	github.com/pulumi/pulumi/sdk/v2 v2.12.0
)

replace github.com/cfeenstra67/pylumi/go/pylumi => ./pylumi
