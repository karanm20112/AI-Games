"""
Name: Jeet Thakur, Karan pankaj Makhija
Title: Agent1
Version: Python 2.7
"""
import argparse
import sys, numpy, random, math
# import pdb
import gym
from gym import wrappers, logger
import numpy as np
import platform

print(platform.python_version())

class Agent(object):

    def __init__(self, action_space):
        self.action_space = action_space


        self.exit = []

    def exitpass(self, myrow, mycol, r, c, wall, mypos, er, ec):
        """
              This method is used when all the enemies are died and then the agent tries to exit the maze and clear the level
              :param myrow: Current agent row
              :param mycol: Current agent column
              :param r: r is the row location of exit pass
              :param c: c is the column location of exit pass
              :param wall: wall list
              :param mypos: mypos list
              :param er: enemy row
              :param ec: enemy column
              :return: The action to be perfomed
              """
        flag = True
        if r == 180:
            r = r - 5
            for i in range(myrow, r - 10):
                if [i, mycol] in wall:
                    print(True)
                    flag = False
            if not flag:
                act = self.follow_coll(myrow, mycol, r, c, wall, mypos)
                return act
            act = self.nowperform(mypos[-1][0], mypos[-1][1], wall, mypos, er, ec, r, c)
            if act == 11:
                act = 3
            if act == 13 or act == 12:
                act = 5
            if mypos[-1][1] - 10 > c - 20 and mypos[-1][1] < c + 20:
                return 5
            return act
        if r == 5:
            r = r + 5

            act = self.nowperform(myrow, mycol, wall, mypos, er, ec, r, c)
            if act == 12:
                act = 4
            if act == 10:
                act = 2
            elif mypos[0][1] > c - 15 and mypos[0][1] < c + 15:
                return 2
            return act

    def follow_row(self, myrow, mycol, r, c, wall, mypos):
        if myrow < r:
            if [mypos[-1][0] + 5, mypos[-1][1] - 8] in wall or [mypos[-1][0] + 5, mypos[-1][1]] in wall:

                return self.follow_coll(myrow, mycol, r, c, wall, mypos)
            return 5
        else:
            if [mypos[0][0] - 5, mypos[0][1]] in wall:
                return self.follow_coll(myrow, mycol, r, c, wall, mypos)
            return 2

    def follow_coll(self, myrow, mycol, r, c, wall, mypos):
        dec = 1
        if myrow > r:
            dec = -1
        for i in range(myrow, r, dec):
            if [i, mycol] in wall:
                if mycol - 157 <= mycol - 5:
                    return 4
                else:
                    return 3

        if mycol < c:

            if [mypos[-1][0], mypos[-1][1] + 4] in wall or [mypos[0][0], mypos[0][1] + 8] in wall:
                return self.follow_row(myrow, mycol, r, c, wall, mypos)
            else:
                return 3
        else:
            if [mypos[-1][0], mypos[-1][1] - 12] in wall or [mypos[0][0], mypos[0][1] - 4] in wall:
                return self.follow_row(myrow, mycol, r, c, wall, mypos)
            else:
                return 4

    def nowperform(self, myrow, mycol, wall, mypos, enpos_r, enpos_c, r=0, c=0):
        """
        This function performs different actions according to condition and positions of enemy. If there is no enemy
        the it follows the exit pass
       :param myrow: Current agent row
        :param mycol: Current agent column
        :param r: r is the row location of exit pass
        :param c: c is the column location of exit pass
        :param wall: wall list
        :param mypos: mypos list
        :param er: enemy row
        :param ec: enemy column
        :return: The action to perform
        """


        flag = False
        flag1 = False
        if myrow in enpos_r:
            index = enpos_r.index(myrow)
            index = enpos_c[index]
            dec = 1
            if mycol > index:
                dec = -1
            for i in range(mycol, index, dec):
                if [myrow, i] in wall:
                    flag = True
            if mycol < index and not flag:
                return 11
            elif mycol >= index and not flag:
                return 12

        if mycol in enpos_c:
            index = enpos_c.index(mycol)
            index = enpos_r[index]
            dec = 1
            if myrow > index:
                dec = -1
            for i in range(myrow, index, dec):
                if [i, mycol] in wall:
                    flag1 = True
            if myrow < index and not flag1:
                return 13
            elif myrow >= index and not flag1:
                return 10
            else:
                return 0


        if r!=180 and c!=80:
            if myrow not in enpos_r and mycol not in enpos_c:
                set10 = [2, 3, 5, 6, 7, 8, 10, 11, 12, 12, 14, 15, 16, 17]
                return (np.random.choice(set10, p=[0.051, 0.051, 0.051, 0.085, 0.085, 0.085, 0.0875, 0.0905, 0.041, 0.041, 0.083, 0.083, 0.083, 0.083]))

        if abs(myrow - r) < abs(mycol - c) and r != 0 and c != 0:
            dec = 1
            if mycol > c:
                dec = -1
            for i in range(mycol, c, dec):
                if [r, i] in wall:
                    ac = self.follow_coll(myrow, mycol, r, c, wall, mypos)
                    return ac
            ac = self.follow_row(myrow, mycol, r, c, wall, mypos)
            return ac
        elif abs(myrow - r) >= abs(mycol - c) and r != 0 and c != 0:
            dec = 1
            if myrow > r:
                dec = -1
            for i in range(myrow, r, dec):
                if [i, c] in wall:
                    ac = self.follow_row(myrow, mycol, r, c, wall, mypos)
                    return ac
            ac = self.follow_coll(myrow, mycol, r, c, wall, mypos)
            return ac
        else:
            return 0



    def findexit(self, myrow, mycol, en_c, en_r, exit, walls):
        """
         This function finds the nearest exit point and calls the exit function to take the exit.
         :param myrow: Current row position of agent
         :param mycol: Current column position of agent
         :param en_c: Current enemy exit coloumn
         :param en_r: Current enemy exit row
         :param exit: Exit list
         :param walls: Walls list
         :return: The exit point
         """
        if len(en_r) < 20:

            if myrow < exit[0][0]:
                mid = (abs(exit[-1][1] + exit[0][1]) // 2)
                return exit[0][0], mid
            else:
                mid = (abs(exit[0][1] + exit[-1][1]) // 2)
                return exit[-1][0], mid



    # You should modify this function
    def act(self, observation, reward, done):
        player = [240, 170, 103]
        points = [232, 232, 74]
        en = [210, 210, 64]
        wall = [84, 92, 214]

        mypos = []
        enpos_r = []
        enpos_c = []
        walls = []
        gun_point = []

        row = 0
        for each in observation:
            row += 1
            column = 0
            if row <= 180:

                for eachone in each:
                    column += 1
                    if column < 160 and 0 not in eachone:
                        if eachone[0] == 240 and eachone[1] == 170 and eachone[2] == 103:
                            if len(mypos) == 0:
                                mypos = [[row, column]]
                            else:
                                if row - mypos[0][0] <= 19:
                                    mypos.append([row, column])
                        elif eachone[0] == 84 and eachone[1] == 92 and eachone[2] == 214:
                            walls.append([row, column])
                        else:
                            enpos_r.append(row)
                            enpos_c.append(column)

        if len(mypos) != 0:
            gun_point = [mypos[0][0] + 7, mypos[0][1] + 4]
            for i in range(len(walls)):
                if walls[i][0] is 5 and len(self.exit) is 0:

                    if walls[i + 1][1] - walls[i][1] > 39:
                        self.exit.append([walls[i][0], walls[i][1]])
                        self.exit.append([walls[i][0], walls[i + 1][1]])
                if walls[i][0] is 180 and len(self.exit) is 2:
                    if walls[i + 1][1] - walls[i][1] > 39:
                        self.exit.append([walls[i][0], walls[i][1]])
                        self.exit.append([walls[i][0], walls[i + 1][1]])
                if walls[i][1] is 5 and len(self.exit) is 0:
                    if walls[i + 1][0] - walls[i][0] > 39:
                        self.exit.append([walls[i][0], walls[i][1]])
                        self.exit.append([walls[i][0], walls[i + 1][1]])
                if walls[i][1] is 155 and len(self.exit) is 2:
                    if walls[i + 1][1] - walls[i][1] > 39:
                        self.exit.append([walls[i][0], walls[i][1]])
                        self.exit.append([walls[i][0], walls[i + 1][1]])

            if len(enpos_r) == 0 or len(enpos_c) == 0:
                r, c = self.findexit(gun_point[0], gun_point[1], enpos_c, enpos_r, self.exit, walls)
                act = self.exitpass(gun_point[0], gun_point[1], r, c, walls, mypos, enpos_r, enpos_c)
                return act

            act = self.nowperform(gun_point[0], gun_point[1], walls, mypos, enpos_r, enpos_c)

            return act

        return 0


## YOU MAY NOT MODIFY ANYTHING BELOW THIS LINE OR USE
## ANOTHER MAIN PROGRAM
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--env_id', nargs='?', default='Berzerk-v0', help='Select the environment to run')
    args = parser.parse_args()

    # You can set the level to logger.DEBUG or logger.WARN if you
    # want to change the amount of output.
    logger.set_level(logger.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = 'random-agent-results'

    env.seed(0)
    agent = Agent(env.action_space)

    episode_count = 100
    reward = 0
    done = False
    score = 0
    special_data = {}
    special_data['ale.lives'] = 3
    ob = env.reset()

    i = 0
    while not done:

        action = agent.act(ob, reward, done)
        if action == 4:
            done = True
        ob, reward, done, x = env.step(action)
        score += reward
        env.render()
        i = i + 1
        # if i == 10:
        #    done=True

    # Close the env and write monitor result info to disk
    print("Your score: %d" % score)
    env.close()