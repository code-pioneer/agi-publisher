from videos.agis import generate_filename, generate_image, generate_social_post, generate_transcript, save_to_file, search_serper, generate_video

def agent_tools():
    tools = []
    tools.append(generate_transcript.setup())
    tools.append(save_to_file.setup())
    tools.append(generate_filename.setup())
    tools.append(generate_image.setup())
    tools.append(generate_video.setup())
    # tools.append(search_serper.setup())
    tools.append(generate_social_post.setup())
    return tools

def tools_profiles():
    profiles = []
    tools = agent_tools()
    for tool in tools:
        profiles.append(tool_profile(tool.name))
    return profiles


def tool_profile(tool_name):
    if profile[tool_name]:
        return profile[tool_name]
    return None

profile = {

    "generate_transcript" : {      
        "name": "Transcript Craftsman",
        "profile": "Transcript Craftsman",
        "task": "Transcript Creation",
        "url": "assets/img/creater.png",
        "start_message": "Armed with inspiration from our Google search, it's time to kickstart the transcript creation process. Let's turn these ideas into engaging content!",
        "end_message": "Transcript creation complete! Drawing from our search results, we've crafted compelling content ready to captivate our audience. Ready to share our insights with the world!",
        },
    
    "save_to_file" : {
        "name": "Publisher",
        "profile": "Publisher",
        "task": "File Saving",
        "url": "assets/img/publisher.png",
        "start_message": "Taking the important step of saving our video content. Let's ensure our hard work is securely stored for future reference and potential updates.",
        "end_message": "Video content successfully saved! Our work is now safely stored, ready for future reference or any necessary revisions. Time to celebrate this milestone!",
        },
    "generate_filename" : {
        "name": "Publisher",
        "profile": "Publisher",
        "task": "Naming",
        "url": "assets/img/publisher.png",
        "start_message": "Gotcha! I'll whip up a catchy title for the video",
        "end_message": "All set! Created Catchy title for the video",
        },
    "generate_image" : {
        "name": "Art Illustrator",
        "profile": "Art Illustrator",
        "task": "Image Generation",
        "url": "assets/img/artist.png",
        "start_message": "I'll craft an eye-catching image to go along with the title",
        "end_message": "Finished! Completed image to complement the video title",
        },
    "generate_video" : {
        "name": "Video Illustrator",
        "profile": "Video Illustrator",
        "task": "Video Generation",
        "url": "assets/img/artist.png",
        "start_message": "I'll craft an eye-catching video to go along with the content",
        "end_message": "Finished! Completed video to complement the video content",
        },
    "search_serper" : {
        "name": "Researcher",
        "profile": "Researcher",
        "task": "Google Search",
        "url": "assets/img/searcher.png",
        "start_message": "Time to gather some inspiration! Initiating a Google search to find engaging content for our blog writing journey.",
        "end_message": "Mission accomplished! We've found some valuable content to fuel our blog writing journey.",
        },
    "organizer" : {
        "name": "Organizer",
        "profile": "Organizer",
        "task": "Orchestration",
        "url": "assets/img/Designer.png",
        "start_message": "Embarking on the orchestration of our video creation process. Let's synchronize our efforts, streamline tasks, and bring our collective vision to life!",
        "end_message": "Mission accomplished! Through effective orchestration, we've successfully navigated the blog creation process, culminating in a cohesive and engaging final product. Cheers to teamwork and creativity!",
        },
    "generate_social_post" : {
        "name": "Influencer",
        "profile": "Influencer",
        "task": "Social Post Content",
        "url": "assets/img/social-avatar.png",
        "start_message": "Time to engage our audience! Beginning the process of crafting captivating social media posts to share our latest blog content and spark conversations.",
        "end_message": "Posting complete! Our social media channels are now buzzing with excitement as we share our latest blog content. Ready to interact with our audience and witness the impact of our work!",
        },
}