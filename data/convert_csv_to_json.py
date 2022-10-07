import json
import csv


ADS_CSV = 'ad.csv'
ADS_JSON = 'ad.json'
ADS_MODEL_NAME = 'ads.ad'

CATEGORY_CSV = 'category.csv'
CATEGORY_JSON = 'category.json'
CATEGORY_MODEL_NAME = 'ads.category'

USER_CSV = 'user.csv'
USER_JSON = 'user.json'
USER_MODEL_NAME = 'users.user'

LOCATION_CSV = 'location.csv'
LOCATION_JSON = 'location.json'
LOCATION_MODEL_NAME = 'users.location'


def convert_csv_to_json(csv_filename, json_filename, model_name):

    with open(csv_filename, encoding='utf-8') as csv_file:
        csv_read = csv.DictReader(csv_file)
        result = []
        for row in csv_read:
            res = {"model": model_name, "pk": int(row['id'] if 'id' in row else row['Id'])}
            if 'id' in row:
                del row['id']
            elif 'Id' in row:
                del row['Id']
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'price' in row:
                row['price'] = int(row['price'])
            if 'author_id' in row:
                row['author_id'] = int(row['author_id'])
            if 'location_id' in row:
                loc_lst: list = []
                loc_lst.append(int(row['location_id']))
                row['location'] = loc_lst
                del row['location_id']
            if 'age' in row:
                row['age'] = int(row['age'])
            res['fields'] = row
            result.append(res)

    with open(json_filename, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(result, indent=3, ensure_ascii=False))


convert_csv_to_json(ADS_CSV, ADS_JSON, ADS_MODEL_NAME)
convert_csv_to_json(CATEGORY_CSV, CATEGORY_JSON, CATEGORY_MODEL_NAME)
convert_csv_to_json(LOCATION_CSV, LOCATION_JSON, LOCATION_MODEL_NAME)
convert_csv_to_json(USER_CSV, USER_JSON, USER_MODEL_NAME)
