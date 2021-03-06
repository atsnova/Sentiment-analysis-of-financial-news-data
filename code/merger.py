import os
import glob
from difflib import SequenceMatcher
 
class Merger(object):
	def __init__(self):
		self.base_path=	os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data')

	def inp(self):
		print("1)Merge File\n2)Get full data\n")
		i = input()
		if i == '1':
			inp = input('Enter the company to merge\n')
			return inp
		else:
			company = input('Enter company for full data processing\n')
			file = 'results_'+company+'_full.data'
			links = [line.rstrip('\n') for line in open(os.path.join(self.base_path,'links',company,file))]
			links = list(set(links)) #assuming date will be same for archive as well as google results
			print(len(links))
			writeToFile(links,company)

			f = open(os.path.join(self.base_path,'links','finallinks',"results_"+company+'_unique.data'),'a+')
			for i in links:
				f.write(str(i)+"\n")
			f.close()


			print("All Done!")
			return None

	def listArchiveFiles(self,company):
		for path, subdirs, files in os.walk(os.path.join(self.base_path,'links',company,'archive')):
			if len(files) > 0:
				return files[0]

	def countFiles(self,company):
		a = []
		b = []
		self.writeToFile([0],company,'random')#creating random file..function stops working without a file in folder
		filew = os.path.join(self.base_path,'links',company,"results_random_unique.data")
		for path, subdirs, files in os.walk(os.path.join(self.base_path,'links',company)):
				if len(files) > 0:
					for i in subdirs:
						cnt = sum([len(files) for r, d, files in os.walk(os.path.join(self.base_path,'links',company,i))])
						a.append(cnt)
		os.remove(filew)#removing random file
		return a				

	def listGoogleFiles(self):
		print("Enter company name to merge results for among ")
		print([ i for i in os.listdir(os.path.join(self.base_path,'links')) if 'empty.txt' not in i])
		company=input()
		if company != None:
			a = []
			b = []
			k = 0
			p = 2
			s = {}
			index = 1
			count = self.countFiles(company)
			max_size = len(count)

			for path, subdirs, files in os.walk(os.path.join(self.base_path,'links',company)):
				if len(files) > 0:
					
					for i in files:
						if 'archive' in i.lower():
							b.append(os.path.join(path,i))
						else:
							a.append(os.path.join(path,i))

							if index < max_size :
								if len(a) == count[index]:
									temp = []
									s.update({p:temp+a})
									a.clear()
									p+=1
									index+=1
							
			files = []
			s[1] = b
			websites = {1:'archive',2:'economictimes.indiatimes.com',3:'moneycontrol.com',4:'ndtv.com',5:'reuters.com',6:'thehindu.com',7:'thehindubusinessline.com'}
		
			for key in s:
				if key == 1:#for archive
					self.getUniqueLinks(s[key],websites[key],company)
				else:
					self.getUniqueLinks(s[key],websites[key],company)

			files.clear()
			for file in os.listdir(os.path.join(self.base_path,'links',company)):
				if file.endswith('.data'):
					files.append(file)
			
			self.getLinks(files,company)
			

	def writeToFile(self,links,company,name=None):
		if name == None:
			f = open(os.path.join(self.base_path,'links',company,"results_"+company+'_unique.data'),'a+')
		else:
			f = open(os.path.join(self.base_path,'links',company,"results_"+name+'_unique.data'),'a+')
		for i in links:
			f.write(str(i)+"\n")
		f.close()

	def getLinks(self,files,company):
		#print(files)
		file = os.path.join(self.base_path,'links',company,'results_'+company+'_full.data')
		with open(file, 'wb') as outfile:
			for f in files:
				with open(os.path.join(self.base_path,'links',company,f), "rb") as infile:
					outfile.write(infile.read())
		return file

	def getUniqueLinks(self,files,website,company):
		filew = os.path.join(self.base_path,'links',company,'results_'+website+'_unique.data')
		print("Working for: ",website)
		with open(filew, 'w+') as outfile:
			for f in files:
				links = [line.rstrip('\n') for line in open(f)]
				if website == 'archive':
					links = self.checkUnique(company,links)
					print(f)
					self.writeToFile(links,company,str(f).split('/')[-1].split('_')[1])
				for i in links:
					outfile.write(str(i)+"\n")


		outfile.close()

	def checkUnique(self,company,links):
		# if company != None:
		# 	file = listGoogleFiles(company)
			
		# 	links = [line.rstrip('\n') for line in open(file)]
		stats={0.2:0,0.4:0,0.6:0,0.8:0,1:0}
		count=0
		a = len(links)
		print(a)
		d = a*a
		

		c = 0
		for i in links:		
			for j in links:
				if(i!=j):
					value = SequenceMatcher(None, i, j).ratio()
					if(value<=0.2):
						stats[0.2]+=1
					elif(value<=0.4):
						stats[0.4]+=1
					elif(value<=0.6):
						stats[0.6]+=1
					elif(value<=0.7):
						stats[0.8]+=1
					elif(value>0.8):
						stats[1]+=1
						links.remove(j)
				c+=1
				b = len(links)*len(links)
			print("%\r",int((1-(b-c)/d)*100),end='')

		print("Stats for this file\n\nSimilarity Score(<=) \t occurances")
		for i in stats:
			print ('\t'+str(i)+'\t\t\t'+str(stats[i]))
		print("final count ",len(links))
		
		return links
		# if company != None:
		# 	writeToFile(links,company)
		# else:
		# 	return links

merge_object = Merger()
merge_object.listGoogleFiles()