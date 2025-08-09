from flask import Flask, render_template, request, redirect, url_for
import wikipedia

app = Flask(__name__)

# Main domains and their subdomains
DOMAIN_STRUCTURE = {
    "sports": ["cricket", "football", "chess", "olympics"],
    "media": ["film", "actors", "anime", "directors"],
    "technology": ["engineering", "space science", "computer", "artificial intelligence"],
    "medicine": ["diseases", "treatments", "mental health"],
    "politics": ["world leaders", "economics", "social movements"],
    "geography": ["countries", "rivers", "mountains", "cities"],
    "history": ["ancient civilization", "world wars", "empires", "languages"],
    "philosophy": ["religion", "philosophers"],
    "internet": ["programming languages", "cyber security", "software", "hardware"]
}

DOMAIN_IMAGES = {
    "sports": "https://cdn-icons-png.flaticon.com/512/861/861512.png",  # cricket bat image
    "media": "https://cdn-icons-png.flaticon.com/512/2922/2922510.png",   
    "technology": "https://cdn-icons-png.flaticon.com/512/2721/2721297.png",
    "medicine": "https://cdn-icons-png.flaticon.com/512/2965/2965567.png",
    "politics": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    "geography": "https://cdn-icons-png.flaticon.com/512/854/854878.png",
    "history": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
    "philosophy": "https://cdn-icons-png.flaticon.com/512/3062/3062633.png",
    "internet": "https://cdn-icons-png.flaticon.com/512/2721/2721290.png"
}

SUBDOMAIN_IMAGES = {
    "sports": {
        "cricket": "https://cdn-icons-png.flaticon.com/512/861/861511.png",      # stump image
        "football": "https://cdn-icons-png.flaticon.com/512/861/861512.png",      # cricket bat image
        "chess": "https://cdn-icons-png.flaticon.com/512/2729/2729129.png",       # chess board image
        "olympics": "https://cdn-icons-png.flaticon.com/512/3004/3004612.png"     # olympic rings image
    },
    "media": {
        "film": "https://cdn-icons-png.flaticon.com/512/833/833314.png",
        "actors": "https://cdn-icons-png.flaticon.com/512/2922/2922506.png",
        "anime": "https://cdn-icons-png.flaticon.com/512/3468/3468376.png",
        "directors": "https://cdn-icons-png.flaticon.com/512/2922/2922561.png"
    },
    "technology": {
        "engineering": "https://cdn-icons-png.flaticon.com/512/2721/2721306.png",
        "space science": "https://cdn-icons-png.flaticon.com/512/3212/3212608.png",
        "computer": "https://cdn-icons-png.flaticon.com/512/1055/1055687.png",
        "artificial intelligence": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
    },
    "medicine": {
        "diseases": "https://cdn-icons-png.flaticon.com/512/2965/2965567.png",
        "treatments": "https://cdn-icons-png.flaticon.com/512/2965/2965561.png",
        "mental health": "https://cdn-icons-png.flaticon.com/512/2965/2965565.png"
    },
    "politics": {
        "world leaders": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "economics": "https://cdn-icons-png.flaticon.com/512/2331/2331947.png",
        "social movements": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    },
    "geography": {
        "countries": "https://cdn-icons-png.flaticon.com/512/854/854878.png",
        "rivers": "https://cdn-icons-png.flaticon.com/512/427/427735.png",
        "mountains": "https://cdn-icons-png.flaticon.com/512/427/427735.png",
        "cities": "https://cdn-icons-png.flaticon.com/512/684/684908.png"
    },
    "history": {
        "ancient civilization": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
        "world wars": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
        "empires": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
        "languages": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png"
    },
    "philosophy": {
        "religion": "https://cdn-icons-png.flaticon.com/512/3062/3062633.png",
        "philosophers": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
    },
    "internet": {
        "programming languages": "https://cdn-icons-png.flaticon.com/512/2721/2721290.png",
        "cyber security": "https://cdn-icons-png.flaticon.com/512/2721/2721291.png",
        "software": "https://cdn-icons-png.flaticon.com/512/2721/2721302.png",
        "hardware": "https://cdn-icons-png.flaticon.com/512/2721/2721303.png"
    }
}

@app.route('/')
def index():
    domains = list(DOMAIN_STRUCTURE.keys())
    return render_template('index.html', domains=domains, domain_images=DOMAIN_IMAGES)

@app.route('/subdomains/<domain>')
def subdomains_page(domain):
    subdomains = DOMAIN_STRUCTURE.get(domain, [])
    img_url = DOMAIN_IMAGES.get(domain)
    subdomain_images = SUBDOMAIN_IMAGES.get(domain, {})
    return render_template(
        'subdomains.html',
        domain=domain,
        subdomains=subdomains,
        img_url=img_url,
        subdomain_images=subdomain_images
    )

@app.route('/domain/<domain>/<subdomain>', methods=['GET', 'POST'])
def subdomain_page(domain, subdomain):
    summary = None
    url = None
    error = None
    search_term = subdomain
    if request.method == 'POST':
        user_query = request.form.get('search')
        if user_query:
            search_term = f"{subdomain} {user_query}"
    try:
        summary = wikipedia.summary(search_term, sentences=3)
        page = wikipedia.page(search_term)
        url = page.url
    except Exception as e:
        error = f"Error: {str(e)}"
    img_url = DOMAIN_IMAGES.get(domain)
    return render_template('domain.html', domain=subdomain.title(), summary=summary, url=url, error=error, img_url=img_url, parent_domain=domain)

if __name__ == '__main__':
    app.run(debug=True)
