# MadnessTheBot
A Tweet bot that runs on Repl.it and tweets final scores of D1 NCAA men's basketball games.

Here is the Repl.it: https://repl.it/@joekreydt/MadnessTheBot10

A scheduled job is configured at cron-job.org. It makes an HTTP request to https://MadnessTheBot10--joekreydt.repl.co every 2 minutes.

There is one file in the Repl.it that you will not see in this GitHub repo: the .env file. It holds Twitter API OAuth codes which are kept private.

Current status: The bot is currently not working because it violates Twitter's policy by sending out too many tweets when several games finish up within a close time frame. I am considering other functions instead: only tweeting game scores when a user tweets a team name @MadnessTheBot, only tweeting final scores of the 64 highest ranked teams, combining the scores of games which finish in close proximity (time-wise) into a single tweet.
