module pylumiconnector

go 1.15

require (
	github.com/pulumi/pulumi/sdk/v2 v2.12.0
	github.com/cfeenstra67/pylumi/go/pylumi v1.2.0
)

replace github.com/cfeenstra67/pylumi/go/pylumi => ./pylumi
