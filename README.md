# Covid-19 Dashboard

### Introduction
The Covid-19 Dashboard allows users to keep up with up to date Covid-19 data across all of England,
in addition to Covid-19 7 day infection data of an English city of their choice. Furthermore, the
dashboard will display the latest English news regarding Covid-19. The user will also be abel to 
schedule up data and news updates for a given time.
### App Features
- Provides news and Covid-19 data updates 
- The user can schedule updates 
- The user can cancel an update
- The user can remove any article, which will not reapear when news updated  
- The news are set to update on an hourly basis not to miss out on any potential headlines 
- Updates can be scheduled on repeat, which will update an item everyday at the specified time 

### Prerequisites
  - Python 3.7+ (I am using version 3.10)
  - An IDE or texteditor (ex. Pycharm, Visual Studio Code, Sublime, etc.)
  - [news] API keys
  - Internet connection
  
### Installation
To install **flask**, run:
```sh
$ pip install Flask
```
To install **uk-covid19**, run:
```sh
$ pip install uk-covid19
```

### How to use
- Run dashboard.py in terminal (mac), command prompt (windows) and search http://127.0.0.1:5000/index
- Once the user is on the site they will see the Covid-19 data and a list of the news
- If the user wishes to scheduel an update they will need to chose a time and a name for the update
- There are 3 boxes which represent what type of update they will schedule
- The boxes can be checked individualy or all together
- If the repeat box is checked then the updates will happen everyday at the same time
- **Nothing** will happen if you set a time that has already passed
- To cancel a scheduled update simply click on the "x" on the top right of the update box
- To remove a news article click on the "x" on the top right of the news article
- Once an artcile is removed it will no longer apear even if you update the news

### Developer's guide
- Download and place all the files in one direcotory
- Download the templates file rename it to index.html
and place it in a folder called templates in the same
directory
- First, make sure to get the API key from the [news] website to be able to pull the news articles
- The code has been designed to show Covid-19 data and news regarding the UK 
- The Covid-19 data cannot be changed for cities or countries outside of the UK, however, if you open the config.json file you will see that there are many english cities you can chose. For the news, you can change the country, language, and the key words to filter the news articles for. 
- To pull data from the config file, config['example'] where example is the name of the dictionary key
- There are plenty of different options to customize the updates. For a full guide on how to access and implement these choices, follow the developer's guide on these websites: 
-- News: https://newsapi.org/docs/endpoints/sources
-- Covid-19: https://coronavirus.data.gov.uk/details/developers-guide
- Feel free to add anything new to the config file, if it is missing something that can improve the 
customizability of the code

### Testing 
- The request-response cycle of the news and weather API was tested using the assert method to confirm that the cycle was completed successfully. 
- To ensure that all the features work as expected, the app was loaded and the features were tested from a user's perspective
- All testing results will be logged so we can keep track of anything that fails the test
- Testing will be scheduled on an hourly basis


### Links and Sources
- News API: https://newsapi.org/docs/endpoints/sources
- Covid-19 API: https://coronavirus.data.gov.uk/details/developers-guide
- Flask guide: https://flask.palletsprojects.com/en/1.1.x/quickstart/


### License
Copyright (c) [2020] [Grygoriy Vanetsyan]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files "covid19-dashboard", to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.






   [weather]: <https://openweathermap.orgr>
   [news]: <https://newsapi.org/>
   
