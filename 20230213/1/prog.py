#!/usr/bin/python3
import zlib
from glob import iglob

def get_branches():
    '''
    Возврашает словарь <ветка> : <путь> 
    '''
    return {branch.split('/')[-1]: branch for branch in iglob('../../.git/refs/heads/*', recursive=True)}


def get_last_commit(branch):
    '''
    Возвращает последний коммит ветки branch: <commit_message>, <commit_message>
    '''
    branches = get_branches()

    if branch not in branches.keys():
        return "Такой ветки не существует."

    
    with open(branches[branch], 'r') as commit_hash_file:
        commit_hash = commit_hash_file.read()
        commit_file_path = '../../.git/objects/' + commit_hash[0:2] + '/' + commit_hash[2:].replace('\n', '')
        

        with open(commit_file_path, 'rb') as commit_file:
            data = commit_file.read()
            commit_data = zlib.decompress(data)
            i = commit_data.rindex(b'+0300\n\n')
            commit_msg = commit_data[i + len(b'+0300\n\n'):]
            commit_data = str(commit_data[:i + len(b'+0300\n\n') - 1])
            j = commit_data.index('x00')
            commit_data = commit_data[j+3:len(commit_data) - 1].split('\\n')
            
            commit_data[2] = commit_data[2].split()
            commit_data[2] = ' '.join(commit_data[2][:len(commit_data[2]) - 2])
            commit_data[3] = commit_data[3].split()
            commit_data[3] = ' '.join(commit_data[3][:len(commit_data[3]) - 2])
            commit_msg = commit_msg.decode()
            commit_msg = commit_msg[:len(commit_msg) - 1]
            return commit_data, commit_msg


def tree(branch):
    '''
    Выводит объект-дерево, на который указывает последний коммит ветки branch
    '''
    commit_data, commit_msg = get_last_commit(branch)
    tree_hash = commit_data[0].split()[1]

    tree_file_path = '../../.git/objects/' + tree_hash[0:2] + '/' + tree_hash[2:].replace('\n', '')

    with open(tree_file_path, 'rb') as tree_file:
        tree_data = zlib.decompress(tree_file.read())
        data = tree_data.partition(b'\x00')[-1]
        while data:
            obj, _, data = data.partition(b'\x00')
            obj_mode, obj_name = obj.split()
            obj_num = data[:20].hex()
            data = data[20:]
            if obj_mode.decode() == '40000':
                obj_type = 'tree'
            if obj_mode.decode() == '100644':
                obj_type = 'blob'
            print(obj_type, obj_num, obj_name.decode())


def main():
    branch = input()
    tree(branch)
    # commit_data, commit_msg = get_last_commit(branch)
    # print(*commit_data, commit_msg, sep='\n')



if __name__ == "__main__":
    main()
