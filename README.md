# Recycletron
Recycletron is an AI-powered tool designed to classify trash instantly as recyclable or non-recyclable. It empowers users to make informed decisions about waste disposal, ensuring recyclables don’t end up in landfills. Recycletron is scalable globally, working seamlessly for individuals, businesses, and governments alike. By integrating gamification and educational features, Recycletron not only promotes proper waste management but also makes it engaging and rewarding for users. Whether you’re a global corporation, a developing nation, or simply looking to teach children the value of sustainability, Recycletron is here to help.

# How we built it

Meta’s detectron2 object identification model
Flask for backend implementation
HTML, Javascript for frontend
“Detectron2 is Facebook AI Research's next generation library that provides state-of-the-art detection and segmentation algorithms. It is the successor of Detectron and maskrcnn-benchmark. It supports a number of computer vision research projects and production applications in Facebook.” - From Meta/Facebook GitHub README.md.

Object identification is a class of novel computer vision algorithms that uses advanced methods to find multiple objects within one image. This contrasts with traditional image classification techniques that can only put one label on an image. It does this by first learning how to “split” an image into multiple possible regions where images could exist, and then runs a Convolutional Neural Network, Swin Transformer, or other computer vision models across each region individually. Detectron2 is a library that allows users to test multiple advanced methods, already trained on enormous data of everyday household objects. For more specifics, feel free to check out Detectron2’s detailed documentation.

# Challenges we faced

The largest challenge was finding a class of models that would fit our use case, and being able to understand it well enough to use it. Traditional Convolutional Neural Networks would work okay, but our vision was to have a model that could take a pile of waste and determine what is recyclable and what is not; after all, in households and in recycling factories, where we hope to deploy this technology to facilitate the recycling process and incentivize individuals to recycle, there aren’t usually ways to individually separate each waste material into its own individual picture to then classify. We were able to find object identifying networks, but there are many versions, including YOLO models, R-CNN, and Weak Supervised Segmentation, and finding a codebase that had prepackaged models as well as useable modules was tough. We also ran into challenges when we finally looked to deploy our model. Though these models are extraordinarily fast, they used lots of memory which made it tough to deploy these models through virtual servers. Since we didn't have advanced GPUs, we had to push these models through our cpus, which made them a lot slower and harder to host. We got around this by hosting our backend on one computer, pushing all the calculations from there before sending it back to the frontend for the user to view.

# What's next for Recycletron

We wanted to make Recycletron more gamified, so that users could log in, upload images, and be rewarded for recycling and also adding to our database of recycled items. We added a basic framework for username, password, and score storage but in the future we would like to fully develop this into a sort of game. While deploying our model, we struggled with finding a way to host the network. Virtual machines would get overloaded with their low memory, and our computers did not have GPUs, sometimes making inference slow, especially in real-time. In the future we'd like to get a small server with a GPU to have a centralized place for users. There are more advanced object identification models trained on over 20,000 different objects and ready-to-go. An example is the Detic model created by Facebook, which is much more robust than Detectron2. However, these models were too heavy for us to use for inference

# Tech Stack:
Meta’s detectron2 object identification model
Flask, Python for backend implementation
HTML, Javascript for frontend


# Usage: 
1. Clone the repository
2. Run main.py to host the web app in the local computer
3. Upload an image to identify recyclable vs. non-recyclable items.
4. Using a camera to real-time classify between recyclable vs. non-recyclable items.

## Wireframe
# Miro Board
<img width="937" alt="Screenshot 2024-10-13 at 7 43 58 AM" src="https://github.com/user-attachments/assets/0d726810-2b54-47fc-82b1-650f45ece234">
