# 以下是输入的策略文本，它包含了一系列的访问控制列表策略，每条策略有不同的规则和命中计数信息
policy_text = """
access-list out_to_in line 712 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.71.7 eq 7721 (hitcnt=0) 0xc5d2107c 
access-list out_to_in line 713 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.71.7 eq 12300 (hitcnt=0) 0xa78787b0 
access-list out_to_in line 714 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.71.10 eq 7001 (hitcnt=0) 0xa57dc031 
access-list out_to_in line 715 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.71.10 eq 8021 (hitcnt=0) 0x476a82b9 
access-list out_to_in line 716 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.16.52 eq 7001 (hitcnt=0) 0x3bed2dbe 
access-list out_to_in line 717 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.16.52 eq 7002 (hitcnt=0) 0x88beb100 
access-list out_to_in line 718 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.16.52 eq 7005 (hitcnt=0) 0x312d685b 
access-list out_to_in line 719 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.16.52 eq 8021 (hitcnt=0) 0x810589a8 
access-list out_to_in line 720 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.16.52 eq 8022 (hitcnt=0) 0xfb6e9aa9 
access-list out_to_in line 721 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.18.50 eq 9081 (hitcnt=3) 0x55ca63c8 
access-list out_to_in line 722 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.18.54 eq www (hitcnt=4) 0x6f0d50b7 
access-list out_to_in line 723 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.18.51 eq 5100 (hitcnt=5) 0x9960c2dc 
access-list out_to_in line 724 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.18.51 eq 8000 (hitcnt=0) 0xbe67313b 
access-list out_to_in line 725 extended permit tcp 10.128.76.0 255.255.255.0 host 10.192.18.35 eq www (hitcnt=0) 0x4b6fd5fa
"""

# 把输入的策略文本去除首尾的空白字符，并按换行符分割成一个策略列表
policies = policy_text.strip().split('\n')

# 初始化一个空列表，用于存储未命中的策略
unused_policies = []

# 遍历策略列表中的每一条策略
for policy in policies:
    # 查找策略中 "(hitcnt=" 字符串的起始位置
    start_index = policy.find("(hitcnt=")
    # 如果找到了 "(hitcnt="
    if start_index != -1:
        # 查找对应的 ")" 的位置
        end_index = policy.find(")", start_index)
        # 如果也找到了 ")"
        if end_index != -1:
            # 提取出命中计数的字符串部分
            hit_count_str = policy[start_index + len("(hitcnt="):end_index]
            try:
                # 把命中计数的字符串转换为整数
                hit_count = int(hit_count_str)
                # 如果命中计数为 0，说明该策略未命中
                if hit_count == 0:
                    # 将未命中的策略添加到 unused_policies 列表中
                    unused_policies.append(policy)
            except ValueError:
                # 如果转换整数失败，跳过这条策略，继续处理下一条
                continue

# 初始化一个空列表，用于存储删除未命中策略的配置脚本
delete_scripts = []

# 遍历未命中的策略列表
for policy in unused_policies:
    # 查找策略中 "line " 字符串的起始位置，并加上 "line " 的长度，定位到行号的起始位置
    line_start_index = policy.find("line ") + len("line ")
    # 查找行号后面的第一个空格位置，确定行号的结束位置
    line_end_index = policy.find(" ", line_start_index)
    # 提取出行号
    line_number = policy[line_start_index:line_end_index]
    # 生成删除该未命中策略的配置脚本
    delete_script = f"no access-list out_to_in line {line_number}"
    # 将生成的删除脚本添加到 delete_scripts 列表中
    delete_scripts.append(delete_script)

# 打印提示信息，表明接下来要输出未命中的策略
print("未命中的策略:")
# 遍历未命中的策略列表并打印每一条策略
for policy in unused_policies:
    print(policy)

# 打印提示信息，表明接下来要输出删除未命中策略的配置脚本
print("\n删除未命中项的配置脚本:")
# 遍历删除脚本列表并打印每一条脚本
for script in delete_scripts:
    print(script)

# 打开一个名为 delete_unused_policies.txt 的文件，以写入模式操作
with open('delete_unused_policies.txt', 'w') as f:
    # 遍历删除脚本列表
    for script in delete_scripts:
        # 将每条删除脚本写入文件，并添加换行符
        f.write(script + '\n')

# 打印提示信息，告知用户删除脚本已保存到指定文件
print("\n删除脚本已保存到 delete_unused_policies.txt")