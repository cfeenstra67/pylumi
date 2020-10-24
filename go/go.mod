module pylumiconnector

go 1.15

require (
	github.com/pulumi/pulumi/sdk/v2 v2.12.0
	pylumi v0.0.1
)

replace pylumi => ./pylumi
