class Person(object): #always inherit from object.  It's just a good idea...
    @staticmethod
    def call_person():
        print "hello person"

#Calling static methods works on classes as well as instances of that class
Person.call_person()  #calling on class
p = Person()
p.call_person()       #calling on instance of class