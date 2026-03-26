# Web Scraping of Minecraft Fandom

### Tools used:
1. Claude Code
2. Python
3. Libraries Cloudscraper and beautifulsoup4


### Link: https://minecraft-archive.fandom.com/robots.txt

### What did I found in robot.txt?

I was specifically looking into scraping mobs, and I found this line:"  - /wiki/Mob -- a regular content page which can be scraped. Some of the pages was disallowed, such as user profiles, discussions, and admin pages. 

### What was done?

Scrapes mob data from https://minecraft-archive.fandom.com/wiki/Mob
Collects mob names, links, and classifications (Utility, Passive,
Neutral, Hostile, Boss) from the main Mob page.

### Why did I choose this wiki fandom? 

When I was a kid, I used to play Minecraft a lot with my brother and my cousins. It was a way for us to connect together, and I still remember how bonding and fun it was. Going to servers, building houses and going hunting together and trying not to be close to creeper - all of these adventures still bring me warmth in my heart. Sometimes, I want to play again just to go back to these momennts when you are 12 and all of your cousins together. 

### What did you decide to scrape?

I decided to scrape all of the mobs and their classifications (health, attack_strength, drops, location, link, description). The main reason is I think that the choice of the characters is very unqiue: each of them have specific charcter, their abilities, and their look. Learning from our lectures about how websites, games, artifacts, and data might just disappear one day - it's scary. I would love to have the data on Mob's web scraped to preserve these characters and use it as a historical artifact. 


### WHy it might be valuable / useful for researchers? 

I think researches whio care about game preservation might use this data simply as a historical artifact. Other cases it might be used for research projects and charactertiics decisions for the video game characters. Addtionally, it can be used as an idea and brainstorming for future game development.


---
### Disclaimer on AI usage: 

I used Claude AI to assist me with the steps that I should complete for this assignment. After, they were uploaded as a markdown file in the local repo for webscraping. Claude Code DIDN'T web scrapped the website since AI bots in the robot.txt prohibited. ClaudeCode gave snippets of the code to run for webscrapping. 

### Claude Code Flow


1. Get the description and step-by-step guide of the assignment and lesson on webscraping
2. Put it in a markdown file in the folder
3. Checked if the fandom that I found is allowed to scrape with AI bot --> it wasnt allowed to scrape it at all


### Claude Code Prompts

yes it gives me 403 error. Is it cokay to use curl? is it outlined in the assignemrnt steps?  
2.  can I use these fandom wikis??                                                                                      
                                                                                                                      
1. https://minecraft-archive.fandom.com/wiki/Minecraft_Wiki                                                           
2. https://www.minecraftforum.net/                                                                                    
3. https://wiki.hypixel.net/Main_Page

4. now modify web scraping instrcutions for this fandom https://minecraft-archive.fandom.com/wiki/Minecraft_Wiki
5. wait can you explain how does it decide on what to scrape? Did i intrusct it somehow, somewhere?
6. can you explain it to me?    (asking to exaplain the code)

