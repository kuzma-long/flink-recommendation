# coding=utf-8
import math
from math import sqrt, pow
import operator
import random


class UserCf():

    def __init__(self, data):
        self.data = data

    def getItems(self, username1, username2):
        return self.data[username1], self.data[username2]

    def pearson(self, user1, user2):
        sumXY = 0.0
        n = 0
        sumX = 0.0
        sumY = 0.0
        sumX2 = 0.0
        sumY2 = 0.0
        try:
            for movie1, score1 in user1.items():
                if movie1 in user2.keys():
                    n += 1
                    sumXY += score1 * user2[movie1]
                    sumX += score1
                    sumY += user2[movie1]
                    sumX2 += pow(score1, 2)
                    sumY2 += pow(user2[movie1], 2)

            molecule = sumXY - (sumX * sumY) / n
            denominator = sqrt((sumX2 - pow(sumX, 2) / n) * (sumY2 - pow(sumY, 2) / n))
            r = molecule / denominator
        except Exception as e:
            print("异常信息:", e)
            return None
        return r

    def test1(self, user1, user2):

        # 取出两位用户评论过的电影和评分
        user1_data = self.data[user1]
        user2_data = self.data[user2]
        distance = 0
        common = {}

        # 找到两位用户都评论过的电影
        for key in user1_data.keys():
            if key in user2_data.keys():
                common[key] = 1
        if len(common) == 0:
            return 0  # 如果没有共同评论过的电影，则返回0
        n = len(common)  # 共同电影数目
        print(n, common)

        ##计算评分和
        sum1 = sum([float(user1_data[movie]) for movie in common])
        print(sum1)
        sum2 = sum([float(user2_data[movie]) for movie in common])
        print(sum2)
        ##计算评分平方和
        sum1Sq = sum([pow(float(user1_data[movie]), 2) for movie in common])
        sum2Sq = sum([pow(float(user2_data[movie]), 2) for movie in common])

        ##计算乘积和
        PSum = sum([float(user1_data[it]) * float(user2_data[it]) for it in common])
        print(PSum)
        ##计算相关系数
        num = PSum - (sum1 * sum2 / n)
        print(num)
        den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

        if den == 0:
            return 0
        r = num / den
        print(111111)
        print(r)
        return r

    def nearstUser(self, username, n=1):
        distances = {}
        for otherUser, items in self.data.items():
            if otherUser not in username:
                print(otherUser)
                distance = self.pearson(self.data[username], self.data[otherUser])
                if distance is None:
                    continue
                distances[otherUser] = distance
        print(distances)

        sortedDistance = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)
        print("排序后的用户为：", sortedDistance)
        return sortedDistance[:n]

    def recomand(self, username, n=1):
        recommand = {}
        for user, score in dict(self.nearstUser(username, n)).items():
            print("推荐的用户：", (user, score))
            for movies, scores in self.data[user].items():
                if movies not in self.data[username].keys():
                    print("%s为该用户推荐的：%s" % (user, movies))
                    if movies not in recommand.keys():
                        recommand[movies] = scores

        return sorted(recommand.items(), key=operator.itemgetter(1), reverse=True)

    def Euclidean(self, user1, user2):
        # 取出两位用户评论过的电影和评分
        user1_data = self.data[user1]
        user2_data = self.data[user2]
        distance = 0
        # 找到两位用户都评论过的电影，并计算欧式距离
        for key in user1_data.keys():
            if key in user2_data.keys():
                # 注意，distance越大表示两者越相似
                distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

        return 1 / (1 + sqrt(distance))  # 这里返回值越小，相似度越大

    # 计算某个用户与其他用户的相似度
    def top10_simliar(self, userID):
        res = []
        for userid in self.data.keys():
            # 排除与自己计算相似度
            if not userid == userID:
                simliar = self.Euclidean(userID, userid)
                res.append((userid, simliar))
        res.sort(key=lambda val: val[1])
        return res[:4]

    # 推荐商品给其他人
    def recommend(self, user):
        try:
            # 相似度最高的用户
            top_sim_user = self.top10_simliar(user)[0][0]
            print(top_sim_user)
            # 相似度最高的用户的观影记录
            items = self.data[top_sim_user]
            recommendations = []
            # 筛选出该用户未观看的电影并添加到列表中
            for item in items.keys():
                if item not in self.data[user].keys():
                    recommendations.append((item, items[item]))
            recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
            # 返回评分最高的10部电影
            if len(recommendations) == 1:
                recommendations = []
                lists = []
                for key, value in self.data.items():
                    for keys, values in value.items():
                        lists.append((keys, values))
                for i in range(4):
                    recommendations.append(random.choice(lists))
                recommendations = list(set(recommendations))

            return recommendations[:10]
        except:
            return ''

    # def ItemSimilarity(train):
    #     # 物品-物品的共同矩阵
    #     C = dict()
    #     # 物品被多少个不同用户购买
    #     N = dict()
    #     for u, items in train.items():
    #         for i in items.keys():
    #             N.setdefault(i, 0)
    #             N[i] += 1
    #             C.setdefault(i, {})
    #             for j in items.keys():
    #                 if i == j:
    #                     continue
    #                 C[i].setdefault(j, 0)
    #                 C[i][j] += 1
    #     # 计算相似度矩阵
    #     W = dict()
    #     for i, related_items in C.items():
    #         W.setdefault(i, {})
    #         for j, cij in related_items.items():
    #             W[i][j] = cij / math.sqrt(N[i] * N[j])
    #     return W


if __name__ == '__main__':
    users = {'root': {1: 5}, 'Annihilator': {38: 4.0}, '刷鞋大王': {39: 1.0}, 'Ashlynn': {40: 5.0}, '芽芽平安喜乐': {41: 4.0},
             '朝暮雪': {42: 2.0}, 'R荣十二': {43: 5.0}, '珍珠奶猹': {44: 5.0}, '朴灿烈': {45: 5.0}, '😈': {46: 5.0},
             '天下行走': {47: 1.0}, '不朽浩克': {48: 5.0}, '败雪、残鳞': {49: 1.0}, '谢谢你们的鱼': {50: 1.0}, '鸭博士': {51: 4.0},
             '也无风雨也无晴': {52: 4.0}, '任芙敏': {53: 4.0}, '丧气少女茄茄番': {54: 4.0}, '惨绿青年大学习': {55: 5.0}, 'hey': {56: 5.0},
             '魄魄_北平遗址': {57: 5.0}, '呆头猫猫': {58: 5.0}, '我是江湖骗子': {59: 4.0}, 'Runian': {60: 5.0}, '张凌岛': {61: 4.0},
             '操纵士peni鸲子': {62: 3.0}, '走开': {63: 4.0}, '寥原': {64: 3.0}, '阿甘正二': {65: 5.0}, '合欢': {66: 5.0},
             '雨后初晴': {67: 5.0}, 'Fenster': {68: 5.0}, '马尾鱼': {69: 4.0}, '逗瓣丸': {70: 5.0}, '威士忌与爱': {71: 4.0},
             '玫玫': {72: 5.0}, '诸事大吉': {73: 4.0}, '江湖骗子': {74: 4.0}, 'Miraitowa': {75: 1.0}, '小小小杯子': {76: 1.0},
             '陈年老大': {77: 2.0}, '陆冠均': {78: 4.0}, '聂小欠': {79: 4.0}, '水野': {80: 1.0}, '胡思': {81: 4.0}, '阿曼妮卡': {82: 3.0},
             '拿潘太克斯的熊📷': {83: 1.0}, 'SoldierBear': {84: 1.0}, '🎯志新': {85: 5.0}, '胡萝卜糊了': {86: 5.0}}

    # print(users)
    userCf = UserCf(data=users)
    # recommandList=userCf.recomand('root', 2)
    # print("最终推荐：%s"%recommandList)
    r = userCf.recommend('root')
    print(r)
