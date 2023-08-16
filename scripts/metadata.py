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
            "trait_type": "NFT id",
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
        }
        ]
    }

# def main():
#     create_metadata(accounts.add(config["wallets"]['from_key']))

def create_metadata(_from, token_id):
    # кол-во выпущеных токенов
    print(f'Token id: {token_id}')
    # копируем шаблон метаданных
    collectible_metadata = metadata_template.copy()
    # имя токена = его id
    collectible_metadata["name"] = str(token_id)

    # получаем инфу о контракте
    promissory_info = get_promissory_info(_from, token_id)
    print(f'Promissory info: {promissory_info}')
    # сохраняем данные контракта в виде атрибутов
    for i in range(9):
        metadata_template["attributes"][i]["value"] = str(promissory_info[i])
        
    # имя файла метаданных
    metadata_filename = f"./scripts/metadata/tokens/{token_id}.json"
    with open(metadata_filename, "w") as f:
        # Запишите метаданные локально
        json.dump(collectible_metadata, f, indent=4)

    # загрузка данных в ipfs(Pinata)
    metadata_hash = upload_to_ipfs(collectible_metadata)
    metadata_uri = f"<https://ipfs.io/ipfs/{metadata_hash}>"
 
    # добавляем uri в json файл   
    with open('./scripts/metadata/metadata_hashes.json', 'r') as f:
        json_file = json.load(f)
    with open('./scripts/metadata/metadata_hashes.json', 'w') as ff:
        json_file.append(metadata_uri)
        json.dump(json_file, ff)

    print('Metadata created success!')
    return metadata_uri

# token_id - id токена, метаданные которого будут обновляться
# data - массив, где первый элемент адрес holder, а второй дата закрытия
# Если один из элементов data равен None, то данные этогго атрибута не меняются
def update_metadata(_from, token_id):
    print(f'Token id: {token_id}')
    metadata_filename = f"./scripts/metadata/tokens/{token_id}.json"
    print(f'Metadata file: {metadata_filename}')
    promissory_info = get_promissory_info(_from, token_id)
    # Чтение и запись файла с обновлёнными таданными адреса и даты закрытия векселя
    with open(metadata_filename, 'r') as f:
        json_file = json.load(f)
    with open(metadata_filename, 'w') as metadata_file:
        for i in range(9):
            json_file["attributes"][i]['value'] = str(promissory_info[i])
        json.dump(json_file, metadata_file, indent=4)
    #обновляю данные в Pinata

def upload_to_ipfs(data):
    endpoint = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f'Bearer {os.environ.get("PINATA_API_JWT")}',
    }
    pinata_content = {
        'pinataContent': json.dumps(data, indent=2),
        'pinataMetadata': json.dumps({"name": "NAME"}, indent=2)
    }

    # запрос пин-кода в pinata
    response = requests.post(endpoint, headers=headers, json=pinata_content)
    # print(f'Response: {response.json()}')
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
