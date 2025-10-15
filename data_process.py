# ,name,region,country,lat,lon,tz_id,localtime_epoch,localtime,sunrise,sunset,moonrise,moonset,moon_phase,moon_illumination,is_moon_up,is_sun_up
class WeatherSystem:
    def __init__(self, source_file):
        # self.source_file = open("./countryAstronomy.csv","r")
        self.source_file = open(f"{source_file}", "r")
        self.data_list = self.source_file.readlines()
        self.source_file.close()
        
        # filter data_list
        self.data_list = self.data_filter(self.data_list)

    # ultities
    def data_filter(self, data):
        remove_duplicate = []
        duplicate_id = []
        data = data[1:len(data)]
        for i in data: 
            if i.split(',')[1] not in duplicate_id:
                duplicate_id.append(i.split(',')[1])
                remove_duplicate.append(i)
            elif i.split(',')[1] in duplicate_id:
                if i.split(',')[1].lower() == "kingston":
                    remove_duplicate.append(i)
                else:
                    pass
            else:
                pass
        return remove_duplicate
    
    # ultities
    def time_conversion(self, time):
            separate_time = time.split(':')
            hours = separate_time[0]
            minutes = separate_time[1].split(' ')[0]
            meridian_id = separate_time[1].split(' ')[1]

            if meridian_id.lower() == "pm":
                hours = int(hours) + 12

            total_minutes = (int(hours) * 24) + int(minutes)
            return [f'{hours}:{minutes}', total_minutes]
    
    # utilities
    def rev_time_conversion(self, time):
            separate_time = time.split(':')
            hours = int(separate_time[0])
            minutes = int(separate_time[1])
            meridian_id = 'AM'

            if hours > 12:
                hours = int(hours) - 12
                meridian_id = "PM"
            return f'{hours}:{minutes} {meridian_id}'

    # ultities
    def format_date(self, date) -> str:
        date = date.split('/')

        months = {
            "01" : "January", "02" : "February", "03" : "March", 
            "04" : "April", "05" : "May", "06" : "June",
            "07" : "July", "08" : "August", "09" : "September",
            "10" : "October", "11" : "November", "12" : "December", 
        }

        return f"{months[date[0]]} {date[1]}, {date[2]}"
    
    # utilities
    def time_duration(self, time1, time2):
        morning_time = time1.split(':')
        night_time = time2.split(':')

        day_mins = (int(morning_time[0])*24) + int(morning_time[1])
        night_mins = (int(night_time[0])*24) + int(night_time[1])

        duration = night_mins - day_mins

        hrs_diff = duration  // 24
        mins_diff = (int(night_time[1]) - int(morning_time[1])) + 60
        if mins_diff > 60: 
            mins_diff -= 60
        elif duration  % 24 == 0:
            mins_diff = 0

        return [f'{hrs_diff} hrs & {mins_diff} mins', duration ]
    
    def ave_time(self, tz_place, state):
        duration_list = []
        ave_placeholder = 0
        if state == "day":
            for id_1 in self.data_list:
                data_1 = id_1.split(',')
                if tz_place.lower() == data_1[6].lower().split('/')[0]:
                    duration_list.append(self.time_duration(self.time_conversion(data_1[9])[0], self.time_conversion(data_1[10])[0])[1])
            for rise_time in duration_list:
                ave_placeholder += int(rise_time)
        elif state == "night":
            for id_1 in self.data_list:
                data_1 = id_1.split(',')
                if tz_place.lower() == data_1[6].lower().split('/')[0]:
                    duration_list.append(self.time_duration(self.time_conversion(data_1[12])[0], self.time_conversion(data_1[11])[0])[1])
            for rise_time in duration_list:
                ave_placeholder += int(rise_time)

        
        ave_value = round(ave_placeholder / len(duration_list))
        time_hrs = ave_value // 24
        time_mins = ave_value % 60
        return ave_value

    def time_comparison(self, converted_time1, converted_time2):
        time_1 = converted_time1.split('&')
        time_2 = converted_time2.split('&')

        time_1_hrs = int(time_1[0].removesuffix(' hrs '))
        time_1_mins = int(time_1[1].removesuffix(' mins'))

        time_2_hrs = int(time_2[0].removesuffix(' hrs '))
        time_2_mins = int(time_2[1].removesuffix(' mins'))

        if ((time_1_hrs) * 24 + time_1_mins) > ((time_2_hrs) * 24 + time_2_mins):
            return 'Day is longer than Night'
        else:
            return 'Night is longer than Day'

    def analyze_data(self, info) -> list:
        while True:
            if info:
                for details in info:
                    sort_data = details.split(',') 
                    print(f'''==================================================================
>>>> Last Updated: {self.format_date(sort_data[8])}
Country: {sort_data[3]}                     Latitude: {sort_data[4]}
Region: {sort_data[2]}                      Longitude: {sort_data[5]}
Place: {sort_data[1]}                       Timezone: {sort_data[6]}
Daylight Duration: {self.time_duration(self.time_conversion(sort_data[9])[0], self.time_conversion(sort_data[10])[0])[0]}
{self.time_duration(self.time_conversion(sort_data[9])[0], self.time_conversion(sort_data[10])[0])[1]//5 * '█'}
Night Duration: {self.time_duration(self.time_conversion(sort_data[12])[0], self.time_conversion(sort_data[11])[0])[0]} 
{self.time_duration(self.time_conversion(sort_data[12])[0], self.time_conversion(sort_data[11])[0])[1]//5 * '█'}
->> {self.time_comparison(self.time_duration(self.time_conversion(sort_data[9])[0], self.time_conversion(sort_data[10])[0])[0], self.time_duration(self.time_conversion(sort_data[12])[0], self.time_conversion(sort_data[11])[0])[0])}
-> Night Illumination: {int(sort_data[14])}%
-> Moon Phase: {sort_data[13]}
==================================================================
''', end="")
                query = input("Go Back (Y): ").strip()
                if query.lower() == "y":
                    break 
                else: 
                    print(">>>> Invalid Output\n")
            else:
                break

    def search_by_name(self, name): 
        while True:
            places = []     
            for id in self.data_list:
                data = id.split(',')
                # this also delete in case
                if name.lower() == "":
                    break

                # then make this if
                elif name.lower() == data[1].lower() or name.lower() == data[2].lower():
                    places.append(id)
                else:
                    pass
            if places:
                print(f"\nPlace Found: {places[0].split(',')[1]}")
                return self.analyze_data(places)
            # delete this in case
            elif name.lower() == "":
                print(">>>> Invalid Input")
                break
            elif name.lower() == "n":
                return "n"
            else:
                print("\n>>>>>> Place not found \n>>>>>> Back to Home")
                break

    def search_by_country(self, country):
        info_list = []
        for id in self.data_list:
            data = id.split(',')
            if country.lower() == data[3].lower():
                info_list.append(id)

        # selected_data = selected_data[1:len(selected_data)]
        if info_list:
            print(f"\nPlaces Found")
            # for details in selected_data:
            #     print(f'- {details.split(',')[2]}, {details.split(',')[1]}')
            return info_list
        else:
            print("\n>>>> Country Not Found")

    # def search_by_timezone(self, timezone):
    #     while True: 
    #         available_timezone = []
    #         timezone_places = []
    #         for id in self.data_list:
    #             data = id.split(',')
    #             if timezone.lower() == data[6].lower().split('/')[0]:
    #                 if data[6].split('/')[1] not in available_timezone:
    #                     available_timezone.append(data[6].split('/')[1])
    #                 else: 
    #                     pass
    #             else:
    #                 pass
    #         print(available_timezone)
    #         break

    def search_by_timezone(self):
        while True: 
            available_timezone = []
            timezone_places = []
            selected_tz_place = []

            # sort all timezone regions
            for id in self.data_list:
                data = id.split(',')
                if data[6].split('/')[0] not in available_timezone:
                    available_timezone.append(data[6].split('/')[0])
                        
            # present all available timezone regions
            print('\n====== Timezone Available ======')
            for avail_tz in available_timezone:
                print(f'- {avail_tz}')
            print('- Back')
            
            # timezone_query
            timezone_query = str(input(">>>> Select a Timezone Region: ")).strip()

            for id_2 in self.data_list:
                data_2 = id_2.split(',')
                if timezone_query.lower() == data_2[6].lower().split('/')[0]:
                    timezone_places.append(data_2[6].split('/')[1])

            # present query based timezone available
            if timezone_places:
                print(f'\nAvailable Timezone Places in {timezone_query}\n ==================================================================')
                for idx, place in enumerate(timezone_places, 1):
                    print(f'- {place}', end='  ')
                    if idx % 10 == 0:
                        print("\n")
                print('\n==================================================================')
                
                # place query
                place_query = str(input("\nEnter a Place: ")).strip()

                for id_3 in self.data_list:
                    data_3 = id_3.split(',')
                    if f'{timezone_query.capitalize()}/{place_query.capitalize()}' == data_3[6]:
                        selected_tz_place.append(id_3)
                self.analyze_data(selected_tz_place)
                break
            elif timezone_query.lower() == 'back':
                break
            else:
                print('\n>>>> Invalid Input')

        # for id in self.data_list:
        #     data = id.split(',')
        #     if timezone.lower() == data[6].lower().split('/')[0]:
        #         print(f'- {data[6].split('/')[1]}')

        # print(self.data_list)

        # countries = []
        # for id in self.data_list:
        #     data = id.split(',')
        #     if data not in countries:
        #         countries.append(data[1])
        
        # for i in countries[1:len(countries)]:
        #     print(i, end=", ")

    def daytime_analytics(self):
        while True: 
            available_timezone = []
            ave_list = []

            # sort all timezone regions
            for id in self.data_list:
                data = id.split(',')
                if data[6].split('/')[0] not in available_timezone:
                    available_timezone.append(data[6].split('/')[0])
            
            for tz in available_timezone:
                if tz.lower() == "asia":
                    # for id_1 in self.data_list:
                    #     data_1 = id_1.split(',')
                    #     if tz.lower() == data_1[6].lower().split('/')[0]:
                    #         asia_list.append(self.time_duration(self.time_conversion(data_1[12])[0], self.time_conversion(data_1[11])[0])[1])
                    # for rise_time in asia_list:
                    #     ave_placeholder += int(rise_time)
                    # asia_ave = round(ave_placeholder / len(asia_list))
                    # time_hrs = asia_ave // 24
                    # time_mins = asia_ave % 60
                    ave_list.append({"asia" : self.ave_time(tz.lower(), "day")})

                elif tz.lower() == "europe":
                    ave_list.append({"europe" : self.ave_time(tz.lower(), "day")})
            
                elif tz.lower() == "africa":
                    ave_list.append({"africa" : self.ave_time(tz.lower(), "day")})

                elif tz.lower() == "pacific":
                    ave_list.append({"pacific" : self.ave_time(tz.lower(), "day")})
                
                elif tz.lower() == "america":
                    ave_list.append({"america" : self.ave_time(tz.lower(), "day")})
                
                elif tz.lower() == "australia":
                    ave_list.append({"australia" : self.ave_time(tz.lower(), "day")})
                
                elif tz.lower() == "atlantic":
                    ave_list.append({"atlantic" : self.ave_time(tz.lower(), "day")})

                elif tz.lower() == "indian":
                    ave_list.append({"indian" : self.ave_time(tz.lower(), "day")})

            print(f'''
==================================================================
Day Time Average Duration Per Timezone
- Asia: 
{int(ave_list[0]['asia'])//5 * '█'}
- Europe: 
{int(ave_list[1]['europe'])//5 * '█'}
- Africa: 
{int(ave_list[2]['africa'])//5 * '█'}
- Pacific: 
{int(ave_list[3]['pacific'])//5 * '█'}
- America: 
{int(ave_list[4]['america'])//5 * '█'}
- Australia: 
{int(ave_list[5]['australia'])//5 * '█'}
- Atlantic: 
{int(ave_list[6]['atlantic'])//5 * '█'}
- Indian: 
{int(ave_list[7]['indian'])//5 * '█'}
==================================================================
''')
            query = input("Go Back (Y): ").strip()
            if query.lower() == "y":
                break 
            else: 
                print(">>>> Invalid Output\n")

    def nighttime_analytics(self):
        while True: 
            available_timezone = []
            ave_list = []

            # sort all timezone regions
            for id in self.data_list:
                data = id.split(',')
                if data[6].split('/')[0] not in available_timezone:
                    available_timezone.append(data[6].split('/')[0])
            
            for tz in available_timezone:
                if tz.lower() == "asia":
                    # for id_1 in self.data_list:
                    #     data_1 = id_1.split(',')
                    #     if tz.lower() == data_1[6].lower().split('/')[0]:
                    #         asia_list.append(self.time_duration(self.time_conversion(data_1[12])[0], self.time_conversion(data_1[11])[0])[1])
                    # for rise_time in asia_list:
                    #     ave_placeholder += int(rise_time)
                    # asia_ave = round(ave_placeholder / len(asia_list))
                    # time_hrs = asia_ave // 24
                    # time_mins = asia_ave % 60
                    ave_list.append({"asia" : self.ave_time(tz.lower(), "night")})

                elif tz.lower() == "europe":
                    ave_list.append({"europe" : self.ave_time(tz.lower(), "night")})
            
                elif tz.lower() == "africa":
                    ave_list.append({"africa" : self.ave_time(tz.lower(), "night")})

                elif tz.lower() == "pacific":
                    ave_list.append({"pacific" : self.ave_time(tz.lower(), "night")})
                
                elif tz.lower() == "america":
                    ave_list.append({"america" : self.ave_time(tz.lower(), "night")})
                
                elif tz.lower() == "australia":
                    ave_list.append({"australia" : self.ave_time(tz.lower(), "night")})
                
                elif tz.lower() == "atlantic":
                    ave_list.append({"atlantic" : self.ave_time(tz.lower(), "night")})

                elif tz.lower() == "indian":
                    ave_list.append({"indian" : self.ave_time(tz.lower(), "night")})

            print(f'''
==================================================================
Night Time Average Duration Per Timezone
- Asia: 
{int(ave_list[0]['asia'])//5 * '█'}
- Europe: 
{int(ave_list[1]['europe'])//5 * '█'}
- Africa: 
{int(ave_list[2]['africa'])//5 * '█'}
- Pacific: 
{int(ave_list[3]['pacific'])//5 * '█'}
- America: 
{int(ave_list[4]['america'])//5 * '█'}
- Australia: 
{int(ave_list[5]['australia'])//5 * '█'}
- Atlantic: 
{int(ave_list[6]['atlantic'])//5 * '█'}
- Indian: 
{int(ave_list[7]['indian'])//5 * '█'}
==================================================================
''')
            query = input("Go Back (Y): ").strip()
            if query.lower() == "y":
                break 
            else: 
                print(">>>> Invalid Output\n")

                            

#     def timezone_id(self):
#         available_timezone = []
#         user_timezone = ""
#         while True:
#             for id in self.data_list:
#                 data = id.split(',')
#                 country = data[6].split('/')
#                 available_timezone.append(country)
#                 if country[0] not in self.timezones:
#                     self.timezones.append(country[0])
#                 else:
#                     pass
#             self.timezones = self.timezones[1:len(self.timezones)]
#             available_timezone = available_timezone[1:len(available_timezone)]
#             for id, tz in enumerate(self.timezones):
#                 print(f'{id+1}.) {tz}')
            
#             print("9.) Back")
#             user_query = str(input("Select a Timezone Region: "))
#             match user_query:
#                 case "1":
#                     asian_times = []
#                     user_timezone = "Asia"
#                     for tz_2 in available_timezone:
#                         if tz_2[0] == user_timezone:
#                             asian_times.append(tz_2[1])
#                         else:
#                             pass
                    
#                     for id, time in enumerate(asian_times):
#                         print(f'- {time}')
                    
#                     while True:
#                         print(f"- Back") 
#                         query = str(input("Enter a Timezone Place eg. `Manila`: "))
#                         for place in asian_times:
#                             if query.lower() == place.lower():
#                                 pass
#                             elif query.lower() == "back":
#                                 break
#                             else: 
#                                 pass

#                 case "2":
#                     pass
#                 case "3":
#                     pass
#                 case "4":
#                     pass
#                 case "5":
#                     pass
#                 case "6":
#                     pass
#                 case "7":
#                     pass
#                 case "8":
#                     pass
#                 case "9":
#                     break
#                 case _:
#                     print("Invalid Choice")

#         print(f'''
# {user_timezone} Timezones available: 
# ''')

def main():
    weather_astronomy = WeatherSystem("./countryAstronomy.csv")

    while True:
        print('''
====== Welcome to the Weather System ======
              
    1.) Find Place/Region
    2.) Search by Country
    3.) Search by Timezone 
    4.) Day Time Duration Analytics
    5.) Night Time Duration Analytics
    6.) Exit

===========================================
        ''')
        user_input = input("Please select an option: ").strip()
        match user_input:
            case "1":
                while True:
                    name = str(input("Enter a place you want to search (type N to exit): ")).strip()
                    result = weather_astronomy.search_by_name(name)
                    if result == None:
                        break
            case "2":
                country = str(input("Enter a country you want to search: ")).strip()
                country_result = weather_astronomy.search_by_country(country)
                weather_astronomy.analyze_data(country_result)
            case "3":
                weather_astronomy.search_by_timezone()
            case "4": 
                weather_astronomy.daytime_analytics()
            case "5":
                weather_astronomy.nighttime_analytics()
            case "6": 
                print("\n====== THANK YOU FOR USING THE WEATHER SYSTEM ======\n")
                break
            case _:
                print("\n>>> Invalid Input")


if __name__ == "__main__":
    main()

# weather_astronomy = WeatherSystem("./countryAstronomy.csv")
# print(weather_astronomy.time_conversion("9:20 PM")[0].split(':'))
# weather_astronomy.data_filter(weather_astronomy.data_list)
# weather_astronomy.search_by_timezone("Asia")
# weather_astronomy.search_by_timezone()
# weather_astronomy.time_comparison(weather_astronomy.time_duration("9:20", "21:30"), weather_astronomy.time_duration('21:35', '8:55'))
# for idx, i in enumerate(weather_astronomy.data_list, 1):
#     print(i.split(',')[3], end=', ')
    # if idx % 6 == 0:
    #     print()
# weather_astronomy.moonrise_analytics()


# ['Brazzaville', 'Kingston', 'Kuala Lumpur', 'Abuja', "Saint George's", 'Republic', 'Leonards']
# kingston