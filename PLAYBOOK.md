## COS 460/540 - Computer Networks
# Project 2: HTTP Server

# <<Sarah Lawrence>>

This project is written in <<Python>> on <<MacOS>>.

## How to compile
The compatable python version used was:
- Python 3.11.0

## How to run
Batch file:
- Http_Server.py

How to run the project on browser:
1. Terminal Run: python3 Http_Server.py 2247
2. Browser one: http://localhost:2247/www/index.html
3. Browser two: http://localhost:2247/www/index.html
4. Browser one: Enjoy cat photo!
5. Browser two: Enjoy your own cat photo!

How to run the project on terminal:
1. Terminal Run: python3 Http_Server.py /www 2247
2. Terminal two: nc localhost 2247
3. Terminal two: GET www/index.html HTTP/1.1
                 User-Agent: Simple-Client/0.5
4. Terminal two: Enjoy header and Html!

## My experience with this project
Brief summary of your experience with the project and what was learned.

Overall, I learned how to parse a request and how to respond to it. The request was parsed by the command GET and by the file path (ex,/pub/WWW/index.html). The response used the file path to then give the appropriate header. If the path was there, return a 200 header; else, return a 404 header. This then sent the header and the file contents to the HTTP server. 

It's silly, but I learned that formatting is very important. In response_codes for the headers, I didn't have \r\n to help go to the start of the next line. I only had \n. This messed with the site's formatting and made it so images wouldn't work at all. I fixed this, and the formatting was fixed. I then tested the site on Safari, and it broke due to a similar formatting error. Something fun I learned was that the request had the file path it wanted in it. I didn't understand it at first, but after this, I thought it was cool. 


