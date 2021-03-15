import * as pulumi from "@pulumi/pulumi"
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import {FileArchive} from "@pulumi/pulumi/asset";

const STACK = pulumi.getStack()
const config = new pulumi.Config()

const clock_entries_table = new aws.dynamodb.Table(`${STACK}-clock-entries`, {
    name: "clock_entries",
    attributes: [
        {
            name: "chat_id",
            type: "S"
        },
        {
            name: "date",
            type: "S"
        }
    ],
    billingMode: "PROVISIONED",
    hashKey: "chat_id",
    rangeKey: "date",
    readCapacity: 15,
    writeCapacity: 15,
    ttl: {
        enabled: true,
        attributeName: "ttl"
    }
})


const user_info_table = new aws.dynamodb.Table(`${STACK}-user-info`, {
    name: "user_info",
    attributes: [
        {
            name: "chat_id",
            type: "S"
        }
    ],
    billingMode: "PROVISIONED",
    hashKey: "chat_id",
    readCapacity: 10,
    writeCapacity: 10,
})


const role = new aws.iam.Role(`${STACK}-bot-role`, {
    path: `/time-tracking-bot/${STACK}/`,
    assumeRolePolicy: `{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
`,
})


const policy = new aws.iam.Policy(`${STACK}-bot-dynamo-logs-policy`, {
    description: "Allow the bot to Read/Write items to DynamoDB and log events to Cloud Watch",
    path: `/time-tracking-bot/${STACK}/`,
    policy: pulumi.interpolate`{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:UpdateItem",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:884445114654:table/clock_entries",
                "arn:aws:dynamodb:us-east-1:884445114654:table/user_info",
                "arn:aws:logs:us-east-1:884445114654:*"
            ]
        }
    ]
}`
})


const attachment = new aws.iam.RolePolicyAttachment(`${STACK}-bot-policy-attachment`, {
    policyArn: policy.arn,
    role: role.name
})


const lambda = new aws.lambda.Function(`${STACK}-bot-lambda`, {
    code: new FileArchive('./bot_files/deployment.zip'),
    environment: {
        variables: {
            CLOCK_ENTRIES_TABLE: "clock_entries",
            USER_INFO_TABLE: "user_info",
            GOOGLEMAPS_TOKEN: config.getSecret("GOOGLEMAPS_TOKEN") || "",
            TELEGRAM_TOKEN: config.getSecret("TELEGRAM_TOKEN") || "",
            TTL: "5356800",
        }
    },
    handler: "lambda_handler.lambda_handler",
    runtime: "python3.8",
    role: role.arn,
})


const apiGateway = new awsx.apigateway.API(`${STACK}-bot-api`, {
    routes: [
        {
            path: "/time-tracking-bot",
            method: "POST",
            eventHandler: lambda,
        }
    ],
})


export const apiUrl = pulumi.interpolate`${apiGateway.url}time-tracking-bot`
