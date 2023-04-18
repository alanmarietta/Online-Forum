import datetime
import pandas as pd
import random
import numpy as np

class Forum_Page:

    def __init__(self, name):
        self.__name = name
        self.__board = pd.DataFrame(columns = ['Title','Date', 'Author', 'Post', 'Votes'])
        self.__board.set_index('Title', inplace = True)
        self.__board['Votes'] = self.__board['Votes'].astype('int')
        self.__anon_words = self.__process('words.txt')
        
    
    def __process(self, filename):
        with open(filename,'r', encoding = 'UTF8') as file:
            result = [line.rstrip() for line in file]
        return result
        
    def __exists(self, title):
        return title in self.__board.index
    
    def checker(self):
        return self.__board.copy()
    
    def get_name(self):
        return self.__name   
    
    def __generate_anon(self, maxlength = 15, min_num = 1, max_num = 3):
        # Invalid Specifications
        if max_num < min_num:
            max_num = min_num
        if min_num > max_num:
            print('Invalid Specifications')
            user = None
        else:
            def username_generator():
                # Tokenize list
                with open('words.txt', encoding='UTF-8') as names:
                    NAME_LIST = names.read().split()
                selection = random.choices(NAME_LIST, k=2) 
                # Digits in username
                container =''
                i=0
                while min_num != i <= max_num:
                    number = str(random.randint(0,9))
                    if number not in container:
                        container += number
                        i += 1
                username = selection[0] + '_' + selection[1] + '_' + container
                return username
            # Ensures username hasn't been used yet
            user = username_generator()
            while len(user) > maxlength or user in self.__board['Author']:
                user = username_generator()
        return user
        
    def add_post(self, title, post, author = None, date = None, maxlength = 15, min_num = 1, max_num = 3):
        # No author
        if author == None:
            author = self.__generate_anon(maxlength, min_num, max_num)
        # No date
        if date == None:
            date = str(datetime.date.today())
        # Checks to see if title is original
        if not self.__exists(title):
            votes = 0  
            self.__board.loc[title] = [date, author, post, votes]
        return
        
    def delete_post(self, title):
        if self.__exists(title):
            self.__board.loc[title, 'Post'] = np.nan
            self.__board.loc[title, 'Author'] = np.nan
        return
        
    def vote_post(self, title, up = True):
        if self.__exists(title):
            votes = self.__board.loc[title, 'Votes']
            if up == True:
                self.__board.loc[title, 'Votes'] = votes + 1
            if up == False:
                self.__board.loc[title, 'Votes'] = votes - 1
        return
        
        
    def find_author_by_keyword(self, keyword):
        copy = self.__board.copy()
        keyword = keyword.upper()
        copy['Post'] = copy['Post'].str.upper()
        authors = copy.loc[copy['Post'].str.contains(keyword), 'Author']
        list = authors.to_list()
        return list

    
    def get_post_date_info(self, title):
        weekday_convert = {2:'Monday', 3:'Tuesday', 4:'Wednesday', 5:'Thursday', 6:'Friday', 0:'Saturday', 1:'Sunday'}
        days_in_month = {'01':31, '02':28 , '03':31 , '04':30, '05':31, '06':30, '07':31, '08':31, '09':30, '10':31, '11':30, '12':31}
        month_number = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                           'September', 'October', 'November', 'December']
        # Ensure the post exists
        if self.__exists(title):
            date = self.__board.loc[title, 'Date']
            date_string = str(date)
            # Zeller's congruence
            day_of_month = date_string[8:]
            month = date_string[5:7]
            month2 = date_string[5:7]
            year = date_string[:4]
            year2 = int(date_string[:4])
            if month == '01':
                month = '13'
                year = int(year) - 1
            if month == '02':
                month = '14'
                year = int(year) - 1
            century_year = (int(year)%100)
            zero_year = (int(year)//100)
            weekday_number = (int(day_of_month) + (13 * (int(month) + 1)) // 5 + century_year + century_year // 4 + zero_year // 4 - 2 * zero_year) % 7
            weekday = weekday_convert.get(weekday_number)
            # Month
            numbers_and_months = {}
            for number, name in zip(month_number, month_name):
                numbers_and_months[number] = name
            month3 = numbers_and_months.get(month2)
            # Day number
            if day_of_month.startswith('0'):
                day_of_month = day_of_month[1]
            # Number day of the year
            index = month_number.index(month2)
            indices = month_number[:index]
            if (year2%4 == 0 and year2%100 != 0) or (year2%400 == 0):
                days_in_month['02'] = 29
            total_days = 0
            for x in indices:
                total_days += days_in_month.get(x)
            total_days += int(day_of_month)
            # Correct suffix
            total_days = str(total_days)
            if total_days[-1] == '1':
                suffix = 'st'
            elif total_days[-1] == '2':
                suffix = 'nd'
            elif total_days[-1] == '3':
                suffix = 'rd'
            elif total_days[-1] in ['4','5','6','7','8','9'] or total_days[-2:] in ['11','12','13','14','15','16','17','18','19']:
                suffix = 'th'
            elif (int(total_days)%10 == 0):
                suffix = 'th'
            string = title + ' posted on ' + weekday + ', ' + month3 + ' ' + day_of_month + ', the ' + total_days + suffix + ' day of ' + date_string[:4]
            return string


       
    
    def __str__(self):
        # Get rid of missing data
        name = self.get_name()
        active_posts = self.__board.copy()
        active_posts = active_posts.dropna()
        titles = list(active_posts.index)
        header2 = '\n'.join(titles)
        header = 'Titles for ' + name + ':' + '\n' + header2
        return header