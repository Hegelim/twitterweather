## About
This project is for the course EECS 6893 Big Data Analytics. Built using some of the most popular
frameworks and packages such as Django, scikit-learn, NLTK, pandas, this project trains 6 different 
regression models and provides a fully functional dashboard which shows the real-time twitter sentiment
prediction based on the current weather condition.

## Installation
To run this project locally, open your terminal and clone the repository
```shell
git clone https://github.com/Sapphirine/202112-49-Quantifying-Correlation-between-Weather-and-Tweet-Sentiment.git
```
Then, create a virtual environment using conda
```shell
conda create --name myenv
```
Activate your environment and install required dependencies from requirements.txt
```shell
conda activate myenv
pip install -r requirements.txt
```
In order for the Django server to run successfully,you need to generate a new secret key
```shell
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Copy and paste that key to twitterweathersite/settings.py and set
```python
SECRET_KEY = "what you just copied"
```
Once you set your secret key, you should not change it. Remember not to push codes with your 
secret key to github. 

Additionally, apply for Twitter Developer API and fill in display\gettwitter.py and display\gettwitter2.py. 
Apply for OpenWeatherMap API and fill in your credential in display\getweather.py

Optionally, if you want to train the models on yourself from fresh, you also need to install Apache Airflow.
See [here](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html#using-pypi) 
for more information.

After installation, you can start the Django server and see the results from local host
```shell
python .\manage.py runserver
```

## Further Info
You can check further info in the articles directory.


## Contact Authors
* Frederico Araujo (fca2118@columbia.edu)
* Yewen Zhou (yz4175@columbia.edu)
* Uday Mukhija (um2158@columbia.edu)