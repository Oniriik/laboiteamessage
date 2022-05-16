# Disclaimer
   This code is not 'Public' ready, I will rewrite it ASAP ! 
# laboiteamessage
   Laboiteamessage is a Instagram / Twitter bot, users can send anonymous messages to people on this two platforms.<br/><br/>
   There is a website ( simple static form ) where user select the platform then input the target's @ and the message. 
   By clicking sumbmit infos are sent to a strapi Rest API.<br/><br/>
   
   Each x time, the program fetch pending message and post them on the selected platform.
   
   Twitter :<br/>
   It use tweepy library (twitter api based library) to post a tweet using this format `@target : message`. The target get mentionned and receive the message.<br/><br/>
   Instagram:<br/>
   It use pillow to create a custom image displaying the target's @ and use selenium to automate a chrome instance and make a new publication using custom image and set as `@target : message`.
   The target get mentionned and receive the message.<br/><br/>
   
   Unfortunately instagram limit my posts rate so i decided to stop the project until i find an alternative and twitter banned my account :/<br/><br/>
   https://www.instagram.com/laboiteamessage<br/>
 
   Post example:<br/><br/>
   ![example](https://i.ibb.co/2gJbGLQ/laboiteamessage.jpg)
   
   
   
   
