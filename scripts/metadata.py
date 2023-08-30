import os, requests, json
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
    print(f'Token id: {token_id}')
    # копируем шаблон метаданных
    collectible_metadata = metadata_template.copy()
    # имя токена = его id
    collectible_metadata["name"] = f"Cypto-promise №{str(token_id)}"

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

def upload_to_ipfs(data):
    endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "accept": "application/json",
        "authorization": f'Bearer {os.environ.get("PINATA_API_JWT")}',
    }
    files = {
        'file': json.dumps(data, indent=4)
    }
    metadata = {
        'pinataMetadata': json.dumps({"name": data[0]})
    }
    # запрос пин-кода в pinata
    response = requests.post(endpoint, headers=headers, files=files, data=metadata)
    print(f'Response: {response.json()}')
    # возвращаем хэш ipfs, где хранятся все нужные данные
    return response.json()['IpfsHash']

# получение инфы о векселе из фабрики
def get_promissory_info(_from, token_id):
    promissory = PromissoryNFT[-1].getPromissory(token_id, {
        'from': _from
    })
    promissory_info = Promissory.at(promissory).getPromissoryInfo({
        'from': _from
    })
    # чистка promissory info
    promissory_info = str(promissory_info).translate(str.maketrans('', '', "()''")).split(', ')
    return promissory_info