'''
Descripttion: 
version: 
Author: sch
Date: 2020-10-21 14:12:46
LastEditors: sch
LastEditTime: 2020-10-22 18:44:58
'''
import numpy as np
from ase.visualize import view
from ase.io import read
from ase.build import cut
from .distance_bet_plane import inner_product, distance_bet_sites, vector_minus, epsilon_criterion
import random
epsilon = 0.3  # delta z < epsilon： sites处于同层
number_per_layer = 100  # 每层最多30个原子


class vacancyMigration1(object):
    def __init__(self, cifFile=' '):
        # 类传参，可无
        self.cifFile = cifFile

        self.crystal = read(cifFile)

        # 得到所有阵点之间的距离
        self.distances_bet_sites = self.crystal.get_all_distances()

        # 得到所有阵点的坐标(index --> atoms的编号), 并转化成list形式
        # 95个sites
        self.site_positions = list(list(x)
                                   for x in self.crystal.get_positions())


# 一、 原子分层

    def get_layers(self):
        # (1) 取出所有阵点的z(unrepeated)，z的数目 代表 层数
        self.z_lst = [0]
        mark = 1
        for i in self.site_positions:
            mark = 1
            for j in self.z_lst:
                if (epsilon_criterion(x=i[2], standard=j, epsilon=epsilon)):
                    mark = 0
                    break

            if (mark == 1):
                self.z_lst.append(i[2])
        self.z_lst.remove(0)
        #print(z_lst)

        # (2) 将不同层(z不同)原子分组
        # note: [[]] * num : 一种极其傻逼的定义多维数组的方式
        self.siteLabel_per_layer = [[] for i in range(len(self.z_lst))]
        for i in self.site_positions:
            for j in self.z_lst:
                if (epsilon_criterion(x=i[2], standard=j, epsilon=epsilon)):
                    '''
                    print(j, i[2])
                    print(z_lst.index(j))
                    '''
                    '''
                    print("编号为 {0} 的原子属于 {1} 层".format(
                        self.site_positions.index(i), self.z_lst.index(j)))
                    '''
                    self.siteLabel_per_layer[self.z_lst.index(j)].append(
                        self.site_positions.index(i))

    # 计算层间距离
    def distances_bet_plane(self):
        self.get_layers()

        for i in range(len(self.z_lst)):
            for j in range(len(self.z_lst)):
                if (i < j):
                    minus_vector = vector_minus(
                        self.site_positions[self.siteLabel_per_layer[i][0]], self.site_positions[self.siteLabel_per_layer[j][0]])
                    distance = inner_product(minus_vector, [0, 0, 1])
                    #distance_bet_planes.append(abs(distance))
                    print("第 {0} 层 和 第 {1} 层的层间距离为 {2}".format(
                        i, j, abs(distance)))

    # 单层可视化
    def view_layer(self):
        layer3_atom = cut(self.crystal, a=[1, 0, 0], b=[
                          0, 1, 0], c=[0, 0, 1], nlayers=1, origo=48)
        view(layer3_atom)


# 二、 找出空位可能扩散的位点

    # (1) 取出原子的两特殊原子层，此处为3和4层（0-indexed）
    def get_diffusion_layers(self):
        self.get_layers()

        self.layer3 = self.siteLabel_per_layer[3]     # layer: 16个原子
        self.layer4 = self.siteLabel_per_layer[4]     # layer: 15个原子
        print("编号为3的层内含有原子: ", self.layer3,
              "\n总计{0}个".format(len(self.layer3)))
        print("编号为4的层内含有原子: ", self.layer4,
              "\n总计{0}个".format(len(self.layer4)))

    # (2) 找出同层内的最邻近原子（最近的2/4/6个原子)
    # center为中心原子
    def get_nearest_sites_sameplane(self, center=57):
        self.center = center
        self.get_diffusion_layers()
        #print('\n')

        # (2.1) 在layer3中，以某一原子找出相邻原子的大致距离
        sites_distance_sameplane = []
        if self.center in self.layer3:
            for i in self.layer3:
                # 选取不同的中心原子layer3:16个(48~63号)，此处选择9号原子。 layer4:15个(64~78号)
                sites_distance_sameplane.append(self.distances_bet_sites[self.center][i])
        if self.center in self.layer4:
            for i in self.layer4:
                sites_distance_sameplane.append(self.distances_bet_sites[self.center][i])
        # 去除 1 ，因为np.sort(self.sites_distance_sameplane)[0] = 0
        self.nearest_criterion_sameplane = np.sort(sites_distance_sameplane)[1]
        print("层内相邻原子间距为：", sites_distance_sameplane)

        # (2.2) 以相邻原子间距为判据，找出某原子的所有相邻原子
        self.nearest_sites_samelayer = []
        if self.center in self.layer3:
            for i in self.layer3:
                #print(distances_bet_sites[55][i], nearest_criterion)
                if (epsilon_criterion(x=self.distances_bet_sites[self.center][i], standard=self.nearest_criterion_sameplane, epsilon=epsilon)):
                    self.nearest_sites_samelayer.append(i)
        if self.center in self.layer4:
            for i in self.layer4:
                if (epsilon_criterion(x=self.distances_bet_sites[self.center][i], standard=self.nearest_criterion_sameplane, epsilon=epsilon)):
                    self.nearest_sites_samelayer.append(i)
        print("同层原子间距为：{}".format(self.nearest_criterion_sameplane))
        print('以编号为{}原子为中心，同层内最邻近原子为: '.format(center), self.nearest_sites_samelayer)
        return self.nearest_sites_samelayer

    # (3) 寻找异层内最近原子
    def get_nearest_sites_diffplane(self, center=57):
        self.center = center
        #self.get_nearest_sites_sameplane(center=self.center)
        self.get_diffusion_layers()
        #print('\n')

        # (3.1) 以layer3中某原子为中心，并寻找其距layer4中的最邻近原子的距离
        sites_distance_diffplane = []
        
        if self.center in self.layer3:
            for i in self.layer4:
                sites_distance_diffplane.append(self.distances_bet_sites[self.center][i])
        if self.center in self.layer4:
            for i in self.layer3:
                sites_distance_diffplane.append(self.distances_bet_sites[self.center][i])
        self.nearest_criterion_diffplane = np.sort(sites_distance_diffplane)[1]
        #print(np.sort(sites_distance_diffplane))

        # (3.2) 以异层的相邻原子间距为判据，找出某原子的所有异层相邻原子
        self.nearest_sites_difflayer = []
        if self.center in self.layer3:
            for i in self.layer4:
                #print(distances_bet_sites[55][i], nearest_criterion)
                if (epsilon_criterion(x=self.distances_bet_sites[self.center][i], standard=self.nearest_criterion_diffplane, epsilon=epsilon)):
                    self.nearest_sites_difflayer.append(i)
        if self.center in self.layer4:
            for i in self.layer3:
                if (epsilon_criterion(x=self.distances_bet_sites[self.center][i], standard=self.nearest_criterion_diffplane, epsilon=epsilon)):
                    self.nearest_sites_difflayer.append(i)
        print("异层原子间距为：{}".format(self.nearest_criterion_diffplane))
        print('以编号为{}原子为中心，异层间最邻近原子及异层为: '.format(self.center), self.nearest_sites_difflayer)
        return self.nearest_sites_difflayer


# 三、 氧空位随机扩散n步
    def migration_nsteps(self, center=57, nsteps=5):
        self.center = center
        self.nsteps = nsteps

        self.center_lst = [self.center]
        for i in range(nsteps):
            print("\n\n\n第{0}步扩散具体情况：".format(i+1))
            # prob_sites 是可能的扩散位点
            prob_site = self.get_nearest_sites_sameplane(center=self.center) + self.get_nearest_sites_diffplane(center=self.center)
            self.center = random.choice(prob_site)
            self.center_lst.append(self.center)
        
        print("空位扩散路径为: ", center, end='')
        for i in range(1, len(self.center_lst)):
            print('->{0}'.format(self.center_lst[i]), end='')
        print('\n')
        return self.center


if __name__ == '__main__':
    motion = vacancyMigration1(cifFile='/Users/mac/desktop/CONTCAR.cif')
    # motion.get_nearest_sites_sameplane(center=57)
    motion.migration_nsteps(center=57, nsteps=5)