

# [forests1, forests2]
# [tree1, tree2]
# {'tree': treeid, 'top': [] or id_list, 'bottom': [] or id_list, 'left': [] or id_list, 'right': [] or id_list }
forests = [[{'tree': '66', 'top': ['141'], 'bottom': ['142'], 'left': [], 'right': ['78']}, {'tree': ' 65', 'top': ['118', '119'], 'bottom': ['120'], 'left': ['72'], 'right': ['73']}], [{'tree': ' 8', 'top': ['131'], 'bottom': ['108'], 'left': ['81'], 'right': ['82']}]]
def process_forests_info(forests, cards):
    info = []
    player_info = {}
    # [[{'tree': '66', 'top': ['141'], 'bottom': ['142'], 'left': [], 'right': ['78']}, {'tree': ' 65', 'top': ['118', '119'], 'bottom': ['120'], 'left': ['72'], 'right': ['73']}], [{'tree': ' 8', 'top': ['131'], 'bottom': ['108'], 'left': ['81'], 'right': ['82']}]]
    for forest in forests:
        player_info = {}
        tree_info = {
            "fushuCount": 0,
            "tree_name": "", # used by hongsongshu("xiangshu"),cangtouyanque("shanmaoju")
            "isGuanmu": False,
            "ChanchuCountUnderTheTree": 0, #  计算大蟾蜍时使用，两个大蟾蜍共享这个位置
        }
        forest_info = {
            # tree type count
            "duanshuCount": 0,
            "xiangshuCount": 0,
            "fullTreeCount": 0,
            "yinshanCount": 0,
            "baihuaCount": 0,
            "shanmaojuCount": 0,
            "meiguowutongCount": 0,
            "huaqisongCount": 0,
            "ouzhouqiyeshuCount": 0,
            "gaoshanluoyesongCount": 0, # pro1
            "ruishiwuyesongCount": 0,

            # tree count
            "shanmaojuTreeCount": 0,
            "ouzhouqiyeshuTreeCount": 0,
            "duanshuTreeCount": 0,
            
            # type symbol count
            "treeCount": 0, # include shumiao  used by dabanzhuomuniao
            "birdCount": 0,
            "plantCount": 0,
            "butterflyCount": 0,
            "liangqidongwuCount": 0,
            "batCount": 0,
            "deerCount": 0,
            "insectCount": 0,
            "outiCount": 0,
            "youzhuaCount": 0,
            "moguCount": 0,


            "goashanCount": 0,
            "lindibianyuanCount": 0,

            
            "downTreeCount": 0, # used by muyi, 位于树木下面的卡牌数量


            "butterflys": [],
            "yinghuochongCount": 0,

            "differentPlants": set(), # 毛地黄使用
            "differentBirds": set(), # 蓝莓使用



        }
        print(forest) # [{'tree': '66', 'top': ['141'], 'bottom': ['142'], 'left': [], 'right': ['78']}, {'tree': ' 65', 'top': ['118', '119'], 'bottom': ['120'], 'left': ['72'], 'right': ['73']}]
        for tree in forest:
            if tree['tree'] == 0:
                forest_info['treeCount'] += 1
                tree_info['tree_name'] = "shumiao"
            # tree
            if tree['tree'] in list(map(str, range(1, 10))): # duanshu
                forest_info['treeCount'] += 1
                forest_info['duanshuCount'] += 1
                forest_info['duanshuTreeCount'] += 1
                tree_info['tree_name'] = "duanshu"
            elif tree['tree'] in list(map(str, range(10, 17))): # xiangshu
                forest_info['treeCount'] += 1
                forest_info['xiangshuCount'] += 1
                tree_info['tree_name'] = "xiangshu"
            elif tree['tree'] in list(map(str, range(17, 23))): # yinshan
                forest_info['treeCount'] += 1
                forest_info['yinshanCount'] += 1
                tree_info['tree_name'] = "yinshan"
            elif tree['tree'] in list(map(str, range(23, 33))): # baihua
                forest_info['treeCount'] += 1
                forest_info['baihuaCount'] += 1
                tree_info['tree_name'] = "baihua"
            elif tree['tree'] in list(map(str, range(33, 43))): # shanmaoju
                forest_info['treeCount'] += 1
                forest_info['shanmaojuCount'] += 1
                forest_info['shanmaojuTreeCount'] += 1
                tree_info['tree_name'] = "shanmaoju"
            elif tree['tree'] in list(map(str, range(43, 49))): # meiguowutong
                forest_info['treeCount'] += 1
                forest_info['meiguowutongCount'] += 1
                tree_info['tree_name'] = "meiguowutong"
            elif tree['tree'] in list(map(str, range(49, 56))): # huaqisong
                forest_info['treeCount'] += 1
                forest_info['huaqisongCount'] += 1
                tree_info['tree_name'] = "huaqisong"
            elif tree['tree'] in list(map(str, range(56, 67))): # ouzhouqiyeshu
                forest_info['treeCount'] += 1
                forest_info['ouzhouqiyeshuCount'] += 1
                forest_info['ouzhouqiyeshuTreeCount'] += 1
                tree_info['tree_name'] = "ouzhouqiyeshu"
            elif tree['tree'] in ["A01", "A02", "A03", "A04", "A05", "A06", "A07"]:
                forest_info["tree_count"] += 1
                forest_info["gaoshanluoyesongCount"] += 1
                tree_info["tree_name"] = "ouzhouluoyesong"
                forest_info["goashanCount"] += 1
            elif tree['tree'] in ["A08", "A09", "A10", "A11", "A12", "A13", "A14"]:
                forest_info["tree_count"] += 1
                forest_info["ruishiwuyesongCount"] += 1
                tree_info["tree_name"] = "lisong"
                forest_info["goashanCount"] += 1

            # up
            if tree['up']:
                tree_info['fushuCount'] += len(tree['up'])
                for id in tree['up']:
                    idIncludeSide = f"{id}-up"
                    # 查找 "9-up" 对应的 name
                    card_info = next(
                        (item[idIncludeSide] for item in cards if idIncludeSide in item),
                        None  # 如果没有找到，返回 None（可选）
                    )
                    tree_type = card_info["color"]
                    forest_info[f"{card_info["color"]}Count"] += 1 # forest_info["duanshuCount"] += 1
                    # type include "insect, butterfly", bird, crawled
                    if "insect" in card_info['type']:
                        forest_info['insectCount'] += 1
                    if "butterfly" in card_info['type']:
                        forest_info['butterflyCount'] += 1
                        forest_info['butterflys'].append(card_info["name"])
                    if "bird" in card_info['type']:
                        forest_info['birdCount'] += 1
                        forest_info['differentBirds'].add(card_info['name'])
                    if 'crawled' in card_info['type']:
                        forest_info['youzhuaCount'] += 1

                    if "lindibianyuan" in card_info['type']:
                        forest_info['lindibianyuanCount'] += 1
                    if "gaoshan" in card_info['type']:
                        forest_info['goashanCount'] += 1

                pass

            # down
            if tree['down']:
                tree_info['fushuCount'] += len(tree['down'])
                forest_info['downTreeCount'] += len(tree['down'])
                for id in tree['down']:
                    idIncludeSide = f"{id}-down"
                    # 查找 "9-up" 对应的 name
                    card_info = next(
                        (item[idIncludeSide] for item in cards if idIncludeSide in item),
                        None  # 如果没有找到，返回 None（可选）
                    )
                    forest_info[f"{card_info["color"]}Count"] += 1 # forest_info["duanshuCount"] += 1
                    # type include mogu, insect, plant, xiyi,youzhua,lindibianyuan,gaoshan
                    if "insect" in card_info['type']:
                        forest_info['insectCount'] += 1
                    if "mogu" in card_info['type']:
                        forest_info['moguCount'] += 1
                    if "plant" in card_info['type']:
                        forest_info['plantCount'] += 1
                        forest_info['differentPlants'].add(card_info['name'])
                    if 'crawled' in card_info['type']:
                        forest_info['youzhuaCount'] += 1
                    if 'amphibian' in card_info['type']:
                        forest_info['liangqidongwuCount'] += 1

                    if "lindibianyuan" in card_info['type']:
                        forest_info['lindibianyuanCount'] += 1
                    if "gaoshan" in card_info['type']:
                        forest_info['goashanCount'] += 1

                    if card_info['name'] == "dachanchu":
                        tree_info['ChanchuCountUnderTheTree'] += 1
                    
                    if card_info['name'] == "yinghuochou":
                        forest_info['yinghuochongCount'] += 1

            # left
            if tree['left']:
                tree_info['fushuCount'] += len(tree['left'])
                pass

            # right
            if tree['right']:
                tree_info['fushuCount'] += len(tree['right'])
                pass

            # tree_all

            # forest_all
            if tree['up'] and tree['down'] and tree['left'] and tree['right']:
                forest_info['fullTreeCount'] += 1
            
            # butterfly ?
