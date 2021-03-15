# TimeTrackingBot

Find me on telegram: `@worktimetracking_bot`.  

This bot will help you to keep track of your work periods. 
Just start a conversation with the bot and follow the instructions.  

### Functionalities 
 - Clock In/Out (with an obligatory description when you clock out).
 - Generate reports of many distinct periods.
 - Edit entries.
 - Erase all personal data.

## Privacy 
All your data will be stored in plain text in a NoSQL database managed by Amazon Web Services (DynamoDB).  
Although I promise to you that I won't -in any time- look at your data, collect it or analyze it in any form you still might be 
concerned about the lack of privacy when using the bot. In this case you can, first, delete all your data from my database and run your 
own instance of the bot. Check the developer sections below for more instructions.  

## Developer section
### Infrastructure 
The bot is being deployed in AWS Lambda, exposed to the web through an API Gateway and storing chat/user data in DynamoDB.  
Due to this configuration, the bot is running with a free tier usage of the services, and probably will remain in this place forever.  

For the ease of provisioning and deploying the project on the cloud, Pulumi is being used.  

__docs being improved__

