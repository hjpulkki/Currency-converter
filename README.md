# Currency-converter
Web application which generates easy to remember formulas to calculate currency conversions quickly without a calculator.

The formulas are generated with a python script and saved into a .csv file. That file is used as part of an lambda function on Amazon Web Services to provide formulas quickly to the user via an API gateway. The frontend, also included in the project, uses various JavaScript libraries to visualise the results to the user.

This demonstration is running at http://webappsheikki.s3.amazonaws.com/index.html

If you are interested of writing your own front end without having to worry about lambda functions and such, feel free to use my API at https://gmkydyl926.execute-api.eu-west-1.amazonaws.com/V1/rate/1.8
