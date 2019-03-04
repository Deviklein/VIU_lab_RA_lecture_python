#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 12:28:35 2019

@author: Devi
(lecture material for 3/4/19)
VIU-lab RA Lecture
"""
#always put code to import packages at the beginning of your scripts!!!!!!!!! 
#(very important)
import collections #used to create student and TA "named tuples," 
#a data structure that is new in python 3+
import numpy as np #used for generating random data, sampled from normal distr.
from operator import itemgetter #used for sorting lists 
import pandas as pd #import useful 
from scipy.stats import chi2 #used to compute chi-squared critical value at
                             # alpha = .05 level. 

###############################################################################
#Start of code to create dataset
###############################################################################
'''
Create the data set from scratch

Class Grading scheme: 
Homework 40%, Midterm 25%, Final 35%

Grade distribution:
A: 100-93.00,    A-: 92.99-90.00
B+: 89.99-87.00, B: 86.99-83.00, B-: 82.99-80.00
C+: 79.99-77.00, C: 76.99-73.00, C-: 72.99-70.00
D+: 69.99-67.00, D: 66.99-63.00, D-: 62.99-60.00
F: 59.99-0

TAs: Jim Lahey, Bubbles, Ricky, Julian, J-Roc

Total number of students in class: 420

Section TA:     Number of Students
Jim Lahey-            90
Bubbles-              82
Ricky-                80
Julain-               84
J-Roc-                84
'''

#set the seed so the data is the same everytime the script is run 
np.random.seed(10100011)

'''
Create a student class called, "student."
This class is a named tuple where the index of the tuple corresponds to a 
particular attribute of the student.

index 1: TA_name- the name of the TA leading the section for this student

index 2: Homework_grade- proportion of total possible points for homework 
component of total grade

index 3: Midterm_grade- proportion of total possible points for midterm exam 
component of total grade

index 4: Final_grade- proportion of total possible points for final exam 
component of total grade

index 5: Total_grade- sum of all the components that make up final grade 
(i.e. homework_grade + midterm_grade + final_grade)

index 6: Letter grade associated with grade percentage in the class 
(i.e. Total_grade)
'''
student = collections.namedtuple('student', 
   'TA_name Homework_grade Midterm_grade Final_grade Total_grade Letter_grade')

'''
Create a teacher assistant class called, "ta."
This class is a named tuple where the tuple[index] returned value of the tuple 
corresponds to a particular atttribute of the teacher assistant.

index 1: name- the name of the TA
index 2: mean- on average how well have sudents in the past done in this TA's 
section (score ranging from 0-100 percent points)
index 3: variance- what is the spread of the scores for students in the past 
who were in this TAs section
'''
ta = collections.namedtuple('ta', 
                            'name mean variance')

#TAs for this particular class in Winter 2019 
TAs = (ta('Jim Lahey', 78, 15),
       ta('Bubbles', 90, 3),
       ta('Ricky', 57, 10),
       ta('Julian', 76, 6),
       ta('J-Roc', 66, 8),
       )


#420 total students in this class
students_per_TA = [90,
                   82,
                   80,
                   84,
                   84,
                   ]

class Astrophysics_course:
    '''
    This python "class" simulates student grades in an astrophyics course 
    at Nova Scotia Community College in Hailfax, Canada. The students are 
    partitioned into several "TA sections."
    
    Parameters:
        TAs (type tuple): a sequence of TAs for this astrophysics course
        
        students_per_TA (type list): a sequence of integers where the value at
        a specific index in the sequence corresponds to the number of students
        in a particular TA's section. The index of this tuple corresponds to 
        the index of the TAs sequence (passed as a co-parameter to this class). 
    '''
    def __init__(self, TAs, students_per_TA):
        'This function is needed whenever you create your own classes.' 
        self.t = TAs #tuple of TAs
        self.s_p_t = students_per_TA #list of number of students per TA section
        self.hw = .4 #weighted percentage towards final grade
        self.midterm = .25 #weighted percentage towards final grade
        self.final = .35 #weighted percentage towards final grade
        self.grades = {'A': (100.00,90.00), #dictionary mapping letters (keys)                                                                      to 
                       'B': (89.00, 80.00), #to percentages (values)
                       'C': (79.00, 70.00),
                       'D': (69.00, 60.00),
                       'F': (59.00, 0.00),}
       
    def pct_to_letter(self, score):
        '''Convert a percentage score into a letter grade by using the grading 
        rubric, "self.grades" class attribute.'''
        for letter, grade in self.grades.items():
            if (score <= grade[0]) and (score >= grade[1]):
                return letter
        
    def create_score(self, TA):
        '''Randomly generate grade points between 0-100 percent.'''
        score = np.random.normal(TA[1],TA[2])
        #print ('score when method called is {}'.format(score))
        if (score >= 0.0) and (score <= 100.0):
            return score
        else:
            new_score = self.create_score(TA)
            #print ('intermediate result for score is {}'.format(score))
            return new_score
    
    def create_student(self, TA):
        '''Simulate a student's test and homework grades and final grade in the 
        class. Return an instance of the named tuple,"student." '''
        hw = self.create_score(TA) * self.hw
        mid = self.create_score(TA) * self.midterm
        fin = self.create_score(TA) * self.final
        total = hw + mid + fin
        letter = self.pct_to_letter(round(total))
        return student(TA[0], hw, mid, fin, total, letter)
    
    def create_students(self):
        '''Simulate an entire class of students with their finalized grades.
        Return a list of a length specified by the sum of the integers in the 
        students_per_TA parameter.'''
        students = []
        for ta,studs in zip(self.t,self.s_p_t):
            for _ in range(studs):
                students.append(self.create_student(ta))
        return students

#create an instance of the class defined above
class_2019 = Astrophysics_course(TAs, students_per_TA)
#call the method to create a group of students   
class_grades = class_2019.create_students()

###############################################################################
#End of code to create dataset
###############################################################################


###############################################################################
#Start of code for creating a datastructure 
###############################################################################
'''We can put the data we created in the list above into a datastructure
lets put the data into a dataframe (super easy with namedTuples)'''
df = pd.DataFrame(class_grades)#put data in list into dataframe

df.shape #returnsthe dimensions of the dataframe

df.columns #provides us with the names of the columns in the dataframe

df['Letter_grade']# returns a vector corresponding to the letter grades 
#in the data set

#lets plot a histogram of the distribution of class scores %'s
df.hist('Total_grade')

#lets make a histogram of letter grades
df['Letter_grade'].value_counts()[class_2019.grades.keys()].plot(kind = 'bar')
#has a normal distribution look to it, right? this is an interesting property 
###############################################################################
#End of code for creating a datastructure
###############################################################################


###############################################################################
#Start of code for sorting the dataset
###############################################################################
#lets take a look at the class grades
print (class_grades) #this is a long list

#maybe lets print just a subset of the entire list, how do we do this?
#use slice syntax
print (class_grades[:10]) #print first ten elements in list

print (class_grades[1:100:10]) # print student scores that are in the first 100 
#indices but skipping every 10 scores

print (class_grades[-10]) #print the last 10 elements in the list

#sort students in class by their letter grade
sorted_by_letter = sorted(class_grades, key=itemgetter(5))
print (sorted_by_letter[:10]) #prints the first 10 students in the list 

#sort students in the class by their grade percentage in the course
sorted_by_percentage = sorted(class_grades, key = itemgetter(4))
print (sorted_by_percentage[-10])
###############################################################################
#End of code for sorting the dataset
###############################################################################


###############################################################################
#Start of code for breaking the dataset up into smaller chunks for hypothesis
#testing
###############################################################################
'''now lets split up students based off the TA section they are in to answer 
our question posed at the beginning of lecture and do a hypothesis test on the 
data
'''
                      ###---method 1 of doing this---###
students_by_ta = [] #lets create an empty list to store multiple lists in 
#later
#loop through sequence of TAs so that we can cover every ta in our goal for 
#sorting students based on TAs into seperate lists
for ta in TAs:
    temp_ta_name = ta[0] #first element in the tuple correspond to the TA names
    temp_students = [] #create another empty list that we will populate 
                           #with students
    for student in class_grades: #another for loop to iterate through the 
                                 #class of students
        if student[0] == temp_ta_name: #boolean expression 
            temp_students.append(student) #will execute this code only if 
                                #the boolean expression above evaluates to True
    students_by_ta.append(temp_students) #add the temporary list of 
      #students who all have the same TA to the empty list outside the for loop

                      ###---Method 2 of doing this---###
#another way to break up the students into seperate lists based on TA they 
#belong to
sorted_by_ta = sorted(class_grades, key = itemgetter(0))#sort class students 
                                                        #by ta they belong to
index_list = [] #create empty list for later use
ta_student_lists1 = []#this will be the same exact list as ta_student_lists
ta_name = 'Bubbles' #this variable will change as we go through the
                      #for loop below
                      
for index, student in enumerate(sorted_by_ta): #the enumerate fucntion returns
        #the index in addition to the student in the list we are iterating over
    if student[0] != ta_name:
        index_list.append(index)
        ta_name = student[0]
        
students_by_ta1 = [sorted_by_ta[:index_list[0]],
                  sorted_by_ta[index_list[0]:index_list[1]],
                  sorted_by_ta[index_list[1]:index_list[2]],
                  sorted_by_ta[index_list[2]:index_list[3]],
                  sorted_by_ta[index_list[3]:],
                  ]
 
                      ###---Method 3 of doing this---###       
#another way to achieve the same goal using the pandas dataframe we created 
#earlier
students_by_ta2 = []
for ta in TAs:
    students_by_ta2.append(df[df['TA_name']==ta[0]])
    
#can you think of another way to sort the class data by TAs and create
#a list of lists like above?    
###############################################################################
#End of code for breaking the dataset up into smaller chunks for hypothesis
#testing
###############################################################################
    

###############################################################################
#Start of code for breaking down the students letter grades for each TA 
#section into seperate data structures and printing results
###############################################################################

# I am going to use a quick method for figuring out the grade distribution
#per ta course. If time permits, I will go over the logic behind how i did this
g_p_t = {} #letter grades per TA dictionary
for ind, ta in enumerate(TAs):
    grades = [ta[0]]
    for letter in class_2019.grades.keys():
        grades.append(len(df[(df['TA_name']==ta[0]) & (df['Letter_grade'] == letter)]))
    grades.append(students_per_TA[ind])
    g_p_t[ta[0]] = grades

g_p_t['Letter grades'] = [len(df[df['Letter_grade']== 'A']),
                          len(df[df['Letter_grade']== 'B']),
                          len(df[df['Letter_grade']== 'C']),
                          len(df[df['Letter_grade']== 'D']),
                          len(df[df['Letter_grade']== 'F']),
                         ]
         ###---print out a contigency table for the data---###
print('TA                   Letter Grades            Total')
print('___________________________________________________')
print('                A     B     C     D     F          ')
print('                                                   ')
print('{}       {}     {}    {}    {}    {}       {}'.format(*g_p_t[TAs[0][0]]))
print('{}         {}    {}    {}     {}     {}       {}'.format(*g_p_t[TAs[1][0]]))
print('{}           {}     {}     {}     {}    {}      {}'.format(*g_p_t[TAs[2][0]]))
print('{}          {}     {}    {}    {}     {}       {}'.format(*g_p_t[TAs[3][0]]))
print('{}           {}     {}     {}    {}    {}       {}'.format(*g_p_t[TAs[4][0]]))
print('___________________________________________________')
print('Total           {}    {}    {}   {}   {}      420'.format(*g_p_t['Letter grades'])),

###############################################################################
#End of code for breaking down the students letter grades for each TA 
#section into seperate data structures and printing results
###############################################################################


###############################################################################
#start of code for Lecture assignment (to be turned in)
#Calculate the chi-squared test statistic using python as a calculator and
#variable holder. compare to the chi-squared critical value and make decison
#about whether to reject or fail to reject the null hypothesis that letter 
#grades of students are independent of TA.
###############################################################################
#Chi-squared test statistic calculation goes as follows:
#1) for each cell do the following:
    #(Observed score - expected score)^2/expected score
        #to calculate expected score:
            #row_total*column_total/Total in class
            #e.g. expected value for 'Jim Lahey' and student getting an 'A' is:
                #45*90/420 = 9.64

#2)do the above calculation for ALL 25 cells
#3)Sum the 25 values together to get your final test statistic.
# You will later compare this test statistic to a given critical value in order 
# to make a decision in your hypothesis test. 

#you can either do this by hand by looking at the printed layout or by using
#what we learned today about indexing into lists to write some code to do
#these calculcations for us really quickly 

###---Enter your code here for the assignment---###
#frequency counts of letter grades in class to help you get started
total_As = len(df[df['Letter_grade']=='A'])
total_Bs = len(df[df['Letter_grade']=='B'])
total_Cs = len(df[df['Letter_grade']=='C'])
total_Ds = len(df[df['Letter_grade']=='D'])
total_Fs = len(df[df['Letter_grade']=='F'])
'''
Hint 1: you can use the sum() built-in function to find the sum of values in a 
list. e.g. sum(g_p_t['Jim Lahey']) will give you the row total for Jim Lahey,
i.e. the number of students in Jim Lahey's sections = 90. 

Hint 2: Think about creating a list of expected values for each letter grade
#per TA. Maybe use a for loop and some arithmetic operations
Use the following syntax for arithmetic operations to compute expected values:
-multiplication: *, e.g. 2*4 = 8.0
-division: / , e.g. 4/2 = 2.0
-x^2: x**2 / , 2**3 = 8.0
- remember to use parentheses in your arithmetic operations to ensure you don't
make any mistakes


Hint 3: Use the built-in enumerate function to iterate over the observed and 
expected value lists (they are of the same dimension) to compute
I have already given you the observed values of letter grades per TA
these observed values are stored in the dictionary. The syntax to obtain the
observed values is as follows: to get the letter grades for Bubbles, I can
index into the dictionary by g_p_t['Bubbles']. try this in the interpreter, it 
will return the second row in the printed contingency table. 

Hint 4: 
'''







#Lets calculate the degrees of freedom needed for finding the critical value
#for our hypothesis test
#(number of rows-1)*(number of columns -1 ) = (5-1)*(5-1) = 4*4 = 16
    
#we are doing a hypothesis test with a set alpha level at .05 
#the critical value we need is a chi squared random variable, denoted as
#x^2,16,.95
critical_value = chi2.ppf(.95, 16)

#test decision: reject the null hypothesis if the
#observed test statisitc is greater than the critical value calculated above

#print your observed test statisitc below

#if observed test statistic > critical_value: reject Ho
#conclusion: write your own here and use the print function

#if observed test statistic < critical_value: fail to reject Ho
#conclusion: write your own here and use the print function
     
