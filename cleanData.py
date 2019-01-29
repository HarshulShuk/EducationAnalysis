"""
We have 
	- Male/female teacher counts for each school per year
	- Math/English MCAS scores for each school per yearw per gender
	- List of public schools, charter schools (optional)

Cleaning
	- Must be (inputted) # years of records for the boys MCAS, girls MCAS, and teacher's gender stats
	- Schools must have at least 10 teachers total
	- Schools must be in the list of public/charter schools
	- Format data such that:
		TeacherColumns = ['school_name','school_code','f_teacher_count','m_teacher_count']
		StudentColumns = ['school_name','school_code','subject','count','CPI']
"""



import pandas as pd
import sys

def readRawData(startYear,numYears):
	relevantTeacherColumns = ['SCHOOL','Org Code','Females (# )', 'Males (# )']
	relevantStudentColumns = ['School Name','School Code','Subject','Student Included','CPI']
	betterTeacherColumns = ['school_name','school_code','f_teacher_count','m_teacher_count']
	betterStudentColumns = ['school_name','school_code','subject','student_count','CPI']
	totalTeacherData = pd.DataFrame([],columns=betterTeacherColumns)
	totalStudentData = pd.DataFrame([],columns=betterStudentColumns)
	validSchoolCodes = set()
	validSubjects = set(['MATHEMATICS','ENGLISH LANGUAGE ARTS'])
	for year in range(startYear,startYear+numYears):
		teacherData = pd.read_excel('teacherData/teacher_stats.xlsx',sheet_name=str(year))[relevantTeacherColumns]
		maleData = pd.read_excel('MCAS/F_' + str(year) + '.xlsx',skiprows=1)[relevantStudentColumns]
		femaleData = pd.read_excel('MCAS/M_' + str(year) + '.xlsx',skiprows=1)[relevantStudentColumns]
		teacherData.columns = betterTeacherColumns
		maleData.columns = betterStudentColumns
		femaleData.columns = betterStudentColumns
		teacherData['year'] = year
		maleData['year'] = year
		femaleData['year'] = year
		maleData['gender'] = 'male'
		femaleData['gender'] = 'female'

	
		maleData = maleData.loc[maleData['subject'].isin(validSubjects)]
		femaleData = femaleData.loc[femaleData['subject'].isin(validSubjects)]
		teacherData = teacherData.loc[(teacherData['f_teacher_count'] + teacherData['m_teacher_count']) >= 10]

		if(len(validSchoolCodes) == 0):
			validSchoolCodes = set.intersection(set(teacherData['school_code']),set(maleData['school_code']),set(femaleData['school_code']))
		else:
			validSchoolCodes = validSchoolCodes.intersection(set(teacherData['school_code']),set(maleData['school_code']),set(femaleData['school_code']))

		totalTeacherData = totalTeacherData.append(teacherData,sort=False)
		totalStudentData = totalStudentData.append(maleData,sort=False).append(femaleData,sort=False)
	return (validSchoolCodes, totalTeacherData, totalStudentData)

def findMalePercent(row):
	return row.m_teacher_count / (row.f_teacher_count + row.f_teacher_count)

startYear = int(str(int(sys.argv[1]) + 1)[2:])
numYears = int(sys.argv[2])
print("startMCASYear: " + str(sys.argv[1]) + ", numYears: " + str(numYears))

validSchoolCodes, totalTeacherData, totalStudentData = readRawData(startYear,numYears)
totalTeacherData = totalTeacherData[totalTeacherData['school_code'].isin(validSchoolCodes)]
totalStudentData = totalStudentData[totalStudentData['school_code'].isin(validSchoolCodes)]
assert (totalTeacherData.shape[0] == len(validSchoolCodes) * numYears ),'Error in Teacher Data'	   #Mult by numYears cuz entry for each school each year
assert (totalStudentData.shape[0] == len(validSchoolCodes) * 4 * numYears),'Error in Student Data' #Mult by 4 cuz boys,girl with ESL,math for 1 school

print("We have " + str(len(validSchoolCodes)) + " unique valid schools") 
if totalTeacherData.isnull().values.any():
	print("Null vals")
if totalStudentData.isnull().values.any():
	print("Null vals")
totalTeacherData['percent_male'] = totalTeacherData.apply(lambda row: row.m_teacher_count / (row.f_teacher_count + row.m_teacher_count),axis=1)
totalStudentData.loc[:,'CPI'] = totalStudentData.loc[:,'CPI'] / 100
## Make CPI scores decimals
## Find % 
totalTeacherData.to_csv('cleanedData/totalTeacherData.csv', index=False)
totalStudentData.to_csv('cleanedData/totalStudentData.csv', index=False)

#cleanedData