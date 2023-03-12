-- Classes aren't built in; there are different ways
-- to make them using tables and metatables.

-- Explanation for this example is below it.

Dog = {}

function Dog:new()
    newObj = {sound = "wolf"}
    self.__index = self
    return setmetatable(newObj, self)
end

function Dog:makeSound()
    print('I say' .. self.sound)
end

mrDog = Dog:new()
mrDog:makeSound() -- I say wolf

-- 1. Dog acs like a class; it's really a table
-- 2. function tablename:fn(...) is the same as 
--    function tablename.fn(self, ...)
--    The : just adds a first arg called self.
--    Read 7 & 8 below for how self gets its value.
-- 3. newObj will be an instance of class Dog.
-- 4. self = the class being instantiated. Often
--    self = Dog, but inheritance can change it.
--    newObj gets self's functions when we set both 
--    newObj's metatable and self's __index to self.
-- 5. Reminder: setmetatable returns its first arg.
-- 6. The : works as in 2, but this time we expect 
--    self to be instance instead of a class.
-- 7. Same as Dog.new(Dog), so self = Dog in new()

-- Inheritance example:
LoudDog = Dog:new()

function LoudDog:makeSound()
    s = self.sound .. ' '
    print(s .. s .. s)
end

seymour = LoudDog:new()
seymour:makeSound() -- "woof woof woof"