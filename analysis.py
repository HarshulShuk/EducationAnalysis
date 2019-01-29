import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def do(g):
	# print('-----------------------------------------------------------')
	# print(g.head())
	value = (g.student_count * g.CPI).mean()
	return value

def fuc(g):
	female = g.f_teacher_count.sum()
	male = g.m_teacher_count.sum()
	return male / (male + female)


startYear = int(str(int(sys.argv[1]) + 1)[2:])
numYears = int(sys.argv[2])
print("startMCASYear: " + str(sys.argv[1]) + ", numYears: " + str(numYears))

totalTeacherData = pd.read_csv('cleanedData/totalTeacherData.csv')
totalStudentData = pd.read_csv('cleanedData/totalStudentData.csv')


#F>M, E>M
lst = totalStudentData.groupby(['gender','subject','school_code']).apply(lambda frame: frame.CPI.mean() - .5 )
obj = [lst[i:i+548] for i in range(0, len(lst), 548)]
print(obj)
teach = totalTeacherData.groupby('school_code').apply(lambda frame: fuc(frame))
print(teach.head(teach.shape[0]))

plt.subplot(221)
plt.title('Female + ELA')
plt.scatter(teach,obj[0])
plt.xlabel('% Male Teachers')
plt.ylabel('CPI average')

plt.subplot(222)
plt.title('Female + Math')
plt.scatter(teach,obj[1])
plt.xlabel('% Male Teachers')
plt.ylabel('CPI average')

plt.subplot(223)
plt.title('Male + ELA')
plt.scatter(teach,obj[2])
plt.xlabel('% Male Teachers')
plt.ylabel('CPI average')

plt.subplot(224)
plt.title('Male + Math')
plt.scatter(teach,obj[3])
plt.xlabel('% Male Teachers')
plt.ylabel('CPI average')

plt.savefig('result.png')

lm = LinearRegression()
lm.fit([teach],[obj[0]])
print(lm.coef_[0][0])