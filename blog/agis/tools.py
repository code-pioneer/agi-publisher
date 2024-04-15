from blog.agis import create_blog, generate_filename, generate_image, generate_social_post, proof_reading_blog, revise_blog, publish_blog_html, publish_blog_md, save_to_file, search_serper

def agent_tools():
    tools = []
    tools.append(create_blog.setup())
    tools.append(proof_reading_blog.setup()) 
    tools.append(revise_blog.setup())       
    tools.append(publish_blog_html.setup())
    # tools.append(publish_blog_md.setup())
    tools.append(save_to_file.setup())
    tools.append(generate_filename.setup())
    tools.append(generate_image.setup())
    tools.append(search_serper.setup())
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

    "create_blog" : {      
        "name": "Content Craftsman",
        "profile": "Content Craftsman",
        "task": "Blog Writing",
        "url": "assets/img/creater.png",
        "start_message": "Armed with inspiration from our Google search, it's time to kickstart the blog creation process. Let's turn these ideas into engaging content!",
        "end_message": "Blog creation complete! Drawing from our search results, we've crafted compelling content ready to captivate our audience. Ready to share our insights with the world!",
        },
    "proof_reading_blog" : {
        "name": "Editor",
        "profile": "Editor",
        "task": "Proof Reading",
        "url": "assets/img/editor.png",
        "start_message": "Time to polish our work! Beginning the crucial step of proofreading and editing to ensure our blog content is flawless and ready to shine.",
        "end_message": "Proofreading and editing complete! Our blog content is now refined and polished, ready to make a lasting impression on our readers. Let's hit publish and share our masterpiece with the world!",
        },
    "revise_blog" : {
        "name": "Editor",
        "profile": "Editor",
        "task": "Blog Editer",
        "url": "assets/img/editor.png",
        "start_message": "Entering the revision phase of our blog journey, incorporating feedback from thorough proofreading. Let's refine our content to ensure clarity, coherence, and impact.",
        "end_message": "Revision complete! Our blog has undergone meticulous scrutiny, resulting in enhanced clarity and coherence. Ready to showcase our refined work to the world!",
        },
    "publish_blog_html" : {
        "name": "Publisher",
        "profile": "Publisher",
        "task": "HTML Preping",
        "url": "assets/img/publisher.png",
        "start_message": "Transitioning to the final stage: preparing our content for publishing as HTML. Let's ensure every detail is in place for a seamless online presentation",
        "end_message": "HTML preparation complete! Our content is now formatted and optimized for online publishing. It's time to hit the 'publish' button and share our creation with the world!",
        },
    "publish_blog_md" : {
        "name": "Publisher",
        "profile": "Publisher",
        "task": "Markdown Preping",
        "url": "assets/img/publisher.png",
        "start_message": "Transitioning to the final stage: preparing our content for publishing as Markdown. Let's ensure every detail is in place for a seamless online presentation",
        "end_message": "Markdown preparation complete! Our content is now formatted and optimized for online publishing. It's time to hit the 'publish' button and share our creation with the world!",

        },
    "save_to_file" : {
        "name": "Publisher",
        "profile": "Publisher",
        "task": "File Saving",
        "url": "assets/img/publisher.png",
        "start_message": "Taking the important step of saving our blog content. Let's ensure our hard work is securely stored for future reference and potential updates.",
        "end_message": "Blog content successfully saved! Our work is now safely stored, ready for future reference or any necessary revisions. Time to celebrate this milestone!",
        },
    "generate_filename" : {
        "name": "Publisher",
        "profile": "Publisher",
        "task": "Blog Naming",
        "url": "assets/img/publisher.png",
        "start_message": "Gotcha! I'll whip up a catchy title for the blog post",
        "end_message": "All set! Created Catchy title for the blog post",
        },
    "generate_image" : {
        "name": "Art Illustrator",
        "profile": "Art Illustrator",
        "task": "Image Generation",
        "url": "assets/img/artist.png",
        "start_message": "'ll craft an eye-catching image to go along with the title",
        "end_message": "Finished! Completed image to complement the blog post title",
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
        "start_message": "Embarking on the orchestration of our blog creation process. Let's synchronize our efforts, streamline tasks, and bring our collective vision to life!",
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