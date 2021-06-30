from aws_cdk import (
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_lambda as lambda_,
    core as cdk
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.


class ServerlessUsersDbStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self, id="users-store-30-6-2021", bucket_name="users-store-30-6-2021")

        handler = lambda_.Function(self, "user_db",
                                   runtime=lambda_.Runtime.PYTHON_3_7,
                                   code=lambda_.Code.from_asset('resources'),
                                   handler='lambda_handler',
                                   environment=dict(BUCKET=bucket.bucket_name)
                                   )
        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self, "user-db-api",
                                 rest_api_name="User Db",
                                 description="This is an API that outputs the data of all users registered.")
        get_api_integration = apigateway.LambdaIntegration(handler,
                                                           request_templates={'application/json': '{"statusCode": "200"}'})
        api.root.add_method("GET", get_api_integration)