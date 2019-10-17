"""
Author: Jeet Thakur
Author: Karam Makhija
File: Agent3.py
pyhton 2.7
"""
import argparse
import sys,numpy,random,math
#import pdb
import gym
from gym import wrappers, logger


class Agent(object):
    """The Real World Agent"""
    def __init__(self, action_space):
        self.action_space = action_space
        self.acti=[]
        #self.check = True

        self.exit = []
    def exitpass(self,myrow,mycol,r,c,wall,mypos,er,ec):
        """
        The exit function maps which is the best way to exit from the point we stand
        :param myrow: The agent gunpoint row
        :param mycol: The agent gunpoint col
        :param r: The exit cordinate
        :param c: The exit cordinate
        :param wall: The walls
        :param mypos: The head and Toe location of the agent
        :param er: The enemy array
        :param ec: The enemy array
        :return: The action to exit in the way prescribed
        """
        if r==5:
            r=r+5
            act = self.nowperform(myrow,mycol,r,c,wall,mypos,er,ec)
            if act==12:
                act=4
            if act==10:
                act=2
            return act

        if r==179:
            r= r-9
            act = self.nowperform(mypos[-1][0],mypos[-1][1],r,c,wall,mypos,er,ec)
            if act ==11:
                act = 3
            if act==13 or act == 12:
                act = 5
            if mypos[-1][1]-10 > c-20 and mypos[-1][1] < c+20 :
                return 5
            return act

    def follow_row(self,myrow,mycol,r,c,wall,mypos):
        """
        The function to follow the points prescibed in a row based approach - meaning going down or up
        :param myrow: The gunpoint row location
        :param mycol: The gunpoint col location
        :param r: The enemy location
        :param c: The enemy location
        :param wall: The walls
        :param mypos: The head and toe location of the agent
        :return: The action to perform 2,5
        """

        if myrow < r:
            dec = 1
            if mycol > c:
                dec = -1
            for i in range(mycol, c, dec):
                if [r, i] in wall:
                    if [mypos[-1][0], mypos[-1][1] + 6] in wall or [mypos[0][0]+20,mypos[0][1]] in wall or [mypos[-1][0], mypos[-1][1] + 4] in wall:
                        return 2
                    elif mycol < c:
                        return 3
                    elif mycol > c:
                        return 4
            dec = 1
            if mycol > c:
                    dec = -1
            for i in range(myrow, r, dec):
                    if [i,mycol] in wall:
                        cnt = 0
                        cnt2 = 0
                        temp=mycol+4
                        while[i,temp] in wall:
                            cnt+=1
                            temp-=1
                        temp=mycol-4
                        while [i,temp] in wall:
                            cnt2+=1
                            temp+=1
                        if cnt<=cnt2:
                            return 4
                        else:
                            return 3

            if [mypos[-1][0]+20,mypos[-1][1]-5] in wall or [mypos[-1][0]+20,mypos[-1][1]] in wall:
                if [mypos[-1][0],mypos[-1][1]+5] in wall:
                    return 3

                if [mypos[-1][0], mypos[-1][1] - 8] not in wall:
                    return 4
                else:
                    return 2

            return 5
        else:
            dec = 1
            if mycol > c:
                dec = -1
            for i in range(mycol, c, dec):
                if [myrow, i] in wall:
                    if [mypos[-1][0], mypos[-1][1] + 6] in wall:

                        return 5
                    elif mycol < c and mypos[-1][1]+6 not in wall:
                        return 3
                    elif mycol > c:
                        return 4
            if mypos[0][0] + 3 in wall:
                return 5
            return 2

    def follow_coll(self,myrow,mycol,r,c,wall,mypos):
        """
        The function to follow the points prescribed in a collumn based approach - meaning going left or right
        :param myrow: The gunpoint row
        :param mycol: The gunpoint col
        :param r: The enemy loc
        :param c: The enemy loc
        :param wall: The wall
        :param mypos: The toe and head location
        :return: The action to perform 3,4
        """
        if mycol < c:

            if [mypos[-1][0]+5, mypos[-1][1] + 4] in wall or [mypos[0][0],mypos[0][1]+8] in wall:
                if myrow>r:
                    return 2
                else:
                    cnt = 0
                    cnt2 = 0
                    temp = myrow
                    while [temp, mycol+2] in wall:
                        cnt += 1
                        temp += 1
                    temp = myrow
                    while [temp, mycol+2] in wall:
                        cnt2 += 1
                        temp -= 1
                    if cnt >= cnt2:
                        if [mypos[0][0]-5,mypos[0][1]] in wall:
                            return 5
                        return 2
                    else:
                        return 5
            else:
                return 3
        else:
            dec = 1
            if myrow > r:
                dec = -1
            if [mypos[-1][0], mypos[-1][1] - 9] in wall or [mypos[0][0],mypos[0][1]-6] in wall:
                if dec == 1:
                    return 5
                else:
                    return 2
            else:
                return 4

    def nowperform(self,myrow,mycol,r,c,wall,mypos,enpos_r,enpos_c):
        """
        The correct action of shooting to perform
        :param myrow: The gunpoint row
        :param mycol: The gunpoint coll
        :param r: The enemy
        :param c: The enemy
        :param wall: The wall
        :param mypos: The head and toe location
        :param enpos_r: The other enemy locations
        :param enpos_c: The other enemy locations
        :return: The action sequence to perform to shoot
        """
        if myrow == r:
            dec=1
            if mycol>c:
                dec=-1
            for i in range(mycol,c,dec):
                if [myrow,i] in wall:
                    if [myrow,(mycol+3)] not in wall:
                        return 3
                    else:
                        cnt=0
                        cnt2=0
                        temp=myrow
                        while [temp,i] in wall:
                            cnt+=1
                            temp+=1
                        temp=myrow
                        while [temp, i] in wall:
                            cnt2 += 1
                            temp -= 1
                        if cnt>cnt2 and [mypos[0][0]+5,mypos[0][1]] not in wall:
                            return 2
                        else:
                            return 5

            if mycol < c:
                return 11
            else:
                return 12

        if mycol == c:
            dec = 1
            if myrow > r:
                dec = -1
            for i in range(myrow,r,dec):

                if [i,mycol] in wall:
                    if [myrow+38,mycol] not in wall:
                        return 3
                    else:
                        cnt = 0
                        cnt2 = 0
                        temp = mycol
                        while [i,temp] in wall:
                            cnt += 1
                            temp += 1
                        temp = mycol
                        while [i,temp] in wall:
                            cnt2 += 1
                            temp -= 1
                        if cnt > cnt2 and [mypos[-1][0],mypos[-1][0]+5] not in wall:
                            return 3
                        else:
                            return 4
            else:
                    if myrow < r:
                        return 13
                    else:
                        return 10
        else:
            """
            The diagonal shooting actions decisions 
            """
            if mycol<c and myrow <r:
                tc = c-mycol
                tr= myrow+tc
                if tr in enpos_r:
                    tr=myrow
                    tc=mycol
                    #shoot diagnol down right
                    for i in range(tr,r):
                        if [tr,tc] not in wall:
                            tc+=1
                    if tc in enpos_c or tc+1 in enpos_c or tc+2 in enpos_c:
                        return 16
            elif mycol>c and myrow<r:
                tc = mycol-c
                tr = myrow + tc
                if tr in enpos_r:
                    tr = myrow
                    tc = mycol
                    # shoot diagnol down left
                    for i in range(tr, r):
                        if [tr, tc] not in wall:
                            tc -= 1
                    if tc in enpos_c or tc - 1 in enpos_c or tc - 2 in enpos_c:
                        return 17

            elif mycol>c and myrow>r:
                tc = abs(mycol-c)
                tr = myrow - tc
                if tr in enpos_r:
                    tr = myrow
                    tc = mycol
                    # shoot diagnol down left
                    for i in range(tr, r,-1):
                        if [tr, tc] not in wall:
                            tc -= 1
                    if tc in enpos_c:
                        return 15
            elif mycol<c and myrow>r:
                tc = abs(mycol-c)
                tr = myrow + tc
                if tr in enpos_r:
                    tr = myrow
                    tc = mycol
                    # shoot diagnol down left
                    for i in range(tr, r,-1):
                        if [tr, tc] not in wall:
                            tc -= 1
                    if tc in enpos_c:
                        return 14
            """
            The option when the enemy is not in sight but at a place away from the agent 
            """
            if abs(myrow-r) < abs(mycol-c):
                dec = 1
                if mycol > c:
                    dec = -1
                for i in range(mycol,c,dec):
                    if [r,i] in wall:
                        ac=self.follow_coll(myrow,mycol,r,c,wall,mypos)
                        return ac
                ac=self.follow_row(myrow,mycol,r,c,wall,mypos)
                return ac
            else:
                dec = 1
                if myrow > r:
                    dec = -1
                for i in range(myrow,r,dec):
                    if [i,c] in wall:
                        ac=self.follow_row(myrow,mycol,r,c,wall,mypos)
                        return ac
                ac=self.follow_coll(myrow,mycol,r,c,wall,mypos)
                return ac

    def findNearestEnemy(self,myrow,mycol,en_c,en_r,exit,walls):
        """
        The function to find the nearest enemy present and send its cordinates to the agent for actions to be performed
        :param myrow: The gunpoint row
        :param mycol: The gunpoint col
        :param en_c: The other enemy row loc
        :param en_r: The other enemy col loc
        :param exit: The exit locations
        :param walls: The wall
        :return: The cordinates to the next nearest location
        """
        if len(en_r)<20:

            if myrow<exit[0][0]:
                mid=(abs(exit[-1][1]+exit[0][1])//2)
                return exit[0][0],mid,True
            else:
                mid = (abs(exit[0][1] + exit[-1][1])//2)
                return exit[-1][0], mid, True
        else:
            if myrow in en_r:
                tempC = en_r.index(myrow)
                tempC = en_c[tempC]
                dec = 1
                if mycol > tempC:
                    dec = -1
                if tempC==mycol:

                    return myrow,tempC,False
                for i in range(mycol,tempC,dec):
                    if [myrow,tempC] not in walls:
                        return myrow,tempC,False

            if mycol in en_c:
                tempR = en_c.index(mycol)
                tempR = en_r[tempR]
                dec = 1
                if myrow > tempR:
                    dec = -1
                for i in range(myrow,tempR,dec):
                     if [i,mycol] not in walls:
                        return tempR,mycol,False

            if mycol not in en_c or myrow not in en_r:

                temp1=0
                temp_r=0
                dist,dist2,dist3,dist4=200,200,200,200
                for i in range(myrow,en_r[-1]):

                        if i in en_r:
                            temp1 = en_c[en_r.index(i)]
                            dist = abs(mycol - temp1)

                            if dist<20:

                                return i,temp1,False
                            else:
                                temp_r = i
                                temp1 = en_c[en_r.index(i)]
                            break
                for i in range(en_r[0],myrow):
                        if i in en_r:
                            temp2 = en_c[en_r.index(i)]
                            dist2 = abs(mycol - temp2)

                            if dist2<dist:
                                return i,temp2,False
                            else:
                                return i, temp1, False

                return temp_r,temp1,False

    # You should modify this function
    def act(self, observation, reward, done):
        """
        The function which percieves the frame each time it resets
        :param observation: The numpy array
        :param reward: The bonus
        :param done: The terminating condition
        :return: The action to be perfromed
        """
        wall = [84,92,214]
        mypos = []
        enpos_r = []
        enpos_c=[]
        walls=[]
        row=0
        for each in observation:
            row+=1
            column=0
            if row < 180:
                for eachone in each:
                    column+=1
                    if column<160 and 0 not in eachone:
                        if eachone[0] == 240 and eachone[1] == 170 and eachone[2] == 103:
                            if len(mypos)==0:
                                mypos=[[row, column]]
                            else:
                                if row - mypos[0][0] <= 19:
                                    mypos.append([row, column])
                        elif eachone[0] == 84 and eachone[1] == 92 and eachone[2] == 214:
                            walls.append([row, column])
                        else:
                            enpos_r.append(row)
                            enpos_c.append(column)

        if len(mypos)!=0:
            gun_point = [mypos[0][0] + 7, mypos[0][1]+4]
            #print(walls)
            for i in range(len(walls)):

                   if walls[i][0] is 5 and len(self.exit) is 0:

                       if walls[i+1][1] - walls[i][1] > 39:
                           self.exit.append([walls[i][0],walls[i][1]])
                           self.exit.append([walls[i][0],walls[i+1][1]])
                   if walls[i][0] is 179 and len(self.exit) is 2:
                            if walls[i+1][1] - walls[i][1] > 39:
                                self.exit.append([walls[i][0], walls[i][1]])
                                self.exit.append([walls[i][0], walls[i + 1][1]])
                   if walls[i][1] is 5 and len(self.exit) is 0:
                       if walls[i+1][0] - walls[i][0]>39:
                           self.exit.append([walls[i][0], walls[i][1]])
                           self.exit.append([walls[i][0], walls[i + 1][1]])
                   if walls[i][1] is 155 and len(self.exit) is 2:
                            if walls[i+1][1] - walls[i][1]>39:
                                self.exit.append([walls[i][0], walls[i][1]])
                                self.exit.append([walls[i][0], walls[i + 1][1]])

            r,c,f=self.findNearestEnemy(gun_point[0],gun_point[1],enpos_c,enpos_r,self.exit,walls)
            if f==True:
                act = self.exitpass(gun_point[0],gun_point[1],r,c,wall,mypos,enpos_r,enpos_c)
                return act

            act=self.nowperform(gun_point[0],gun_point[1],r,c,walls,mypos,enpos_r,enpos_c)

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

    i=0
    while not done:
        
        action = agent.act(ob, reward, done)
        if action==4:
            done = True
        ob, reward, done, x = env.step(action)
        score += reward
        env.render()
        i=i+1

    # Close the env and write monitor result info to disk
    print ("Your score: %d" % score)
    env.close()
