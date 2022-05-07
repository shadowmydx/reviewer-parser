from sqlitedict import SqliteDict


def get_target_data(target_db):
    target_data = SqliteDict(target_db, autocommit=True)
    result_dict = dict()
    for key in target_data:
        result_dict[key] = target_data[key]
    target_data.close()
    return result_dict


if __name__ == "__main__":
    test_dict = get_target_data("./db/icse2023.sqlite")
    for name in test_dict["ICSE2023"]:
        if test_dict["ICSE2023"][name][2].find("test") != -1 or test_dict["ICSE2023"][name][2].find("fuzz") != -1 or test_dict["ICSE2023"][name][2].find("Test") != -1 or test_dict["ICSE2023"][name][2].find("Fuzz") != -1 or test_dict["ICSE2023"][name][2].find("edurity") != -1:
            print(name + ": " + str(test_dict["ICSE2023"][name]))

