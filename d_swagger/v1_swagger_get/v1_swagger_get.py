import json
import logging
import os

from common.Json import Json
from common.const import ConstAWS, ConstHttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


def lambda_handler(event, context):
    swagger_html_string = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <meta
        name="description"
        content="SwaggerIU"
      />
      <title>SwaggerUI</title>
      <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.4.1/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist@4.4.1/swagger-ui-bundle.js" crossorigin></script>
      <script src="https://unpkg.com/swagger-ui-dist@4.4.1/swagger-ui-standalone-preset.js" crossorigin></script>
      <script>
        window.onload = () => {
          window.ui = SwaggerUIBundle({
            url: 'https://monter-asset.s3.ap-northeast-2.amazonaws.com/openapi.yaml',
            dom_id: '#swagger-ui',
          });
        };
      </script>
    </body>
    </html>
    '''

    return {
        "statusCode": 200,
        "body": swagger_html_string,
        "headers": {
            'Content-Type': 'text/html',
        }
    }