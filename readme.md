# Flask Toy Project
An EC2 instance scheduler CRUD application flask.

## Built Using
* Python3
* Flask
* AWS

## Create Virtual environment
1. Install virual environment
   > pip install virtualenv
2. Create a virual environment
   > virtualenv environment_name
3. Activate the virual environment
   > source environment_name/bin/activate

## Install the requiremnts
> pip install -r requirements.txt

## Run the Project locally
1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in flask_scheduler_app/.env file
2. Go to the flask_scheduler_app directory
3. Run the flask app
   ```
   flask run
   ```
4. Go to the link generated in the previous step.
5. To create the schedule, hit the URL with ```/create``` endpoint. This is a POST method. The request body will be
   ```
   {
        "schedule_name": "test_schedule_v1",
        "instance": {
            "id": "i-0f9761e0354c04272"
        },
        "days" : ["SAT"],
        "status": "start"
    }
   ```
   or if you want to give the tag-name pair of instance 

   ```
   {
        "schedule_name": "test_schedule_v1",
        "instance": {
            "key_tag": "Tag",
            "value_tag": "Value"
        },
        "days" : ["SAT"],
        "status": "start"
    }
   ```

   Note: ```days``` is a list which can have elements like
   ```
   ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
   ```
6. To update the schedule, endpoint will be ```/update```. This is a POST method. Request body will be same as in the above step.
7. To delete the schedule, endpoint will be ```/delete```. This is a POST method. Request body will be
   ```
   {
        "schedule_name": "test_schedule_v1",
        "instance": {
            "key_tag": "Tag",
            "value_tag": "Value"
        }
    }
   ```

   OR
   ```
   {
        "schedule_name": "test_schedule_v1",
        "instance": {
            "id": "i-0f9761e0354c04272"
        }
    }
   ```
8. To read all the schedules, endpoint will be ```/read```. This is GET method.
9. Press ```CTRL+C``` to quit the local server.
10. Deactivate the virtual environment
   > deactivate

# Author
Sharad Mishra - _rishimishra267@gmail.com_