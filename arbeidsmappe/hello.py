import boto3
import json
from decimal import Decimal


def hello(event, context):
    print("Hei Folkens!")


def load_inventory(event, context):
    s3_client = boto3.client("s3")
    dynamodb_resource = boto3.resource("dynamodb", region_name="eu-west-1")
    inventory_table = dynamodb_resource.Table("kulegruppa-table")
    recordEvent = event["Records"][0]["s3"]
    bucket = recordEvent["bucket"]["name"]
    file = recordEvent["object"]["key"]
    raw_content = s3_client.get_object(Bucket=bucket, Key=file)["Body"].read()
    content = json.loads(raw_content)
    for item in content:
        item["id"] = item["type"] + "-" + item["name"]
        inventory_items = inventory_table.get_item(Key={"id": item["id"]})
        if "Item" in inventory_items:
            inventory_table.update_item(
                Key={"id": item["id"]},
                UpdateExpression="set quantity = quantity + :val",
                ExpressionAttributeValues={":val": Decimal(str(item["quantity"]))},
            )
        else:
            inventory_table.put_item(Item=item)
    print("Bucket:", bucket, "\nFile:", file, "\nContent:", content)
    return {
        "statusCode": 200,
        "body": "success",
    }


if __name__ == "__main__":
    hello()
    load_inventory()
