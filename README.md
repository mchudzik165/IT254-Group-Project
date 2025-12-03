# IT254-Group-Project

10/2/25
Group members: Elliot Cabrera, Brayden Bergman, Michael Chudzik, Matt Lyjak

Project Concept:
Our project concept is a basic home security system powered by AI that uses face detection to let in and stop individuals. It'll warn in the case of an individual that tried to scan in but did so unsuccessfully. We haven't gotten to far in the concept, but it'll most likely flash a light that signals there has been a error scanning the individual's face. The AI will be trained based on our own faces and possibly even on our face expressions. Using face expressions, it will detect the mood or expression a person trying to scan in is safe to let in or not. A person smiling for example will be allowed in and let the door open along with signal with a LED meaning "OK". A person that looks upset/AI deems to be mad or angry will not let in the person and keep the door closed along with signalling a LED to show an error or access denied. The system concept itself seems pretty simple hardware wise, however, programming it may lead into some difficulties. 

Items List: (Not final)
We are most likely planning to use Google Teachable Machine, so we will need:
- A desktop camera
- Servo/s for the door opening system (?)
- Sensor of some sort to ensure door is closed
- Small breadboard
- LED light nodes to check status

10/7/25
Group members met up and created a basic AI algorithm based on photos we captured of ourselves using Teachable Machine. We created three models with the first one being all of us individually as seperate classes and one extra background class to ensure it functions. Were not happy with results and decided to shorten classes down to two classes of being "group members" which is photos of everyone in a group and a background class to simplify the decision-making process of the AI. We then further expanded on the version three of the AI and added more images of the group members to make it appear more accurate. At this stage, we are currently using partially AI-generated code to set a baseline and to see what we can approve upon in terms of our data collection for the Teachable Machine AI. It is not a lot of progress currently, but we are mainly focusing on trying to make a reasonably accurate Teachable Machine AI with the intention to develop new code for the final Arduino system. We just wanted a demo to show off our progress with training our AI to detect people and faces. Outside of that, we have discussed future plans of our project such as making a custom door from cardboard and creating new code for the final product. 

11/9/25
Video instructions / work contributions video: https://youtu.be/_8OfGQ6yXf0 

Quite a lot has happened as its been over a month! I may not remember everything off the top of my head, but I'll try my best to keep the most informed I can be.

1. We finally have a door built thats ready for the code to be developed and implemented. While I do not have any photos, one of my group members, Brayden does as he was the one leading the project to build it. It does work as intended as he has a video demostrating how the door works via motion sensor.
2. We updated our Teachable Machine AI with more photos of ourselves. However, we ran into some issues. However, more on that later.

In terms of progress, its been going well, although slow at some points. As I mentioned previously, we built a door for our final product along with updating the AI machine learning from Teachable Machine. This is great but we are now severely limited by our code. Initially, we generated some code in order to make sure our AI runs on python and we know how to set up the process. It's worked great for this purpose however as we developed our AI models more, we noticed it being further more innacurate and just outright giving the wrong outputs. This is a big issue as our entire project is dependent on our faces in order to open the door with facial recognition. We believe its the code as Teachable Machine's built-in tester with the same exact model works great and is extremely accurate. As of right now, we are looking into it slowly and may just develop a new code entirely, as the current one is after all, still a testbench and probably shouldn't really be used with our final product. There could be some possible solutions we can import from HuggingFace, however we just haven't checked just yet. We would still like to develop the code on our own and see where we can try to improve on. Such as making a box tracking the person it wanting to scan or having the data displayed on the screen all at one current moment so we can further debug and see what the AI is exactly seeing based on its confidence level. 

12/2/25
We progressed a lot in a month and are happy to say we are done with the project for the most part. Some of the things that happened were the following:
1. I simplified and improved the face_detector.py code. Moving into converted_keras(5) with individual labels for each group member and added AI-generated images of individuals to better distinguish the group members from strangers. As a result, the facial detection system is a little more accurate now but still doesn't read quite right. It also now displays a live input of what its seeing and the confidence level percentage of what it sees. With camera detection system finalized, its now easier to intergrate into the arduino code.
2. Matt and Brayden wanted to handle the physical creation of the end product along with the arduino intergration. So a 3D printed door was made along with a basic circuit hooked up to a servo from the arduino IDE board itself. They then built a cardboard box to contain the arduino and the door for the final product. However, due to the inconsistency the AI camera was presenting, it was coded to open if it detected a face of a group members for longer than 3 seconds. This is to ensure that the door wouldn't constantly open and close based on what its actively seeing, but rather as a delayed input. 

Overall, the end product came out decently well, though construction could had been better due to the door not being mounted correctly, but the end product still worked and was able to successfully complete our final demo. It was very fun and I hope others may reuse the code to build their own detection systems.
