#!/usr/bin/env python3
"""生成新数据模型测试数据，每个表不少于200条记录"""

import random
from datetime import datetime
from faker import Faker
import uuid

fake = Faker('zh_CN')
random.seed(100)
fake.seed_instance(100)

def gen_varchar32():
    return str(uuid.uuid4()).replace('-', '')[:32]

def gen_pk(prefix=''):
    return prefix + str(uuid.uuid4()).replace('-', '')[:28]

CP_IDS = [1, 2, 3]
PK_TAX_CLASS_IDS = []
PK_PSNDOC_IDS = []
WA_TAX_COMPUTE_RECORD_IDS = []

print("-- =============================================")
print("-- 新数据模型测试数据生成")
print("-- =============================================\n")

# 1. wa_tax_region - 50条
print("-- 1. wa_tax_region")
for i in range(50):
    name = fake.city() + '市' if i >= 10 else fake.province()
    pk_father = (i % 10) + 1 if i >= 10 else 'NULL'
    print(f"INSERT INTO wa_tax_region VALUES ({i+1}, '{str(i+1).zfill(6)}', '{name}', {pk_father}, 'system', NOW(), 'system', NOW());")
print(f"-- 生成 50 条\n")

# 2. wa_tax_class - 200条
print("-- 2. wa_tax_class")
for i in range(200):
    cp_id = random.choice(CP_IDS)
    pk_tax_class = gen_pk('PLAN_')
    areaid = random.randint(1, 50)
    agent_code = fake.numerify(text='##########')
    nsrsbh = fake.numerify(text='##########')
    PK_TAX_CLASS_IDS.append((pk_tax_class, cp_id, i+1))
    print(f"INSERT INTO wa_tax_class (pk_tax_class, agent_code, agent_name, nsrsbh, status, code, areaid, name, cp_id, creator, create_time, modify_time) VALUES ('{pk_tax_class}', '{agent_code}', '{fake.company()}', '{nsrsbh}', 'NORMAL', 'TAX{i+1:04d}', {areaid}, '方案{i+1}', {cp_id}, 'system', NOW(), NOW());")
print(f"-- 生成 200 条\n")

# 3. wa_tax_dict - 75条
print("-- 3. wa_tax_dict")
dict_types = [('zzlx', 10), ('rylx', 5), ('jbqk', 5), ('qylx', 10), ('gr_lx', 5)]
idx = 1
for dtype, cnt in dict_types:
    for j in range(cnt):
        print(f"INSERT INTO wa_tax_dict (dict_type, dict_code, dict_name, sort_order, enabled, dr, creator, create_time, modify_time) VALUES ('{dtype}', '{dtype}{j+1}', '{dtype}名称{j+1}', {idx}, 1, 0, 'system', NOW(), NOW());")
        idx += 1
print(f"-- 生成 {idx-1} 条\n")

# 4. wa_tax_api_router - 30条
print("-- 4. wa_tax_api_router")
for i in range(30):
    print(f"INSERT INTO wa_tax_api_router (cp_id, provider, enabled, dr, creator, create_time, modify_time) VALUES ({random.choice(CP_IDS)}, 'BASE_TAX_V1', 1, 0, 'system', NOW(), NOW());")
print(f"-- 生成 30 条\n")

# 5. wa_tax_income_category - 3条
print("-- 5. wa_tax_income_category")
cats = [('01', '综合所得'), ('02', '分类所得'), ('03', '非居民所得')]
for i, (code, name) in enumerate(cats):
    print(f"INSERT INTO wa_tax_income_category (code, name, sort_order, enabled, dr, creator, create_time, modify_time) VALUES ('{code}', '{name}', {i+1}, 1, 0, 'system', NOW(), NOW());")
print(f"-- 生成 3 条\n")

# 6. wa_tax_income_sub_category - 12条
print("-- 6. wa_tax_income_sub_category")
sub_cats = [(1,'工资薪金'),(1,'劳务报酬'),(1,'稿酬所得'),(1,'特许权使用费'),(2,'经营所得'),(2,'财产租赁'),(2,'财产转让'),(2,'利息股息红利'),(2,'偶然所得'),(3,'非居民工资薪金'),(3,'非居民劳务报酬'),(11,'个体工商户生产经营所得')]
for i, (cat_id, name) in enumerate(sub_cats):
    print(f"INSERT INTO wa_tax_income_sub_category (category_id, name, sort_order, enabled, dr, api_request_field, creator, create_time, modify_time) VALUES ({cat_id}, '{name}', {i+1}, 1, 0, 'api_{i+1}', 'system', NOW(), NOW());")
print(f"-- 生成 {len(sub_cats)} 条\n")

# 7. wa_tax_income_item - 200条
print("-- 7. wa_tax_income_item")
items = [
    (1, '01010101', '0101', '正常工资薪金', 'CUMULATIVE'),
    (1, '01010102', '0102', '全年一次性奖金', 'FLAT_RATE'),
    (1, '01010103', '0103', '解除劳动合同补偿金', 'FLAT_RATE'),
    (2, '01020101', '0201', '一般性劳务报酬', 'CUMULATIVE'),
    (2, '01020102', '0202', '保险营销员佣金', 'CUMULATIVE'),
    (3, '01030101', '0301', '稿酬所得', 'CUMULATIVE'),
    (4, '01040101', '0401', '特许权使用费', 'CUMULATIVE'),
    (5, '02010101', '0501', '个体工商户经营所得', 'CUMULATIVE'),
    (6, '02020101', '0601', '房屋租赁所得', 'FLAT_RATE'),
    (7, '02030101', '0701', '股权转让所得', 'FLAT_RATE'),
    (8, '02040101', '0801', '利息所得', 'FLAT_RATE'),
    (8, '02040102', '0802', '股息红利所得', 'FLAT_RATE'),
    (9, '02050101', '0901', '偶然所得', 'FLAT_RATE'),
    (10, '03010101', '1001', '非居民工资薪金', 'CUMULATIVE'),
]
for i in range(200):
    sub_id, item_code, sdxm, name, tax_method = items[i % len(items)]
    suffix = i // len(items) + 1
    print(f"INSERT INTO wa_tax_income_item (sub_category_id, item_code, sdxm, name, tax_method, sort_order, enabled, dr, creator, create_time, modify_time) VALUES ({sub_id}, '{item_code}_{suffix}', '{sdxm}', '{name}-{suffix}', '{tax_method}', {i+1}, 1, 0, 'system', NOW(), NOW());")
print(f"-- 生成 200 条\n")

# 8. bd_psndoc - 500条
print("-- 8. bd_psndoc")
for i in range(500):
    pk_person = gen_varchar32()
    tc_data = random.choice(PK_TAX_CLASS_IDS)
    PK_PSNDOC_IDS.append((pk_person, tc_data[1]))
    zzhm = fake.numerify(text='###########X')
    kjsrybm = fake.numerify(text='##########')
    csny = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime('%Y-%m-%d')
    rzsgrq = fake.date_between(start_date='-5y', end_date='-1y').strftime('%Y-%m-%d')
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    xb = random.choice(['1', '2'])
    lxdh = fake.phone_number()[:11]
    bszt = random.choice(['待同步', '已同步', '同步失败'])
    xl = random.choice(['本科', '硕士', '博士'])
    print(f"INSERT INTO bd_psndoc (pk_person, gh, xm, zzlx, zzhm, kjsrybm, kjsry, csny, xb, lxdh, sfgy, rzsgrq, sdyf, sfkcjcfy, bszt, pk_tax_class, xl, rydq, dr, create_time, update_time) VALUES ('{pk_person}', 'GH{i+1:05d}', '{fake.name()}', '1', '{zzhm}', '{kjsrybm}', '{fake.company()}', '{csny}', '{xb}', '{lxdh}', 'DOMESTIC', '{rzsgrq}', '{sdyf}', '1', '{bszt}', '{tc_data[0]}', '{xl}', 'DOMESTIC', 0, NOW(), NOW());")
print(f"-- 生成 500 条\n")

# 9. bd_psndoc_domestic - 300条
print("-- 9. bd_psndoc_domestic")
for i in range(300):
    pk = random.choice([p[0] for p in PK_PSNDOC_IDS[:300]])
    sfcj = random.choice(['0', '1'])
    sfgl = random.choice(['0', '1'])
    sfls = random.choice(['0', '1'])
    print(f"INSERT INTO bd_psndoc_domestic (pk_person, sfcj, sfgl, sfls, create_time, update_time, dr) VALUES ('{pk}', '{sfcj}', '{sfgl}', '{sfls}', NOW(), NOW(), 0);")
print(f"-- 生成 300 条\n")

# 10. bd_psndoc_overseas - 200条
print("-- 10. bd_psndoc_overseas")
countries = ['美国', '日本', '韩国', '英国', '德国', '新加坡', '香港', '澳大利亚']
for i in range(200):
    pk = random.choice([p[0] for p in PK_PSNDOC_IDS[300:500]])
    gj = random.choice(countries)
    csd = random.choice(countries)
    scrjsj = fake.date_between(start_date='-5y', end_date='-1y').strftime('%Y-%m-%d')
    print(f"INSERT INTO bd_psndoc_overseas (pk_person, gj, csd, scrjsj, create_time, update_time, dr) VALUES ('{pk}', '{gj}', '{csd}', '{scrjsj}', NOW(), NOW(), 0);")
print(f"-- 生成 200 条\n")

# 11. wa_tax_compute_record - 500条
print("-- 11. wa_tax_compute_record")
for i in range(500):
    psn_data = random.choice(PK_PSNDOC_IDS)
    sre = round(random.uniform(5000, 50000), 2)
    jcfy = 5000.0
    jbxf = round(sre * 0.08, 2)
    ylbxf = round(sre * 0.02, 2)
    sylbx = round(sre * 0.01, 2)
    gjj = round(sre * 0.12, 2)
    kcxm = jbxf + ylbxf + sylbx + gjj
    ynssde = max(0, sre - jcfy - kcxm)
    sl = random.choice([0.03, 0.10, 0.20, 0.25, 0.30])
    sskcs = random.choice([0, 210, 1410, 2660, 4410])
    ynse = max(0, round(ynssde * sl - sskcs, 2))
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    zzhm = fake.numerify(text='###########X')
    print(f"INSERT INTO wa_tax_compute_record (cp_id, nsrsbh, sdyf, pk_psndoc, xm, zzlx, zzhm, income_item_id, sre, jcfy, jbylaobxf, jbylbxf, sybxf, zfgjj, ynssde, sl, sskcs, ynse, status, source_type, dr, creator, create_time, modify_time) VALUES ({psn_data[1]}, '{fake.numerify(text='##########')}', '{sdyf}', '{psn_data[0]}', '{fake.name()}', '1', '{zzhm}', {random.randint(1,50)}, {sre}, {jcfy}, {jbxf}, {ylbxf}, {sylbx}, {gjj}, {ynssde}, {sl}, {sskcs}, {ynse}, 0, 'IMPORT', 0, 'system', NOW(), NOW());")
    WA_TAX_COMPUTE_RECORD_IDS.append(i+1)
print(f"-- 生成 500 条\n")

# 12. wa_tax_jmsx_detail - 300条
print("-- 12. wa_tax_jmsx_detail")
jmsx_names = ['随军家属免税', '军转干部免税', '自然灾害减免', '残疾人减免', '孤老减免']
for i in range(300):
    cr_id = random.choice(WA_TAX_COMPUTE_RECORD_IDS)
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    zzhm = fake.numerify(text='###########X')
    jmfs = random.choice([1, 2])
    jmsx = random.choice(jmsx_names)
    jmje = round(random.uniform(100, 2000), 2)
    print(f"INSERT INTO wa_tax_jmsx_detail (cp_id, compute_id, sdyf, zzhm, jmfs, jmsx, jmje, dr, creator, create_time, modify_time) VALUES ({random.choice(CP_IDS)}, {cr_id}, '{sdyf}', '{zzhm}', {jmfs}, '{jmsx}', {jmje}, 0, 'system', NOW(), NOW());")
print(f"-- 生成 300 条\n")

# 13. wa_tax_jz_detail - 250条
print("-- 13. wa_tax_jz_detail")
donation_orgs = ['中国红十字会', '中华慈善总会', '中国扶贫基金会', '希望工程']
for i in range(250):
    cr_id = random.choice(WA_TAX_COMPUTE_RECORD_IDS)
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    zzhm = fake.numerify(text='###########X')
    szdwmc = random.choice(donation_orgs)
    szdwnsrsbh = fake.numerify(text='##############')
    jzpzh = f"JZ{i+1:010d}"
    jzrq = fake.date_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d')
    jzje = round(random.uniform(100, 5000), 2)
    sjjze = round(random.uniform(100, 3000), 2)
    print(f"INSERT INTO wa_tax_jz_detail (cp_id, compute_id, sdyf, zzhm, szdwmc, szdwnsrsbh, jzpzh, jzrq, jzje, sjjze, dr, creator, create_time, modify_time) VALUES ({random.choice(CP_IDS)}, {cr_id}, '{sdyf}', '{zzhm}', '{szdwmc}', '{szdwnsrsbh}', '{jzpzh}', '{jzrq}', {jzje}, {sjjze}, 0, 'system', NOW(), NOW());")
print(f"-- 生成 250 条\n")

# 14. wa_tax_syjkbx_detail - 250条
print("-- 14. wa_tax_syjkbx_detail")
for i in range(250):
    cr_id = random.choice(WA_TAX_COMPUTE_RECORD_IDS)
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    zzhm = fake.numerify(text='###########X')
    sysbm = f"SY{i+1:010d}"
    bdsxrq = fake.date_between(start_date='-2y', end_date='-1y').strftime('%Y-%m-%d')
    ndbf = round(random.uniform(1200, 6000), 2)
    ydbf = round(random.uniform(100, 500), 2)
    bqkcje = round(random.uniform(100, 300), 2)
    print(f"INSERT INTO wa_tax_syjkbx_detail (cp_id, compute_id, sdyf, zzhm, sysbm, bdsxrq, ndbf, ydbf, bqkcje, dr, creator, create_time, modify_time) VALUES ({random.choice(CP_IDS)}, {cr_id}, '{sdyf}', '{zzhm}', '{sysbm}', '{bdsxrq}', {ndbf}, {ydbf}, {bqkcje}, 0, 'system', NOW(), NOW());")
print(f"-- 生成 250 条\n")

# 15. wa_tax_deduction_special_detail - 300条
print("-- 15. wa_tax_deduction_special_detail")
for i in range(300):
    psn = random.choice(PK_PSNDOC_IDS)
    tc = random.choice(PK_TAX_CLASS_IDS)
    taxperiod = fake.date_between(start_date='-1y', end_date='now').strftime('%Y-%m')
    znjyzc = round(random.uniform(0, 12000), 2)
    yyezhfzc = round(random.uniform(0, 12000), 2)
    jxjyzc = round(random.uniform(0, 4800), 2)
    zfzjzc = round(random.uniform(0, 18000), 2)
    zfdklxzc = round(random.uniform(0, 12000), 2)
    sylrzc = round(random.uniform(0, 24000), 2)
    grylj = round(random.uniform(0, 12000), 2)
    print(f"INSERT INTO wa_tax_deduction_special_detail (pk_wa_tax_deducti, cp_id, pk_tax_class, pk_psndoc, taxyear, taxperiod, znjyzc, yyezhfzc, jxjyzc, zfzjzc, zfdklxzc, sylrzc, grylj, update_time) VALUES ('{gen_pk('DED_')}', {psn[1]}, '{tc[0]}', '{psn[0]}', '2025', '{taxperiod}', {znjyzc}, {yyezhfzc}, {jxjyzc}, {zfzjzc}, {zfdklxzc}, {sylrzc}, {grylj}, NOW());")
print(f"-- 生成 300 条\n")

# 16. wa_tax_60k_deduction_detail - 200条
print("-- 16. wa_tax_60k_deduction_detail")
for i in range(200):
    psn = random.choice(PK_PSNDOC_IDS)
    tc = random.choice(PK_TAX_CLASS_IDS)
    print(f"INSERT INTO wa_tax_60k_deduction_detail (pk_wa_tax_deducti, cp_id, pk_tax_class, pk_psndoc, taxyear, sfkc, status) VALUES ('{gen_pk('60K_')}', {psn[1]}, '{tc[0]}', '{psn[0]}', '2024', 'Y', 'SUCCESS');")
print(f"-- 生成 200 条\n")

# 17. wa_tax_donation_detail - 250条
print("-- 17. wa_tax_donation_detail")
for i in range(250):
    psn = random.choice(PK_PSNDOC_IDS)
    tc = random.choice(PK_TAX_CLASS_IDS)
    taxperiod = fake.date_between(start_date='-6m', end_date='now').strftime('%Y-%m')
    donation_org_code = fake.numerify(text='##############')
    donation_org_name = random.choice(['中国红十字会', '中华慈善总会', '中国扶贫基金会'])
    donation_cert_no = f"CERT{i+1:010d}"
    donation_date = fake.date_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d')
    donation_amount = round(random.uniform(100, 10000), 2)
    deduction_ratio = random.choice([30, 50, 100])
    print(f"INSERT INTO wa_tax_donation_detail (pk_wa_tax_deducti, cp_id, pk_tax_class, pk_psndoc, taxyear, taxperiod, donation_org_code, donation_org_name, donation_cert_no, donation_date, donation_amount, deduction_ratio, status) VALUES ('{gen_pk('DN_')}', {psn[1]}, '{tc[0]}', '{psn[0]}', '2025', '{taxperiod}', '{donation_org_code}', '{donation_org_name}', '{donation_cert_no}', '{donation_date}', {donation_amount}, {deduction_ratio}, 'ACTIVE');")
print(f"-- 生成 250 条\n")

# 18. wa_tax_declaration - 200条
print("-- 18. wa_tax_declaration")
for i in range(200):
    psn = random.choice(PK_PSNDOC_IDS)
    tc = random.choice(PK_TAX_CLASS_IDS)
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    current_income = round(random.uniform(50000, 500000), 2)
    total_income = round(random.uniform(100000, 1000000), 2)
    tax_amount = round(random.uniform(5000, 100000), 2)
    tax_payers = random.randint(10, 200)
    print(f"INSERT INTO wa_tax_declaration (declaration_biz_id, cp_id, tax_class_code, nsrsbh, nsrsbh_name, sdyf, category_code, category_name, current_income, total_income, tax_amount, tax_payers, compute_status, declaration_type, declaration_status, dr, creator, create_time, modify_time) VALUES ('{gen_pk('DECL_')}', {psn[1]}, 'TAX{tc[2]:04d}', '{fake.numerify(text='##########')}', '{fake.company()}', '{sdyf}', '01', '综合所得', {current_income}, {total_income}, {tax_amount}, {tax_payers}, 0, 'NORMAL', 'UNREPORTED', 0, 'system', NOW(), NOW());")
print(f"-- 生成 200 条\n")

# 19. wa_tax_declaration_detail - 400条
print("-- 19. wa_tax_declaration_detail")
for i in range(400):
    psn = random.choice(PK_PSNDOC_IDS)
    sdyf = fake.date_between(start_date='-1y', end_date='now').strftime('%Y%m')
    sre = round(random.uniform(5000, 30000), 2)
    ynssde = max(0, sre - 5000)
    sl = random.choice([0.03, 0.10, 0.20, 0.25])
    ynse = round(ynssde * sl, 2)
    zzhm = fake.numerify(text='###########X')
    jbxf = round(sre * 0.08, 2)
    ylbxf = round(sre * 0.02, 2)
    sylbx = round(sre * 0.01, 2)
    gjj = round(sre * 0.12, 2)
    print(f"INSERT INTO wa_tax_declaration_detail (cp_id, nsrsbh, sdyf, category_code, pk_psndoc, xm, zzhm, sre, ynssde, sl, ynse, jcfy, jbylaobxf, jbylbxf, sybxf, zfgjj, create_time, update_time) VALUES ({psn[1]}, '{fake.numerify(text='##########')}', '{sdyf}', '01', '{psn[0]}', '{fake.name()}', '{zzhm}', {sre}, {ynssde}, {sl}, {ynse}, 5000, {jbxf}, {ylbxf}, {sylbx}, {gjj}, NOW(), NOW());")
print(f"-- 生成 400 条\n")

# 20. wa_tax_jmsx_dict - 100条
print("-- 20. wa_tax_jmsx_dict")
jmsx_list = [
    (1, '0101', '随军家属就业免征个人所得税'),
    (1, '0101', '军转干部免税'),
    (2, '0101', '自然灾害减免个人所得税'),
    (2, '0201', '残疾、孤老、烈属减免'),
]
for i in range(100):
    jm = jmsx_list[i % len(jmsx_list)]
    print(f"INSERT INTO wa_tax_jmsx_dict (jmfs, jmfs_name, income_item_id, sdxm, sdxm_name, jmsx, sort_order, enabled, dr, creator, create_time, modify_time) VALUES ({jm[0]}, '减免税额', {i % 50 + 1}, '{jm[1]}', '正常工资薪金', '{jm[2]}', {i+1}, 1, 0, 'system', NOW(), NOW());")
print(f"-- 生成 100 条\n")

# 21. operation_log - 500条
print("-- 21. operation_log")
op_types = ['TAX_CLASS_CREATE', 'PERSON_ADD', 'PERSON_UPDATE', 'TAX_COMPUTE', 'TAX_DECLARE', 'TAX_PAYMENT']
for i in range(500):
    op_time = fake.date_time_between(start_date='-6m', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    operator_name = fake.name()
    op_type = random.choice(op_types)
    client_ip = fake.ipv4()
    print(f"INSERT INTO operation_log (operation_time, operator_id, operator_name, operation_type, operation_desc, operation_result, client_ip, created_at, updated_at) VALUES ('{op_time}', {random.randint(1,100)}, '{operator_name}', '{op_type}', '操作描述{i}', 'SUCCESS', '{client_ip}', NOW(), NOW());")
print(f"-- 生成 500 条\n")

# 22. wa_tax_call_queue - 200条
print("-- 22. wa_tax_call_queue")
for i in range(200):
    tc = random.choice(PK_TAX_CLASS_IDS)
    print(f"INSERT INTO wa_tax_call_queue (pk_tax_process, pk_tax_class, interface_type, task_status, dr, creator, create_time) VALUES ('{gen_pk('QUEUE_')}', '{tc[0]}', 'SKJS', '02', 0, 'system', NOW());")
print(f"-- 生成 200 条\n")

print("-- =============================================")
print("-- 数据生成完成!")
print("-- =============================================")
