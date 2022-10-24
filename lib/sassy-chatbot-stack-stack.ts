import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Code, LayerVersion, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';
import { PythonFunction, PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha'
import { RemovalPolicy } from 'aws-cdk-lib';

export class SassyChatbotStackStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const runtime = lambda.Runtime.PYTHON_3_9;
    const timeout = cdk.Duration.seconds(3);
    const memorySize = 2048;

    const openAILayer = new PythonLayerVersion(this, 'openai-launchdarkly-layer', {
      removalPolicy: RemovalPolicy.DESTROY,
      entry: './openai-launchdarkly-layer',
      compatibleRuntimes: [Runtime.PYTHON_3_9]
    })

     new PythonFunction(this, "sass-bot-9000", {
      memorySize,
      timeout,
      runtime,
      description:
        "used to handle questions from the Sass Bot API",
      handler: 'handler',
      entry: './sassy-chatbot-function',
      layers: [openAILayer]
    });
  }
}
