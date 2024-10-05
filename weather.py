import requests, smtplib, json
from tkinter import *

my_email = "mallibennur141@gmail.com"
my_password = "ymwsvxlbaonwildr"

while True:
    add_or_send = input("Do you want to add or send or exit : ")

    if add_or_send.capitalize() == "Add":
        num_of_districts = int(input("Enter the number of districts : "))
        taluks = []
        district_taluk_dictionary = {}

        for i in range(num_of_districts):

            district = input("Enter the name of the district : ")
            num_of_taluks = int(input(f"Enter the number of the taluks in {district} : "))

            district_taluk_dictionary[district] = []

            for i in range(num_of_taluks):
                taluk = input("Enter the taluk : ")
                taluks.append(taluk)

                email = input("Enter the email : ")
                district_taluk_dictionary[district].append({taluk: email})

        with open(r"datafile.json", "a") as weather_file:
            json.dump(district_taluk_dictionary, weather_file)

    elif add_or_send.capitalize() == "Send":

        window = Tk()
        window.config(bg="#d17ef7")
        window.geometry("600x400")
        window.title("Weather report")

        new_districts = Label(window, text="Enter the District", font=("Courier New", 18, "bold"), fg="#2060e8")
        new_districts.pack(padx=50, pady=50)

        new_districts_entry = Entry(window, width=20, font=("Courier New", 18, "bold"), fg="#000000")
        new_districts_entry.pack(padx=50, pady=25)


        def submit_emails():

            global district_taluk_dictionary, new_districts_entry, taluk, email

            with open("datafile.json", "r") as weather_json:
                text = weather_json.read()
                final_data = json.loads(text)

            list_of_districts = final_data[new_districts_entry.get()]
            APIID_weather = "2fc2cad49eaa563a6a1e1a4c2cdbcb8a"

            for i in range(len(list_of_districts)):

                keyss = list(list_of_districts[i].keys())

                keys_list = []
                for j in range(len(list_of_districts)):
                    keys_list.append(list((list_of_districts[j].keys()))[0])

                response_weather = requests.get(
                    f"https://api.openweathermap.org/data/2.5/forecast?q={keyss[0]}&cnt=25&appid={APIID_weather}")

                try:
                    base = response_weather.json()['list']

                    temperature1 = (round(base[1]['main']['temp'] - 273.15, 2))
                    pressure1 = base[1]['main']['pressure']
                    humidity1 = base[1]['main']['humidity']
                    description1 = base[1]['weather'][0]['description']
                    cloud_percentage1 = base[1]['clouds']['all']
                    date_current1 = str(base[1]['dt_txt']).split()[0]

                    temperature2 = (round(base[9]['main']['temp'] - 273.15, 2))
                    pressure2 = base[9]['main']['pressure']
                    humidity2 = base[9]['main']['humidity']
                    description2 = base[9]['weather'][0]['description']
                    cloud_percentage2 = base[9]['clouds']['all']
                    date_current2 = str(base[9]['dt_txt']).split()[0]

                    temperature3 = (round(base[17]['main']['temp'] - 273.15, 2))
                    pressure3 = base[17]['main']['pressure']
                    humidity3 = base[17]['main']['humidity']
                    description3 = base[17]['weather'][0]['description']
                    cloud_percentage3 = base[17]['clouds']['all']
                    date_current3 = str(base[17]['dt_txt']).split()[0]

                    APIID_ltlg = "5bfbb8ab8b754c48b56c25c421beec8a"

                    response_ltlg = requests.get(
                        f"https://api.geoapify.com/v1/geocode/search?text={keyss[0]}&lang=en&limit=5&format=json&apiKey={APIID_ltlg}")

                    latitude = response_ltlg.json()["results"][0]["lat"]
                    longitude = response_ltlg.json()["results"][0]["lon"]

                    repsonse_pollution = requests.get(
                        f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={APIID_weather}")

                    aqi = repsonse_pollution.json()["list"][0]['main']['aqi']

                    base_components = repsonse_pollution.json()["list"][0]['components']

                    co = base_components['co']
                    no = base_components['no']
                    no2 = base_components['no2']
                    o3 = base_components['o3']
                    so2 = base_components['so2']
                    nh3 = base_components['nh3']

                    weather_message = (f"Subject:Yeh There!!Weather report update here in {keyss[0].capitalize()}!\n\n"
                                       f"Weather on {date_current1}\n"
                                       f"\nTemperature is {temperature1}C\n"
                                       f"Pressure is {pressure1} millibar\n"
                                       f"Humidity is {humidity1} %\n"
                                       f"Climate is of {description1}\n"
                                       f"Clouds are present in {cloud_percentage1}%\n"
                                       f"\nWeather on {date_current2}\n"
                                       f"\nTemperature is {temperature2}C\n"
                                       f"Pressure is {pressure2} millibar\n"
                                       f"Humidity is {humidity2} %\n"
                                       f"Climate is of {description2}\n"
                                       f"Clouds are present in {cloud_percentage2}%\n"
                                       f"\nWeather on {date_current3}\n"
                                       f"\nTemperature is {temperature3}C\n"
                                       f"Pressure is {pressure3} millibar\n"
                                       f"Humidity is {humidity3} %\n"
                                       f"Climate is of {description3}\n"
                                       f"Clouds are present in {cloud_percentage3}%\n")

                    pollution_message = (
                        f"\nThe amount of different gases (microgram/cubic meter) present in given place are as follows\n\n"
                        f"Carbon Monoxide : {co}\n"
                        f"Nirogen oxide : {no}\n"
                        f"Nirogen Dioxide : {no2}\n"
                        f"Oxygen Trioxide/Ozone : {o3}\n"
                        f"Sulpher Dioxide : {so2}\n"
                        f"Ammonia : {nh3}\n\n")

                    aqi_dictionary = {5: "Air Quality Index is 5. Very poor air quality!!\n",
                                      4: "Air Quality Index is 4. Poor air quality!\n",
                                      3: "Air Quality Index is 3. Moderate air quality!\n",
                                      2: "Air Quality Index is 2. Fair air quality!\n",
                                      1: "Air Quality index is 1. Very good air quality!!\n"}

                    if (80 <= humidity1 <= 100 or 80 <= humidity2 <= 100 or 80 <= humidity2 <= 100) and (
                            950 <= pressure1 <= 1010 or 950 <= pressure2 <= 1010 or 950 <= pressure3 <= 1010):
                        message = (weather_message + pollution_message + aqi_dictionary[aqi] +
                                   f"\nWarning Alert!!\n"
                                   f"Climate conditions indicating cyclone weather!\n"
                                   f"Please take the possible precautions as soon as possible\n")

                    else:
                        message = (weather_message + pollution_message + aqi_dictionary[aqi] +
                                   f"\nNo extreme weather. Enjoy the climate in {keyss[0]}\n")

                    connection = smtplib.SMTP("smtp.gmail.com", port=587)
                    connection.starttls()

                    connection.login(user=my_email, password=my_password)
                    connection.sendmail(from_addr=my_email, to_addrs=list_of_districts[i][keys_list[i]], msg=message)
                    connection.close()

                    successfull_label = Label(window, text="EMAIL SENT SUCCESSFULLY!!",
                                              font=("Times New Roman", 14, "bold"), fg="#d2a319")
                    successfull_label.pack(padx=50, pady=25)
                    print("Email sent successfully!!")
                    print("Check your email")

                except:
                    error_label = Label(window, text="INVALID INPUT", fg="#d2a319",
                                        font=("Times New Roman", 14, "bold"))
                    error_label.pack(padx=50, pady=25)


        submit_button = Button(window, text="Submit emails", command=submit_emails, font=("Courier New", 18, "bold"),
                               fg="#e0283b")
        submit_button.pack(padx=50, pady=40)
        window.mainloop()

    elif add_or_send.capitalize() == "Exit":
        print("Thank you")
        break