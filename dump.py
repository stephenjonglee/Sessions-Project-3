#!/usr/bin/python3

# imports
import sys
import requests


# function to check if there is an argument
# there should only be one extra argument: the server
def check_arg():
    num_arg = len(sys.argv)
    if num_arg != 2:
        return False
    else:
        return True


# function get argument
def get_arg():
    arg = sys.argv
    return arg[1]


# function get keys of the kv-pair
# param: url of the server
def get_keys(url):
    # request to get list of keys
    response = requests.get(url)
    if response.status_code != 200:
        print("request error")
        return 0
    return response.json()


# function get the key-value pair
# params: url of server and list of keys
def kv(url, keys):
    kv_list = []
    for key in keys["keys"]:
        # request to get key value pair of a specific key
        response = requests.get(f"{url}/{key}")
        if response.status_code != 200:
            print("request error")
            return 0
        kv_list.append(response.text)
    return kv_list


# main function
def main():
    if not check_arg():
        print("arg error")
    else:
        url = get_arg()
        # print(url)
        keys = get_keys(url)
        # print(keys)
        # print(keys["keys"])
        kv_list = kv(url, keys)
        for item in kv_list:
            print(item)


# run main
if __name__ == "__main__":
    main()

# example of requests
# resp = requests.get('https://todolist.example.com/tasks/')
# if resp.status_code != 200:
#     # This means something went wrong.
#     raise ApiError('GET /tasks/ {}'.format(resp.status_code))
# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))

# example of request
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# r.status_code
# 200
# r.headers['content-type']
# 'application/json; charset=utf8'
# r.encoding
# 'utf-8'
# r.text
# '{"type":"User"...'
# r.json()
# {'private_gists': 419, 'total_private_repos': 77, ...}
