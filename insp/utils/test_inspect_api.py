# --*-- coding: utf-8 --*--
import json

import requests
import os
from config import D_UP_LOADS

header = {
    # "Host": ob['domain'],
    # "Connection": "keep-alive",
    # "Pragma": "no-cache",
    # "Cache-Control": "no-cache",
    # "Referer": item['refer'],
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    # "Accept-Encoding": "gzip, deflate",
    # # "Cookie": ob.get('cookie')
    "Content-Type": "application/json; charset=utf-8",
}


def test_inspect_system_get():
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_inspect_system_post():
    data = dict(
        system_name="等保系统测试1",
        system_no="Ksegeuiree1",
        system_data_json=json.dumps({"system_name":"等保系统测试1"}),
        describe="testeweset1"
    )
    json_data = json.dumps(data)
    file_name = os.path.join(D_UP_LOADS, "资产管理子系统.docx")
    files = {'file': open(file_name, 'rb')}
    print json_data
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems"
    resp = requests.post(url, data=data, files=files)
    print json.dumps(resp.json())


def test_get_system_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems/assess/1"
    resp = requests.get(url)
    print json.dumps(resp.json())


def test_post_system_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/systems/assess/1"
    data_dict = {
        "business_assess": {
            "social_normal": False,
            "social_special": False,
            "country_specail": True,
            "citizen_serious": False,
            "citizen_normal": False,
            "social_serious": True,
            "country_normal": False,
            "citizen_special": True,
            "country_serious": False
        },

        "system_id": 1,
        "system_assess": {
            "social_normal": True,
            "social_special": False,
            "country_specail": False,
            "citizen_serious": True,
            "citizen_normal": False,
            "social_serious": False,
            "country_normal": True,
            "citizen_special": False,
            "country_serious": False
        }
    }
    # print json.dumps(data_dict)
    resp = requests.post(url, json=json.dumps(data_dict), headers=header)
    print json.dumps(resp.json())


def test_post_demands():
    url = "http://127.0.0.1:8092/insp/api/v1.0/demands"
    requests.post(url)


def test_post_manage_demands():
    url = "http://127.0.0.1:8092/insp/api/v1.0/manage/demands"
    requests.post(url)


def test_get_manage_demands():
    url = "http://127.0.0.1:8092/insp/api/v1.0/manage/demands"
    requests.get(url)


def test_get_tech_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/tech/assess/1"
    resp = requests.get(url)
    # print resp.json()
    print json.dumps(resp.json())


def test_post_tech_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/tech/assess/1"
    data_list = {

        "tech_assess": {
            "tech_4_c84029b29eeba53ac683f6827ec640a7": False,
            "tech_4_849dde28910d5940e092fba7e3b648a6": False,
            "tech_4_b5eab036092551401cf6c3424f2875cc": False,
            "tech_4_c125b7b394420d6cb5f16a709fbb0093": False,
            "tech_4_8b12a2cf9a0c9eec064b9c09a1ebf95c": False,
            "tech_4_0882d21670d70557ef9c232e821ace4d": False,
            "tech_4_e35b0a6add802f4d9ec781e0f1da1d04": False,
            "tech_4_e34235044f31e0f9c801c8cdde2f6f06": False,
            "tech_4_e8d0fee3e2a46b582ea400f0534f6112": False,
            "tech_4_1c307f5f1915d547a7b71e985f91eb4c": False,
            "tech_4_6a4e40e359ea8f75c8288d71184b8cd7": False,
            "tech_4_0cfe7f0258357519ef9101c41688f963": True,
            "tech_4_6da570ae0fbc060a33e69816af469eac": False,
            "tech_4_6a3ec74413d83f71569b801b5ffe1b73": False,
            "tech_4_02e22ef93ed2027c13cdcd2a4e56022f": False,
            "tech_4_9d7927bd8dcb6d745fb9b71a413cff25": False,
            "tech_4_c0f0862f05d7c5c6b8ac66fba4f32c54": True,
            "tech_4_b9f137837cd7b8340d141a33d9081226": False,
            "tech_4_e60d7bcd759c591e4b5daba040277cfe": False,
            "tech_4_c0a693e717ad8db2f6ed592b0b9e40ff": False,
            "tech_4_73c851730a6a8616e3cd1764b8533a6a": False,
            "tech_4_20a74ac007edf7779b84d446b5ef4910": False,
            "tech_4_7da0ad5c4f0cf8cea729d99427f52da5": False,
            "tech_4_8c31c108ecef183f6bb56be2a6af0e10": False,
            "tech_4_54fa492902e364a6f551c0e093ec7729": False,
            "tech_4_fa58b5bf97b0564ee4138f424166e29f": False,
            "tech_4_746972ed654b139b11bb4233edd7d001": False,
            "tech_4_0b26ac6ea674596909269808eb7f8f75": False,
            "tech_4_87224ed46306cda7135226d668efaeef": False,
            "tech_4_17aba70d2736236857f49ea87dd0a91a": False,
            "tech_4_56c03d94e564bf08f44237c5ff23ee2e": False,
            "tech_4_016b9d319fb231c13b4f6a04ec154ce9": False,
            "tech_4_53eac9565188c5879453c491cbf92dde": False,
            "tech_4_551421c68b5a3448f7af164aa4d6a792": False,
            "tech_4_f8e5ec9314baf20e6868a5629521eacb": False,
            "tech_4_3dc981337dfcd8d4e20ec64d0026e5c4": False,
            "tech_4_21ad3934a3978d92474f59d91e67e61d": False,
            "tech_4_22e40b9ed32d006b86f53730ba6ad0d4": False,
            "tech_4_39c654050dc969eb29dedfb5e2ec26cc": False,
            "tech_4_d77d4e07ecfd02dca214aba2720f9b09": False,
            "tech_4_ff50a8390c0875a616220ab18e140552": False,
            "tech_4_79f74f905891b698a74b6f883f7386ea": False,
            "tech_4_0e785ac527e346129630a0205fe1219d": False,
            "tech_4_24c0b1026dee899c8144d0ac46740d67": False,
            "tech_4_8a29e81f6682e2ff4544fd845e5c5fc5": False,
            "tech_4_51c7164a29ed74e48bdb3f6f037a8d43": False,
            "tech_4_67c6dad22ece5fc258ba0ba263ac7348": False,
            "tech_4_22fb62899529e6c0e587967cd32880f2": False,
            "tech_4_85922139bdb23708391e935ede1778bd": True,
            "tech_4_1b51dc2d4ed3bbe71728c25d7f6d0f76": False,
            "tech_4_41486591ac6545414b5c0403534cf98f": False,
            "tech_4_1be1b639edda223cf70094686f28ddb7": False,
            "tech_4_646a0c8b530e86fb0c537f6699235b0e": False,
            "tech_4_4cd45c449016cfeb62bca6909f9c3740": False,
            "tech_4_9f08aa10be9f2752fb43e6fba87635c7": False,
            "tech_4_b70559a65a607ae9c110a9b426889560": False,
            "tech_4_c2182b9a4318c0bcd5a8140b07b6daa8": False,
            "tech_4_1bb2beb479693568ac36e0bfd8a1b07e": False,
            "tech_4_59c8d49719b143604d2dcc7bf06ed03d": False,
            "tech_4_cbdf9f79e94b61844a7e8bb4e2036b7f": False,
            "tech_4_d3350364667cc19d3799b4b52aa4bc06": False,
            "tech_4_efdb1ad253ca31c0970165319f6ee9f9": False,
            "tech_4_6143c17cee973d6bb8a96f1b653e9b86": False,
            "tech_4_83fa74a1e7ed1f0db00c4700c6d59f3b": False,
            "tech_4_e5b57a55f70856c81a40c7b525cdded6": False,
            "tech_4_9e792858130c71d38f5d2b773dc5b647": False,
            "tech_4_47fdc19c5cbb9cfcc53168ffa0889c9b": False,
            "tech_4_45d1b51805d9235fcda0e1adb04b219a": False,
            "tech_4_37243a4c0ffddca5e701abd4298addf5": False,
            "tech_4_e1ad1364c045ae1aaf180982943d9134": False,
            "tech_4_58b5521a03185d6599ea2993039e2ec2": False,
            "tech_4_375bef6f9b1824870d10fa126b7c0463": False,
            "tech_4_88de033f0b976e7736b28a8247ed43e3": False,
            "tech_4_0b0c45967439096c13eb3984ab080f08": False,
            "tech_4_cd9ccba5a562f730096ab4c7f006bc42": False,
            "tech_4_48f8e4aa7e35edba07c55aeaf4d229de": False,
            "tech_4_b4bbfa71b377eb9cf0f71f42bf3df76b": False,
            "tech_4_c2aed29667653c002310699a7dc912fa": False,
            "tech_4_6d989b8bbfb8f2bf5db3f96e40e79b05": False,
            "tech_4_e0700418373bb6279d1bdc642c4c08c0": False,
            "tech_4_073853a7b1da359a4d43bd216e92861e": False,
            "tech_4_12803640cfd61acd1ecb018d66a483df": False,
            "tech_4_5aa9876f4ea24e2a24b7d96f8e21f072": False,
            "tech_4_ed6c22ce560dc69a9786a88ba9233400": False,
            "tech_4_5f66286097ae0d7c1ae4517215a886ce": False,
            "tech_4_25ddcd8443f3c0bc0bd62073636117ff": False,
            "tech_4_505d1423446b0a2b88f3183dd3f84eeb": False,
            "tech_4_ed0480999b5ab062393cf85ec653284c": False,
            "tech_4_1ad553f870d68087b2ca3f9ef2e5a7a8": False,
            "tech_4_6083ac262c3b067bd24877d0281665ad": False,
            "tech_4_1e6ea84aff15e04530304c6c9a73d1b4": False,
            "tech_4_9b0962f78513067e7f5ebee29f0f8819": False,
            "tech_4_7d584df39c2e11ab18d0fa94748b2a07": False,
            "tech_4_cbdbece0902e891474ff20a4cf883165": False,
            "tech_4_7dcd3ba2d92770cdba20d75df2bcbf5d": False,
            "tech_4_1b92d86416361c3b7786555ba8f3a3f3": False,
            "tech_4_01e44b2fc6f38afe8a022056549e731d": False,
            "tech_4_024559e738a2d273ffa0ce6418db1c4c": False,
            "tech_4_b84d9b4c81d8329fe18be2b2f598e0e2": False,
            "tech_4_b571845403091994600dace74ea09325": False,
            "tech_4_f35071975cf085d51bb54cde6fa067e4": False,
            "tech_4_58eb95a1746bf374cbf7d724ddfb354a": False,
            "tech_4_afcf135789ccd6a479706cdf2436d88b": False,
            "tech_4_8fc1d78fdcae8ff64757cdb234efd7ec": False,
            "tech_4_3e132cd59946e9b74b8ed4362d01a8b2": False,
            "tech_4_58f8260e48b5c66b0474844f287424f0": False,
            "tech_4_03e6c66a502fced69f6349253d99ea9b": False,
            "tech_4_b757918196e2dd4ef7e24ea012d953f7": False,
            "tech_4_ed5fe3e68332d195927b63971f82e704": False,
            "tech_4_aaca964b489e8696008ee34b405e0611": False,
            "tech_4_839cd9df3300fa110c2ac326da9f1457": False,
            "tech_4_9adf853b0124231350edbc63b206040f": False,
            "tech_4_94b8f70eb2f4c6b77072172e415b3797": False,
            "tech_4_708f8771cea17673b251daa09e2becf8": False,
            "tech_4_fdc03384a0fbdfef66af15d7b28993a7": False,
            "tech_4_3182b80f97e8de16dd21f8a944da8dda": False,
            "tech_4_668c380ad56aa1fdadcbb57592efe90e": False,
            "tech_4_cb327008b5fe201af9e484f9e3f270a6": False,
            "tech_4_7fc3befd6909ddb524b0bac0f79bd4a9": False,
            "tech_4_708b59a0d66ba369efb784c476b923e4": False,
            "tech_4_3e830a8c146ed4e461ddc612f6878773": False,
            "tech_4_d0e070ae51e07b8178e195ff69c63465": False,
            "tech_4_87b10f1d1f4e94477a0284d387d90508": False,
            "tech_4_a7fe621869806ab654b59a1060f45387": False,
            "tech_4_b0b199471b6794e49263437c498ab3d8": False,
            "tech_4_c5f4ac43417d67783b848281790712ad": False,
            "tech_4_ea1618e7a8ddf6b866bb11011bb3e611": False,
            "tech_4_8ec8bb169e944239d32283e88568c84d": False,
            "tech_4_b7bacb714c295f8d5606acbbbe66d7b3": False,
            "tech_4_b23df1a4fdde5ac9a1ffad076f3f12ae": False,
            "tech_4_4e9c89595fdfbec8eea0d35d9b9e1587": False,
            "tech_4_b08e59e7db169b6496353f3e064240f3": False,
            "tech_4_120eab8ffbbdae6612935a330225fcd5": False,
            "tech_4_f51546c505fd011d35a7d971cd8ecc6a": False,
            "tech_4_52ae33837406384779b51a5ff53e9dc5": False,
            "tech_4_a7d32890ed089dee7adb346bd7a4ec64": True,
            "tech_4_729ada3391b3a61fef5f648a1fd3f91a": False,
            "tech_4_3860781a17028df9214246adfc7bfafc": False,
            "tech_4_48a9d9411b1fab9914530560f9bfe868": False,
            "tech_4_3b0d33942072c3e6af565c3640e0e006": False,
            "tech_4_779c3a9c539d63b10240ddfe5ae8afc8": False,
            "tech_4_7ed7de822f3dbdfc439c0469086122e0": False,
            "tech_4_bfe5068dcda314f156078eef4fc007cf": False,
            "tech_4_a0c114b247b805d08f81bbeb8b8583a4": False,
            "tech_4_0c5b2ce703c07d3ff75e59d2fbb61d6e": False,
            "tech_4_b57d2a5f7ac9692376d057cd81d37258": False,
            "tech_4_1caf718db55f75ddcede3e2783077008": False,
            "tech_4_6eb7d7a4cae409663cd75ff3b3192ef2": False,
            "tech_4_0b2e94a14886b2e2f246bc5557169e3f": False,
            "tech_4_4b35880c8e4544a91d46eaaeb60bc829": False
        },
        "system_id": 1,
        "security_level": 4
    }
    resp = requests.post(url, json=json.dumps(data_list), headers=header)
    print json.dumps(resp.json())


def test_get_manage_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/manage/assess/1"
    resp = requests.get(url)
    # print resp.json()
    print json.dumps(resp.json())


def test_post_manage_assess():
    url = "http://127.0.0.1:8092/insp/api/v1.0/manage/assess/1"
    data_list = {
        "manage_assess": {
            "manage_4_5632ce02ad46d277a2df8eae1d24635f": False,
            "manage_4_066182ac96b0849d9880c24e3de6a36a": False,
            "manage_4_d54e3e4dc660d4124b25c0c96980f494": True,
            "manage_4_76716eb43df3567c5ed6b188a8b47fdd": False,
            "manage_4_10daef5bbe24a06a76c39e0896059840": False,
            "manage_4_9ea83032a64975bec561075d1b2ef156": False,
            "manage_4_14df7ba5dc3fbf14ed5898233f5896e8": False,
            "manage_4_cff9f54431cfe72837d0d5fce4812c0e": False,
            "manage_4_451a378bb130e37c0d6df8ade5ee878d": False,
            "manage_4_62e6ea8450dc11c783647133dc8b1554": True,
            "manage_4_de46d98a01545b07759eb91f5d9f6987": True,
            "manage_4_b7c98041fd8581cba620a358fd8edb75": False,
            "manage_4_4368285008630edf7778c66da254dcf4": False,
            "manage_4_b52f5f9287e9e0579a61440528186569": False,
            "manage_4_38d031c966024f3595b2bf8f9585b8ae": False,
            "manage_4_a03ca7fc5a14b85f3f3f928a8d95c341": True,
            "manage_4_a3bbd7277f73d693e2b5c4d55b234590": False,
            "manage_4_56922f04db70967bcc4b72af91c9744e": False,
            "manage_4_de1246e5cb1930457113543ebaa4b130": False,
            "manage_4_bc827454956c16867166ab8331d67118": False,
            "manage_4_8d330a272821944b135de0bd17a893c5": False,
            "manage_4_e9d1eae819bd91d183cc90b2d34c4852": False,
            "manage_4_3456ba8782c9cf701e44fb5bd1430c18": False,
            "manage_4_026bf9a9ea41b6fd5769e531cd1bae57": False,
            "manage_4_0e558a8054de07eef8489a8120a4f6b5": False,
            "manage_4_9004da7bb73e3ac7de31529593cb1ced": False,
            "manage_4_adb9e9ce1f5caff3eb25293577d1d982": False,
            "manage_4_74d8cbb1962d864490a38c613fa378bd": False,
            "manage_4_79b3a69dba14385b93aab9f443c3cb9a": False,
            "manage_4_b99f96d633ec4cca32b0a754440b7895": False,
            "manage_4_62949930b8d807f9b832f866b0d7d471": False,
            "manage_4_1471a27379c7520d8e9827274f4eda4c": False,
            "manage_4_53787b2e00ab03bc3e5c95bbebf57e35": False,
            "manage_4_1784702f03a7a2deb07cc38a4e6a7676": False,
            "manage_4_16d466abdb3c26d7a496d0a67b4010a3": False,
            "manage_4_278f3f6593391ec67bcee8d089b8c150": False,
            "manage_4_82439849d89f32d9af15797fb0a648d5": False,
            "manage_4_ffff835fe83366332dfdde5afc4b84df": False,
            "manage_4_d422c1106341fb6636105224fb8a191d": False,
            "manage_4_ffdefc228bb8e3d7f56b69847849038a": False,
            "manage_4_7ed26d75aa5fc9f64aa2e928e0bc6820": False,
            "manage_4_de95ecbdb72168bc543dd72f9d861a4f": False,
            "manage_4_f89059fa8cf6a4e2aa4ac25bf918eb93": False,
            "manage_4_2dbb880d5a9f9a98599a90b58dc63e35": False,
            "manage_4_2680b594ea04e1eaa2f0f86fa8703927": False,
            "manage_4_d70335f3e47765777e97a6df470954f0": False,
            "manage_4_366952a4034149cf5580d8c46ba00ff8": False,
            "manage_4_446ece75157eb3fccc8aa63c14b85def": False,
            "manage_4_b8d89523101aa1498be492504c819771": False,
            "manage_4_eb00f80d664cb611ce62816a4ad23594": False,
            "manage_4_432c059aaf53700a850b48b27b70cd97": False,
            "manage_4_912d60f11677fed3e391c9e5b2bb9794": False,
            "manage_4_de1f51138b5b887be514efec84ebf4b8": False,
            "manage_4_4489de51b0b204faf4b88b978549ea2b": False,
            "manage_4_c14108c1fcbacaa193fbb485a829b017": False,
            "manage_4_be14cfe0e2fc00e3ae156c923b5050e1": False,
            "manage_4_798c851a424a86c0cadbe5100929ba9b": False,
            "manage_4_66a1f16743a91b24fe6844b17872a430": False,
            "manage_4_498b6c9c20a1da7863fbea9f8e215de4": False,
            "manage_4_c0dca038c0236fdfe708f4c330efcccc": False,
            "manage_4_7d7e295174d1f7a3d5e3bf8bc4d73942": False,
            "manage_4_bbf6746909a10ea06b5bf90da3febe75": False,
            "manage_4_d9b06ee39794d7ba5009e48973557e7d": False,
            "manage_4_bf42ff8e6e1abb8fd6eda46d1b65392f": False,
            "manage_4_ab64611b27126aa5fa6bb00e14dbe770": False,
            "manage_4_4755a88b0f54d0e29bc41c473021f100": False,
            "manage_4_a5ea40bde1d5bd6b43ce3e3bb807d538": False,
            "manage_4_dfccd9642f75f1f62888307aa5301bcb": False,
            "manage_4_0acaae47ebcd6bec3f2e79b7d0957ff5": False,
            "manage_4_1a92576ece35e4ff790e03e7dd647238": False,
            "manage_4_f2996afbc040676b42fcfa9104f440cb": False,
            "manage_4_05f7a6bc8b65f288cc98aae76f8ae12d": False,
            "manage_4_782f8101b4770f25ffe86634f1e1b318": False,
            "manage_4_b8f4d43a8298c9e63655bf4ed949816e": False,
            "manage_4_ac58c1c56627222eda2b9b82fb5fd95a": False,
            "manage_4_4c7e79be1f9dc3635f77864148d2f95e": False,
            "manage_4_53bf79a63924b1c57b3b48cdaa1c86c7": False,
            "manage_4_411923a861d031194161faf46e18bbc6": False,
            "manage_4_f576fc31ec07438895c5d9fb7c3d90ab": False,
            "manage_4_c1983b64fa2e69ba09728a887d228188": False,
            "manage_4_5aa761326a701eb01719b8e633277493": False,
            "manage_4_cc999f9227c2b8e0a11b2d6829291088": False,
            "manage_4_a010c3e6ea6992ec91a5fb88a9fb81e1": False,
            "manage_4_54637e5fc9c3dd067c7f6289f5247010": False,
            "manage_4_dff0c79df0904929718acaf090a74bdf": False,
            "manage_4_7864f4e8b0104e5c8e21e8af13ad6d09": False,
            "manage_4_0516050074fa345f10017f2816a732d2": False,
            "manage_4_f6dfa8d9685a26c0ce81348d2d380a1a": False,
            "manage_4_242cf7b5c644c245b6290caecd11c3cd": False,
            "manage_4_112b1dd14dc3be34ab5c2a94164b1289": False,
            "manage_4_f2abe985570eedf6eeda3df7d13a2094": False,
            "manage_4_0c7a27e7151c71506068714a16a1396a": False,
            "manage_4_785886cd58745f75c9c7fa0ba9b47d12": False,
            "manage_4_487e496ccbbf6c1ca5ee589ec67b8a2f": False,
            "manage_4_74abadfdeb7decb4d0577a40ef150f1d": False,
            "manage_4_99bb3d870245bb85dffc7264c753d8ec": False,
            "manage_4_659b66e1c96f72fd43653213283dad6c": False,
            "manage_4_ea4763bbd1b49c428b0b2fb3f8dded89": False,
            "manage_4_3048060d9498288d2aeba3c4e5d5ba15": False,
            "manage_4_5f9c1f54ce9c89bea9b3833c811c450b": False,
            "manage_4_c18cf11fc3ebb6fd9d95b2e420144b92": False,
            "manage_4_2e170ca61b2c314d970ef9e10e6ec138": False,
            "manage_4_5fff530e4e66488a3954d0e78de763d0": False,
            "manage_4_335dcb273e0ba2bb5636934cd5a2aa70": False,
            "manage_4_e0bcac6378e3fcb149335f5dcba32356": False,
            "manage_4_e328c5236eb83fa6d0432e417eb4c25f": False,
            "manage_4_1ef6036e9d9b07e287a79750e6a5748b": False,
            "manage_4_5fec878ecdcdf5b2511085585b08ed52": False,
            "manage_4_1aeb980bd390f9be7a4bdc8b172ae828": False,
            "manage_4_6ecba0f5f0ecfe74cc87fcdc3c99ef54": False,
            "manage_4_d29661a94cf457ec07499954dd05d7f2": False,
            "manage_4_a918c6d98e42bff00f1df3aacf09f754": False,
            "manage_4_874597474ec6e42287c373525d53fcbd": False,
            "manage_4_2ba8cf705aea312e43d958248adddae2": False,
            "manage_4_c79ebd2801044f09160a6ecf71e963e9": False,
            "manage_4_bcc9a00112c9315164f179e190d7204d": False,
            "manage_4_2e0da90099efab7fe7989659d5b70903": False,
            "manage_4_294113df964c4fc6e0211071f973de04": False,
            "manage_4_75b5af1d8a6026cb3bd5a21ff0497cfa": False,
            "manage_4_41538c05be28fd77c59e821c15a0fa9d": False,
            "manage_4_e07847847dc9633438c176d82f36c6e5": False,
            "manage_4_fa47342b49c0f17671e3640a2ee2f5c1": False,
            "manage_4_0861209991e052d001cf674a1335307a": False,
            "manage_4_9d7aca86b492f2f3de6e76cc46eb6f1f": False,
            "manage_4_07c29fbb71d381c92d80336967c49931": False,
            "manage_4_e32678ef5c68343293c8a9bb11a71860": False,
            "manage_4_ae21f04ed8a69c59ea7b34b01b71d4b8": False,
            "manage_4_0284a53b1891d3ecbbbf5e2355c88aab": False,
            "manage_4_a57ba6720d4dcb0731d3e87e9223f663": False,
            "manage_4_c37e4a282ab9471c1087c8bd01fb900d": False,
            "manage_4_b74624489b34ddf9f0bc7b533b827a67": False,
            "manage_4_3e7810971bd64c16c3d7e1cc1e60f531": False,
            "manage_4_f3e71772c13bc31ddc51abdda96e88be": False,
            "manage_4_d6478bc788a13f3f60530e69e2a84297": False,
            "manage_4_573556ac1861d2c80afee3792df1b908": False,
            "manage_4_1d5848c20332b61028c2dae44d381bdc": False,
            "manage_4_06976eb5f713263d7dbfdd3c3b8d6a6f": False,
            "manage_4_4a6f4d2a223dd0cbd58fa3391eba3566": False,
            "manage_4_8db141fd5e8dddb3594bed79ee674186": False,
            "manage_4_430e75afb6e21afb74d07ac670891c0e": False,
            "manage_4_cd38778d09b32c7abb4095dce7ea3867": False,
            "manage_4_75863819c2c6a33959e7117cecedf582": False,
            "manage_4_b4b892f4057915c31a561ff3b100799a": False,
            "manage_4_e8f3a25a0a3775964b63bfccbb287af3": False,
            "manage_4_81e62723630207cfcae11df7ef24c560": False,
            "manage_4_46d8521a50355dbfe0244bc190f5c6d4": False,
            "manage_4_e9a856899df2c12b16c6c603fba4b411": False,
            "manage_4_0ab905737e33f544d9afa1ef1e88497b": False,
            "manage_4_65eb85a42b370990d6897109e471f843": False,
            "manage_4_b4011036049c7d4fb25b99c174fdfc59": False,
            "manage_4_dedb98b74bce9f2f7eca72985ea9d7dd": False,
            "manage_4_29321414df8be6688ab025127fda9289": False,
            "manage_4_07941e72cf8767ad23314a0a783b73b6": False,
            "manage_4_c3831721cf393a34e36a8d2095a20a34": False,
            "manage_4_dcca99ed1b358a46b7400da590394f87": False,
            "manage_4_177fe7fe11cffab5b0c767492e7b453e": False,
            "manage_4_8630039b1afea0b842b6ab05ec0a1d89": False,
            "manage_4_df528b717c7728adcda5d76590a0b4f6": False,
            "manage_4_fb725c2ca87dd9b56b09081c42cb9e60": False,
            "manage_4_99778777b99cd0eb74d863765df5025e": False,
            "manage_4_90a1b26319d44f4e9597ff2f1fe80afa": False,
            "manage_4_14cdd5aad050d35790f96d974af2649c": False,
            "manage_4_e93d61b20525888e48a176c41c3f538b": False,
            "manage_4_857f5958942444fdeb35771ab224bd42": False,
            "manage_4_dde46ebbd8c24c0f1d1f233ffe240069": False,
            "manage_4_b9892ddb8a0b9654d4ff8406993faa96": False,
            "manage_4_52ec361c63e26a864749fb265fad4988": False,
            "manage_4_1b2fa800469f72920e553be8f0f0050a": False,
            "manage_4_265a1c4bf93a596bef3040e3588568ea": False,
            "manage_4_361cf309388b8cf38c5f5bc0ec61bce3": False,
            "manage_4_9c12977d0ee8bc7bc2907fe3ae86c1ce": False
        },
        "system_id": 1,
        "security_level": 4
    }
    resp = requests.post(url, json=json.dumps(data_list), headers=header)
    print json.dumps(resp.json())


if __name__ == '__main__':
    test_inspect_system_get()
    # test_inspect_system_post()
    # test_get_system_assess()
    # test_post_system_assess()
    # test_post_demands()
    # test_post_manage_demands()
    # test_get_manage_demands()
    # test_get_tech_assess()
    # test_post_tech_assess()
    # test_get_manage_assess()
    # test_post_manage_assess()
