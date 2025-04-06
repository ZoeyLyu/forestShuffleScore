import json


def init(json_file):
    cards = []
    with open(json_file, 'r', encoding='utf-8') as f:
        cards = json.load(f)
        print(cards[0]) # [{'1': {'name': 'duanshu', 'color': 'duanshu', 'cost': 1, 'type': 'tree', 'condition': None, 'rewards': None, 'effect': None, 'score_rules': 'duanshuScore'}}]
    return cards

def parse_forest_string(forest_str):
    """解析森林字符串"""
    players = forest_str.split(';')
    forests = []
    for player in players:
        trees = player.split(',') if player else []
        forest = []
        for tree in trees:
            parts = tree.split('-')
            tree_id = parts[0]
            top = parts[1].split('/') if parts[1] else []
            bottom = parts[2].split('/') if parts[2] else []
            left = parts[3].split('/') if parts[3] else []
            right = parts[4].split('/') if parts[4] else []
            forest.append({
                'tree': tree_id,
                'top': top,
                'bottom': bottom,
                'left': left,
                'right': right
            })
        forests.append(forest)
    print(forests)
    return forests

def calculate_score(forest_str):
    """计算所有玩家的得分"""
    forests = parse_forest_string(forest_str)
    scores = []
    for i, forest in enumerate(forests):
        print(f"\n=== 玩家 {i+1} 得分明细 ===")
        score = calculate_player_score(forest)
        scores.append(score)
        print(f"玩家 {i+1} 总分: {score}\n")
    return scores

def calculate_player_score(forest):
    return 2




cards_file = 'based_cards.json'
cards = init(cards_file)
inputs = "66-141-142--78, 65-118/119-120-72-73; 8-131-108-81-82"
#forests = parse_forest_string(inputs)
# [[{'tree': '66', 'top': ['141'], 'bottom': ['142'], 'left': [], 'right': ['78']}, {'tree': ' 65', 'top': ['118', '119'], 'bottom': ['120'], 'left': ['72'], 'right': ['73']}], [{'tree': ' 8', 'top': ['131'], 'bottom': ['108'], 'left': ['81'], 'right': ['82']}]]
#print(forests)

scores = calculate_score(inputs)