import requests
import sys
from bs4 import BeautifulSoup
from sqlitedict import SqliteDict


def url_request(target_url):
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def default_pc_parser(target_lst):
    return target_lst[0]


def parse_personal_research_interest(target_url):
    soup = url_request(target_url)
    all_divs = soup.find_all("div", "profile-item")
    for single_div in all_divs:
        title_msg = single_div.find("span").text
        if title_msg.find("interests") != -1:
            return single_div.find(text=True, recursive=False)
    return None


def parse_single_pc_member(single_pc_member):
    result_lst = list()
    research_interest = None
    personal_page = single_pc_member.find("a", "navigate")
    if personal_page is not None:
        research_interest = parse_personal_research_interest(personal_page.get("href"))
    personal_information = single_pc_member.find("div", "media-body")
    personal_information = personal_information.find_all("h5", "media-heading")
    for each_item in personal_information:
        target_str = each_item.find(text=True, recursive=False)
        result_lst.append(target_str if target_str is not None and len(target_str) != 0 else each_item.text)
    pc_name, pc_university, pc_nation = tuple(
        [result_lst[index] if index < len(result_lst) else None for index in range(3)])
    return pc_name, pc_university, pc_nation, research_interest


def retrieve_information_to_dict(target_url, conference_name, pc_parser=None):
    result_dict = dict()
    result_dict[conference_name] = dict()
    soup = url_request(target_url)
    target_lst = soup.find_all("ul", "list-group")
    if pc_parser is not None:
        target_lst = pc_parser(target_lst)
    else:
        target_lst = target_lst[1]
    print(len(target_lst))
    for lst_item in target_lst:
        name, university, nation, research_interest = parse_single_pc_member(lst_item)
        result_dict[conference_name][str(name).strip()] = (str(university).strip(), str(nation).strip(), str(research_interest).strip())
        print("Finished parsing " + ",".join(
            [str(name).strip(), str(university).strip(), str(nation).strip(), str(research_interest).strip()]))
    return result_dict


def store_information(target_dict, target_path):
    store_dict = SqliteDict(target_path, autocommit=True)
    for key in target_dict:
        store_dict[key] = target_dict[key]
        for name in target_dict[key]:
            store_dict[key][name] = target_dict[key][name]
    store_dict.close()


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    print(sys.getrecursionlimit())
    # test_dict = retrieve_information_to_dict("https://conf.researchr.org/track/ase-2022/ase-2022-research-papers",
    #                                          "ASE2022")
    # store_information(test_dict, "./db/ase2022.sqlite")
    test_dict = retrieve_information_to_dict("https://conf.researchr.org/track/icse-2023/icse-2023-technical-track", "ICSE2023", default_pc_parser)
    store_information(test_dict, "./db/icse2023.sqlite")

