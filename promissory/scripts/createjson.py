import requests
import os
import json

from scripts.deploy_promissory import getPromissoryInfoArr

metadata_template = {
    "name": "",
    "attributes": [
        {
            "trait_type": "holder address",
            "value": ""
        },
        {
            "trait_type": "debtor address",
            "value": ""
        },
        {
            "trait_type": "commission in percents",
            "value": ""
        },
        {
            "trait_type": "amount",
            "value": ""
        },
        {
            "trait_type": "date of registration",
            "value": ""
        },
        {
            "trait_type": "date of close",
            "value": ""
        },
        {
            "trait_type": "date of holder consent",
            "value": ""
        },
        {
            "trait_type": "date of debtor consent",
            "value": ""
        },
        {
            "trait_type": "holder consent",
            "value": ""
        },
        {
            "trait_type": "debtor consent",
            "value": ""
        }
        ]
    }

def main():
    create_metadata(1)

def create_metadata(i):
    # разворачиваем контракт и получаем инфу о нём
    promissory_info = getPromissoryInfoArr().split(', ')

    # Массив для хранения метаданных
    metadata_hashes = []

    for token_id in range(i):
        # копируем шаблон метаданных
        collectible_metadata = metadata_template.copy()
        # имя файла метаданных
        metadata_filename = f"./scripts/metadata/{token_id + 1}.json"
        # имя токена = его id
        collectible_metadata["name"] = str(token_id)

        # Сохраняем данные контракта в виде атрибутов
        for i in range(10):
            metadata_template["attributes"][i]["value"] = str(promissory_info[i])

        with open(metadata_filename, "w") as f:
            # Запишите метаданные локально
            json.dump(collectible_metadata, f)

        # загрузка данных в ipfs(Pinata)
        metadata_hash = upload_to_ipfs(collectible_metadata)
        metadata_path = f"<https://ipfs.io/ipfs/{metadata_hash}>"
 
        # Добавить uri метаданные в массив
        metadata_hashes.append(metadata_path)
    
    with open('./scripts/metadata/data.json', 'w') as f:
        # Наконец, мы запишем массив URI метаданных в файл
        json.dump(metadata_hashes, f)
 
    return metadata_hashes



def upload_to_ipfs(data):
    pinata_api_jwt = os.environ.get("PINATA_API_JWT")
    print(pinata_api_jwt)

    endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        'Authorization': pinata_api_jwt,
    }

    encode_data = json.dumps(data, indent=2).encode('utf-8')

    print(f"Just data: {data}")
    
    files = {
        'file': encode_data
    }

    # запрос пин-кода в pinata
    response = requests.post(endpoint, headers=headers, files=files)
    hashh = response.json()['IpfsHash']

    print(f"Сам запрос{response.json()}")
    print(f"Возвращаемое значение {hashh}")
    
    # возвращаем хэш ipfs, где хранятся все нужные данные
    return hashh