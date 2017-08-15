# -*- coding: utf-8 -*-
import json
import requests
from lib.common import check_in_file
from config import conf
from lib.common import get_int, dict2file, do_ten_times_til_true

class chromeStoreSpider(object):
    ext_item_url='https://chrome.google.com/webstore/ajax/item?hl=zh-CN&gl=US&pv=20170206&mce=atf%2Ceed%2Cpii%2Crtr%2Crlb%2Cgtc%2Chcn%2Csvp%2Cwtd%2Cc3d%2Cncr%2Cctm%2Cac%2Chot%2Cmac%2Cfcf%2Crma%2Cigb%2Cpot%2Cevt&requestedCounts=mcol%23personalize_chrome%3A11%3A1%3Atrue%2Cmcol%23screen_capture%3A11%3A1%3Atrue%2Cmcol%23artistic_extension%3A11%3A1%3Atrue%2Cmcol%23chrome_toolkit%3A11%3A1%3Atrue%2Cmcol%23games_extension%3A11%3A1%3Atrue%2Cmcol%23social%3A11%3A1%3Atrue%2Cmcol%23pdf_extensions%3A11%3A1%3Atrue%2Cmcol%23lifehacker%3A11%3A1%3Atrue%2Cmcol%233p_accessibility_extensions%3A11%3A1%3Atrue%2Cmcol%23customize_your_new_tab_page%3A11%3A1%3Atrue&token=featured%3A0%402720145%3A6%3Afalse%2Cmcol%23get_started%3A0%402720146%3A12%3Atrue%2Cmcol%23new_noteworthy_extensions%3A0%402720147%3A12%3Atrue%2Cmcol%23editors_picks_extensions%3A0%402720148%3A12%3Atrue%2Cmcol%23spring_cleaning%3A0%402720149%3A12%3Atrue&category=extensions&_reqid=279129&rt=j'
    def __init__(self):
        super(chromeStoreSpider, self).__init__()
        self.json_path = conf['data_file']
    
    def run(self):
        url = self.ext_item_url.format()
        res = self.get_ext_item_reps(url)
        jsonlist = self._res_to_info_list(res)
        if jsonlist:
            for json in jsonlist:
                id_str, users, info = self._list2info(json)
                if users >= conf['more_then_user_num']:
                    print('[*] id : %s'%id_str)
                    dict2file(info, path=self.json_path)
                else:
                    break

    def _list2info(self, list):
        if list:
            try:
                id_str = list[0]
                users = get_int(str(list[23]))
                info = {
                    "id" : id_str,
                    "name" : list[1],
                    "stars" : list[22],
                    "users" : list[23],
                    "category" : list[9],
                    "url" : list[37]
                }
                return (id_str, users, info)
            except IndexError as e:
                # raise e
                # import pdb;pdb.set_trace()
                pass

    @do_ten_times_til_true
    def get_ext_item_reps(self, url):
        # 尝试请求十次防止请求失败，数据丢失。
        try:
            response = requests.post(url, verify=False,\
                    allow_redirects=False, timeout=10, headers=conf['HTTP_HEADERS'])
            res = response.text
            if response.status_code != 200:
                raise requests.RequestException(u"Status code error: {}".format(response.status_code))
            if response.status_code == 200:
                return res
        except requests.RequestException as e:
            return False

    def _res_to_info_list(self, res=''):
        if res:
            infojson = json.loads(res.lstrip(")]}'\n"))
            a=infojson[0][1][7]
            b=[]
            c=[]
            for i in range(0,10):
                for j in range(0,10):
                    c=a[i][1][j]
                    b.append(c)
            return b

        else: 
            # import pdb;pdb.set_trace()
            # raise Exception() 
            pass


