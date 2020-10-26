module pylumiconnector

go 1.15

require (
	github.com/pulumi/pulumi/sdk/v2 v2.12.0
	github.com/cfeenstra67/pylumi v0.0.4
)

replace github.com/cfeenstra67/pylumi => ./pylumi
