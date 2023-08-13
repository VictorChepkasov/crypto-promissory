import requests
import os
import json
from brownie import PromissoryNFT, Promissory, accounts, config
from dotenv import load_dotenv

load_dotenv()

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
    create_metadata(accounts.add(config["wallets"]['from_key']))

def create_metadata(_from):
    # кол-во выпущеных токенов
    existing_tokens = PromissoryNFT[-1].tokenCounter()
    print(f'Existing tokens: {existing_tokens}')
    # копируем шаблон метаданных
    collectible_metadata = metadata_template.copy()
    # имя токена = его id
    collectible_metadata["name"] = str(existing_tokens)

    # получаем инфу о контракте
    promissory_info = get_promissory_info(_from, existing_tokens)
    print(f'Promissory info: {promissory_info}')
    # сохраняем данные контракта в виде атрибутов
    for index in range(10):
        metadata_template["attributes"][index]["value"] = str(promissory_info[index])
        
    # имя файла метаданных
    metadata_filename = f"./scripts/metadata/tokens/{existing_tokens}.json"
    with open(metadata_filename, "w") as f:
        # Запишите метаданные локально
        json.dump(collectible_metadata, f)

    # загрузка данных в ipfs(Pinata)
    metadata_hash = upload_to_ipfs(collectible_metadata)
    metadata_uri = f"<https://ipfs.io/ipfs/{metadata_hash}>"
 
    # добавляем uri в json файл   
    write_to_json(metadata_uri)

    print('Metadata created success!')
    return metadata_uri

def upload_to_ipfs(data):
    endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    pinata_api_key = os.environ.get("PINATA_API_KEY")
    pinata_secret_api_key = os.environ.get("PINATA_API_SECRET")
    headers = {
        'pinata_api_key': pinata_api_key,
        'pinata_secret_api_key': pinata_secret_api_key
    }
    encode_data = json.dumps(data, indent=2).encode('utf-8')
    files = {
        'file': encode_data
    }

    # запрос пин-кода в pinata
    response = requests.post(endpoint, headers=headers, files=files)
    # print(f'Response: {response.json()}')
    returned_hash_IPFS = response.json()['IpfsHash']

    # возвращаем хэш ipfs, где хранятся все нужные данные
    return returned_hash_IPFS

# получение инфы о векселе из фабрики
def get_promissory_info(_from, token_id):
    promissory_info = PromissoryNFT[-1].getPromissory(token_id, {
        'from': _from
    })
    promissory_info = Promissory.at(promissory_info).getPromissoryInfo({'from': _from})
    # чистка promissory info
    promissory_info = str(promissory_info).translate(str.maketrans('', '', "()''")).split(', ')
    return promissory_info

# функция записи uri метаданных в json файл
def write_to_json(metadata_uri):
    with open('./scripts/metadata/metadata_hashes.json', 'r') as f:
        json_file = json.load(f)
    with open('./scripts/metadata/metadata_hashes.json', 'w') as ff:
        json_file.append(metadata_uri)
        # print(json_file)
        json.dump(json_file, ff)