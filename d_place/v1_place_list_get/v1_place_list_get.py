import json
import logging

from common.pg_util import pg_util, to_dict_by_relations
from common.response_handler import ResponseHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


@ResponseHandler.api
def lambda_handler(event, context):
    select_all_places_query = f'''
        SELECT
            place.id, 
            place.name, 
            place."zipCode", 
            place.address, 
            place.latitude, 
            place.longitude, 
            place.tags as tags,
            franchise.id as franchise_id, 
            franchise.name as franchise_name,
            franchise."colorImgUrl" as "franchise_colorImgUrl",
            franchise."darkImgUrl" as "franchise_darkImgUrl",
            franchise.tags as franchise_tags
        FROM place
            LEFT JOIN franchise  
                ON place."franchiseId" = franchise.id;
    '''

    rows = pg_util.execute_query(select_all_places_query)
    return list(map(lambda x: to_dict_by_relations(x, relation_table="franchise"), rows))


if __name__ == '__main__':
    print(lambda_handler({}, {}))
