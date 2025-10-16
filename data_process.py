class WeatherSystem:
    def __init__(self, source_file):
        self.source_file = open(f"{source_file}", "r")
        self.data_list = self.source_file.readlines()
        self.source_file.close()
        
        # filter data_list
        self.data_list = self.data_filter(self.data_list)

    # ultility
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
    
    # ultility
    def time_conversion(self, time):
            separate_time = time.split(':')
            hours = separate_time[0]
            minutes = separate_time[1].split(' ')[0]
            meridian_id = separate_time[1].split(' ')[1]

            if meridian_id.lower() == "pm":
                hours = int(hours) + 12

            total_minutes = (int(hours) * 24) + int(minutes)
            return [f'{hours}:{minutes}', total_minutes]

    # ultility
    def format_date(self, date) -> str:
        date = date.split('/')

        months = {
            "01" : "January", "02" : "February", "03" : "March", 
            "04" : "April", "05" : "May", "06" : "June",
            "07" : "July", "08" : "August", "09" : "September",
            "10" : "October", "11" : "November", "12" : "December", 
        }

        return f"{months[date[0]]} {date[1]}, {date[2]}"
    
    # ultility
    def time_duration(self, time1, time2):
        set_time = time1.split(':')
        rise_time = time2.split(':')

        set_mins = (int( set_time[0])*60) + int( set_time[1])
        rise_mins = (int(rise_time[0])*60) + int(rise_time[1])

        if rise_mins > set_mins:
            duration = rise_mins -  set_mins
        elif set_mins > rise_mins:
            duration = set_mins - rise_mins
         
        hrs_diff = duration // 60
        mins_diff = duration - (hrs_diff*60)
        return [f'{hrs_diff} hrs & {mins_diff} mins', duration]

    # ultility
    def ave_time(self, tz_place, state):
        duration_list = []
        ave_placeholder = 0
        if state == "day":
            for id_1 in self.data_list:
                data_1 = id_1.split(',')
                if tz_place.lower() == data_1[6].lower().split('/')[0]:
                    duration_list.append(self.time_duration(self.time_conversion(data_1[9])[0], self.time_conversion(data_1[10])[0])[1])
            for time in duration_list:
                ave_placeholder += int(time)
        elif state == "night":
            for id_1 in self.data_list:
                data_1 = id_1.split(',')
                if tz_place.lower() == data_1[6].lower().split('/')[0]:
                    duration_list.append(self.time_duration(self.time_conversion(data_1[11])[0], self.time_conversion(data_1[12])[0])[1])
            for time in duration_list:
                ave_placeholder += int(time)

        
        ave_value = round(ave_placeholder / len(duration_list))
        time_hrs = ave_value // 60
        time_mins = (ave_value % 60) + 60
        if time_mins >= 60:
            time_mins -= 60
        elif ave_value % 60 == 0:
            time_mins = 0
        return [ave_value, f'{time_hrs} hours & {time_mins} minutes']

    # ultility
    def time_comparison(self, converted_time1, converted_time2):
        if converted_time1 > converted_time2:
            return 'Day Time is longer than Night Time'
        elif converted_time1 == converted_time2:
            return 'Day and Night Durations are Equal'
        else:
            return 'Night Time is longer than Day Time'

    # ultility
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
Sunrise: {sort_data[9]}                     Sunset: {sort_data[10]}
Daylight Duration: 
{self.time_duration(self.time_conversion(sort_data[9])[0], self.time_conversion(sort_data[10])[0])[1]//15 * '█'} {self.time_duration(self.time_conversion(sort_data[9])[0], self.time_conversion(sort_data[10])[0])[0]}

Moonrise: {sort_data[11]}                   Moonset: {sort_data[12]}
Night Duration: 
{self.time_duration(self.time_conversion(sort_data[11])[0], self.time_conversion(sort_data[12])[0])[1]//15* '█'} {self.time_duration(self.time_conversion(sort_data[11])[0], self.time_conversion(sort_data[12])[0])[0]}
->> {self.time_comparison(self.time_duration(self.time_conversion(sort_data[9])[0], self.time_conversion(sort_data[10])[0])[1], self.time_duration(self.time_conversion(sort_data[11])[0], self.time_conversion(sort_data[12])[0])[1])}
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
                if name.lower() == "":
                    break
                elif name.lower() == data[1].lower() or name.lower() == data[2].lower():
                    places.append(id)
                else:
                    pass
            if places:
                print(f"\nPlace Found: {places[0].split(',')[1]}")
                return self.analyze_data(places)
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

        if info_list:
            print(f"\nPlaces Found")
            return info_list
        else:
            print("\n>>>> Country Not Found")

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
                    if data_2[6].split('/')[1] not in timezone_places:
                        timezone_places.append(data_2[6].split('/')[1])
                    else: 
                        pass

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
Mean Daytime Duration Across Major Timezone Places
                  
- Asia: 
{int(ave_list[0]['asia'][0])//15 * '█'} {ave_list[0]['asia'][1]} 
- Europe: 
{int(ave_list[1]['europe'][0])//15 * '█'} {ave_list[1]['europe'][1]}
- Africa: 
{int(ave_list[2]['africa'][0])//15 * '█'} {ave_list[2]['africa'][1]}
- Pacific: 
{int(ave_list[3]['pacific'][0])//15 * '█'} {ave_list[3]['pacific'][1]}
- America: 
{int(ave_list[4]['america'][0])//15 * '█'} {ave_list[4]['america'][1]}
- Australia: 
{int(ave_list[5]['australia'][0])//15 * '█'} {ave_list[5]['australia'][1]}
- Atlantic: 
{int(ave_list[6]['atlantic'][0])//15 * '█'} {ave_list[6]['atlantic'][1]}
- Indian: 
{int(ave_list[7]['indian'][0])//15 * '█'} {ave_list[7]['indian'][1]}
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
Mean Nighttime Duration Across Major Timezone Places
                  
- Asia: 
{int(ave_list[0]['asia'][0])//15 * '█'} {ave_list[0]['asia'][1]} 
- Europe: 
{int(ave_list[1]['europe'][0])//15 * '█'} {ave_list[1]['europe'][1]} 
- Africa: 
{int(ave_list[2]['africa'][0])//15 * '█'} {ave_list[2]['africa'][1]} 
- Pacific: 
{int(ave_list[3]['pacific'][0])//15 * '█'} {ave_list[3]['pacific'][1]} 
- America: 
{int(ave_list[4]['america'][0])//15 * '█'} {ave_list[4]['america'][1]}
- Australia: 
{int(ave_list[5]['australia'][0])//15 * '█'} {ave_list[5]['australia'][1]} 
- Atlantic: 
{int(ave_list[6]['atlantic'][0])//15 * '█'} {ave_list[6]['atlantic'][1]} 
- Indian: 
{int(ave_list[7]['indian'][0])//15 * '█'} {ave_list[7]['indian'][1]} 
==================================================================
''')
            query = input("Go Back (Y): ").strip()
            if query.lower() == "y":
                break 
            else: 
                print(">>>> Invalid Output\n")

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
