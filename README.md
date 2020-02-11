#### Task 1.
Write aggregator service.

##### Preset:
* Fill database random data.

##### Required:
* Dockerfile
* docker-compose.yml
* Makefile
* requirements.txt
* generator.py - Fill database random data for last year (should be at least 200 000 records per month).

##### Database:
* MySQL

##### Routes:

* Healthcheck:
    * GET `/healthcheck` - check database
    * Example:
        ```
        <- GET /healthcheck
        -> Http code 200
        ```

* Gathering:
    * POST `/event?id=[int lenght 4]&uid=[int lenght 4]&action=[string lenght 4-12]`
    * Example:
        ```
        <- POST /event?id=9999&uid=9999&action=test
        -> Http code 200
        ```

* Count by day:
    * GET `/count?day=[dd-mm-yyyy]&id=[int lenght 4]`
	* GET `/count?day=[dd-mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]`
	* GET `/count?day=[dd-mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]&action=[string lenght 4-12]`
	* GET `/count?day=[dd-mm-yyyy]&action=[string lenght 4-12]`
	* Example:
        ```
        <- GET /count?day=01-01-2019&id=9999
	    -> 20
        ```

* Count by month:
    * GET `/count?month=[mm-yyyy]&id=[int lenght 4]`
	* GET `/count?month=[mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]`
	* GET `/count?month=[mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]&action=[string lenght 4-12]`
	* GET `/count?month=[mm-yyyy]&action=[string lenght 4-12]`
	* Example:
        ```
	    <- GET /count?month=01-2019&id=9999
	    -> 20
	    ```

* Statistics by day:
	* GET `/stats?day=[dd-mm-yyyy]&id=[int lenght 4]`
	* GET `/stats?day=[dd-mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]`
	* GET `/stats?day=[dd-mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]&action=[string lenght 4-12]`
	* GET `/stats?day=[dd-mm-yyyy]&action=[string lenght 4-12]`
	* Example:
        ```
        <- GET /stats?day=01-01-2019&id=9999
	    -> 9999,9999,01-01-2019,test,20
	    ```

* Statistics by month:
	* GET `/stats?month=[mm-yyyy]&id=[int lenght 4]`
	* GET `/stats?month=[mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]`
	* GET `/stats?month=[mm-yyyy]&id=[int lenght 4]&uid=[int lenght 4]&action=[string lenght 4-12]`
	* GET `/stats?month=[mm-yyyy]&action=[string lenght 4-12]`
	* Example:
	    ```
    	<- GET /stats?month=01-2019&id=9999
	    -> 9999,9999,01-01-2019,test,20
	    ```
