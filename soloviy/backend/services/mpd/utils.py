def group_by_folders(data: list[dict]) -> dict[list[dict]]:
    res = dict()
    for item in data:
        if directory := item.get("directory"):
            res[directory] = []
            partial_res = res[directory]
            continue
        partial_res.append(item)
    return res
