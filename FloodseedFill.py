import cv2
import numpy as np



'''

by Fan WU

   04/04/2017 



'''

class Floodelement(object):
    y = 0
    L = 0
    R = 0
    PL= 0
    PR= 0
    deplace = 0

    def __init__(self,y,L,R,PL,PR,deplace):
        self.y = y
        self.L = L
        self.R = R
        self.PL = PL
        self.PR = PR
        self.deplace = deplace

def FloodseedFill(filename,begin_y,begin_x,new_gray):

    img = cv2.imread(filename)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    height = img.shape[0]
    width  = img.shape[1]


    if (begin_x > width)|(begin_y >height):
        print ("out of bound")
    else:
        img_2 =floodseedfill(img,begin_y,begin_x,new_gray)
        
    return img_2


def floodseedfill(img,begin_y,begin_x,new_value):
    '''

     in this code L is the left boundary and R is the right boundary
     PL is the previous left boundary and PR is the previous right boundary

     when we begin at the beginning point ,we must go to two direction : up and down ,but when we take the decision at up or down ,we need to continue in the same
     direction ,either up ,either down . so that is why before while(len()>0),we set PL=R+1 and PR=R for it possible to go to up and down direction but after that we just
     go to one direction

     data[1]and data[2] is just to supplement the point special for 8-connectivity


    '''
    

    UP=1
    DOWN=-1

    save_element=[]
    height = img.shape[0]
    width = img.shape[1]
    img_2 = img.copy()

    old_value = img[begin_y,begin_x]

    # from the begin ,we must set the L and R
    # we begin from the line where (begin_y,begin_x) is define
    L = R = begin_x

    while ((L-1>=0)&(img[begin_y,L]==old_value)):
        L=L-1
        img_2[begin_y,L] = new_value

    while ((R+1<width)&(img[begin_y,R]==old_value)):
        R=R+1
        img_2[begin_y,L] = new_value


    floodelement = Floodelement(begin_y,L,R,R+1,R,UP)
    save_element.append(floodelement)
    indice = 0


    print(L)
    print(R)

    while (len(save_element)>0):
        
        temp_flood = save_element[0]
        del save_element[0]
        temp_y = temp_flood.y
        temp_L = temp_flood.L
        temp_R = temp_flood.R
        temp_PL = temp_flood.PL
        temp_PR = temp_flood.PR
        temp_deplace = temp_flood.deplace

        # here we chose the 8-connectivity
        data = [[-temp_deplace,temp_L-1,temp_R+1],[temp_deplace,temp_L-1,temp_PL-1],[temp_deplace,temp_PR+1,temp_R+1]]


        for k in range(3):
            if temp_y >= height:
                continue
            
            temp_y = temp_y+data[k][0]
            left = data[k][1]
            right = data[k][2]
            i = left
            while ((i>=left)&(i<right)):
                flag = 0
                if ((i<width)&(img[temp_y,i]==old_value)):
                    flag = 1
                    j = i
                    img[temp_y,i]= new_value

                    while((j-1>0)&(img[temp_y,j-1]==old_value)):
                        j=j-1
                        img[temp_y,j]= new_value
                        

                    while((i+1<width)&(img[temp_y,i+1]==old_value)):
                        i=i+1
                        img[temp_y,i]=new_value
                        


                    temp_flood_new = Floodelement(temp_y,j,i,temp_L,temp_R,-data[k][0])
                    save_element.append(temp_flood_new)
                    
                if (flag== 0):
                    i=i+1
             
    return img
            
        
    

        
            

    
    

    

    

    

    
