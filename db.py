from sqlitedict import SqliteDict


def get_target_data(target_db):
    target_data = SqliteDict(target_db, autocommit=True)
    result_dict = dict()
    for key in target_data:
        result_dict[key] = target_data[key]
    target_data.close()
    return result_dict


if __name__ == "__main__":
    test_dict = get_target_data("./db/ASE2022.sqlite")
    test_dict = test_dict["ASE2022"]
    name_lst = list()
    for name in test_dict:
        if test_dict[name][2].find("test") != -1 or test_dict[name][2].find("fuzz") != -1 or test_dict[name][2].find("Test") != -1 or test_dict[name][2].find("Fuzz") != -1 or test_dict[name][2].find("edurity") != -1:
            name_lst.append(name)
    test_dict = get_target_data("./db/icse2023.sqlite")
    test_dict = test_dict["ICSE2023"]
    new_name_lst = list()
    for name in name_lst:
        if name in test_dict:
            new_name_lst.append((name, test_dict[name]))
            # print("name: " + name + " " + str(test_dict[name]))
    new_name_lst.sort(key=lambda x: len(x[1][2]))
    for name in new_name_lst:
        print(name)

