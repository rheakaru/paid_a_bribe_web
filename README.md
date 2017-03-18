I made this bot to go to ipaidabribe.com and pull recent reports of bribes paid in India, and matched this data with a csv file containing information about the Chief Ministers of Indian states. I did this because there's a lot of reports that contain a lot of information and while the website is really cool, I don't think a lot of people visit it or see what they can do about the reports. This app will give them information about their own state and their own representative so they can take action based on the reports.

On of the primary limitations of this data is that ipaidabribe.com didn't have an RSS head, and so I can only get the results on the recent page if I want an updated list. Another problem was that not all the reports followed the same format (people filled out the fields in weird ways) so some of the interesting fields (like descriptions of the event) weren't something I could use in a reliable way. There's a lot of fields of information though and while I used them earlier when tweets about the incidents were sent out, I think this web app does less just because of the format of taking one argument from the user.

Another big challenge was making sense of this page and trying to get the fields because the structure was very specific and unfamiliar to me so it took a while to figure out what was a list, what was a class etc.

Finding data about the CM's of Indian states was fine, but there was no source on Twitter handles so I had to do that manually.

The data transformation I do is find all the relevant reports of bribes from the list and return a count from your state, hopefully so it can give people a big picture idea of the stats instead of them having to go through a bunch of information on ipaidabribe.com.  
