import sys   #sys module is used to extract arguments from the command line
import os 	 #os module is used to ensure the existence of the files task.txt and completed.txt

#The two if statements written below ensure the existence of task.txt and completed.txt
if not(os.path.isfile("./task.txt")):
	 with open("task.txt","w") as fp:
	 	pass
if not(os.path.isfile("./completed.txt")):
	with open("completed.txt","w") as fp:
		pass

#args contains the arguments passed in the command line
args=sys.argv

def sorter():
	"""

	Sorts the items in ascending order of priority
	Lesser the priority number implies greater importance

	"""
	with open("task.txt", "r") as fp:
		task_lst = fp.readlines()
	flag = 1
	while flag :
		flag = 0
		for i in range(len(task_lst)-1):
			 if(task_lst[i][0] > task_lst[i+1][0]):
				 task_lst[i], task_lst[i+1] = task_lst[i+1], task_lst[i]
				 flag = 1
	with open("task.txt","w") as fp:
		fp.writelines(task_lst)	

def helpoutfunc():
    """
    
	Prints the usage help menu when the command is executed without any arguments or with the argument help.

    """
    
    print("""Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics
     """)

def listfunc():
	"""

	Outputs the tasks present in task.txt
	
	Every item is printed on a new line, with the following format

	[index] [task] [priortiy]

	"""

	with open("task.txt","r") as fp:
		task_lst = fp.readlines();
		if(len(task_lst)==0):
			print("There are no pending tasks!")
		else:
			serial = 1
			for task in task_lst:
				lst = task.split()
				taskstring = ""
				for sub in range(1,len(lst)):
					if(sub != len(lst)-1):
						taskstring += lst[sub] + " "
					else:
						taskstring += lst[sub]
				print(serial ,". ", taskstring, " [", lst[0], "]", sep="")
				serial += 1

def adderfunc():
	"""

	Appends the given task to task.txt

	"""
	if len(args)<4 :
		print("Error: Missing tasks string. Nothing added!")
	else:
		for i in range(len(args)-3):						#this is done to accomodate multiple tasks
			with open("task.txt","r") as fp:
				task_lst = fp.readlines()
			reqstring = args[2] + " " + args[3+i]
			reqsubstring = reqstring[2:]
			reqstring += '\n'
			index = len(task_lst)-1
			for j in range(len(task_lst)-1,-1,-1):
				if(int(args[2]) <= int(task_lst[j][0])):
					index = j + 1
					break
			task_lst.insert(index,reqstring)
			with open("task.txt","w") as fp:
				fp.writelines(task_lst)
			print('Added task: "', reqsubstring, '" with priority ', args[2], sep = "")
			sorter()

def deleterfunc():
	"""
	
	Deletes an item present in task.txt by its index.

	"""
	if len(args)<3:			#Checking if index is given
		print("Error: Missing NUMBER for deleting tasks.")
	else:
		with open("task.txt","r") as fp:			#Extracting incomplete items
			task_lst = fp.readlines()
		if((int(args[2])-1) >= 0 and (int(args[2])-1) < len(task_lst)):		#Checking if a task exists at given index
			del task_lst[int(args[2])-1]
			with open("task.txt","w") as fp:	
				fp.writelines(task_lst)		
				print("Deleted task #", args[2], sep = "")
		else:
			print("Error: task with index #", args[2], " does not exist. Nothing deleted.", sep = "")

def completemarker():
	"""

	Marks an item as complete by its index and then removes it from task.txt. Finally the item is appended to completed.txt .

	"""
	if len(args)<3:		#Checking if index is given
		print("Error: Missing NUMBER for marking tasks as done.")
	else:
		with open("task.txt","r") as fp:						#Extracting incomplete tasks from task.txt
			task_lst = fp.readlines()
		if(int(args[2]) < 1 or int(args[2]) > len(task_lst)):	#Checking if task exists
			print("Error: no incomplete item with index #",args[2]," exists.",sep="")
		else:
			removed_task = task_lst.pop(int(args[2])-1)
			lst = removed_task.split()
			reqstring = ""
			for it in range(1,len(lst)):
				if(it != len(lst)-1):
					reqstring += lst[it]+" "
				else:
					reqstring += lst[it]+"\n"
			with open("task.txt","w") as fp:
				fp.writelines(task_lst)
			with open("completed.txt","r") as fp:
				comp_prev = fp.readlines()
				comp_prev.append(reqstring)
			with open("completed.txt","w") as fp:
				fp.writelines(comp_prev)
			print("Marked item as done.")

def reporter():
	"""
	
	Shows the number of complete and incomplete items. It also shows the completed and incomplete items in separate groups.

	"""
	with open("task.txt","r") as fp: 				#Extracting incomplete items and printing
		task_lst = fp.readlines()
		print("Pending : ", len(task_lst), sep = "")
		serial = 1
		for task in task_lst:
			b = task.split()
			taskstring=""
			for sub in range(1,len(b)):
				if sub != len(b)-1 :
					taskstring += b[sub]+" "
				else:
					taskstring += b[sub]
			print(serial,". ",taskstring," [",b[0],"]",sep="")
			serial += 1
		print()
	with open("completed.txt","r") as fp:			#Extracting completed items and printing
		done_lst = fp.readlines()
		print("Completed : ", len(done_lst), sep="")
		serial = 1
		for sub in done_lst:
			length = len(sub)
			print(serial,". ", sub[:length-1], sep="")
			serial += 1
		print()

def main():	
	if(len(args) == 1):
		helpoutfunc()	
	elif(args[1] == 'help'):
		helpoutfunc()
	elif(args[1] == 'ls'):
		listfunc()
	elif(args[1] == 'add'):
		adderfunc()
	elif(args[1] == 'del'):
		deleterfunc()
	elif(args[1] == 'done'):
		completemarker()
	elif(args[1] == 'report'):
		reporter()	
		
main()

