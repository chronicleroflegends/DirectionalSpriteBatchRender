# Chrono's Directional Sprite Batch Render
 A directional sprite batch render addon for blender.
 
## Uses:
 * Generate a sequence of images that can be used as animation in any 2.5d game engine.
 * No complicated camera or parenting setup, includes buttons to generate what you need and set render settings.
 * Enter a few settings, click Render, and take a break! Come back to a folder of images sorted by animation and direction.

## Inspiration:
 The original idea for this addon is not mine, and instead belongs to seece's [SpriteBatchRender](https://github.com/seece/SpriteBatchRender).
 I have re-written the script from scratch to be compatible with newer versions of Blender, as well as tweaked a few things to make the user interface more to my liking. I made this addon to help with rendering sprites for a mod for GZDoom I am working on, but it should be useful for a number of different types of games.

## Installation:
 1) Download the newest release from the sidebar and unzip it somewhere you can find it.
 2) Open Blender and navigate to Edit > Preferences > Addons and click install.
 3) Open the folder you unzipped and select SpriteRenderer.py
 4) When Blender finishes installing the addon, make sure you check the box to activate it.

## Instructions for use:

 ### Basic Instructions
 Get started with a sample scene to get to know the tool.
 1) Make a new project.
 2) Delete the default camera, but leave the cube and light.
 3) Navigate to your Properties Panel > Output Properties > Chrono's Directional Sprite Renderer.
 4) Click 'Set render transparent'. You may not see any changes, but this ensures you will have sprites with transparent backgrounds.
 5) Click the default cube, and optionally move it up 1 unit so it sits on the 'ground'.
 6) Back in the addon, (with the default cube still selected) click 'Create RotationOrigin'. A circle should appear on the ground under the default cube. You can now move and rotate the default cube using this circle. Leave it where it is.
 7) Make sure the default cube is still selected and click 'Create SpriteCamera'. A new camera should appear, with a line connecting it to a small sphere inside of the cube.
 8) Move the sphere called 'CameraTarget' on the Z axis to be in the center of the cube (If it isn't already there.) The camera will always point directly at this sphere.
 9) Change to active camera view and move the Camera on the Z and Y axis until you can clearly see the cube in the center of the camera's view.
 10) It is unnecessary to move CameraTarget on the X or Y axes. Similarly you should not move the SpriteCamera on the X axis. The addon will handle all rotation in just a bit.
 11) Now your scene is set up and almost ready!
 12) Change these settings for a test render:
     * Sprite Export Path: Create a new folder to put your test sprites in. When you click render all the generated sprites will appear in this folder.
     * Angles to Render: Click on '8 Dir' for now, I will explain the other options in a bit.
     * Animation: This is probably set to some absurdly high number. Change it to 'Start Frame 1' 'End Frame 1'
     * Resolution: Set this to 800px by 800px
 13) You are ready to render! This is **VERY IMPORTANT**: Click the circle 'RotationOrigin' and then click the big render button. If you don't click the RotationOrigin first, your renders will probably come out aligned wierd. The addon expects it to be the active object when it starts rendering.
 14) Oh no! Nothing changed on the screen and Blender isn't responding! If I click on anything I just get the frozen hourglass of doom! 
 You are fine, don't worry. The rendering is happening as a background process, so you cannot see anything happening. Depending on the complexity of this scene this may continue for a while. (The objects I was using to test took about 3 minutes. The default cube should only halt things for about half a minute.) When Blender starts responding again go look in the folder you specified in step 12. You should see 8 images of the cube from different angles. Success!
 15) Now go on and use this to render your own sprites. Make some cool games for me to play!

### Details of each of the addon's functions:
* Set Render Transparent - I always forget to change the render background to transparent, so I made a button so you don't have to go searching for it!
* Create RotationOrigin - This creates an empty with a circle shape to act as a turntable for your object. The selected object gets parented to this. Select your rig if it is an animated character model.
* Create SpriteCamera - This is completely optional. If you have your own camera setup already, use that instead. This just sets up a simple targeted camera in roughly the right position.
* Sprite Export Path - This is just the folder to generate your sprites in.
* Sprite Prefix - This is the general name of your sprites. All the generated sprites will start with this prefix. It's default is 'SPRI' because it is setup in ZDoom's sprite format, which is: SPRIA1 - Prefix|Frame|Angle. In the ZDoom engine, the prefix can only be 4 characters, if you are using this for any other game engine, feel free to use as many characters as you want for the prefix.
* Angles to render - How many directions do you want to render the object from? 1 Direction will only give you the camera view for each frame. 8 direction gives you the standard doom billboard sprites. 16 Dir gives a more detailed billboard sprite.
* Custom Angles - This just directly sets the angles to render. Some examples of what you could set this to would be 2 for a sidescroller, or 4 for an isometric top-down RPG.
* Frame Names - When the images are saved, letters are used instead of numbers. This is because of the Doom sprite format again. Frames are designated by letters and angles by numbers. If enough people tell me they need more frames of animation than there are letters of the alphabet, I'll make a toggle that swaps the two around.
* Animation - Set your start and end frames for your animation here. I would recommend rendering out each animation 1 at a time and giving them each a unique prefix instead of doing all of the objects animations at once.
* Resolution - This just does the same thing that the dimension controls higher up in the output properties do. I just duplicated them here for conveniance.
* Render - This sets it all in motion. Remember, don't get scared when Blender stops responding! Its just working to get all that rendering done for you in the background.

### License:
GNU General Public License v3.0

You are free to do whatever you want with this, no need to credit me. Just use it to make some cool stuff!
