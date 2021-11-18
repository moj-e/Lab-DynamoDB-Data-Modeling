import boto3

def create_table(
        ddb_table_name,
        partition_key,
        sort_key
    ):

    dynamodb = boto3.resource('dynamodb')
    
    table_name = ddb_table_name
    
    attribute_definitions = [
        { 'AttributeName' : partition_key, 'AttributeType' : 'S' },
        { 'AttributeName' : sort_key, 'AttributeType' : 'S' },
        { 'AttributeName' : 'status', 'AttributeType' : 'S' },
        { 'AttributeName' : 'sd', 'AttributeType' : 'S' }
        ]
    
    key_schema = [
        { 'AttributeName' : partition_key, 'KeyType': 'HASH' }, 
        { 'AttributeName' : sort_key, 'KeyType': 'RANGE' }
        ]
                  
    provisioned_throughput = { 'ReadCapacityUnits' : 5, 'WriteCapacityUnits' : 10 }
    
    global_secondary_indexes = [{
            'IndexName' : 'status_gsi',
            'KeySchema' : [
                { 'AttributeName' : 'status', 'KeyType' : 'HASH' },
                { 'AttributeName' : partition_key, 'KeyType' : 'RANGE' }
                ],
            'Projection' : { 'ProjectionType' : 'INCLUDE',
                           'NonKeyAttributes' : [ sort_key, 'address' ]
            },
            'ProvisionedThroughput' : { 'ReadCapacityUnits' : 5, 'WriteCapacityUnits' : 10 }
    },
    {
            'IndexName': 'inverted-index',
            'KeySchema': [
                {'AttributeName': sort_key, 'KeyType': 'HASH'},
                {'AttributeName': partition_key, 'KeyType': 'RANGE'}],
            'Projection': {'ProjectionType': 'INCLUDE',
                           'NonKeyAttributes': ['quantity',	'price', 'status', 'product_name']
            },
            'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
    }
    ]
    
    local_secondary_indexes = [{
            'IndexName' : 'sd_lsi',
            'KeySchema' : [
                { 'AttributeName' : partition_key, 'KeyType' : 'HASH' },
                { 'AttributeName' : 'sd', 'KeyType' : 'RANGE' }
                ],
            'Projection' : { 'ProjectionType' : 'INCLUDE',
                           'NonKeyAttributes' : [ sort_key, 'address', 'date' ]
            }
    }]
    
    try:
        table = dynamodb.create_table(TableName = table_name,
                                      KeySchema = key_schema,
                                      AttributeDefinitions = attribute_definitions,
                                      ProvisionedThroughput = provisioned_throughput,
                                      GlobalSecondaryIndexes = global_secondary_indexes,
                                      LocalSecondaryIndexes = local_secondary_indexes
                                      )
        return table
    except Exception as err:
        print("{0} Table could not be created".format(table_name))
        print("Error message {0}".format(err))
        

if __name__ == '__main__':
    table = create_table("users-orders-items", "pk", "sk")