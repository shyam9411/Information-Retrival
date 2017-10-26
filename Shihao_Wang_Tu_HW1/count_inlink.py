import json
import os

in_link_file = open(os.getcwd()+'/json_file/dfs_in_link_dict.json', 'r')
out_link_file = open(os.getcwd()+'/json_file/bfs_in_link_dict.json', 'r')
D_LINK = json.load(in_link_file)
B_LINK = json.load(out_link_file)

for i in B_LINK:
    B_LINK[i] = len(B_LINK[i])
for i in D_LINK:
    D_LINK[i] = len(D_LINK[i])

D_LINK = sorted(D_LINK.items(), key=lambda x: x[1], reverse=True)
B_LINK = sorted(B_LINK.items(), key=lambda x: x[1], reverse=True)

print(D_LINK)
