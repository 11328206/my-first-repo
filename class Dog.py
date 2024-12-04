class Dog:
    # 屬性
    def __init__(self, name, age):
        self.name = name  # 屬性
        self.age = age    # 屬性

    # 方法
    def intro(self):
        print(f"{self.name} is {self.age} years old!")

# 創建物件
dog1 = Dog("Buddy", 3)
dog1.intro()  # 輸出：Buddy is 3 years old!
dog2 = Dog("Candy", 5)
dog2.intro()  # 輸出：Candy is 5 years old!