import requests
import threading
import time
heards={
'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFRTXdaUzVxYWtnZEUxOEtFc3Q3WSJ9.eyJodHRwczovL3RoZWJlYWNvbi5nZy91c2VyX2lkIjoiYzdhMGFkNjEtNGZmYy00YjZlLTkzZDYtNjkwYzIwNjgxZjU1IiwiaXNzIjoiaHR0cHM6Ly9uZnEtcHJvZHVjdGlvbi51cy5hdXRoMC5jb20vIiwic3ViIjoidHdpdHRlcnwxNDM3NjE2MDc2NzQ1ODkxODQyIiwiYXVkIjpbImh0dHBzOi8vbmZxLXByb2R1Y3Rpb24udXMuYXV0aDAuY29tL2FwaS92Mi8iLCJodHRwczovL25mcS1wcm9kdWN0aW9uLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MTg1NDgzNzcsImV4cCI6MTcxODYzNDc3Nywic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCByZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX2lkZW50aXRpZXMiLCJhenAiOiJLUDNKdTNrRmNYZllOc2d1dk02d3dldHprekJ5alNCRiJ9.Dtkp1Wbj6eUaZLCFUBCPM5wgJPKjyIiDfRQL3rcHvFOeqhGFNOWWQM6cz5TPYVQ-wr1CdG3ro9tzbdijGMhYREZy4_NKvaBWxVGDXXuAXPZ3Py9abp94b6DcwANES9jckEXEn1fxwalboepGSYU0Sw-7L5ft1ajRRnjFxiqk5XJ-L7uu_An0Hp7bBBoEFABZoAE8n4muq1xyEpN6CfdoV_xPtpDeWz6UafvK-WPopUROI89Z0m8sUfaDkt5FTSD8Jie5AF1KTbaUKrq5Lztn54cwd3W_v2pEcchAavNiui5-BssMaGrv2__r2034Ck-qHFemEWEaCz5GjdfbrEdj3A',
'Cookie':'ph_phc_tk2o4SiS2sDMPP3NP20jAzFAdHk24GhgB9qNv5DvGEj_posthog=%7B%22distinct_id%22%3A%2201901b63-5939-7769-8747-e0b2ff3e7f16%22%2C%22%24sesid%22%3A%5B1718548888286%2C%2201902123-2f88-7d52-be9b-cc160a9b8337%22%2C1718542872456%5D%7D'


}
addresss=['7e10c134-cc00-4e9d-bda3-61fbd5a09be3','1304d0bf-dd62-4442-ba2f-89f837c9351a','78dcf387-39e5-447b-9a02-7d6e1dde2017',
          '64b39d86-0adc-44f0-a0dc-accae634f62b','8efd7989-dbf5-444b-b1a7-aa890776a354','bb7d1200-aef8-4daa-92da-9a6cf54ac861',
          '9d7fa13d-26f5-4358-957b-d58aa6243638','106f1095-9dc2-4647-be0c-1e36cc1d4bb9','3aa8ab2c-5a6c-497c-ac50-0728d70b8e8f',
          '1445fe90-ae9d-4822-8e67-0cc9a1633519','527b9f81-4038-405b-a1c8-0e3bdecc9cd2','aeeef5d6-efad-4aaa-9639-392af5e10ff6',
          '30096e66-16bf-4a98-80e5-50c007fb9db2','0e48a6ee-44c0-4e55-98e6-dfc055ef814c','0f37d1eb-bfaf-4a2c-b873-080bebddb648',
          '55e53d80-52a4-4f35-9bbb-d97eea6ea863',

          '8fc2aef3-acab-4ab5-a00b-fc53215fb7e4','6ee01071-3cd1-43ee-b962-1ee6146cbed2','5d4aed4a-5232-46a3-8822-41e8e4f6987b',
          'b64b88e6-a541-49b6-9fe0-0f278adddef5','f84fc81d-cadf-43a7-8ccc-dd7e71a1b274'
          #完成dis绑定后才能做的任务列表                                 
          #'18532053-5f1f-465f-a078-f5f9efec41bb'这个需要绑定dis，
          '7aa18270-ec54-4543-bda4-7dbbc29e8f6b','20676b24-ea1b-4125-a5ef-a397fea9c186',
]
a='30096e66-16bf-4a98-80e5-50c007fb9db2'
address=f'https://nfq-api.thebeacon.gg/api/users/c7a0ad61-4ffc-4b6e-93d6-690c20681f55/quests/{a}'
verifys=requests.post(f'{address}/verify',headers=heards)
verify=verifys.json()
print(verify)
claims=requests.post(f'https://nfq-api.thebeacon.gg/api/users/c7a0ad61-4ffc-4b6e-93d6-690c20681f55/quests/{a}/claim',headers=heards)
claim=claims.json()
print(claim)