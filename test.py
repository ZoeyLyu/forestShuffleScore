import json
from collections import defaultdict

class ForestScorer:
    def __init__(self, cards_json):
        """初始化计分器，加载卡牌数据"""
        with open(cards_json, 'r', encoding='utf-8') as f:
            self.cards = json.load(f)
        self.card_dict = self.cards
        
    def parse_forest_string(self, forest_str):
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
        return forests
    
    def calculate_score(self, forest_str):
        """计算所有玩家的得分"""
        forests = self.parse_forest_string(forest_str)
        scores = []
        for i, forest in enumerate(forests):
            print(f"\n=== 玩家 {i+1} 得分明细 ===")
            score = self.calculate_player_score(forest)
            scores.append(score)
            print(f"玩家 {i+1} 总分: {score}\n")
        return scores
    
    def calculate_player_score(self, forest, card_dict):
        """计算单个玩家的得分"""
        total_score = 0
        visible_cards = set()
        card_counts = defaultdict(int)
        species_counts = defaultdict(int)
        tree_types = set()
        position_counts = defaultdict(int)
        
        # 收集所有可见卡牌和统计信息
        for tree in forest:
            tree_card = self.card_dict.get(tree['tree'])
            if tree_card:
                visible_cards.add(tree['tree'])
                if tree_card['type'] == 'tree':
                    tree_types.add(tree_card['color'])
            for position in ['top', 'bottom', 'left', 'right']:
                for card_id in tree[position]:
                    if card_id:
                        card = card_dict.get(f"{card_id}-{position}")
                        if card:
                            visible_cards.add(f"{card_id}-{position}") # f"{card_id}-{position}"
                            card_counts[card['name']] += 1
                            species_counts[card['type']] += 1
                            position_counts[position] += 1
        
        # 计算树木得分
        tree_score = 0
        for tree in forest:
            tree_card = card_dict.get(tree['tree'])
            if tree_card and tree_card['type'] == 'tree':
                # 基础分
                tree_score += tree_card['base_points']
                
                # 检查树木是否被占满
                is_full = all(tree[pos] for pos in ['top', 'bottom', 'left', 'right'])
                if is_full and 'full_tree_bonus' in tree_card:
                    tree_score += tree_card['full_tree_bonus']
                    print(f"{tree_card['name']} 被占满奖励: +{tree_card['full_tree_bonus']}分")
                
                print(f"{tree_card['name']}: {tree_card['base_points']}分")
        
        total_score += tree_score
        print(f"树木总分: {tree_score}")
        
        # 计算生物卡牌得分
        creature_score = 0
        bonus_details = defaultdict(list)
        
        for card_id in visible_cards:
            card = self.card_dict.get(card_id)
            if card and card['type'] != 'tree':
                # 基础分
                creature_score += card['base_points']
                print(f"{card['name']} 基础分: {card['base_points']}分")
                
                # 检查奖励条件
                if 'bonus_conditions' in card:
                    for condition in card['bonus_conditions']:
                        met = False
                        bonus_points = condition['points']
                        
                        if condition['type'] == 'same_species_count':
                            count = species_counts.get(card['species'], 0)
                            if count >= condition['threshold']:
                                met = True
                                bonus_details[card['name']].append(
                                    f"{condition['description']}: +{bonus_points}分"
                                )
                                
                        elif condition['type'] == 'different_species_count':
                            unique_species = set()
                            for cid in visible_cards:
                                c = self.card_dict.get(cid)
                                if c and c['species'] in condition['species_list']:
                                    unique_species.add(c['species'])
                            if len(unique_species) >= condition['threshold']:
                                met = True
                                bonus_details[card['name']].append(
                                    f"{condition['description']}: +{bonus_points}分"
                                )
                                
                        elif condition['type'] == 'position_count':
                            count = position_counts.get(condition['position'], 0)
                            if count >= condition['threshold']:
                                met = True
                                bonus_details[card['name']].append(
                                    f"{condition['description']}: +{bonus_points}分"
                                )
                        
                        if met:
                            creature_score += bonus_points
        
        # 打印奖励详情
        for card_name, bonuses in bonus_details.items():
            for bonus in bonuses:
                print(f"{card_name} {bonus}")
        
        total_score += creature_score
        print(f"生物卡牌总分: {creature_score}")
        
        # 洞穴卡牌数量（简化处理，假设每张洞穴卡1分）
        cave_cards = 0  # 实际应从输入获取
        total_score += cave_cards
        print(f"洞穴卡牌: +{cave_cards}分")
        
        return total_score


# 示例使用
if __name__ == "__main__":
    # 假设cards.json包含所有卡牌数据
    scorer = ForestScorer('based_cards.json')
    
    # 示例森林字符串
    # 格式："树木ID-上-下-左-右,另一棵树...;另一玩家..."
    example_forest = (
        "T1-T1U-T1D-T1L-T1R,T2-T2U-T2D-T2L-T2R;"
        "T3-T3U-T3D-T3L-T3R"
    )
    
    scores = scorer.calculate_score(example_forest)
    print("最终得分:", scores)