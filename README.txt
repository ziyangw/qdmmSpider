*******************************-Requirement-**********************************

This project is mainly written in python 2.7.
In order to run the project, please install the following packages:
python 2.7	scrapy 1.1 	 twisted   pillow 3.3  
MySQL 5.7	django 1.10  django_bootsrap3   
memcached 1.4    python_memcached 1.58

For enabling django debugging, please install django_debug_toolbar

For using virtual environment, please install virtualenv

****************************-Run the Project-*********************************

Initialize a virtual environment:
go to ./qdmmDjango directory, start the environment:
	$source qdmmvm/bin/activate
end the environment:
	$deactivate


Create database and table:
commands are specified in ./qdmmSQLdb/database.sql


Collect data through scrapy:
in this directory, type in terminal
	$scrapy crawl qdmm
Pipeline options at ./EasySpider/settings.py:
	Enable EasySpider.pipelines.JsonlinesWriterPipeline to store scraped data locally in text file
	Enable EasySpider.pipelines.ImageDownloadPipeline to store scraped image locally in jpg file
	Enable EasySpider.pipelines.SQLStorePipeline to store scraped data locally in MySQL database
	Enable EasySpider.pipelines.DjangoStorePipeline to store scraped data into django specified database
	Enable EasySpider.pipelines.DjangoImageStorePipeline to store image locally where django object imagefield can access


Run django:
go to ./qdmmDjango, run server:
	$python manage.py runserver
DEBUG is set to True by default, set it to False to disable django_debug_toolbar


To activate memcache:
find where memcache is downloaded:
	$which memcached
copy the path:
	$path_copied -d

