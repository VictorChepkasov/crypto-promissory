import os
import requests  
import json
from brownie import PromissoryNFT, Promissory
from dotenv import load_dotenv

load_dotenv()

metadata_template = {
    "name": "crypto-promise",
    "description": "",
    "image": "https://ipfs.io/ipfs/QmPFQksqBbkF6o6qbVNHZGkEiZXro7Ji6vJ8SembbchDK5",
    "attributes": [
        {
            "trait_type": "Holder address",
            "value": ""
        },
        {
            "trait_type": "Debtor address",
            "value": ""
        },
        {
            "trait_type": "NFT id",
            "value": ""
        },
        {
            "display_type": "number",
            "trait_type": "Commission in percents",
            "value": 0
        },
        {
            "display_type": "number",
            "trait_type": "Amount to pay",
            "value": 0
        },
        {
            "display_type": "date",
            "trait_type": "Date of registration",
            "value": 0
        },
        {
            "display_type": "date",
            "trait_type": "Date of close",
            "value": 0
        },
        {
            "display_type": "date",
            "trait_type": "Date of holder consent",
            "value": 0
        },
        {
            "display_type": "date",
            "trait_type": "Date of debtor consent",
            "value": 0
        }
        ]
    }

def create_metadata(_from, token_id):
    # кол-во выпущеных токенов
    print(f'Token id: {token_id}')
    # копируем шаблон метаданных
    collectible_metadata = metadata_template.copy()
    # имя токена = его id
    collectible_metadata["name"] = f"Cypto-promise №{str(token_id)}"

    # получаем инфу о контракте
    promissory_info = get_promissory_info(_from, token_id)
    print(f'Promissory info: {promissory_info}')
    # сохраняем данные контракта в виде атрибутов
    for i in range(9):
        metadata_template["attributes"][i]["value"] = str(promissory_info[i]) if type(metadata_template["attributes"][i]["value"]) == type('') else int(promissory_info[i])
    collectible_metadata["description"] = f"Crypto-promissory for ${promissory_info[4]}"
    # имя файла метаданных
    metadata_filename = f"./scripts/metadata/{token_id}.json"
    with open(metadata_filename, "w") as f:
        # Запишите метаданные локально
        json.dump(collectible_metadata, f, indent=4)

    # загрузка данных в ipfs(Pinata)
    print(collectible_metadata)
    # metadata_hash = upload_to_ipfs(collectible_metadata)
    metadata_hash = upload_to_ipfs("./scripts/metadata/")
    metadata_uri = f"<https://ipfs.io/ipfs/{metadata_hash}/>"
 
    # добавляем uri в json файл   
    with open('./scripts/metadata_hashes.json', 'r') as f:
        json_file = json.load(f)
    with open('./scripts/metadata_hashes.json', 'w') as ff:
        json_file.append(metadata_uri)
        json.dump(json_file, ff)

    print('Metadata created success!')
    return metadata_uri

# token_id - id токена, метаданные которого будут обновляться
# data - массив, где первый элемент адрес holder, а второй дата закрытия
# Если один из элементов data равен None, то данные этогго атрибута не меняются
def update_metadata(_from, token_id):
    print(f'Token id: {token_id}')
    metadata_filename = f"./scripts/metadata/{token_id}.json"
    print(f'Metadata file: {metadata_filename}')
    promissory_info = get_promissory_info(_from, token_id)

    # Чтение и запись файла с обновлёнными таданными адреса и даты закрытия векселя
    with open(metadata_filename, 'r') as f:
        json_file = json.load(f)
    with open(metadata_filename, 'w') as metadata_file:
        for i in range(9):
            json_file["attributes"][i]['value'] = str(promissory_info[i]) if type(json_file["attributes"][i]['value']) == type('') else int(promissory_info[i])
        json.dump(json_file, metadata_file, indent=4)

    #обновляю данные в Pinata
    hash_ipfs = 'QmeccHuGmE9gXZLdbhKpBhTX8ajrwGszaV8QtRYUYxWtf7'
    endpoint = "https://api.pinata.cloud/pinning/hashMetadata"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {os.environ.get("PINATA_API_JWT")}'
    }
    hash_ipfs_json = {
        "ipfsPinHash": hash_ipfs,
        'keyvalues': json.dumps(json_file, indent=2)
        }
    response = requests.put(endpoint, headers=headers, json=hash_ipfs_json)
    print(response.text)

def upload_to_ipfs(data):
    endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "accept": "application/json",
        # "content-type": "application/json",
        "authorization": f'Bearer {os.environ.get("PINATA_API_JWT")}',
    }
    token_id = data['attributes'][2]['value']
    files = {
        'file': json.dumps(data, indent=4)
    }
    metadata = {
        'pinataMetadata': json.dumps({"name": data["name"]}, indent=4)
    }
    # запрос пин-кода в pinata
    response = requests.post(endpoint, headers=headers, files=files, data=metadata)
    print(f'Response: {response.json()}')
    returned_hash_IPFS = response.json()['IpfsHash']
    # возвращаем хэш ipfs, где хранятся все нужные данные
    return returned_hash_IPFS

# получение инфы о векселе из фабрики
def get_promissory_info(_from, token_id):
    promissory_info = PromissoryNFT[-1].getPromissory(token_id, {
        'from': _from
    })
    promissory_info = Promissory.at(promissory_info).getPromissoryInfo({
        'from': _from
    })
    # чистка promissory info
    promissory_info = str(promissory_info).translate(str.maketrans('', '', "()''")).split(', ')
    return promissory_info