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
