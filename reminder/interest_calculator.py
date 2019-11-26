class fd():	
	Amount=0
	Interest=0
	Division=1
	simple_intrest=0
	values=[]
	Time=0
	period=1
	
	def fill(self,Amount,Interest,Time,Choice,period, month_number=1):
		self.Amount=Amount
		self.Interest=Interest
		self.Time=Time
		self.period=period
		self.Choice=Choice
		self.month_number = month_number


	def clacu(self):
		if self.Choice == 1:
			pass
		elif self.Choice == 2:
			self.Interest = self.Interest/2
			self.Division = 2
		elif self.Choice == 3:
			self.Interest = self.Interest/4
			self.Division = 4
		elif self.Choice == 4:
			self.Interest = self.Interest/12
			self.Division = 12
		if self.Time == 2:
			i = self.Interest/100
			i=i+1
			self.Amount = i * self.Amount
			return self.Amount
			
		elif self.Time == 1:
			t = (self.Amount * self.Interest)/100
			interest = t * self.month_number
			return self.Amount + interest

	def refill(self):
		self.Amount=0
		self.Interest=0
		self.Division=1
		self.simple_intrest=0
		del self.values[:]
		self.Time=0
		self.period=1
		self.month_number=1
			


# Amount=eval(input("enter the Principal Amount"))
# Interest=eval(input("enter the rate of interest"))
# print("1 : simple\n2 : compound")
# Time=eval(input("Enter your choice"))
# print("1 : Annually\n2 : Half yearly\n3 : Quarterly\n 4 : Monthly") 
# Choice=eval(input('Enter your choice'))
# period=int(input("enter the period"))

# f = fd()
# f.fill(Amount,Interest,Time,Choice,period, 2)
# print(f.clacu())


