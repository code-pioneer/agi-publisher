site_name = "Creativify"
seo_description = "Hire digital content creators, aka AGI workers, to generate content like blog and relevant marketing material"
seo_keywords = "Autonomous Content creator, AGI, Opensource"

menuitems = [ 
                {   "uri":"/",
                    "menu":"Home",
                    "header":"Creativify",
                    "subheader":"Autonomous digital content creators",
                    "desc":"Short description of Homepage",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-house-door",
                    "primary": True,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/home.png',
                    "tags":[]
                },  
                {   "uri":"/docs/",
                    "menu":"Get Started",
                    "header":"Get Started",
                    "subheader":"Creativify",
                    "desc":"Short description of Documentation",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-book",
                    "primary": True,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/documentation.png',
                    "tags":[]
                },  
                {   "uri":"/theme/",
                    "menu":"Theme",
                    "header":"Theme Documentation",
                    "subheader":"Creativify",
                    "desc":"Nest theme documentation",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-filetype-html",
                    "primary": True,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/documentation.png',
                    "tags":[]
                },
                {   "uri":"/profile/",
                    "menu":"Profile",
                    "header":"Profile",
                    "subheader":"Creativify",
                    "desc":"Love to hear from you",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-person-fill",
                    "primary": False,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/profile.png',
                    "tags":[]
                },             
                {   "uri":"/contactus/",
                    "menu":"Contact Us",
                    "header":"Contact Us",
                    "subheader":"Creativify",
                    "desc":"Love to hear from you",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-pencil-square",
                    "primary": False,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/contactus.png',
                    "tags":[]
                },                                
                {   "uri":"/aboutus/",
                    "menu":"About Us",
                    "header":"About Us",
                    "subheader":"Creativify",
                    "desc":"More about us",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-buildings-fill",
                    "primary": False,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/aboutus.png',
                    "tags":[]
                },
                {   "uri":"/disclaimer/",
                    "menu":"Disclaimer",
                    "header":"Disclaimer",
                    "subheader":"Creativify",
                    "desc":"Detail disclaimer",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-info-square-fill",
                    "primary": False,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/disclaimer.png',
                    "tags":[]
                },
                {   "uri":"/blog",
                    "menu":"Blog",
                    "header":"Creativify",
                    "subheader":"Autonomous digital content creators",
                    "desc":"Short description of Homepage",
                    "pub":"Active since 8/2/2023",
                    "icon": "bi-pencil-square",
                    "primary": True,
                    "badge":False,
                    "badgetext":"3",
                    "badgetype":"success",
                    "logo": 'assets/img/chat.png',
                    "tags":[]
                },                                   
] 
    
def get_navbar(menukey):
    retval = {'menuitems' : menuitems, 'menu': '',  'header' : site_name,'subheader' : site_name, 'desc' : '','icon' : '','logo' : '','tags' : '',}
    for item in menuitems:
        if menukey == item['menu']:
            retval['menu'] = item['menu']
            retval['header'] = item['header']
            retval['subheader'] = item['subheader']
            retval['desc'] = item['desc']
            retval['icon'] = item['icon']
            retval['logo'] = item['logo']
            retval['tags'] = item['tags']
            break
    retval['seo_description'] = seo_description
    retval['seo_keywords'] = seo_keywords
    return retval
    
