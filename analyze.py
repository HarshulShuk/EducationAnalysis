"""
We have 
	- Male/female teaher counts for each school per year
		-% wise, compare
	- Math/English MCAS scores for each school per year
	- List of public schools, charter schools

Cleaning
	- School must appear all 8 yrs
	- School must have at least 10 teachers total
	- School's code must appear in list of public or charter schools
"""



import pandas as pd
import sys

def findPercentMale(row):
	return row.m_teacher_count / (row.f_teacher_count + row.m_teacher_count)

def wrangleGroup(group):
	if len(group) != 8:
		print(len(group))
		print(group.head())
	return ((group['f_teacher_count'] + group['m_teacher_count']) > 10).all() and len(group) == 8

def readRawData(startYear,numYears):
	relevantTeacherColumns = ['SCHOOL','Org Code','Females (# )', 'Males (# )']
	relevantStudentColumns = ['School Name','School Code','Subject','Student Included','CPI']
	betterTeacherColumns = ['school_name','school_code','f_teacher_count','m_teacher_count']
	betterStudentColumns = ['school_name','school_code','subject','count','CPI']
	totalTeacherData = pd.DataFrame([],columns=betterTeacherColumns)
	totalStudentData = pd.DataFrame([],columns=betterStudentColumns)
	validSchoolCodes = set()
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

		validSubjects = set(['MATHEMATICS','ENGLISH LANGUAGE ARTS'])
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


startYear = int(str(int(sys.argv[1]) + 1)[2:])
numYears = int(sys.argv[2])
print("startYear: " + str(sys.argv[1]) + ", numYears: " + str(numYears))

validSchoolCodes, totalTeacherData, totalStudentData = readRawData(startYear,numYears)



# school_directory = pd.read_excel('schoolDirectory/valid_schools.xlsx')
# validSchoolCodes = validSchoolCodes.intersection(set(school_directory['Org Code']))

print(totalTeacherData.shape)
print(totalStudentData.shape)

totalTeacherData = totalTeacherData[totalTeacherData['school_code'].isin(validSchoolCodes)]
totalStudentData = totalStudentData[totalStudentData['school_code'].isin(validSchoolCodes)]
assert (totalTeacherData.shape[0] == len(validSchoolCodes) * 8 ),'Error in Teacher Data'
assert (totalStudentData.shape[0] == len(validSchoolCodes) * 32),'Error in Student Data'



print(len(validSchoolCodes))
print(totalTeacherData.shape)
print(totalStudentData.shape)